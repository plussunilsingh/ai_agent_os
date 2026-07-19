"""
AI-SE OS Scheduler
Manages task scheduling, leases, and work distribution
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import time
import threading
import heapq

from ..core.events import Event, EventType, EventPriority, get_event_bus
from ..core.state_machines import (
    create_task_state_machine,
    create_lease_state_machine,
    TaskState,
    LeaseState
)


@dataclass
class Lease:
    """Execution lease for exclusive work"""
    id: str = field(default_factory=lambda: str(uuid4()))
    task_id: str = ""
    agent_id: str = ""
    repository_id: str = ""
    session_id: str = ""
    acquired_at: Optional[str] = None
    expires_at: Optional[str] = None
    ttl_seconds: int = 300  # 5 minutes default
    state: LeaseState = LeaseState.AVAILABLE
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        if not self.expires_at:
            return False
        return datetime.now() > datetime.fromisoformat(self.expires_at)

    def time_remaining(self) -> float:
        if not self.expires_at:
            return float('inf')
        remaining = (datetime.fromisoformat(self.expires_at) - datetime.now()).total_seconds()
        return max(0, remaining)


@dataclass
class ScheduledTask:
    """A task scheduled for execution"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    priority: int = 5  # 1-10 (10=highest)
    scheduled_at: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    state: TaskState = TaskState.CREATED
    retry_count: int = 0
    max_retries: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __lt__(self, other: "ScheduledTask") -> bool:
        """For priority queue ordering"""
        return self.priority > other.priority


class Scheduler:
    """
    Task scheduler with lease management.
    
    Handles:
    - Task queuing and prioritization
    - Lease acquisition and expiration
    - Dependency resolution
    - Retry logic
    """

    def __init__(self):
        self._task_queue: List[ScheduledTask] = []
        self._tasks: Dict[str, ScheduledTask] = {}
        self._leases: Dict[str, Lease] = {}
        self._active_leases: Dict[str, str] = {}  # task_id -> lease_id
        self._lock = threading.RLock()
        self._event_bus = get_event_bus()
        self._running = False

    # ========================================================================
    # Task Management
    # ========================================================================

    def enqueue_task(self, task: ScheduledTask) -> str:
        """Enqueue a task for scheduling"""
        with self._lock:
            task.state = TaskState.QUEUED
            self._tasks[task.id] = task
            heapq.heappush(self._task_queue, task)

            self._event_bus.publish(Event(
                type=EventType.TASK_QUEUED,
                source="scheduler",
                producer="scheduler",
                payload={
                    "task_id": task.id,
                    "task_name": task.name,
                    "priority": task.priority
                }
            ))

            return task.id

    def dequeue_task(self) -> Optional[ScheduledTask]:
        """Dequeue the highest priority ready task"""
        with self._lock:
            # Clean expired entries from queue
            while self._task_queue:
                task = heapq.heappop(self._task_queue)

                # Check dependencies
                if self._dependencies_met(task):
                    task.state = TaskState.PLANNING
                    self._tasks[task.id] = task

                    self._event_bus.publish(Event(
                        type=EventType.TASK_PLANNING,
                        source="scheduler",
                        producer="scheduler",
                        payload={"task_id": task.id}
                    ))

                    return task
                else:
                    # Re-queue with lower priority for later
                    task.priority = max(1, task.priority - 1)
                    heapq.heappush(self._task_queue, task)

            return None

    def _dependencies_met(self, task: ScheduledTask) -> bool:
        """Check if all dependencies are met"""
        for dep_id in task.dependencies:
            dep_task = self._tasks.get(dep_id)
            if dep_task and dep_task.state != TaskState.SUCCEEDED:
                return False
        return True

    def update_task_state(self, task_id: str, new_state: TaskState) -> bool:
        """Update task state"""
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return False

            task.state = new_state
            self._tasks[task_id] = task

            # Publish event
            event_map = {
                TaskState.RUNNING: EventType.TASK_RUNNING,
                TaskState.SUCCEEDED: EventType.TASK_SUCCEEDED,
                TaskState.FAILED: EventType.TASK_FAILED,
                TaskState.CANCELLED: EventType.TASK_CANCELLED,
            }

            event_type = event_map.get(new_state)
            if event_type:
                self._event_bus.publish(Event(
                    type=event_type,
                    source="scheduler",
                    producer="scheduler",
                    payload={"task_id": task_id, "task_name": task.name}
                ))

            return True

    # ========================================================================
    # Lease Management
    # ========================================================================

    def acquire_lease(
        self,
        task_id: str,
        agent_id: str,
        repository_id: str,
        session_id: str,
        ttl_seconds: int = 300
    ) -> Optional[Lease]:
        """Acquire an exclusive lease for a task"""
        with self._lock:
            # Check if task already has an active lease
            existing_lease_id = self._active_leases.get(task_id)
            if existing_lease_id:
                existing = self._leases.get(existing_lease_id)
                if existing and not existing.is_expired():
                    return None  # Lease already held

            # Create new lease
            now = datetime.now()
            lease = Lease(
                task_id=task_id,
                agent_id=agent_id,
                repository_id=repository_id,
                session_id=session_id,
                acquired_at=now.isoformat(),
                expires_at=(now + timedelta(seconds=ttl_seconds)).isoformat(),
                ttl_seconds=ttl_seconds,
                state=LeaseState.ACTIVE
            )

            self._leases[lease.id] = lease
            self._active_leases[task_id] = lease.id

            self._event_bus.publish(Event(
                type=EventType.LEASE_ACQUIRED,
                source="scheduler",
                producer="scheduler",
                priority=EventPriority.HIGH,
                payload={
                    "lease_id": lease.id,
                    "task_id": task_id,
                    "agent_id": agent_id,
                    "ttl_seconds": ttl_seconds
                }
            ))

            return lease

    def release_lease(self, lease_id: str) -> bool:
        """Release a lease"""
        with self._lock:
            lease = self._leases.get(lease_id)
            if not lease:
                return False

            lease.state = LeaseState.RELEASED
            self._active_leases.pop(lease.task_id, None)

            self._event_bus.publish(Event(
                type=EventType.LEASE_RELEASED,
                source="scheduler",
                producer="scheduler",
                payload={
                    "lease_id": lease_id,
                    "task_id": lease.task_id,
                    "agent_id": lease.agent_id
                }
            ))

            return True

    def renew_lease(self, lease_id: str, ttl_seconds: int = 300) -> bool:
        """Renew an existing lease"""
        with self._lock:
            lease = self._leases.get(lease_id)
            if not lease or lease.is_expired():
                return False

            now = datetime.now()
            lease.expires_at = (now + timedelta(seconds=ttl_seconds)).isoformat()
            lease.ttl_seconds = ttl_seconds
            return True

    def get_lease(self, lease_id: str) -> Optional[Lease]:
        """Get lease by ID"""
        return self._leases.get(lease_id)

    def get_task_lease(self, task_id: str) -> Optional[Lease]:
        """Get active lease for a task"""
        lease_id = self._active_leases.get(task_id)
        if lease_id:
            lease = self._leases.get(lease_id)
            if lease and not lease.is_expired():
                return lease
        return None

    def expire_stale_leases(self) -> int:
        """Expire all stale leases"""
        expired_count = 0
        with self._lock:
            for lease_id, lease in list(self._leases.items()):
                if lease.state == LeaseState.ACTIVE and lease.is_expired():
                    lease.state = LeaseState.EXPIRED
                    self._active_leases.pop(lease.task_id, None)
                    expired_count += 1

                    self._event_bus.publish(Event(
                        type=EventType.LEASE_EXPIRED,
                        source="scheduler",
                        producer="scheduler",
                        priority=EventPriority.HIGH,
                        payload={
                            "lease_id": lease_id,
                            "task_id": lease.task_id,
                            "agent_id": lease.agent_id
                        }
                    ))

        return expired_count

    # ========================================================================
    # Query & Stats
    # ========================================================================

    def get_pending_tasks(self) -> List[ScheduledTask]:
        """Get all pending tasks"""
        with self._lock:
            return [
                t for t in self._tasks.values()
                if t.state in [TaskState.CREATED, TaskState.QUEUED, TaskState.PLANNING]
            ]

    def get_active_tasks(self) -> List[ScheduledTask]:
        """Get all active tasks"""
        with self._lock:
            return [
                t for t in self._tasks.values()
                if t.state == TaskState.RUNNING
            ]

    def get_active_leases(self) -> List[Lease]:
        """Get all active leases"""
        with self._lock:
            return [
                l for l in self._leases.values()
                if l.state == LeaseState.ACTIVE and not l.is_expired()
            ]

    def get_stats(self) -> Dict[str, Any]:
        """Get scheduler statistics"""
        with self._lock:
            total = len(self._tasks)
            pending = len(self.get_pending_tasks())
            active = len(self.get_active_tasks())
            succeeded = sum(1 for t in self._tasks.values() if t.state == TaskState.SUCCEEDED)
            failed = sum(1 for t in self._tasks.values() if t.state == TaskState.FAILED)
            active_leases = len(self.get_active_leases())
            queue_size = len(self._task_queue)

            return {
                "total_tasks": total,
                "pending_tasks": pending,
                "active_tasks": active,
                "succeeded_tasks": succeeded,
                "failed_tasks": failed,
                "queue_size": queue_size,
                "active_leases": active_leases,
                "stale_leases_expired": self.expire_stale_leases()
            }
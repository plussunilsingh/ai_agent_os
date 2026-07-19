"""
AI-SE OS Event System
Defines event types, event bus, and event handlers
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Callable, Set
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
import asyncio
import json
import logging

logger = logging.getLogger(__name__)


class EventPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class EventType(str, Enum):
    # System Events
    SYSTEM_STARTUP = "system.startup"
    SYSTEM_SHUTDOWN = "system.shutdown"
    SYSTEM_ERROR = "system.error"

    # Repository Events
    REPOSITORY_REGISTERED = "repository.registered"
    REPOSITORY_ANALYZED = "repository.analyzed"
    REPOSITORY_INDEXED = "repository.indexed"
    REPOSITORY_ERROR = "repository.error"

    # Task Events
    TASK_CREATED = "task.created"
    TASK_QUEUED = "task.queued"
    TASK_PLANNING = "task.planning"
    TASK_RUNNING = "task.running"
    TASK_SUCCEEDED = "task.succeeded"
    TASK_FAILED = "task.failed"
    TASK_CANCELLED = "task.cancelled"

    # Execution Events
    EXECUTION_STARTED = "execution.started"
    EXECUTION_COMPLETED = "execution.completed"
    EXECUTION_FAILED = "execution.failed"
    EXECUTION_CANCELLED = "execution.cancelled"

    # Validation Events
    VALIDATION_STARTED = "validation.started"
    VALIDATION_PASSED = "validation.passed"
    VALIDATION_FAILED = "validation.failed"
    VALIDATION_WARNING = "validation.warning"

    # Recovery Events
    RECOVERY_STARTED = "recovery.started"
    RECOVERY_SUCCEEDED = "recovery.succeeded"
    RECOVERY_FAILED = "recovery.failed"
    RECOVERY_ESCALATED = "recovery.escalated"

    # Knowledge Events
    KNOWLEDGE_UPDATED = "knowledge.updated"
    KNOWLEDGE_GRAPH_UPDATED = "knowledge.graph.updated"
    GENOME_SNAPSHOT_CREATED = "genome.snapshot.created"

    # Cache Events
    CACHE_HIT = "cache.hit"
    CACHE_MISS = "cache.miss"
    CACHE_INVALIDATED = "cache.invalidated"
    CACHE_DIVERGENCE = "cache.divergence"

    # Policy Events
    POLICY_DECISION = "policy.decision"
    POLICY_VIOLATION = "policy.violation"

    # Lease Events
    LEASE_ACQUIRED = "lease.acquired"
    LEASE_RELEASED = "lease.released"
    LEASE_EXPIRED = "lease.expired"
    LEASE_REVOKED = "lease.revoked"

    # Agent Events
    AGENT_SESSION_STARTED = "agent.session.started"
    AGENT_SESSION_ENDED = "agent.session.ended"
    AGENT_HANDOFF = "agent.handoff"

    # Learning Events
    EXPERIENCE_RECORDED = "experience.recorded"
    PLAYBOOK_UPDATED = "playbook.updated"
    BENCHMARK_UPDATED = "benchmark.updated"


@dataclass
class Event:
    """Base event with provenance"""
    id: UUID = field(default_factory=uuid4)
    type: EventType = EventType.SYSTEM_STARTUP
    source: str = ""
    producer: str = ""
    priority: EventPriority = EventPriority.NORMAL
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    trace_id: Optional[str] = None
    correlation_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "type": self.type.value,
            "source": self.source,
            "producer": self.producer,
            "priority": self.priority.value,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "trace_id": self.trace_id,
            "correlation_id": self.correlation_id
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class EventSubscription:
    """Represents a subscription to an event type"""

    def __init__(
        self,
        event_type: EventType,
        handler: Callable,
        filter_fn: Optional[Callable[[Event], bool]] = None,
        priority: EventPriority = EventPriority.NORMAL
    ):
        self.event_type = event_type
        self.handler = handler
        self.filter_fn = filter_fn
        self.priority = priority
        self.id = str(uuid4())


class EventBus:
    """
    Central event bus for AI-SE OS
    Supports sync and async handlers, filtering, and prioritization
    """

    def __init__(self):
        self._subscriptions: Dict[EventType, List[EventSubscription]] = {}
        self._global_subscriptions: List[EventSubscription] = []
        self._history: List[Event] = []
        self._max_history = 1000
        self._handlers: Dict[str, Callable] = {}

    def subscribe(
        self,
        event_type: EventType,
        handler: Callable,
        filter_fn: Optional[Callable[[Event], bool]] = None,
        priority: EventPriority = EventPriority.NORMAL
    ) -> str:
        """Subscribe to an event type"""
        sub = EventSubscription(event_type, handler, filter_fn, priority)
        if event_type not in self._subscriptions:
            self._subscriptions[event_type] = []
        self._subscriptions[event_type].append(sub)
        return sub.id

    def subscribe_all(
        self,
        handler: Callable,
        filter_fn: Optional[Callable[[Event], bool]] = None
    ) -> str:
        """Subscribe to all events"""
        sub = EventSubscription(EventType.SYSTEM_STARTUP, handler, filter_fn)
        self._global_subscriptions.append(sub)
        return sub.id

    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from events"""
        for event_type, subs in self._subscriptions.items():
            for sub in subs:
                if sub.id == subscription_id:
                    subs.remove(sub)
                    return True

        for sub in self._global_subscriptions:
            if sub.id == subscription_id:
                self._global_subscriptions.remove(sub)
                return True

        return False

    def publish(self, event: Event) -> None:
        """Publish an event synchronously"""
        self._record_event(event)

        # Notify global subscribers
        for sub in self._global_subscriptions:
            if not sub.filter_fn or sub.filter_fn(event):
                try:
                    sub.handler(event)
                except Exception as e:
                    logger.error(f"Global handler error for {event.type}: {e}")

        # Notify type-specific subscribers
        subs = self._subscriptions.get(event.type, [])
        for sub in sorted(subs, key=lambda s: s.priority.value, reverse=True):
            if not sub.filter_fn or sub.filter_fn(event):
                try:
                    sub.handler(event)
                except Exception as e:
                    logger.error(f"Handler error for {event.type}: {e}")

    async def publish_async(self, event: Event) -> None:
        """Publish an event asynchronously"""
        self._record_event(event)

        tasks = []

        # Global subscribers
        for sub in self._global_subscriptions:
            if not sub.filter_fn or sub.filter_fn(event):
                if asyncio.iscoroutinefunction(sub.handler):
                    tasks.append(sub.handler(event))
                else:
                    try:
                        sub.handler(event)
                    except Exception as e:
                        logger.error(f"Global handler error for {event.type}: {e}")

        # Type-specific subscribers
        subs = self._subscriptions.get(event.type, [])
        for sub in sorted(subs, key=lambda s: s.priority.value, reverse=True):
            if not sub.filter_fn or sub.filter_fn(event):
                if asyncio.iscoroutinefunction(sub.handler):
                    tasks.append(sub.handler(event))
                else:
                    try:
                        sub.handler(event)
                    except Exception as e:
                        logger.error(f"Handler error for {event.type}: {e}")

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    def _record_event(self, event: Event) -> None:
        """Record event in history"""
        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history.pop(0)

    def get_history(
        self,
        event_type: Optional[EventType] = None,
        limit: int = 50
    ) -> List[Event]:
        """Get event history"""
        if event_type:
            filtered = [e for e in self._history if e.type == event_type]
            return filtered[-limit:]
        return self._history[-limit:]

    def get_stats(self) -> Dict[str, Any]:
        """Get event bus statistics"""
        type_counts: Dict[str, int] = {}
        for event in self._history:
            type_counts[event.type.value] = type_counts.get(event.type.value, 0) + 1

        return {
            "total_events": len(self._history),
            "subscriptions": sum(len(s) for s in self._subscriptions.values()),
            "global_subscriptions": len(self._global_subscriptions),
            "event_type_counts": type_counts,
            "unique_types": len(type_counts)
        }

    def clear_history(self) -> None:
        """Clear event history"""
        self._history.clear()


# Singleton instance
global_event_bus = EventBus()


def get_event_bus() -> EventBus:
    """Get the global event bus instance"""
    return global_event_bus
"""
Authoritative Task Manager – single source of truth for all task state.
Supports state machine validation, event sourcing, worker heartbeat tracking, and session ownership.
"""

import asyncio
import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set
import logging

from ai_se_os.telemetry.task_state_machine import InvalidStateTransitionError

logger = logging.getLogger(__name__)



class TaskStatus(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    PLANNING = "planning"
    EXECUTING = "executing"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskStage(str, Enum):
    INIT = "init"
    PLAN = "plan"
    EXECUTE = "execute"
    VALIDATE = "validate"
    BROWSER = "browser"
    LLM = "llm"


@dataclass
class TaskEvent:
    timestamp: float
    status: TaskStatus
    stage: Optional[TaskStage]
    progress: int
    step: str
    worker_id: Optional[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    id: str
    created_at: float
    status: TaskStatus
    stage: Optional[TaskStage]
    progress: int
    step: str
    worker_id: Optional[str]
    pid: Optional[int]
    host: Optional[str]
    session_id: Optional[str]
    events: List[TaskEvent] = field(default_factory=list)
    heartbeat_at: float = 0.0
    timeout_seconds: int = 3600  # global fallback


class TaskManager:
    """
    Authoritative Task Manager – thread-safe and async-safe state owner.
    """
    def __init__(self):
        self._tasks: Dict[str, Task] = {}
        self._event_log: List[TaskEvent] = []
        self._lock = asyncio.Lock()

    async def create_task(self, task_id: str, session_id: Optional[str] = None) -> str:
        async with self._lock:
            if task_id in self._tasks:
                return task_id
            task = Task(
                id=task_id,
                created_at=time.time(),
                status=TaskStatus.CREATED,
                stage=None,
                progress=0,
                step="Initializing...",
                worker_id=None,
                pid=None,
                host=None,
                session_id=session_id,
                events=[]
            )
            self._tasks[task_id] = task
            await self._append_event(task_id, TaskStatus.CREATED, None, 0, "Task created")
            logger.info(f"Task {task_id} created")
            return task_id

    async def transition(
        self,
        task_id: str,
        new_status: TaskStatus,
        stage: Optional[TaskStage] = None,
        progress: Optional[int] = None,
        step: Optional[str] = None,
        worker_id: Optional[str] = None,
        pid: Optional[int] = None,
        host: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        async with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                # Auto-create if not pre-registered
                await self.create_task(task_id)
                task = self._tasks[task_id]

            # Allow idempotent status calls
            if task.status != new_status:
                if not self._is_valid_transition(task.status, new_status):
                    logger.warning(
                        f"Invalid task transition attempted for {task_id}: {task.status.value} -> {new_status.value}"
                    )
                task.status = new_status

            if stage is not None:
                task.stage = stage
            if progress is not None:
                task.progress = progress
            if step is not None:
                task.step = step
            if worker_id:
                task.worker_id = worker_id
            if pid:
                task.pid = pid
            if host:
                task.host = host

            await self._append_event(task_id, new_status, stage or task.stage, task.progress, task.step, metadata or {})
            logger.info(f"Task {task_id} → {new_status.value} ({task.step})")

    async def heartbeat(self, task_id: str, progress: Optional[int] = None, step: Optional[str] = None):
        async with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return
            task.heartbeat_at = time.time()
            if progress is not None:
                task.progress = progress
            if step is not None:
                task.step = step
            await self._append_event(task_id, task.status, task.stage, task.progress, f"Heartbeat: {task.step}", heartbeat=True)

    async def _append_event(
        self,
        task_id: str,
        status: TaskStatus,
        stage: Optional[TaskStage],
        progress: int,
        step: str,
        metadata: Optional[Dict[str, Any]] = None,
        heartbeat: bool = False
    ):
        task = self._tasks.get(task_id)
        worker_id = task.worker_id if task else None
        event = TaskEvent(
            timestamp=time.time(),
            status=status,
            stage=stage,
            progress=progress,
            step=step,
            worker_id=worker_id,
            metadata=metadata or {}
        )
        if task:
            task.events.append(event)
        self._event_log.append(event)

    def _is_valid_transition(self, from_status: TaskStatus, to_status: TaskStatus) -> bool:
        allowed: Dict[TaskStatus, Set[TaskStatus]] = {
            TaskStatus.CREATED: {TaskStatus.QUEUED, TaskStatus.PLANNING, TaskStatus.EXECUTING, TaskStatus.FAILED, TaskStatus.CANCELLED},
            TaskStatus.QUEUED: {TaskStatus.PLANNING, TaskStatus.EXECUTING, TaskStatus.FAILED, TaskStatus.CANCELLED},
            TaskStatus.PLANNING: {TaskStatus.EXECUTING, TaskStatus.WAITING, TaskStatus.FAILED, TaskStatus.CANCELLED},
            TaskStatus.EXECUTING: {TaskStatus.WAITING, TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED},
            TaskStatus.WAITING: {TaskStatus.EXECUTING, TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED},
            TaskStatus.COMPLETED: set(),
            TaskStatus.FAILED: set(),
            TaskStatus.CANCELLED: set(),
        }
        return to_status in allowed.get(from_status, set())

    async def get_task(self, task_id: str) -> Optional[Task]:
        async with self._lock:
            return self._tasks.get(task_id)

    async def list_active(self) -> List[Task]:
        async with self._lock:
            return [
                t for t in self._tasks.values()
                if t.status not in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED)
            ]

    async def get_history(self, task_id: str) -> List[TaskEvent]:
        async with self._lock:
            task = self._tasks.get(task_id)
            return list(task.events) if task else []


# Global singleton instance for app-wide use
task_manager = TaskManager()

"""
AI-SE OS Centralized Task State Machine & Transition Validator (PR 1)
Enforces valid state transitions and prevents direct illegal status mutations across all workers.
"""

from enum import Enum
import logging
import threading
import time
from typing import Dict, Any, Optional, Set

logger = logging.getLogger("TaskStateMachine")


class TaskState(str, Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    CANCELLED = "CANCELLED"


class InvalidStateTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""
    def __init__(self, task_id: str, current_state: TaskState, target_state: TaskState):
        super().__init__(
            f"Invalid task state transition for task '{task_id}': {current_state.value} -> {target_state.value}"
        )
        self.task_id = task_id
        self.current_state = current_state
        self.target_state = target_state


# Allowed state transition graph
ALLOWED_TRANSITIONS: Dict[TaskState, Set[TaskState]] = {
    TaskState.CREATED: {TaskState.QUEUED, TaskState.PLANNING, TaskState.EXECUTING, TaskState.CANCELLED},
    TaskState.QUEUED: {TaskState.PLANNING, TaskState.EXECUTING, TaskState.CANCELLED, TaskState.FAILED},
    TaskState.PLANNING: {TaskState.EXECUTING, TaskState.FAILED, TaskState.CANCELLED, TaskState.TIMED_OUT},
    TaskState.EXECUTING: {TaskState.COMPLETED, TaskState.FAILED, TaskState.TIMED_OUT, TaskState.CANCELLED},
    # Terminal states — no transitions allowed out of terminal states
    TaskState.COMPLETED: set(),
    TaskState.FAILED: set(),
    TaskState.TIMED_OUT: set(),
    TaskState.CANCELLED: set(),
}


class TaskManager:
    """
    Centralized thread-safe Task State Manager.
    Single owner for task state transitions, ensuring atomic updates and strict graph validation.
    """
    _lock = threading.RLock()
    _task_states: Dict[str, TaskState] = {}
    _transition_history: Dict[str, list] = {}

    @classmethod
    def get_state(cls, task_id: str) -> Optional[TaskState]:
        with cls._lock:
            return cls._task_states.get(task_id)

    @classmethod
    def register(cls, task_id: str, initial_state: TaskState = TaskState.CREATED) -> TaskState:
        with cls._lock:
            cls._task_states[task_id] = initial_state
            if task_id not in cls._transition_history:
                cls._transition_history[task_id] = []
            cls._transition_history[task_id].append({
                "from": None,
                "to": initial_state.value,
                "timestamp": time.strftime("%H:%M:%S IST"),
                "reason": "Task registered"
            })
            return initial_state

    @classmethod
    def transition(
        cls,
        task_id: str,
        target_state: TaskState,
        reason: Optional[str] = None
    ) -> TaskState:
        """
        Atomically transitions a task to target_state if valid.
        Raises InvalidStateTransitionError if transition is illegal.
        """
        with cls._lock:
            current_state = cls._task_states.get(task_id)

            # If task not registered yet, register as CREATED first
            if current_state is None:
                cls.register(task_id, TaskState.CREATED)
                current_state = TaskState.CREATED

            # Allow idempotent transitions (same state)
            if current_state == target_state:
                return current_state

            allowed = ALLOWED_TRANSITIONS.get(current_state, set())
            if target_state not in allowed:
                logger.error(
                    f"Illegal state transition blocked for task '{task_id}': "
                    f"{current_state.value} -> {target_state.value} (Allowed: {[s.value for s in allowed]})"
                )
                raise InvalidStateTransitionError(task_id, current_state, target_state)

            # Update state
            cls._task_states[task_id] = target_state
            cls._transition_history[task_id].append({
                "from": current_state.value,
                "to": target_state.value,
                "timestamp": time.strftime("%H:%M:%S IST"),
                "reason": reason or "State transition"
            })
            logger.info(f"[TaskManager] Task '{task_id}': {current_state.value} -> {target_state.value}")
            return target_state

    @classmethod
    def get_history(cls, task_id: str) -> list:
        with cls._lock:
            return list(cls._transition_history.get(task_id, []))

    @classmethod
    def clear(cls):
        """Reset state manager (used in testing)."""
        with cls._lock:
            cls._task_states.clear()
            cls._transition_history.clear()

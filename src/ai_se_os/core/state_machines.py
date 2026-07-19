"""
AI-SE OS State Machines
Defines state transitions for all core entities
"""

from enum import Enum
from typing import Dict, List, Set, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime


class TaskState(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    PLANNING = "planning"
    RUNNING = "running"
    WAITING = "waiting"
    RETRYING = "retrying"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    ARCHIVED = "archived"


class ExecutionState(str, Enum):
    PENDING = "pending"
    LEASING = "leasing"
    EXECUTING = "executing"
    VALIDATING = "validating"
    RECOVERING = "recovering"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ValidationState(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"


class RecoveryState(str, Enum):
    NOT_NEEDED = "not_needed"
    RETRYING = "retrying"
    ROLLING_BACK = "rolling_back"
    REPLANNING = "replanning"
    FIXING = "fixing"
    ESCALATED = "escalated"
    RESOLVED = "resolved"


class RepositoryState(str, Enum):
    UNREGISTERED = "unregistered"
    REGISTERED = "registered"
    ANALYZING = "analyzing"
    ANALYZED = "analyzed"
    INDEXING = "indexing"
    INDEXED = "indexed"
    ERROR = "error"


class LeaseState(str, Enum):
    AVAILABLE = "available"
    ACQUIRED = "acquired"
    ACTIVE = "active"
    EXPIRED = "expired"
    RELEASED = "released"
    REVOKED = "revoked"


@dataclass
class StateTransition:
    """Defines a valid state transition"""
    from_state: str
    to_state: str
    trigger: str
    guard: Optional[Callable] = None
    on_transition: Optional[Callable] = None


@dataclass
class StateMachine:
    """Generic state machine with validation"""
    name: str
    states: Set[str]
    initial_state: str
    transitions: List[StateTransition] = field(default_factory=list)
    current_state: str = ""
    history: List[Dict] = field(default_factory=list)

    def __post_init__(self):
        self.current_state = self.initial_state

    def add_transition(self, transition: StateTransition) -> None:
        """Add a valid transition"""
        assert transition.from_state in self.states, f"Invalid from_state: {transition.from_state}"
        assert transition.to_state in self.states, f"Invalid to_state: {transition.to_state}"
        self.transitions.append(transition)

    def can_transition(self, to_state: str, context: Optional[Dict] = None) -> bool:
        """Check if transition is valid"""
        for t in self.transitions:
            if t.from_state == self.current_state and t.to_state == to_state:
                if t.guard and context:
                    return t.guard(context)
                return True
        return False

    def transition(self, to_state: str, trigger: str, context: Optional[Dict] = None) -> bool:
        """Execute a state transition"""
        if not self.can_transition(to_state, context):
            return False

        for t in self.transitions:
            if t.from_state == self.current_state and t.to_state == to_state:
                old_state = self.current_state
                self.current_state = to_state
                self.history.append({
                    "from": old_state,
                    "to": to_state,
                    "trigger": trigger,
                    "timestamp": datetime.now().isoformat(),
                    "context": context or {}
                })
                if t.on_transition:
                    t.on_transition({"from": old_state, "to": to_state, "trigger": trigger})
                return True
        return False

    def get_history(self, limit: int = 10) -> List[Dict]:
        """Get recent transition history"""
        return self.history[-limit:]


# ============================================================================
# Predefined State Machines
# ============================================================================

def create_task_state_machine() -> StateMachine:
    """Create the task lifecycle state machine"""
    sm = StateMachine(
        name="task_lifecycle",
        states={
            "created", "queued", "planning", "running",
            "waiting", "retrying", "succeeded", "failed", "archived"
        },
        initial_state="created"
    )

    sm.add_transition(StateTransition("created", "queued", "enqueue"))
    sm.add_transition(StateTransition("queued", "planning", "start_planning"))
    sm.add_transition(StateTransition("planning", "running", "start_execution"))
    sm.add_transition(StateTransition("running", "waiting", "wait_for_dependency"))
    sm.add_transition(StateTransition("waiting", "running", "dependency_resolved"))
    sm.add_transition(StateTransition("running", "retrying", "retry"))
    sm.add_transition(StateTransition("retrying", "running", "retry_succeeded"))
    sm.add_transition(StateTransition("running", "succeeded", "complete"))
    sm.add_transition(StateTransition("running", "failed", "fail"))
    sm.add_transition(StateTransition("retrying", "failed", "max_retries_exceeded"))
    sm.add_transition(StateTransition("succeeded", "archived", "archive"))
    sm.add_transition(StateTransition("failed", "archived", "archive"))

    return sm


def create_execution_state_machine() -> StateMachine:
    """Create the execution lifecycle state machine"""
    sm = StateMachine(
        name="execution_lifecycle",
        states={
            "pending", "leasing", "executing", "validating",
            "recovering", "completed", "failed", "cancelled"
        },
        initial_state="pending"
    )

    sm.add_transition(StateTransition("pending", "leasing", "acquire_lease"))
    sm.add_transition(StateTransition("leasing", "executing", "lease_acquired"))
    sm.add_transition(StateTransition("leasing", "failed", "lease_denied"))
    sm.add_transition(StateTransition("executing", "validating", "execute_complete"))
    sm.add_transition(StateTransition("validating", "completed", "validation_passed"))
    sm.add_transition(StateTransition("validating", "recovering", "validation_failed"))
    sm.add_transition(StateTransition("recovering", "executing", "recovery_succeeded"))
    sm.add_transition(StateTransition("recovering", "failed", "recovery_failed"))
    sm.add_transition(StateTransition("executing", "failed", "execution_failed"))
    sm.add_transition(StateTransition("pending", "cancelled", "cancel"))
    sm.add_transition(StateTransition("leasing", "cancelled", "cancel"))
    sm.add_transition(StateTransition("executing", "cancelled", "cancel"))

    return sm


def create_lease_state_machine() -> StateMachine:
    """Create the lease lifecycle state machine"""
    sm = StateMachine(
        name="lease_lifecycle",
        states={"available", "acquired", "active", "expired", "released", "revoked"},
        initial_state="available"
    )

    sm.add_transition(StateTransition("available", "acquired", "acquire"))
    sm.add_transition(StateTransition("acquired", "active", "activate"))
    sm.add_transition(StateTransition("active", "released", "release"))
    sm.add_transition(StateTransition("active", "expired", "expire"))
    sm.add_transition(StateTransition("active", "revoked", "revoke"))
    sm.add_transition(StateTransition("acquired", "released", "release"))
    sm.add_transition(StateTransition("acquired", "expired", "expire"))

    return sm
"""
Tests for State Machines
"""

import pytest
from src.core.state_machines import (
    StateMachine,
    StateTransition,
    create_task_state_machine,
    create_execution_state_machine,
    create_lease_state_machine,
    TaskState,
    ExecutionState,
    LeaseState
)


class TestStateMachine:
    def test_initial_state(self):
        sm = create_task_state_machine()
        assert sm.current_state == "created"

    def test_valid_transition(self):
        sm = create_task_state_machine()
        assert sm.can_transition("queued") == True
        assert sm.transition("queued", "enqueue") == True
        assert sm.current_state == "queued"

    def test_invalid_transition(self):
        sm = create_task_state_machine()
        assert sm.can_transition("succeeded") == False  # Can't go directly

    def test_transition_history(self):
        sm = create_task_state_machine()
        sm.transition("queued", "enqueue")
        sm.transition("planning", "start_planning")
        history = sm.get_history(5)
        assert len(history) == 2
        assert history[0]["from"] == "created"
        assert history[0]["to"] == "queued"

    def test_full_task_lifecycle(self):
        sm = create_task_state_machine()
        transitions = [
            ("queued", "enqueue"),
            ("planning", "start_planning"),
            ("running", "start_execution"),
            ("succeeded", "complete"),
            ("archived", "archive")
        ]
        for to_state, trigger in transitions:
            assert sm.transition(to_state, trigger) == True
        assert sm.current_state == "archived"

    def test_execution_state_machine(self):
        sm = create_execution_state_machine()
        sm.transition("leasing", "acquire_lease")
        sm.transition("executing", "lease_acquired")
        sm.transition("validating", "execute_complete")
        sm.transition("completed", "validation_passed")
        assert sm.current_state == "completed"

    def test_lease_state_machine(self):
        sm = create_lease_state_machine()
        assert sm.current_state == "available"
        sm.transition("acquired", "acquire")
        sm.transition("active", "activate")
        sm.transition("released", "release")
        assert sm.current_state == "released"

    def test_retry_flow(self):
        sm = create_task_state_machine()
        sm.transition("queued", "enqueue")
        sm.transition("planning", "start_planning")
        sm.transition("running", "start_execution")
        sm.transition("retrying", "retry")
        sm.transition("running", "retry_succeeded")
        sm.transition("succeeded", "complete")
        assert sm.current_state == "succeeded"
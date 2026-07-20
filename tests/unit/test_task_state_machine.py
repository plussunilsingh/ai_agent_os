"""
Unit tests for TaskManager state machine (PR 1).
"""

import pytest
from ai_se_os.telemetry.task_state_machine import (
    TaskManager,
    TaskState,
    InvalidStateTransitionError
)


@pytest.fixture(autouse=True)
def reset_task_manager():
    TaskManager.clear()
    yield
    TaskManager.clear()


def test_valid_task_lifecycle():
    task_id = "test-task-1"
    TaskManager.register(task_id, TaskState.CREATED)
    assert TaskManager.get_state(task_id) == TaskState.CREATED

    # CREATED -> QUEUED
    state = TaskManager.transition(task_id, TaskState.QUEUED)
    assert state == TaskState.QUEUED

    # QUEUED -> PLANNING
    state = TaskManager.transition(task_id, TaskState.PLANNING)
    assert state == TaskState.PLANNING

    # PLANNING -> EXECUTING
    state = TaskManager.transition(task_id, TaskState.EXECUTING)
    assert state == TaskState.EXECUTING

    # EXECUTING -> COMPLETED
    state = TaskManager.transition(task_id, TaskState.COMPLETED)
    assert state == TaskState.COMPLETED


def test_invalid_state_transition_raises_error():
    task_id = "test-task-2"
    TaskManager.register(task_id, TaskState.CREATED)

    # CREATED -> COMPLETED is illegal (must go through QUEUED/PLANNING/EXECUTING)
    with pytest.raises(InvalidStateTransitionError) as exc_info:
        TaskManager.transition(task_id, TaskState.COMPLETED)

    assert exc_info.value.current_state == TaskState.CREATED
    assert exc_info.value.target_state == TaskState.COMPLETED


def test_terminal_state_blocks_further_transitions():
    task_id = "test-task-3"
    TaskManager.register(task_id, TaskState.CREATED)
    TaskManager.transition(task_id, TaskState.EXECUTING)
    TaskManager.transition(task_id, TaskState.FAILED)

    # Transitioning out of FAILED is illegal
    with pytest.raises(InvalidStateTransitionError):
        TaskManager.transition(task_id, TaskState.EXECUTING)


def test_idempotent_transitions_allowed():
    task_id = "test-task-4"
    TaskManager.register(task_id, TaskState.EXECUTING)

    # Repeating same state is allowed without error
    state = TaskManager.transition(task_id, TaskState.EXECUTING)
    assert state == TaskState.EXECUTING


def test_transition_history_tracking():
    task_id = "test-task-5"
    TaskManager.register(task_id, TaskState.CREATED)
    TaskManager.transition(task_id, TaskState.EXECUTING, reason="Start execution")
    TaskManager.transition(task_id, TaskState.COMPLETED, reason="Done")

    history = TaskManager.get_history(task_id)
    assert len(history) == 3
    assert history[0]["to"] == "CREATED"
    assert history[1]["to"] == "EXECUTING"
    assert history[2]["to"] == "COMPLETED"

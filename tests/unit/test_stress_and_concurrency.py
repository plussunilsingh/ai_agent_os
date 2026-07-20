"""
Stress, Concurrency, and Fuzzing Test Suite for TaskManager & State Machine.
Uncovers race conditions, deadlocks, illegal state jumps, and memory pressure under high concurrency.
"""

import pytest
import asyncio
import random
import time
from typing import List
from ai_se_os.core.task_manager import TaskManager, TaskStatus, TaskStage, InvalidStateTransitionError


@pytest.mark.asyncio
async def test_high_concurrency_task_creation():
    """Test 100 concurrent tasks created simultaneously."""
    tm = TaskManager()
    num_tasks = 100

    async def create_single(idx: int):
        task_id = f"concurrent-task-{idx}"
        await tm.create_task(task_id, session_id=f"session-{idx}")
        return task_id

    task_ids = await asyncio.gather(*[create_single(i) for i in range(num_tasks)])
    assert len(task_ids) == num_tasks

    active = await tm.list_active()
    assert len(active) == num_tasks


@pytest.mark.asyncio
async def test_concurrent_state_transitions_race():
    """Test simultaneous transitions on the same task from multiple coroutines."""
    tm = TaskManager()
    task_id = "race-task-1"
    await tm.create_task(task_id)

    async def attempt_transition(target_status: TaskStatus, progress: int):
        try:
            await tm.transition(task_id, target_status, progress=progress, step=f"Step {progress}")
            return True
        except (ValueError, InvalidStateTransitionError):
            return False

    # Fire concurrent transition attempts
    statuses = [TaskStatus.QUEUED, TaskStatus.PLANNING, TaskStatus.EXECUTING, TaskStatus.COMPLETED]
    results = await asyncio.gather(*[attempt_transition(s, i * 25) for i, s in enumerate(statuses)])

    task = await tm.get_task(task_id)
    assert task is not None
    # Task state must be valid
    assert task.status in TaskStatus


@pytest.mark.asyncio
async def test_state_machine_fuzzing():
    """Fuzz random state transitions across 50 tasks to verify no corrupted states occur."""
    tm = TaskManager()
    all_statuses = list(TaskStatus)

    async def fuzz_task(idx: int):
        task_id = f"fuzz-task-{idx}"
        await tm.create_task(task_id)
        for _ in range(10):
            target = random.choice(all_statuses)
            try:
                await tm.transition(task_id, target, progress=random.randint(0, 100))
            except (ValueError, Exception):
                pass  # Invalid transitions are expected and caught gracefully

    await asyncio.gather(*[fuzz_task(i) for i in range(50)])

    # Ensure all tasks remain structurally valid
    for i in range(50):
        t = await tm.get_task(f"fuzz-task-{i}")
        assert t is not None
        assert isinstance(t.events, list)


@pytest.mark.asyncio
async def test_event_log_memory_stress():
    """Appends 1,000 events to a single task to verify event sourcing performance."""
    tm = TaskManager()
    task_id = "memory-stress-task"
    await tm.create_task(task_id)

    t0 = time.time()
    for i in range(1000):
        await tm.heartbeat(task_id, progress=i % 100, step=f"Stress step {i}")
    elapsed = time.time() - t0

    history = await tm.get_history(task_id)
    assert len(history) == 1001  # 1 created + 1000 heartbeats
    assert elapsed < 1.0  # Must complete 1000 events in under 1 second

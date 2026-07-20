"""
Fault Injection and Edge-Case Test Suite.
Verifies system resilience against worker process crashes, stage timeouts, and corrupted inputs.
"""

import pytest
import asyncio
from ai_se_os.core.task_manager import TaskManager, TaskStatus, TaskStage
from ai_se_os.execution.worker import TaskWorker


@pytest.mark.asyncio
async def test_worker_stage_timeout_fault():
    """Fault Injection: Simulates a stage hanging past its timeout limit."""
    tm = TaskManager()
    task_id = "fault-timeout-task"
    await tm.create_task(task_id)

    worker = TaskWorker(task_id=task_id, manager=tm)

    # Mock _do_execute to simulate a hanging function (takes longer than execution timeout)
    async def hanging_execute():
        await asyncio.sleep(10)  # Simulates hang

    worker._do_execute = hanging_execute

    # Temporarily override execute timeout to 0.2s for fast testing
    from ai_se_os.execution import worker as worker_mod
    original_timeout = worker_mod.STAGE_TIMEOUTS.get("execute")
    worker_mod.STAGE_TIMEOUTS["execute"] = 0.2

    try:
        await worker.run()
        task = await tm.get_task(task_id)
        assert task is not None
        assert task.status == TaskStatus.FAILED
        assert "timed out" in task.step.lower()
    finally:
        worker_mod.STAGE_TIMEOUTS["execute"] = original_timeout


@pytest.mark.asyncio
async def test_worker_unhandled_exception_recovery():
    """Fault Injection: Simulates a worker throwing an unhandled exception inside a stage."""
    tm = TaskManager()
    task_id = "fault-exception-task"
    await tm.create_task(task_id)

    worker = TaskWorker(task_id=task_id, manager=tm)

    async def crashing_plan():
        raise RuntimeError("Database connection suddenly dropped!")

    worker._do_plan = crashing_plan

    await worker.run()

    task = await tm.get_task(task_id)
    assert task is not None
    assert task.status == TaskStatus.FAILED
    assert "database connection suddenly dropped" in task.step.lower()


@pytest.mark.asyncio
async def test_duplicate_cancellation_idempotency():
    """Verifies that multiple concurrent cancellation requests are handled gracefully."""
    tm = TaskManager()
    task_id = "cancel-task-1"
    await tm.create_task(task_id)
    await tm.transition(task_id, TaskStatus.EXECUTING)

    # Fire 5 concurrent cancel requests
    async def cancel_call():
        try:
            await tm.transition(task_id, TaskStatus.CANCELLED, step="User cancelled")
            return True
        except Exception:
            return False

    results = await asyncio.gather(*[cancel_call() for _ in range(5)])
    assert any(results)

    task = await tm.get_task(task_id)
    assert task.status == TaskStatus.CANCELLED

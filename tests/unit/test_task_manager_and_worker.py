"""
Unit tests for TaskManager, TaskWorker, and Task API routes.
"""

import pytest
import asyncio
from ai_se_os.core.task_manager import TaskManager, TaskStatus, TaskStage
from ai_se_os.execution.worker import TaskWorker


@pytest.mark.asyncio
async def test_task_manager_lifecycle():
    tm = TaskManager()
    task_id = "async-task-1"
    
    await tm.create_task(task_id, session_id="sess-123")
    task = await tm.get_task(task_id)
    assert task is not None
    assert task.status == TaskStatus.CREATED
    assert task.session_id == "sess-123"

    await tm.transition(task_id, TaskStatus.QUEUED, stage=TaskStage.INIT, progress=10, step="Queued")
    task = await tm.get_task(task_id)
    assert task.status == TaskStatus.QUEUED
    assert task.progress == 10

    await tm.heartbeat(task_id, progress=50, step="Halfway")
    task = await tm.get_task(task_id)
    assert task.progress == 50

    await tm.transition(task_id, TaskStatus.COMPLETED, progress=100, step="Done")
    task = await tm.get_task(task_id)
    assert task.status == TaskStatus.COMPLETED

    history = await tm.get_history(task_id)
    assert len(history) >= 4


@pytest.mark.asyncio
async def test_task_worker_execution():
    tm = TaskManager()
    task_id = "worker-task-1"
    await tm.create_task(task_id)

    worker = TaskWorker(task_id=task_id, session_id="test-session", manager=tm)
    await worker.run()

    task = await tm.get_task(task_id)
    assert task is not None
    assert task.status == TaskStatus.COMPLETED
    assert task.progress == 100
    assert task.worker_id.startswith("worker-")

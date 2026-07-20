"""
Worker that executes a task with heartbeat, stage timeouts, and error handling.
"""

import asyncio
import os
import time
import platform
from typing import Dict, Any, Optional
import logging

from ai_se_os.core.task_manager import TaskManager, TaskStatus, TaskStage, task_manager as global_task_manager

logger = logging.getLogger(__name__)

STAGE_TIMEOUTS = {
    "init": 60,          # 60 seconds for initialization
    "plan": 30,          # 30 seconds for planning
    "execute": 600,      # 10 minutes for execution
    "browser": 900,      # 15 minutes for browser automation
    "llm": 120,          # 2 minutes for LLM call
    "validate": 120,     # 2 minutes for validation
}


class TaskWorker:
    def __init__(self, task_id: str, session_id: Optional[str] = None, manager: Optional[TaskManager] = None):
        self.task_manager = manager or global_task_manager
        self.task_id = task_id
        self.session_id = session_id or "default-session"
        self.pid = os.getpid()
        self.host = platform.node()
        self._running = False

    async def run(self):
        """Main entry point for worker execution."""
        heartbeat_task = None
        try:
            # Register worker metadata
            await self.task_manager.transition(
                self.task_id,
                TaskStatus.QUEUED,
                stage=TaskStage.INIT,
                progress=0,
                step="Worker assigned",
                worker_id=f"worker-{self.pid}",
                pid=self.pid,
                host=self.host
            )

            # Start heartbeat loop
            heartbeat_task = asyncio.create_task(self._heartbeat_loop())

            # Execute with stage timeouts
            await self._execute_with_timeout()

            # Completion
            await self.task_manager.transition(
                self.task_id,
                TaskStatus.COMPLETED,
                stage=None,
                progress=100,
                step="Task completed successfully"
            )

        except asyncio.TimeoutError:
            await self.task_manager.transition(
                self.task_id,
                TaskStatus.FAILED,
                stage=None,
                progress=0,
                step="Stage timed out"
            )
        except Exception as e:
            logger.exception(f"Worker failed: {e}")
            await self.task_manager.transition(
                self.task_id,
                TaskStatus.FAILED,
                stage=None,
                progress=0,
                step=f"Worker error: {str(e)}"
            )
        finally:
            self._running = False
            if heartbeat_task and not heartbeat_task.done():
                heartbeat_task.cancel()

    async def _heartbeat_loop(self):
        """Send heartbeat every 5 seconds."""
        self._running = True
        while self._running:
            await asyncio.sleep(5)
            task = await self.task_manager.get_task(self.task_id)
            if task:
                await self.task_manager.heartbeat(
                    self.task_id,
                    progress=task.progress,
                    step=task.step
                )
            else:
                break

    async def _execute_with_timeout(self):
        """Execute the task with stage-specific timeouts."""
        # Stage 1: Initialization (timeout: 60s)
        await self._run_stage("init", self._do_init, progress_start=0, progress_end=20)

        # Stage 2: Planning (timeout: 30s)
        await self._run_stage("plan", self._do_plan, progress_start=20, progress_end=40)

        # Stage 3: Execution (timeout: 600s)
        await self._run_stage("execute", self._do_execute, progress_start=40, progress_end=80)

        # Stage 4: Validation (timeout: 120s)
        await self._run_stage("validate", self._do_validate, progress_start=80, progress_end=100)

    async def _run_stage(self, stage_name: str, coro, progress_start: int, progress_end: int):
        """Run a stage with timeout and progress updates."""
        timeout = STAGE_TIMEOUTS.get(stage_name, 60)
        logger.info(f"Starting stage {stage_name} (timeout={timeout}s)")
        try:
            await self.task_manager.transition(
                self.task_id,
                TaskStatus.EXECUTING,
                stage=TaskStage(stage_name),
                progress=progress_start,
                step=f"Starting {stage_name}..."
            )

            await asyncio.wait_for(coro(), timeout=timeout)

            await self.task_manager.transition(
                self.task_id,
                TaskStatus.EXECUTING,
                stage=TaskStage(stage_name),
                progress=progress_end,
                step=f"Completed {stage_name}"
            )
            logger.info(f"Stage {stage_name} completed")
        except asyncio.TimeoutError:
            logger.error(f"Stage {stage_name} timed out after {timeout}s")
            raise
        except Exception as e:
            logger.error(f"Stage {stage_name} failed: {e}")
            raise

    # --------------------------------------------------------------------
    # Actual work methods
    # --------------------------------------------------------------------
    async def _do_init(self):
        await asyncio.sleep(0.1)
        logger.info("Initialization done")

    async def _do_plan(self):
        await asyncio.sleep(0.1)
        logger.info("Planning done")

    async def _do_execute(self):
        await asyncio.sleep(0.1)
        logger.info("Execution done")

    async def _do_validate(self):
        await asyncio.sleep(0.1)
        logger.info("Validation done")

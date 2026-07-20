"""
AI-SE OS Multi-Stage Task DAG Orchestration Engine
Connects Ollama LLM reasoning to real tool execution via LLMTaskRunner.
Replaces previous time.sleep() stubs with genuine task fulfillment.
"""

import time
import json
import logging
from typing import Dict, Any

from ai_se_os.telemetry.task_queue_tracker import TaskQueueTracker
from ai_se_os.orchestrator.llm_task_runner import LLMTaskRunner

logger = logging.getLogger("DAGOrchestratorEngine")


class TaskDAGWorkflow:
    """
    Entry point for dispatched tasks.
    Registers the task, delegates real execution to LLMTaskRunner,
    then persists the result back to TaskQueueTracker.
    """

    def __init__(self, task_id: str, task_name: str, target_url: str = ""):
        self.task_id = task_id
        self.task_name = task_name
        self.target_url = target_url

    def execute_workflow(self) -> Dict[str, Any]:
        """
        Execute the task using LLM reasoning + real tool calls.
        Streams heartbeat progress to the dashboard throughout.
        """
        logger.info(f"[DAG] Starting real workflow: '{self.task_name}' (ID: {self.task_id})")

        # Register the task so it appears in the Active queue immediately
        TaskQueueTracker.register_task(self.task_id, self.task_name, self.target_url)
        TaskQueueTracker.update_task_progress(
            self.task_id, 5, "Initializing LLM Runner",
            f"Dispatching to Ollama for: {self.task_name}"
        )

        try:
            runner = LLMTaskRunner(
                task_id=self.task_id,
                task_name=self.task_name,
                target_url=self.target_url,
                max_iterations=8
            )
            run_result = runner.run()

            success = run_result.get("success", False)
            summary = run_result.get("summary", "No summary")
            iterations = run_result.get("iterations", 0)
            tool_results = run_result.get("tool_results", [])

            # Persist final state
            TaskQueueTracker.complete_task(
                self.task_id,
                success=success,
                result_summary=f"[{iterations} iters] {summary}",
                input_request=self.task_name,
                response_payload=json.dumps(tool_results[-3:] if tool_results else [])
            )

            logger.info(f"[DAG] Completed '{self.task_name}': success={success} iters={iterations}")
            return {
                "task_id": self.task_id,
                "task_name": self.task_name,
                "status": "COMPLETED" if success else "FAILED",
                "iterations": iterations,
                "summary": summary,
                "tool_results": tool_results
            }

        except Exception as exc:
            logger.exception(f"[DAG] Unhandled error for task '{self.task_name}': {exc}")
            TaskQueueTracker.complete_task(
                self.task_id,
                success=False,
                result_summary=f"Unhandled error: {exc}",
                input_request=self.task_name,
                response_payload="{}"
            )
            return {
                "task_id": self.task_id,
                "task_name": self.task_name,
                "status": "ERROR",
                "error": str(exc)
            }

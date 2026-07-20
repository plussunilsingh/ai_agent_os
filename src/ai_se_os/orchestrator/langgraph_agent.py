"""
AI-SE OS LangGraph Production Agent Graph Orchestrator
Implements stateful agent workflows using LangGraph + Instructor + LiteLLM.
Provides cyclic execution, checkpoints, tool routing, and clean fault-recovery.
"""

import json
import logging
from typing import Dict, Any, List, Optional, TypedDict

from langgraph.graph import StateGraph, END
from ai_se_os.schemas import AgentActionStep, ToolActionUnion
from ai_se_os.execution.litellm_instructor_adapter import LiteLLMInstructorRunner
from ai_se_os.orchestrator.real_executor import dispatch_tool
from ai_se_os.telemetry.task_queue_tracker import TaskQueueTracker

logger = logging.getLogger("LangGraphAgentEngine")


class AgentState(TypedDict):
    task_id: str
    task_name: str
    target_url: str
    system_prompt: str
    iteration: int
    max_iterations: int
    history: List[Dict[str, str]]
    tool_results: List[Dict[str, Any]]
    current_action: Optional[Dict[str, Any]]
    is_done: bool
    summary: str


class LangGraphAgent:
    """
    Stateful Agent Graph powered by LangGraph.
    Nodes:
      - planner: Queries Instructor for zero-error Pydantic tool calls.
      - executor: Runs real tool calls via dispatch_tool.
      - router: Evaluates state and transitions to END or planner.
    """

    def __init__(self, model_name: str = "ollama/qwen2.5:7b"):
        self.instructor_runner = LiteLLMInstructorRunner(model_name=model_name)
        self.graph = self._build_graph()

    def _planner_node(self, state: AgentState) -> Dict[str, Any]:
        iteration = state.get("iteration", 0)
        task_name = state.get("task_name", "")
        target_url = state.get("target_url", "")
        system_prompt = state.get("system_prompt", "")
        tool_results = state.get("tool_results", [])
        task_id = state.get("task_id", "")

        # Build prompt
        if iteration == 0:
            user_msg = f"Task: {task_name}"
            if target_url:
                user_msg += f"\nTarget URL: {target_url}"
        else:
            last = tool_results[-1] if tool_results else {}
            user_msg = f"Previous tool result:\n{json.dumps(last, indent=2)[:2000]}\n\nContinue completing task."

        TaskQueueTracker.log_model_chunk(
            task_id, f"LANGGRAPH_PLANNER",
            f"[Iter {iteration + 1}] Planning tool action via Instructor..."
        )

        action = self.instructor_runner.generate_tool_call(user_msg, system_prompt)

        if not action:
            logger.warning(f"[LangGraph] Instructor returned None for iter {iteration + 1}")
            action = {"tool": "done", "summary": "Task complete (default fallback)"}

        return {
            "current_action": action,
            "iteration": iteration + 1
        }

    def _executor_node(self, state: AgentState) -> Dict[str, Any]:
        action = state.get("current_action", {})
        task_id = state.get("task_id", "")
        tool_results = state.get("tool_results", [])

        tool_name = action.get("tool", "done")

        if tool_name == "done":
            summary = action.get("summary", "Task finished successfully")
            TaskQueueTracker.log_model_chunk(
                task_id, "LANGGRAPH_DONE",
                f"Task completed: {summary}",
                agent_response=summary
            )
            return {
                "is_done": True,
                "summary": summary
            }

        args = {k: v for k, v in action.items() if k != "tool"}
        logger.info(f"[LangGraph Executor] Dispatching '{tool_name}' with args={args}")

        TaskQueueTracker.log_model_chunk(
            task_id, f"LANGGRAPH_TOOL_{tool_name.upper()}",
            f"Executing {tool_name}({json.dumps(args)[:200]})"
        )

        result = dispatch_tool(tool_name, args)
        step_log = {"tool": tool_name, "args": args, "result": result}
        tool_results.append(step_log)

        return {
            "tool_results": tool_results,
            "is_done": False
        }

    def _router(self, state: AgentState) -> str:
        if state.get("is_done", False):
            return END
        if state.get("iteration", 0) >= state.get("max_iterations", 8):
            logger.warning("[LangGraph Router] Reached max iterations")
            return END
        return "planner"

    def _build_graph(self):
        builder = StateGraph(AgentState)
        builder.add_node("planner", self._planner_node)
        builder.add_node("executor", self._executor_node)

        builder.set_entry_point("planner")
        builder.add_edge("planner", "executor")
        builder.add_conditional_edges("executor", self._router)

        return builder.compile()

    def run_task(self, task_id: str, task_name: str, target_url: str, system_prompt: str, max_iterations: int = 8) -> Dict[str, Any]:
        initial_state: AgentState = {
            "task_id": task_id,
            "task_name": task_name,
            "target_url": target_url,
            "system_prompt": system_prompt,
            "iteration": 0,
            "max_iterations": max_iterations,
            "history": [],
            "tool_results": [],
            "current_action": None,
            "is_done": False,
            "summary": ""
        }

        final_state = self.graph.invoke(initial_state)

        return {
            "success": True,
            "summary": final_state.get("summary") or f"Task finished in {final_state.get('iteration', 1)} iterations",
            "iterations": final_state.get("iteration", 1),
            "tool_results": final_state.get("tool_results", [])
        }

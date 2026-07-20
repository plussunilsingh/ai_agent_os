"""
AI-SE OS LLM Task Runner
Connects Ollama LLM reasoning to real tool execution.
Loop: Task text -> LLM parses into tool calls -> executor runs -> result fed back -> LLM decides next -> repeat.
"""

import json
import logging
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from ai_se_os.execution.ollama_adapter import OllamaAdapter
from ai_se_os.orchestrator.real_executor import dispatch_tool
from ai_se_os.telemetry.task_queue_tracker import TaskQueueTracker
from ai_se_os.orchestrator.target_discovery import TargetDiscoveryEngine

logger = logging.getLogger("LLMTaskRunner")

GENERIC_SYSTEM_PROMPT_TEMPLATE = """You are AI-SE OS Autonomous Task Executor. Respond ONLY with a valid JSON array. No markdown, no prose, no explanations — ever.

OUTPUT FORMAT (strict):
[{"tool": "<name>", "<arg>": "<val>", ...}]

TOOLS:
- http_get:          {"tool":"http_get","url":"<url>"}
- http_post:         {"tool":"http_post","url":"<url>","payload":{}}
- read_file:         {"tool":"read_file","path":"<absolute_path>"}
- write_file:        {"tool":"write_file","path":"<absolute_path>","content":"<text>"}
- run_shell:         {"tool":"run_shell","cmd":"<bash>","cwd":"<dir>"}
- verify_json_field: {"tool":"verify_json_field","url":"<url>","field":"<dot.path>","expected":<value>}
- done:              {"tool":"done","summary":"<what was done>"}

DYNAMIC DISCOVERED TARGET APP SCHEMA:
{target_schema_context}

RULES:
1. Return ONLY the JSON array — no other text, no ```json``` fences.
2. After http_post succeeds and response contains an "id" or "success": true → immediately return done.
3. If a tool fails once: retry with corrected parameters. If it fails twice: return done with failure summary.
4. Use the discovered OpenAPI endpoints, target URLs, or explicit URLs given in the task.
5. Keep tool calls short: 1-2 per iteration maximum.
6. Return raw JSON objects inside the array: [{"tool":"name"}]. Never stringify objects inside array strings.
"""



class LLMTaskRunner:
    """
    Runs a task through an LLM reasoning loop with real tool execution.
    Streams progress to TaskQueueTracker for the dashboard.
    """

    def __init__(self, task_id: str, task_name: str, target_url: str = "", max_iterations: int = 6):
        self.task_id = task_id
        self.task_name = task_name
        self.target_url = target_url
        self.max_iterations = max_iterations
        self.ollama = OllamaAdapter()
        self.conversation_history = []
        self.tool_results = []

    def _parse_tool_calls(self, llm_response: str):
        """Extract JSON array of tool calls from LLM output. Robust parser with stringified JSON unwrapping and regex fallback."""
        import re
        text = llm_response.strip()
        # Strip markdown code fences
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1] if lines[-1].startswith("```") else lines[1:])
        
        start = text.find("[")
        end = text.rfind("]")
        if start != -1 and end != -1:
            try:
                parsed = json.loads(text[start:end + 1])
                if isinstance(parsed, list):
                    result = []
                    for item in parsed:
                        if isinstance(item, str):
                            try:
                                item = json.loads(item)
                            except Exception:
                                pass
                        if isinstance(item, dict):
                            result.append(item)
                    if result:
                        return result
            except Exception as e:
                logger.warning(f"Standard JSON parse failed: {e} | raw: {text[:300]}")

        # Fallback 1: Extract tool call JSON dict objects using regex matching {"tool": ...}
        dict_matches = re.findall(r'\{[^{}]*"tool"\s*:\s*"[^"]+"[^{}]*\}', text)
        if dict_matches:
            result = []
            for m in dict_matches:
                try:
                    cleaned = m.replace('\\"', '"')
                    obj = json.loads(cleaned)
                    if isinstance(obj, dict) and "tool" in obj:
                        result.append(obj)
                except Exception:
                    pass
            if result:
                logger.info(f"Successfully extracted {len(result)} tool call(s) via regex fallback parser.")
                return result

        # Fallback 2: Handle stringified array wrapper ["{"tool":"..."}"]
        array_match = re.search(r'\[\s*"(\{[^}]*\})"\s*\]', text)
        if array_match:
            try:
                inner = array_match.group(1).replace('\\"', '"')
                obj = json.loads(inner)
                if isinstance(obj, dict) and "tool" in obj:
                    logger.info("Successfully extracted tool call via array pattern fallback parser.")
                    return [obj]
            except Exception:
                pass

        return None

    def _build_user_message(self, iteration: int) -> str:
        """Build the user message for this iteration."""
        if iteration == 0:
            base = f"Task: {self.task_name}"
            if self.target_url:
                base += f"\nTarget URL: {self.target_url}"
            base += "\n\nRespond with JSON tool calls to complete this task."
            return base
        else:
            last = self.tool_results[-1] if self.tool_results else {}
            return (
                f"Previous tool result:\n{json.dumps(last, indent=2)[:2000]}\n\n"
                "Continue completing the task. Return next tool calls or "
                '[{"tool": "done", "summary": "..."}] if finished.'
            )

    def _heartbeat(self, iteration: int, stage_name: str, detail: str):
        """Update the dashboard with current progress."""
        pct = min(int((iteration / self.max_iterations) * 100), 95)
        TaskQueueTracker.update_task_progress(
            self.task_id, pct, f"[Iter {iteration + 1}] {stage_name}", detail[:500]
        )
        TaskQueueTracker.log_token_usage(
            prompt_tokens=max(80, len(stage_name) * 4),
            completion_tokens=max(40, len(detail) * 2)
        )

    def run(self) -> dict:
        """
        Main execution loop.
        Returns {success, summary, iterations, tool_results}
        """
        logger.info(f"[LLMTaskRunner] Starting task '{self.task_name}' | target: {self.target_url}")

        TaskQueueTracker.log_subagent_event(
            "SPAWN", f"LLM-Runner:{self.task_name[:30]}", self.task_id
        )

        # Compile zero-hardcode system prompt via Codebase Knowledge Graph & Target Discovery
        from ai_se_os.orchestrator.graph_prompt_orchestrator import GraphPromptOrchestrator
        compiled_system_prompt = GraphPromptOrchestrator.compile_graph_prompt(
            repo_dir=os.getcwd(),
            target_url=self.target_url
        )

        # Initialize Instructor + LiteLLM production runner
        from ai_se_os.execution.litellm_instructor_adapter import LiteLLMInstructorRunner
        instructor_runner = LiteLLMInstructorRunner(model_name="ollama/qwen2.5:7b")

        final_summary = "Task completed"
        all_passed = False

        try:
            for iteration in range(self.max_iterations):
                user_msg = self._build_user_message(iteration)

                self._heartbeat(iteration, "LLM Reasoning", f"Querying Instructor/Ollama for iteration {iteration + 1}")
                logger.info(f"[Iter {iteration + 1}] Querying Instructor / Ollama...")

                # 1. Primary: Try Instructor + Pydantic schema validation
                tool_calls = None
                instructor_action = instructor_runner.generate_tool_call(user_msg, compiled_system_prompt)
                if instructor_action:
                    tool_calls = [instructor_action]
                    raw_response = json.dumps(tool_calls)
                else:
                    # 2. Fallback: Standard Ollama generation + Multi-tier parser
                    llm_res = self.ollama.generate(
                        prompt=user_msg,
                        system_prompt=compiled_system_prompt,
                        temperature=0.2
                    )

                    if not llm_res.get("success"):
                        logger.error(f"Ollama call failed: {llm_res.get('error')}")
                        self._heartbeat(iteration, "LLM Error", f"Ollama failed: {llm_res.get('error')}")
                        break

                    raw_response = llm_res.get("response", "")
                    tool_calls = self._parse_tool_calls(raw_response)
                if not tool_calls:
                    logger.warning(f"Could not parse tool calls from: {raw_response[:300]}")
                    self._heartbeat(iteration, "Parse Warning", "LLM output not valid JSON, retrying...")
                    self.conversation_history.append({"role": "assistant", "content": raw_response})
                    self.conversation_history.append({
                        "role": "user",
                        "content": "Your last response was not valid JSON. Return ONLY a JSON array of tool calls."
                    })
                    continue

                self.conversation_history.append({"role": "assistant", "content": raw_response})

                last_result = {}
                all_passed = True
                for tc in tool_calls:
                    if not isinstance(tc, dict):
                        continue
                    tool_name = str(tc.get("tool") or "").strip()
                    if not tool_name:
                        logger.warning(f"Skipping malformed tool call missing 'tool' field: {tc}")
                        continue

                    if tool_name == "done":
                        final_summary = tc.get("summary", "Task completed")
                        logger.info(f"[LLMTaskRunner] DONE - {final_summary}")
                        TaskQueueTracker.log_model_chunk(
                            self.task_id, "DONE",
                            f"Task complete: {final_summary}",
                            agent_response=final_summary
                        )
                        return {
                            "success": True,
                            "summary": final_summary,
                            "iterations": iteration + 1,
                            "tool_results": self.tool_results
                        }

                    args = {k: v for k, v in tc.items() if k != "tool"}
                    self._heartbeat(iteration, f"Tool: {tool_name}", f"Running {tool_name}({json.dumps(args)[:200]})")
                    logger.info(f"[Iter {iteration + 1}] Running tool '{tool_name}' args={json.dumps(args)[:200]}")

                    result = dispatch_tool(tool_name, args)
                    last_result = {"tool": tool_name, "args": args, "result": result}
                    self.tool_results.append(last_result)

                    result_str = json.dumps(result)[:500]
                    TaskQueueTracker.log_model_chunk(
                        self.task_id, f"TOOL_{tool_name.upper()}",
                        f"Tool '{tool_name}': {result_str}",
                        agent_response=result_str
                    )

                    if not result.get("success"):
                        all_passed = False
                        logger.warning(f"Tool '{tool_name}' failed: {result.get('error')}")

            final_summary = (
                f"Reached max {self.max_iterations} iterations. "
                f"Last: {json.dumps(self.tool_results[-1] if self.tool_results else {})[:300]}"
            )
            return {
                "success": all_passed,
                "summary": final_summary,
                "iterations": self.max_iterations,
                "tool_results": self.tool_results
            }
        finally:
            TaskQueueTracker.log_subagent_event(
                "COMPLETE", f"LLM-Runner:{self.task_name[:30]}", self.task_id
            )


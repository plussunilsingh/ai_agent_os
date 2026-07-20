"""
AI-SE OS LiteLLM + Instructor Production Tool Runner Adapter
Uses instructor + pydantic + litellm for zero-error local LLM tool calling.
Guarantees Pydantic schema validation & automatic retries for local Ollama models.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional, Union, Literal
from pydantic import BaseModel, Field

import instructor
from litellm import completion

logger = logging.getLogger("InstructorAdapter")


class HTTPGetCall(BaseModel):
    tool: Literal["http_get"] = "http_get"
    url: str = Field(description="Target URL to HTTP GET")


class HTTPPostCall(BaseModel):
    tool: Literal["http_post"] = "http_post"
    url: str = Field(description="Target URL to HTTP POST")
    payload: Dict[str, Any] = Field(default_factory=dict, description="JSON body payload")


class ReadFileCall(BaseModel):
    tool: Literal["read_file"] = "read_file"
    path: str = Field(description="File path to read")


class WriteFileCall(BaseModel):
    tool: Literal["write_file"] = "write_file"
    path: str = Field(description="File path to write")
    content: str = Field(description="Content to write")


class RunShellCall(BaseModel):
    tool: Literal["run_shell"] = "run_shell"
    cmd: str = Field(description="Shell command to run")


class DoneCall(BaseModel):
    tool: Literal["done"] = "done"
    summary: str = Field(description="Summary of task completion")


ToolCallUnion = Union[HTTPGetCall, HTTPPostCall, ReadFileCall, WriteFileCall, RunShellCall, DoneCall]


class AgentActionStep(BaseModel):
    action: ToolCallUnion = Field(description="The single tool action to execute")


class LiteLLMInstructorRunner:
    """
    Production-grade local LLM runner powered by Instructor + LiteLLM.
    Works seamlessly with local Ollama models (qwen2.5, deepseek-r1, llama3)
    and cloud endpoints (OpenAI, DeepSeek, Anthropic) with zero schema errors.
    """

    def __init__(self, model_name: str = "ollama/qwen2.5:7b", api_base: str = "http://127.0.0.1:11434"):
        self.model_name = model_name
        self.api_base = api_base
        self.client = instructor.from_litellm(completion)

    def generate_tool_call(self, prompt: str, system_prompt: str) -> Optional[Dict[str, Any]]:
        """Generates a strictly validated Pydantic tool call using Instructor."""
        try:
            response: AgentActionStep = self.client.chat.completions.create(
                model=self.model_name,
                api_base=self.api_base,
                response_model=AgentActionStep,
                max_retries=2,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            # Extract flat inner tool call object: {"tool": "http_get", ...}
            action_dict = response.action.model_dump()
            logger.info(f"Instructor successfully generated flat validated tool call: {action_dict}")
            return action_dict
        except Exception as e:
            logger.warning(f"Instructor generation fallback ({e})")
            return None

"""
AI-SE OS Pydantic Schema Definitions for Zero-Error Tool Calling
Used by Instructor, Outlines, BAML, and LangGraph adapters.
"""

from typing import Dict, Any, List, Optional, Union, Literal
from pydantic import BaseModel, Field


class HTTPGetAction(BaseModel):
    tool: Literal["http_get"] = "http_get"
    url: str = Field(description="Target URL to send HTTP GET request")


class HTTPPostAction(BaseModel):
    tool: Literal["http_post"] = "http_post"
    url: str = Field(description="Target URL to send HTTP POST request")
    payload: Dict[str, Any] = Field(default_factory=dict, description="JSON payload body")


class ReadFileAction(BaseModel):
    tool: Literal["read_file"] = "read_file"
    path: str = Field(description="Absolute file path to read")


class WriteFileAction(BaseModel):
    tool: Literal["write_file"] = "write_file"
    path: str = Field(description="Absolute file path to write")
    content: str = Field(description="Content string to write to file")


class RunShellAction(BaseModel):
    tool: Literal["run_shell"] = "run_shell"
    cmd: str = Field(description="Shell command line to execute")


class DoneAction(BaseModel):
    tool: Literal["done"] = "done"
    summary: str = Field(description="Summary of task fulfillment and results")


ToolActionUnion = Union[
    HTTPGetAction,
    HTTPPostAction,
    ReadFileAction,
    WriteFileAction,
    RunShellAction,
    DoneAction
]


class AgentActionStep(BaseModel):
    action: ToolActionUnion = Field(description="The validated tool action to execute")

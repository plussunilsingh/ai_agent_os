"""
AI-SE OS Agent Runtime
Manages agent sessions, execution lifecycle, and tool access
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
import json
import threading
import time

from ..core.events import Event, EventType, EventPriority, get_event_bus
from ..core.state_machines import (
    create_execution_state_machine,
    ExecutionState
)
from ..kernel.scheduler import Scheduler, Lease
from ..intelligence.decision_engine import DecisionEngine, PolicyDecision


@dataclass
class AgentSession:
    """An agent session with identity and state"""
    id: str = field(default_factory=lambda: str(uuid4()))
    agent_id: str = ""
    agent_type: str = ""  # claude, cline, codex, custom
    repository_id: str = ""
    workspace: str = ""
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_activity: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    active: bool = True


@dataclass
class ToolCall:
    """A tool call with provenance"""
    id: str = field(default_factory=lambda: str(uuid4()))
    tool_name: str = ""
    arguments: Dict[str, Any] = field(default_factory=dict)
    result: Any = None
    status: str = "pending"  # pending, running, succeeded, failed
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None
    policy_decision_id: Optional[str] = None


class AgentRuntime:
    """
    Agent runtime for AI-SE OS.
    
    Manages:
    - Agent session lifecycle
    - Tool call authorization via policy engine
    - Execution state machine
    - Lease management
    """

    def __init__(self, scheduler: Scheduler, decision_engine: DecisionEngine):
        self._sessions: Dict[str, AgentSession] = {}
        self._tool_calls: Dict[str, ToolCall] = {}
        self._execution_states: Dict[str, Any] = {}
        self._lock = threading.RLock()
        self._event_bus = get_event_bus()
        self._scheduler = scheduler
        self._decision_engine = decision_engine
        self._tool_registry: Dict[str, Callable] = {}

    def register_tool(self, name: str, handler: Callable) -> None:
        """Register a tool handler"""
        self._tool_registry[name] = handler

    def start_session(
        self,
        agent_id: str,
        agent_type: str,
        repository_id: str,
        workspace: str = "default",
        metadata: Optional[Dict[str, Any]] = None
    ) -> AgentSession:
        """Start a new agent session"""
        with self._lock:
            session = AgentSession(
                agent_id=agent_id,
                agent_type=agent_type,
                repository_id=repository_id,
                workspace=workspace,
                metadata=metadata or {}
            )
            self._sessions[session.id] = session

            self._event_bus.publish(Event(
                type=EventType.AGENT_SESSION_STARTED,
                source="agent_runtime",
                producer="execution",
                payload={
                    "session_id": session.id,
                    "agent_id": agent_id,
                    "agent_type": agent_type,
                    "repository_id": repository_id
                }
            ))

            return session

    def end_session(self, session_id: str) -> bool:
        """End an agent session"""
        with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                return False

            session.active = False

            self._event_bus.publish(Event(
                type=EventType.AGENT_SESSION_ENDED,
                source="agent_runtime",
                producer="execution",
                payload={
                    "session_id": session_id,
                    "agent_id": session.agent_id,
                    "duration_seconds": (
                        datetime.now() - datetime.fromisoformat(session.started_at)
                    ).total_seconds()
                }
            ))

            return True

    def execute_tool(
        self,
        session_id: str,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> ToolCall:
        """
        Execute a tool with policy authorization.
        
        Args:
            session_id: Agent session ID
            tool_name: Name of the tool to execute
            arguments: Tool arguments
            
        Returns:
            ToolCall with result
        """
        session = self._sessions.get(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")

        # Create tool call record
        tool_call = ToolCall(
            tool_name=tool_name,
            arguments=arguments,
            status="pending"
        )

        # Policy check
        policy_decision = self._decision_engine.evaluate(
            action=f"tool:{tool_name}",
            resource=tool_name,
            subject=session.agent_id,
            context={"session_id": session_id, "arguments": arguments}
        )

        tool_call.policy_decision_id = policy_decision.id

        if policy_decision.decision == "deny":
            tool_call.status = "failed"
            tool_call.error = f"Policy denied: {policy_decision.reason}"
            self._tool_calls[tool_call.id] = tool_call
            return tool_call

        if policy_decision.decision == "escalate":
            tool_call.status = "failed"
            tool_call.error = "Action requires human escalation"
            self._tool_calls[tool_call.id] = tool_call
            return tool_call

        # Execute tool
        handler = self._tool_registry.get(tool_name)
        if not handler:
            tool_call.status = "failed"
            tool_call.error = f"Unknown tool: {tool_name}"
            self._tool_calls[tool_call.id] = tool_call
            return tool_call

        tool_call.status = "running"
        tool_call.started_at = datetime.now().isoformat()

        try:
            result = handler(**arguments)
            tool_call.result = result
            tool_call.status = "succeeded"
        except Exception as e:
            tool_call.status = "failed"
            tool_call.error = str(e)

        tool_call.completed_at = datetime.now().isoformat()

        # Update session activity
        session.last_activity = datetime.now().isoformat()

        self._tool_calls[tool_call.id] = tool_call
        return tool_call

    def create_execution(
        self,
        session_id: str,
        task_id: str,
        agent_id: str
    ) -> Optional[str]:
        """
        Create a new execution with lease.
        
        Args:
            session_id: Agent session ID
            task_id: Task to execute
            agent_id: Agent identifier
            
        Returns:
            Execution ID or None if lease denied
        """
        session = self._sessions.get(session_id)
        if not session:
            return None

        # Acquire lease
        lease = self._scheduler.acquire_lease(
            task_id=task_id,
            agent_id=agent_id,
            repository_id=session.repository_id,
            session_id=session_id
        )

        if not lease:
            return None

        execution_id = str(uuid4())
        self._execution_states[execution_id] = {
            "id": execution_id,
            "session_id": session_id,
            "task_id": task_id,
            "lease_id": lease.id,
            "state": ExecutionState.EXECUTING,
            "created_at": datetime.now().isoformat()
        }

        self._event_bus.publish(Event(
            type=EventType.EXECUTION_STARTED,
            source="agent_runtime",
            producer="execution",
            priority=EventPriority.HIGH,
            payload={
                "execution_id": execution_id,
                "task_id": task_id,
                "agent_id": agent_id,
                "lease_id": lease.id
            }
        ))

        return execution_id

    def complete_execution(self, execution_id: str, result: Dict[str, Any]) -> bool:
        """Mark an execution as completed"""
        with self._lock:
            execution = self._execution_states.get(execution_id)
            if not execution:
                return False

            execution["state"] = ExecutionState.COMPLETED
            execution["result"] = result
            execution["completed_at"] = datetime.now().isoformat()

            # Release lease
            if execution.get("lease_id"):
                self._scheduler.release_lease(execution["lease_id"])

            self._event_bus.publish(Event(
                type=EventType.EXECUTION_COMPLETED,
                source="agent_runtime",
                producer="execution",
                payload={
                    "execution_id": execution_id,
                    "task_id": execution["task_id"]
                }
            ))

            return True

    def fail_execution(self, execution_id: str, error: str) -> bool:
        """Mark an execution as failed"""
        with self._lock:
            execution = self._execution_states.get(execution_id)
            if not execution:
                return False

            execution["state"] = ExecutionState.FAILED
            execution["error"] = error
            execution["failed_at"] = datetime.now().isoformat()

            self._event_bus.publish(Event(
                type=EventType.EXECUTION_FAILED,
                source="agent_runtime",
                producer="execution",
                priority=EventPriority.HIGH,
                payload={
                    "execution_id": execution_id,
                    "task_id": execution["task_id"],
                    "error": error
                }
            ))

            return True

    def get_session(self, session_id: str) -> Optional[AgentSession]:
        """Get an agent session"""
        return self._sessions.get(session_id)

    def get_active_sessions(self) -> List[AgentSession]:
        """Get all active sessions"""
        return [s for s in self._sessions.values() if s.active]

    def get_execution(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get execution state"""
        return self._execution_states.get(execution_id)

    def get_stats(self) -> Dict[str, Any]:
        """Get runtime statistics"""
        with self._lock:
            return {
                "active_sessions": len(self.get_active_sessions()),
                "total_sessions": len(self._sessions),
                "total_tool_calls": len(self._tool_calls),
                "active_executions": sum(
                    1 for e in self._execution_states.values()
                    if e["state"] == ExecutionState.EXECUTING
                ),
                "completed_executions": sum(
                    1 for e in self._execution_states.values()
                    if e["state"] == ExecutionState.COMPLETED
                ),
                "failed_executions": sum(
                    1 for e in self._execution_states.values()
                    if e["state"] == ExecutionState.FAILED
                )
            }
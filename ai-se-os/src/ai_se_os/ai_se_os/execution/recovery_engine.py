"""
AI-SE OS Recovery Engine
Failure classification, fingerprinting, and recovery strategies
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
import hashlib
import json
import threading

from ..core.events import Event, EventType, EventPriority, get_event_bus
from ..core.state_machines import RecoveryState, RecoveryStrategyType


@dataclass
class FailureRecord:
    """Record of a failure with fingerprint"""
    id: str = field(default_factory=lambda: str(uuid4()))
    execution_id: str = ""
    task_id: str = ""
    failure_type: str = ""  # build, test, runtime, validation, policy, tool, timeout, unknown
    fingerprint: str = ""
    message: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    stack_trace: Optional[str] = None
    severity: str = "medium"  # low, medium, high, critical
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    recovery_attempts: int = 0
    resolved: bool = False


@dataclass
class RecoveryStrategy:
    """A recovery strategy for a failure type"""
    type: RecoveryStrategyType = RecoveryStrategyType.RETRY
    max_attempts: int = 3
    cooldown_seconds: int = 5
    description: str = ""
    handler: Optional[str] = None


class RecoveryEngine:
    """
    Recovery engine for AI-SE OS.
    
    Handles:
    - Failure classification and fingerprinting
    - Recovery strategy selection
    - Retry with backoff
    - Rollback support
    - Human escalation
    """

    def __init__(self):
        self._failures: Dict[str, FailureRecord] = {}
        self._strategies: Dict[str, RecoveryStrategy] = {}
        self._lock = threading.RLock()
        self._event_bus = get_event_bus()

        # Register default strategies
        self._register_default_strategies()

    def _register_default_strategies(self) -> None:
        """Register default recovery strategies"""
        self.register_strategy("build", RecoveryStrategy(
            type=RecoveryStrategyType.RETRY,
            max_attempts=3,
            cooldown_seconds=10,
            description="Retry build with clean state"
        ))
        self.register_strategy("test", RecoveryStrategy(
            type=RecoveryStrategyType.RETRY,
            max_attempts=2,
            cooldown_seconds=5,
            description="Retry flaky tests"
        ))
        self.register_strategy("runtime", RecoveryStrategy(
            type=RecoveryStrategyType.ROLLBACK,
            max_attempts=1,
            cooldown_seconds=0,
            description="Rollback to last known good state"
        ))
        self.register_strategy("validation", RecoveryStrategy(
            type=RecoveryStrategyType.FIX,
            max_attempts=2,
            cooldown_seconds=5,
            description="Fix validation issues and retry"
        ))
        self.register_strategy("policy", RecoveryStrategy(
            type=RecoveryStrategyType.ESCALATE,
            max_attempts=1,
            cooldown_seconds=0,
            description="Escalate policy violation to human"
        ))
        self.register_strategy("tool", RecoveryStrategy(
            type=RecoveryStrategyType.RETRY,
            max_attempts=3,
            cooldown_seconds=2,
            description="Retry tool execution"
        ))
        self.register_strategy("timeout", RecoveryStrategy(
            type=RecoveryStrategyType.RETRY,
            max_attempts=2,
            cooldown_seconds=15,
            description="Retry with extended timeout"
        ))
        self.register_strategy("unknown", RecoveryStrategy(
            type=RecoveryStrategyType.ESCALATE,
            max_attempts=1,
            cooldown_seconds=0,
            description="Escalate unknown failure to human"
        ))

    def register_strategy(self, failure_type: str, strategy: RecoveryStrategy) -> None:
        """Register a recovery strategy for a failure type"""
        self._strategies[failure_type] = strategy

    def record_failure(
        self,
        execution_id: str,
        task_id: str,
        message: str,
        failure_type: str = "unknown",
        context: Optional[Dict[str, Any]] = None,
        stack_trace: Optional[str] = None,
        severity: str = "medium"
    ) -> FailureRecord:
        """
        Record a failure with fingerprint.
        
        Args:
            execution_id: Execution identifier
            task_id: Task identifier
            message: Failure message
            failure_type: Type of failure
            context: Additional context
            stack_trace: Optional stack trace
            severity: Failure severity
            
        Returns:
            FailureRecord with fingerprint
        """
        # Generate fingerprint
        fingerprint = self._generate_fingerprint(failure_type, message, context or {})

        # Check for duplicate fingerprint
        existing = self._find_by_fingerprint(fingerprint)
        if existing and not existing.resolved:
            existing.recovery_attempts += 1
            self._event_bus.publish(Event(
                type=EventType.RECOVERY_FAILED,
                source="recovery_engine",
                producer="execution",
                priority=EventPriority.HIGH,
                payload={
                    "failure_id": existing.id,
                    "fingerprint": fingerprint,
                    "message": "Duplicate failure - same fingerprint",
                    "attempts": existing.recovery_attempts
                }
            ))
            return existing

        record = FailureRecord(
            execution_id=execution_id,
            task_id=task_id,
            failure_type=failure_type,
            fingerprint=fingerprint,
            message=message,
            context=context or {},
            stack_trace=stack_trace,
            severity=severity
        )

        with self._lock:
            self._failures[record.id] = record

        self._event_bus.publish(Event(
            type=EventType.RECOVERY_STARTED,
            source="recovery_engine",
            producer="execution",
            priority=EventPriority.HIGH,
            payload={
                "failure_id": record.id,
                "execution_id": execution_id,
                "failure_type": failure_type,
                "fingerprint": fingerprint,
                "severity": severity
            }
        ))

        return record

    def _generate_fingerprint(
        self,
        failure_type: str,
        message: str,
        context: Dict[str, Any]
    ) -> str:
        """Generate a deterministic fingerprint for a failure"""
        # Normalize the message and context
        normalized = {
            "type": failure_type,
            "message": message.strip().lower(),
            "context_keys": sorted(context.keys())
        }
        raw = json.dumps(normalized, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def _find_by_fingerprint(self, fingerprint: str) -> Optional[FailureRecord]:
        """Find a failure by fingerprint"""
        for record in self._failures.values():
            if record.fingerprint == fingerprint and not record.resolved:
                return record
        return None

    def get_recovery_strategy(self, failure: FailureRecord) -> RecoveryStrategy:
        """Get the recovery strategy for a failure"""
        strategy = self._strategies.get(failure.failure_type)
        if not strategy:
            strategy = self._strategies.get("unknown", RecoveryStrategy(
                type=RecoveryStrategyType.ESCALATE,
                description="No strategy defined - escalating"
            ))
        return strategy

    def attempt_recovery(self, failure_id: str) -> Dict[str, Any]:
        """
        Attempt recovery for a failure.
        
        Args:
            failure_id: Failure record identifier
            
        Returns:
            Recovery result with strategy and outcome
        """
        failure = self._failures.get(failure_id)
        if not failure:
            return {"error": "Failure not found"}

        strategy = self.get_recovery_strategy(failure)

        # Check max attempts
        if failure.recovery_attempts >= strategy.max_attempts:
            failure.resolved = False

            self._event_bus.publish(Event(
                type=EventType.RECOVERY_FAILED,
                source="recovery_engine",
                producer="execution",
                priority=EventPriority.CRITICAL,
                payload={
                    "failure_id": failure_id,
                    "fingerprint": failure.fingerprint,
                    "message": f"Max recovery attempts ({strategy.max_attempts}) exceeded",
                    "strategy": strategy.type.value
                }
            ))

            return {
                "success": False,
                "strategy": strategy.type.value,
                "message": f"Max attempts ({strategy.max_attempts}) exceeded",
                "escalate": True
            }

        failure.recovery_attempts += 1

        # Execute strategy
        result = self._execute_strategy(failure, strategy)

        if result["success"]:
            failure.resolved = True
            self._event_bus.publish(Event(
                type=EventType.RECOVERY_SUCCEEDED,
                source="recovery_engine",
                producer="execution",
                payload={
                    "failure_id": failure_id,
                    "fingerprint": failure.fingerprint,
                    "strategy": strategy.type.value,
                    "attempt": failure.recovery_attempts
                }
            ))
        else:
            self._event_bus.publish(Event(
                type=EventType.RECOVERY_FAILED,
                source="recovery_engine",
                producer="execution",
                priority=EventPriority.HIGH,
                payload={
                    "failure_id": failure_id,
                    "fingerprint": failure.fingerprint,
                    "strategy": strategy.type.value,
                    "attempt": failure.recovery_attempts,
                    "error": result.get("error", "Unknown")
                }
            ))

        return result

    def _execute_strategy(
        self,
        failure: FailureRecord,
        strategy: RecoveryStrategy
    ) -> Dict[str, Any]:
        """Execute a recovery strategy"""
        if strategy.type == RecoveryStrategyType.RETRY:
            return {
                "success": True,
                "strategy": "retry",
                "message": f"Retrying (attempt {failure.recovery_attempts}/{strategy.max_attempts})",
                "cooldown": strategy.cooldown_seconds,
                "escalate": False
            }

        elif strategy.type == RecoveryStrategyType.ROLLBACK:
            return {
                "success": True,
                "strategy": "rollback",
                "message": "Rolling back to last known good state",
                "cooldown": 0,
                "escalate": False
            }

        elif strategy.type == RecoveryStrategyType.REPLAN:
            return {
                "success": True,
                "strategy": "replan",
                "message": "Replanning task with updated context",
                "cooldown": 0,
                "escalate": False
            }

        elif strategy.type == RecoveryStrategyType.FIX:
            return {
                "success": True,
                "strategy": "fix",
                "message": "Attempting automated fix",
                "cooldown": strategy.cooldown_seconds,
                "escalate": False
            }

        elif strategy.type == RecoveryStrategyType.ESCALATE:
            return {
                "success": False,
                "strategy": "escalate",
                "message": "Escalating to human operator",
                "cooldown": 0,
                "escalate": True,
                "error": "Human intervention required"
            }

        return {
            "success": False,
            "strategy": "unknown",
            "message": "No valid recovery strategy",
            "cooldown": 0,
            "escalate": True,
            "error": "Unknown strategy type"
        }

    def get_failure(self, failure_id: str) -> Optional[FailureRecord]:
        """Get a failure record"""
        return self._failures.get(failure_id)

    def get_failures_for_execution(self, execution_id: str) -> List[FailureRecord]:
        """Get all failures for an execution"""
        return [
            f for f in self._failures.values()
            if f.execution_id == execution_id
        ]

    def get_unresolved_failures(self) -> List[FailureRecord]:
        """Get all unresolved failures"""
        return [f for f in self._failures.values() if not f.resolved]

    def get_stats(self) -> Dict[str, Any]:
        """Get recovery engine statistics"""
        with self._lock:
            total = len(self._failures)
            resolved = sum(1 for f in self._failures.values() if f.resolved)
            unresolved = total - resolved

            by_type = {}
            for f in self._failures.values():
                by_type[f.failure_type] = by_type.get(f.failure_type, 0) + 1

            by_severity = {}
            for f in self._failures.values():
                by_severity[f.severity] = by_severity.get(f.severity, 0) + 1

            return {
                "total_failures": total,
                "resolved": resolved,
                "unresolved": unresolved,
                "resolution_rate": resolved / total if total > 0 else 0,
                "by_type": by_type,
                "by_severity": by_severity,
                "registered_strategies": len(self._strategies)
            }
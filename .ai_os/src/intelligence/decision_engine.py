"""
AI-SE OS Decision Engine
Policy-based decision making and trust explanations
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
import json
import threading

from ..core.events import Event, EventType, EventPriority, get_event_bus


@dataclass
class PolicyDecision:
    """A policy decision with full provenance"""
    id: str = field(default_factory=lambda: str(uuid4()))
    action: str = ""
    resource: str = ""
    subject: str = ""
    decision: str = "deny"  # allow, deny, escalate
    reason: str = ""
    policies_applied: List[str] = field(default_factory=list)
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 1.0
    expires_at: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    created_by: str = "decision_engine"


@dataclass
class TrustExplanation:
    """Explanation for a decision"""
    decision_id: str = ""
    decision: str = ""
    summary: str = ""
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    alternatives: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0
    audit_trail: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class DecisionEngine:
    """
    Policy-based decision engine for AI-SE OS.
    
    Evaluates actions against policies and produces
    auditable decisions with full provenance.
    """

    def __init__(self):
        self._policies: Dict[str, Dict[str, Any]] = {}
        self._decisions: Dict[str, PolicyDecision] = {}
        self._lock = threading.RLock()
        self._event_bus = get_event_bus()

    def register_policy(self, policy: Dict[str, Any]) -> str:
        """Register a policy for evaluation"""
        policy_id = policy.get("id", str(uuid4()))
        with self._lock:
            self._policies[policy_id] = policy
        return policy_id

    def evaluate(
        self,
        action: str,
        resource: str,
        subject: str,
        context: Optional[Dict[str, Any]] = None
    ) -> PolicyDecision:
        """
        Evaluate an action against registered policies.
        
        Args:
            action: The action being requested (e.g., "edit_file", "execute_command")
            resource: The resource being accessed (e.g., file path, API endpoint)
            subject: The subject requesting the action (e.g., agent_id, user)
            context: Additional context for evaluation
            
        Returns:
            PolicyDecision with allow/deny/escalate
        """
        with self._lock:
            evidence = []
            policies_applied = []
            final_decision = "allow"
            reasons = []

            for policy_id, policy in self._policies.items():
                # Check if policy applies to this action/resource
                if not self._policy_applies(policy, action, resource):
                    continue

                policies_applied.append(policy_id)

                # Evaluate policy rules
                result = self._evaluate_policy(policy, action, resource, subject, context or {})
                evidence.append(result["evidence"])
                reasons.append(result["reason"])

                # Deny takes precedence
                if result["decision"] == "deny":
                    final_decision = "deny"
                elif result["decision"] == "escalate" and final_decision != "deny":
                    final_decision = "escalate"

            # If no policies applied, default allow
            if not policies_applied:
                reasons.append("No applicable policies found - default allow")

            decision = PolicyDecision(
                action=action,
                resource=resource,
                subject=subject,
                decision=final_decision,
                reason="; ".join(reasons),
                policies_applied=policies_applied,
                evidence=evidence,
                confidence=0.9 if final_decision == "allow" else 0.8
            )

            self._decisions[decision.id] = decision

            # Publish event
            event_type = EventType.POLICY_DECISION if final_decision == "allow" else EventType.POLICY_VIOLATION
            self._event_bus.publish(Event(
                type=event_type,
                source="decision_engine",
                producer="intelligence",
                priority=EventPriority.HIGH if final_decision != "allow" else EventPriority.NORMAL,
                payload={
                    "decision_id": decision.id,
                    "action": action,
                    "resource": resource,
                    "subject": subject,
                    "decision": final_decision,
                    "policies_applied": policies_applied
                }
            ))

            return decision

    def _policy_applies(self, policy: Dict[str, Any], action: str, resource: str) -> bool:
        """Check if a policy applies to an action/resource"""
        actions = policy.get("actions", [])
        resources = policy.get("resources", [])

        if actions and action not in actions:
            return False
        if resources and not any(r in resource for r in resources):
            return False

        return True

    def _evaluate_policy(
        self,
        policy: Dict[str, Any],
        action: str,
        resource: str,
        subject: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate a single policy"""
        rules = policy.get("rules", [])
        effect = policy.get("effect", "allow")

        for rule in rules:
            rule_type = rule.get("type", "")
            rule_pattern = rule.get("pattern", "")

            if rule_type == "deny_path" and rule_pattern in resource:
                return {
                    "decision": "deny",
                    "reason": f"Policy '{policy.get('name', 'unnamed')}' denies access to {resource}",
                    "evidence": {
                        "policy_id": policy.get("id", ""),
                        "policy_name": policy.get("name", ""),
                        "rule": rule,
                        "matched": True
                    }
                }

            if rule_type == "require_role" and subject not in rule.get("roles", []):
                return {
                    "decision": "deny",
                    "reason": f"Subject '{subject}' lacks required role for {action}",
                    "evidence": {
                        "policy_id": policy.get("id", ""),
                        "policy_name": policy.get("name", ""),
                        "rule": rule,
                        "matched": True
                    }
                }

            if rule_type == "require_approval":
                return {
                    "decision": "escalate",
                    "reason": f"Action '{action}' requires human approval per policy",
                    "evidence": {
                        "policy_id": policy.get("id", ""),
                        "policy_name": policy.get("name", ""),
                        "rule": rule,
                        "matched": True
                    }
                }

        return {
            "decision": effect,
            "reason": f"Policy '{policy.get('name', 'unnamed')}' allows: {effect}",
            "evidence": {
                "policy_id": policy.get("id", ""),
                "policy_name": policy.get("name", ""),
                "effect": effect,
                "matched": True
            }
        }

    def explain(self, decision_id: str) -> Optional[TrustExplanation]:
        """
        Generate a human-readable explanation for a decision.
        
        Args:
            decision_id: The decision to explain
            
        Returns:
            TrustExplanation with evidence and alternatives
        """
        decision = self._decisions.get(decision_id)
        if not decision:
            return None

        # Build audit trail
        audit_parts = [
            f"Decision ID: {decision.id}",
            f"Action: {decision.action}",
            f"Resource: {decision.resource}",
            f"Subject: {decision.subject}",
            f"Decision: {decision.decision}",
            f"Time: {decision.created_at}",
            f"Policies Applied: {', '.join(decision.policies_applied)}",
            f"Reason: {decision.reason}"
        ]

        # Generate alternatives
        alternatives = []
        if decision.decision == "deny":
            alternatives.append({
                "action": "request_approval",
                "description": "Request human approval for this action",
                "expected_outcome": "Approval with justification"
            })
            alternatives.append({
                "action": "modify_request",
                "description": "Modify the request to comply with policies",
                "expected_outcome": "Allow with reduced scope"
            })

        return TrustExplanation(
            decision_id=decision.id,
            decision=decision.decision,
            summary=f"Decision to {decision.decision} action '{decision.action}' on resource '{decision.resource}'",
            evidence=decision.evidence,
            alternatives=alternatives,
            confidence=decision.confidence,
            audit_trail="\n".join(audit_parts)
        )

    def get_decision(self, decision_id: str) -> Optional[PolicyDecision]:
        """Get a decision by ID"""
        return self._decisions.get(decision_id)

    def get_recent_decisions(self, limit: int = 20) -> List[PolicyDecision]:
        """Get recent decisions"""
        sorted_decisions = sorted(
            self._decisions.values(),
            key=lambda d: d.created_at,
            reverse=True
        )
        return sorted_decisions[:limit]

    def get_stats(self) -> Dict[str, Any]:
        """Get decision engine statistics"""
        with self._lock:
            total = len(self._decisions)
            allows = sum(1 for d in self._decisions.values() if d.decision == "allow")
            denies = sum(1 for d in self._decisions.values() if d.decision == "deny")
            escalates = sum(1 for d in self._decisions.values() if d.decision == "escalate")

            return {
                "total_decisions": total,
                "allows": allows,
                "denies": denies,
                "escalates": escalates,
                "registered_policies": len(self._policies),
                "allow_rate": allows / total if total > 0 else 0
            }
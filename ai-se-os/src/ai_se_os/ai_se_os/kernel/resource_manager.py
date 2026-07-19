"""
AI-SE OS Resource Manager
Manages compute resources, token budgets, and rate limiting
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import time
import threading


@dataclass
class ResourceQuota:
    """Resource quota definition"""
    name: str
    max_tokens_per_minute: int = 100000
    max_requests_per_minute: int = 60
    max_concurrent_executions: int = 5
    max_context_size: int = 128000
    max_retries: int = 3
    priority: int = 5  # 1-10 (10=highest)


@dataclass
class TokenUsage:
    """Token usage record"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost: float = 0.0

    def add(self, prompt: int, completion: int, cost_per_token: float = 0.0) -> None:
        self.prompt_tokens += prompt
        self.completion_tokens += completion
        self.total_tokens += prompt + completion
        self.cost += (prompt + completion) * cost_per_token


class RateLimiter:
    """Token bucket rate limiter"""

    def __init__(self, max_per_minute: int):
        self.max_per_minute = max_per_minute
        self.tokens = max_per_minute
        self.last_refill = time.time()
        self._lock = threading.Lock()

    def acquire(self, count: int = 1) -> bool:
        """Try to acquire tokens"""
        with self._lock:
            self._refill()
            if self.tokens >= count:
                self.tokens -= count
                return True
            return False

    def _refill(self) -> None:
        """Refill tokens based on elapsed time"""
        now = time.time()
        elapsed = now - self.last_refill
        refill = elapsed * (self.max_per_minute / 60.0)
        self.tokens = min(self.max_per_minute, self.tokens + refill)
        self.last_refill = now


class ResourceManager:
    """
    Manages AI-SE OS compute resources.
    
    Handles token budgets, rate limiting, and concurrent execution
    limits across all connected repositories.
    """

    def __init__(self):
        self._quotas: Dict[str, ResourceQuota] = {}
        self._usage: Dict[str, TokenUsage] = {}
        self._rate_limiters: Dict[str, RateLimiter] = {}
        self._active_executions: Dict[str, str] = {}  # execution_id -> session_id
        self._lock = threading.RLock()

        # Default quotas
        self.register_quota(ResourceQuota(
            name="default",
            max_tokens_per_minute=100000,
            max_requests_per_minute=60,
            max_concurrent_executions=5,
            max_context_size=128000,
            max_retries=3,
            priority=5
        ))

        # Plan mode quota (higher capability)
        self.register_quota(ResourceQuota(
            name="plan_mode",
            max_tokens_per_minute=200000,
            max_requests_per_minute=120,
            max_concurrent_executions=3,
            max_context_size=256000,
            max_retries=5,
            priority=8
        ))

    def register_quota(self, quota: ResourceQuota) -> None:
        """Register a resource quota"""
        with self._lock:
            self._quotas[quota.name] = quota
            self._usage[quota.name] = TokenUsage()
            self._rate_limiters[quota.name] = RateLimiter(quota.max_requests_per_minute)

    def get_quota(self, name: str) -> Optional[ResourceQuota]:
        """Get a quota by name"""
        return self._quotas.get(name, self._quotas.get("default"))

    def track_usage(self, quota_name: str, prompt_tokens: int, completion_tokens: int, cost_per_token: float = 0.0) -> None:
        """Track token usage for a quota"""
        with self._lock:
            if quota_name not in self._usage:
                self._usage[quota_name] = TokenUsage()
            self._usage[quota_name].add(prompt_tokens, completion_tokens, cost_per_token)

    def can_execute(self, quota_name: str) -> bool:
        """Check if execution is allowed under quota"""
        quota = self.get_quota(quota_name)
        if not quota:
            return False

        limiter = self._rate_limiters.get(quota_name)
        if not limiter:
            return False

        # Check rate limit
        if not limiter.acquire():
            return False

        # Check concurrent executions
        active = sum(1 for q in [quota_name] if self._active_executions.get(q))
        if active >= quota.max_concurrent_executions:
            return False

        return True

    def start_execution(self, execution_id: str, session_id: str, quota_name: str = "default") -> bool:
        """Start tracking an execution"""
        with self._lock:
            if not self.can_execute(quota_name):
                return False
            self._active_executions[execution_id] = session_id
            return True

    def end_execution(self, execution_id: str) -> None:
        """End tracking an execution"""
        with self._lock:
            self._active_executions.pop(execution_id, None)

    def get_usage(self, quota_name: Optional[str] = None) -> Dict[str, Any]:
        """Get usage statistics"""
        with self._lock:
            if quota_name:
                usage = self._usage.get(quota_name, TokenUsage())
                return {
                    "quota": quota_name,
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                    "cost": usage.cost,
                    "active_executions": sum(
                        1 for eid, sid in self._active_executions.items()
                        if sid == quota_name
                    )
                }

            return {
                name: {
                    "prompt_tokens": u.prompt_tokens,
                    "completion_tokens": u.completion_tokens,
                    "total_tokens": u.total_tokens,
                    "cost": u.cost
                }
                for name, u in self._usage.items()
            }

    def get_summary(self) -> Dict[str, Any]:
        """Get resource summary"""
        with self._lock:
            return {
                "total_active_executions": len(self._active_executions),
                "quotas": list(self._quotas.keys()),
                "total_tokens": sum(u.total_tokens for u in self._usage.values()),
                "total_cost": sum(u.cost for u in self._usage.values()),
                "active_executions": self._active_executions
            }
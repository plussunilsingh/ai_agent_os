#!/usr/bin/env python3
"""
Cache-Aware Model Router for AI-SE OS
======================================
Routes tasks to optimal models via OpenRouter, considering:
  - Task complexity and risk level
  - Model capability and cost scores
  - Cache warmth (preferring models with warm caches)
  - Plan Mode vs Act Mode
  - Fallback chain on failure

Integrates with CacheService and the OpenRouter model registry.
"""

import json
import os
import time
import uuid
from enum import Enum
from typing import Any, Optional


class TaskType(Enum):
    PLANNING = "planning"
    EXECUTION = "execution"
    RECOVERY = "recovery"
    ANALYSIS = "analysis"
    REVIEW = "review"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ModelRoute:
    """Routing decision output."""

    def __init__(
        self,
        model_id: str,
        provider: str,
        model_name: str,
        route_type: str,
        score: float,
        cache_warm: bool,
        cache_hit_rate: float,
        estimated_cost: float,
        fallback_chain: list[str],
        decision_id: str,
    ):
        self.model_id = model_id
        self.provider = provider
        self.model_name = model_name
        self.route_type = route_type
        self.score = score
        self.cache_warm = cache_warm
        self.cache_hit_rate = cache_hit_rate
        self.estimated_cost = estimated_cost
        self.fallback_chain = fallback_chain
        self.decision_id = decision_id
        self.decided_at = time.time()

    def to_dict(self) -> dict:
        return {
            "id": self.decision_id,
            "schema_version": "1.0",
            "selected_model_id": self.model_id,
            "provider": self.provider,
            "model_name": self.model_name,
            "route_type": self.route_type,
            "score": self.score,
            "cache_warm": self.cache_warm,
            "cache_hit_rate": self.cache_hit_rate,
            "estimated_cost": self.estimated_cost,
            "fallback_chain": self.fallback_chain,
            "decided_at": self.decided_at,
        }


class OpenRouterModelRouter:
    """
    Routes tasks to OpenRouter models based on task type, risk, cost, and cache state.
    """

    def __init__(self, registry_path: str = ".ai_os/models/openrouter_registry.json"):
        self.registry = self._load_registry(registry_path)
        self.models = self.registry.get("models", [])
        self.routing_defaults = self.registry.get("routing_defaults", {})
        self.cache_service = None  # Set externally via set_cache_service()

    def _load_registry(self, path: str) -> dict:
        with open(path) as f:
            return json.load(f)

    def set_cache_service(self, cache_service):
        """Inject cache service for cache-aware routing."""
        self.cache_service = cache_service

    def _get_model_by_id(self, model_id: str) -> Optional[dict]:
        for m in self.models:
            if m["id"] == model_id:
                return m
        return None

    def _assess_complexity(self, task_type: TaskType, risk: RiskLevel) -> float:
        """Return a complexity score from 0.0 to 1.0."""
        complexity_map = {
            (TaskType.PLANNING, RiskLevel.LOW): 0.4,
            (TaskType.PLANNING, RiskLevel.MEDIUM): 0.7,
            (TaskType.PLANNING, RiskLevel.HIGH): 0.9,
            (TaskType.EXECUTION, RiskLevel.LOW): 0.3,
            (TaskType.EXECUTION, RiskLevel.MEDIUM): 0.5,
            (TaskType.EXECUTION, RiskLevel.HIGH): 0.8,
            (TaskType.RECOVERY, RiskLevel.MEDIUM): 0.7,
            (TaskType.RECOVERY, RiskLevel.HIGH): 0.95,
            (TaskType.ANALYSIS, RiskLevel.LOW): 0.3,
            (TaskType.ANALYSIS, RiskLevel.MEDIUM): 0.5,
            (TaskType.ANALYSIS, RiskLevel.HIGH): 0.7,
            (TaskType.REVIEW, RiskLevel.LOW): 0.2,
            (TaskType.REVIEW, RiskLevel.MEDIUM): 0.4,
            (TaskType.REVIEW, RiskLevel.HIGH): 0.6,
        }
        return complexity_map.get((task_type, risk), 0.5)

    def _score_model_for_task(
        self,
        model: dict,
        complexity: float,
        task_type: TaskType,
        context_tokens: int,
    ) -> float:
        """
        Score a model's suitability for a given task.
        Higher score = better match.

        Factors:
          - Capability match (0.4 weight)
          - Cost efficiency (0.3 weight)
          - Cache warmth (0.3 weight)
        """
        # Capability score: does routing_role match task_type?
        role = model.get("routing_role", "")
        role_match = 1.0 if role == task_type.value else 0.5
        if role.startswith("fallback"):
            role_match = 0.3

        # Check context window
        context_window = model.get("context_window", 0)
        context_fit = 1.0
        if context_tokens > context_window:
            context_fit = 0.0

        # Cost score: cheaper = better
        cost_input = model.get("cost_input_per_million", 1.0)
        cost_score = max(0.0, 1.0 - (cost_input / 3.0))

        # Capability breadth
        capabilities = model.get("capabilities", [])
        capability_score = min(1.0, len(capabilities) / 6.0)

        capability_rating = (role_match * 0.6 + capability_score * 0.4) * context_fit

        # Cache warmth score
        cache_warm = 0.5  # default neutral
        if self.cache_service:
            rate = self.cache_service.metrics.get_recent_hit_rate()
            model_id = model["id"]
            # Check if this specific model is in a cache-supporting list
            cache_supported = self.registry.get("cache_strategy", {}).get(
                "prefix_caching_models", []
            )
            if model_id in cache_supported:
                cache_warm = min(1.0, rate + 0.2)  # boost for cache-supported models
            else:
                cache_warm = rate

        total_score = (
            capability_rating * 0.4 + cost_score * 0.3 + cache_warm * 0.3
        )
        return total_score

    def route(
        self,
        task_type: TaskType = TaskType.EXECUTION,
        risk: RiskLevel = RiskLevel.MEDIUM,
        context_tokens: int = 4000,
        mode: str = "act",
    ) -> ModelRoute:
        """
        Route a task to the best OpenRouter model.

        Args:
            task_type: Type of task (planning, execution, etc.)
            risk: Risk level
            context_tokens: Estimated context token count
            mode: "plan" or "act" mode

        Returns:
            ModelRoute with selected model and fallback chain
        """
        # Determine primary routing role from mode and task type
        if mode == "plan":
            primary_role = "planning"
        elif task_type == TaskType.PLANNING:
            primary_role = "planning"
        elif task_type == TaskType.RECOVERY:
            primary_role = "planning"  # recovery needs reasoning
        else:
            primary_role = "execution"

        complexity = self._assess_complexity(task_type, risk)

        # Score all enabled models
        scored_models = []
        for model in self.models:
            if not model.get("enabled", False):
                continue

            score = self._score_model_for_task(
                model, complexity, task_type, context_tokens
            )
            scored_models.append((score, model))

        # Sort by score descending
        scored_models.sort(key=lambda x: x[0], reverse=True)

        if not scored_models:
            raise RuntimeError("No eligible models available in OpenRouter registry")

        # Select best model
        best_score, best_model = scored_models[0]

        # Build fallback chain from remaining scored models
        fallback_chain = [m["id"] for _, m in scored_models[1:]]

        # Get cache hit rate
        cache_hit_rate = 0.0
        cache_warm = False
        if self.cache_service:
            cache_hit_rate = self.cache_service.metrics.get_recent_hit_rate()
            cache_warm = cache_hit_rate > 0.7

        # Estimate cost
        cost_per_million = best_model.get("cost_input_per_million", 0)
        estimated_cost = (context_tokens / 1_000_000) * cost_per_million

        decision_id = str(uuid.uuid4())

        return ModelRoute(
            model_id=best_model["id"],
            provider=best_model["provider"],
            model_name=best_model["model"],
            route_type=primary_role,
            score=best_score,
            cache_warm=cache_warm,
            cache_hit_rate=cache_hit_rate,
            estimated_cost=estimated_cost,
            fallback_chain=fallback_chain,
            decision_id=decision_id,
        )

    def route_plan_mode(
        self, complexity: float = 0.7, context_tokens: int = 8000
    ) -> ModelRoute:
        """Route to planning model (DeepSeek Chat / Claude Sonnet fallback)."""
        return self.route(
            task_type=TaskType.PLANNING,
            risk=RiskLevel.HIGH if complexity > 0.7 else RiskLevel.MEDIUM,
            context_tokens=context_tokens,
            mode="plan",
        )

    def route_execution(
        self, context_tokens: int = 4000
    ) -> ModelRoute:
        """Route to execution model (DeepSeek V3 Flash)."""
        return self.route(
            task_type=TaskType.EXECUTION,
            risk=RiskLevel.MEDIUM,
            context_tokens=context_tokens,
            mode="act",
        )

    def route_fallback(
        self,
        failed_model_id: str,
        task_type: TaskType = TaskType.EXECUTION,
        context_tokens: int = 4000,
    ) -> ModelRoute:
        """
        Route to a fallback model when the primary model fails.
        """
        usable_models = [
            m for m in self.models
            if m.get("enabled", False) and m["id"] != failed_model_id
        ]

        if not usable_models:
            raise RuntimeError(
                f"No fallback models available after {failed_model_id} failed"
            )

        scored = []
        for model in usable_models:
            complexity = self._assess_complexity(task_type, RiskLevel.MEDIUM)
            score = self._score_model_for_task(
                model, complexity, task_type, context_tokens
            )
            scored.append((score, model))

        scored.sort(key=lambda x: x[0], reverse=True)
        best_score, best_model = scored[0]

        fallback_chain = [m["id"] for _, m in scored[1:]]

        decision_id = str(uuid.uuid4())
        cost_per_million = best_model.get("cost_input_per_million", 0)
        estimated_cost = (context_tokens / 1_000_000) * cost_per_million

        cache_hit_rate = 0.0
        cache_warm = False
        if self.cache_service:
            cache_hit_rate = self.cache_service.metrics.get_recent_hit_rate()
            cache_warm = cache_hit_rate > 0.7

        return ModelRoute(
            model_id=best_model["id"],
            provider=best_model["provider"],
            model_name=best_model["model"],
            route_type=task_type.value,
            score=best_score,
            cache_warm=cache_warm,
            cache_hit_rate=cache_hit_rate,
            estimated_cost=estimated_cost,
            fallback_chain=fallback_chain,
            decision_id=decision_id,
        )

    def get_provider_headers(self) -> dict:
        """Get OpenRouter API headers."""
        return {
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY', '')}",
            "HTTP-Referer": "https://botanixui.app",
            "X-Title": "BotanixUI-AI-SE-OS",
            "Content-Type": "application/json",
        }

    def should_send_cache_control(self, model_id: str) -> bool:
        """Check if we should send cache control headers for this model."""
        cache_supported = self.registry.get("cache_strategy", {}).get(
            "prefix_caching_models", []
        )
        return model_id in cache_supported
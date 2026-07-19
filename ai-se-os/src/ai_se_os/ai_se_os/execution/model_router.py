"""
AI-SE OS Model Router with Cache Awareness
Routes tasks to optimal models considering cache state
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

from ai_se_os.cache.cache_service import CacheService


class TaskType(str, Enum):
    PLANNING = "planning"
    EXECUTION = "execution"
    ARCHITECTURE = "architecture"
    SECURITY = "security"
    REFACTORING = "refactoring"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    REVIEW = "review"


@dataclass
class Model:
    """Model definition"""
    id: str
    name: str
    capability_score: float
    cost_rating: int  # 1-5 (1=cheapest, 5=most expensive)
    max_context: int
    latency_ms: int
    best_for: List[str]


@dataclass
class ModelRoute:
    """Model routing decision"""
    model_id: str
    score: float
    cache_hit_rate: float
    cache_warm: bool
    task_type: TaskType
    rationale: str


class ModelRouter:
    """
    Model Router with Cache Awareness
    Routes tasks to optimal models considering cache state
    """

    def __init__(self, cache_service: CacheService):
        self.cache_service = cache_service
        self.models = self._register_models()

        # Plan vs Act mode configuration
        self.plan_mode_model = "deepseek-v4-pro"
        self.act_mode_model = "deepseek-v4-flash"

    def _register_models(self) -> List[Model]:
        """Register available models"""
        return [
            Model(
                id="deepseek-v4-flash",
                name="DeepSeek V4 Flash",
                capability_score=0.75,
                cost_rating=1,
                max_context=128000,
                latency_ms=200,
                best_for=["execution", "refactoring", "testing", "documentation"]
            ),
            Model(
                id="deepseek-v4-pro",
                name="DeepSeek V4 Pro",
                capability_score=0.90,
                cost_rating=3,
                max_context=256000,
                latency_ms=400,
                best_for=["planning", "architecture", "security", "review"]
            ),
            Model(
                id="claude-3.5-sonnet",
                name="Claude 3.5 Sonnet",
                capability_score=0.95,
                cost_rating=4,
                max_context=200000,
                latency_ms=500,
                best_for=["planning", "architecture", "review", "security"]
            ),
            Model(
                id="gpt-4o",
                name="GPT-4o",
                capability_score=0.93,
                cost_rating=4,
                max_context=128000,
                latency_ms=450,
                best_for=["planning", "reasoning", "architecture"]
            ),
            Model(
                id="gemini-pro",
                name="Gemini Pro",
                capability_score=0.80,
                cost_rating=3,
                max_context=128000,
                latency_ms=350,
                best_for=["execution", "documentation", "refactoring"]
            ),
        ]

    def route(self, task_type: TaskType, task: Any) -> ModelRoute:
        """
        Route task to optimal model considering cache state.

        Args:
            task_type: Type of task to route
            task: Task object

        Returns:
            ModelRoute with routing decision
        """
        # 1. Plan vs Act mode routing
        if task_type == TaskType.PLANNING:
            return self._route_plan_mode(task_type, task)
        elif task_type in [TaskType.EXECUTION, TaskType.TESTING, TaskType.REFACTORING]:
            return self._route_act_mode(task_type, task)

        # 2. For other tasks, use cache-aware scoring
        return self._route_with_cache_awareness(task_type, task)

    def _route_plan_mode(self, task_type: TaskType, task: Any) -> ModelRoute:
        """Route to planning model"""
        return ModelRoute(
            model_id=self.plan_mode_model,
            score=0.90,
            cache_hit_rate=self._get_cache_hit_rate(self.plan_mode_model),
            cache_warm=self._is_cache_warm(self.plan_mode_model),
            task_type=task_type,
            rationale="Plan mode: using high-capability model for architecture/planning"
        )

    def _route_act_mode(self, task_type: TaskType, task: Any) -> ModelRoute:
        """Route to execution model"""
        return ModelRoute(
            model_id=self.act_mode_model,
            score=0.85,
            cache_hit_rate=self._get_cache_hit_rate(self.act_mode_model),
            cache_warm=self._is_cache_warm(self.act_mode_model),
            task_type=task_type,
            rationale="Act mode: using cost-effective model for execution"
        )

    def _route_with_cache_awareness(self, task_type: TaskType, task: Any) -> ModelRoute:
        """Route with cache awareness for other task types"""
        model_scores = {}

        for model in self.models:
            cache_hit_rate = self._get_cache_hit_rate(model.id)
            cache_warm = cache_hit_rate > 0.7

            # Score: capability * cost * cache_warm
            score = (
                model.capability_score * 0.4 +
                (1 - model.cost_rating / 5) * 0.3 +
                (1.0 if cache_warm else 0.0) * 0.3
            )

            # Boost score if model is best for this task type
            if task_type.value in model.best_for:
                score += 0.1

            model_scores[model.id] = {
                "score": score,
                "model": model,
                "cache_hit_rate": cache_hit_rate,
                "cache_warm": cache_warm
            }

        # Select best model
        best_id = max(model_scores, key=lambda x: model_scores[x]["score"])
        best = model_scores[best_id]

        return ModelRoute(
            model_id=best_id,
            score=best["score"],
            cache_hit_rate=best["cache_hit_rate"],
            cache_warm=best["cache_warm"],
            task_type=task_type,
            rationale=f"Cache-aware routing: {best_id} scored {best['score']:.2f}"
        )

    def _get_cache_hit_rate(self, model_id: str) -> float:
        """Get cache hit rate for a model"""
        return self.cache_service.get_hit_rate()

    def _is_cache_warm(self, model_id: str) -> bool:
        """Check if cache is warm for a model"""
        return self._get_cache_hit_rate(model_id) > 0.7

    def get_model_config(self, model_id: str) -> Optional[Model]:
        """Get model configuration"""
        for model in self.models:
            if model.id == model_id:
                return model
        return None
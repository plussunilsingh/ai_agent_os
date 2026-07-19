"""
AI-SE OS Cache Tracker
Tracks cache performance and hit rates
"""

import time
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field
from collections import deque


@dataclass
class CacheHitRecord:
    """Record of a cache hit or miss"""
    timestamp: float = field(default_factory=time.time)
    is_hit: bool = True
    key: str = ""
    strategy: str = ""
    latency_ms: float = 0.0
    tokens_saved: int = 0


class CacheTracker:
    """
    Tracks cache performance metrics
    Provides real-time monitoring and alerts
    """

    def __init__(self, max_history: int = 1000):
        self.hits = 0
        self.misses = 0
        self.history: deque[CacheHitRecord] = deque(maxlen=max_history)
        self.token_savings = 0
        self.alert_threshold = 0.70  # Alert if hit rate below 70%

    def record_hit(
        self,
        key: str = "",
        strategy: str = "",
        latency_ms: float = 0.0,
        tokens_saved: int = 0
    ) -> None:
        """Record a cache hit"""
        self.hits += 1
        self.token_savings += tokens_saved
        self.history.append(CacheHitRecord(
            is_hit=True,
            key=key,
            strategy=strategy,
            latency_ms=latency_ms,
            tokens_saved=tokens_saved
        ))

    def record_miss(
        self,
        key: str = "",
        strategy: str = "",
        latency_ms: float = 0.0
    ) -> None:
        """Record a cache miss"""
        self.misses += 1
        self.history.append(CacheHitRecord(
            is_hit=False,
            key=key,
            strategy=strategy,
            latency_ms=latency_ms,
            tokens_saved=0
        ))

    def get_hit_rate(self, window: int = 0) -> float:
        """Get cache hit rate"""
        if window > 0:
            # Recent window
            recent = list(self.history)[-window:]
            hits = sum(1 for r in recent if r.is_hit)
            total = len(recent)
            if total == 0:
                return 0.0
            return hits / total

        # All time
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total

    def get_metrics(self) -> Dict[str, Any]:
        """Get complete metrics"""
        return {
            "hits": self.hits,
            "misses": self.misses,
            "total_requests": self.hits + self.misses,
            "hit_rate": self.get_hit_rate(),
            "hit_rate_100": self.get_hit_rate(100),
            "hit_rate_1000": self.get_hit_rate(1000),
            "token_savings": self.token_savings,
            "alert_triggered": self.get_hit_rate() < self.alert_threshold,
            "history_size": len(self.history)
        }

    def get_recent_ratio(self, seconds: int = 60) -> float:
        """Get hit rate for last N seconds"""
        cutoff = time.time() - seconds
        recent = [r for r in self.history if r.timestamp >= cutoff]
        if not recent:
            return 0.0
        hits = sum(1 for r in recent if r.is_hit)
        return hits / len(recent)

    def detect_divergence(self, threshold: float = 0.70) -> bool:
        """Detect if cache hit rate has dropped below threshold"""
        return self.get_hit_rate(100) < threshold

    def reset(self) -> None:
        """Reset metrics"""
        self.hits = 0
        self.misses = 0
        self.history.clear()
        self.token_savings = 0
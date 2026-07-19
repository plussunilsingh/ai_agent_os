"""
AI-SE OS Observability - Cache Metrics
Tracks cache performance and alerts
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import time


@dataclass
class CacheMetric:
    """Cache metric record"""
    name: str
    value: float
    timestamp: float = field(default_factory=time.time)
    tags: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """
    Collects and tracks cache metrics
    Provides alerting and dashboard data
    """

    def __init__(self):
        self.metrics: List[CacheMetric] = []
        self.alerts: List[Dict[str, Any]] = []

    def record_hit_rate(self, hit_rate: float, model_id: str = "all") -> None:
        """Record cache hit rate"""
        self.metrics.append(CacheMetric(
            name="cache.hit_rate",
            value=hit_rate,
            tags={"model": model_id}
        ))

        # Alert if hit rate drops below 70%
        if hit_rate < 0.70:
            self._trigger_alert(
                severity="warning",
                message=f"Cache hit rate dropped to {hit_rate*100:.1f}%",
                metric="cache.hit_rate",
                value=hit_rate
            )

    def record_token_savings(self, tokens_saved: int, model_id: str = "all") -> None:
        """Record token savings"""
        self.metrics.append(CacheMetric(
            name="cache.token_savings",
            value=float(tokens_saved),
            tags={"model": model_id}
        ))

    def record_cost_savings(self, cost_saved: float, model_id: str = "all") -> None:
        """Record cost savings"""
        self.metrics.append(CacheMetric(
            name="cache.cost_savings",
            value=cost_saved,
            tags={"model": model_id}
        ))

    def record_divergence(self, divergence_detected: bool, model_id: str = "all") -> None:
        """Record divergence detection"""
        if divergence_detected:
            self._trigger_alert(
                severity="warning",
                message=f"Prompt divergence detected for model {model_id}",
                metric="cache.divergence",
                value=1.0,
                tags={"model": model_id}
            )

    def _trigger_alert(
        self,
        severity: str,
        message: str,
        metric: str,
        value: float,
        tags: Optional[Dict[str, str]] = None
    ) -> None:
        """Trigger an alert"""
        self.alerts.append({
            "timestamp": datetime.now().isoformat(),
            "severity": severity,
            "message": message,
            "metric": metric,
            "value": value,
            "tags": tags or {}
        })

    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics"""
        return {
            "metrics": [
                {
                    "name": m.name,
                    "value": m.value,
                    "timestamp": m.timestamp,
                    "tags": m.tags
                }
                for m in self.metrics[-100:]  # Last 100 metrics
            ],
            "alerts": self.alerts[-20:]  # Last 20 alerts
        }

    def get_summary(self) -> Dict[str, Any]:
        """Get summary metrics"""
        hit_rates = [m.value for m in self.metrics if m.name == "cache.hit_rate"]
        token_savings = [m.value for m in self.metrics if m.name == "cache.token_savings"]
        cost_savings = [m.value for m in self.metrics if m.name == "cache.cost_savings"]

        return {
            "avg_hit_rate": sum(hit_rates) / len(hit_rates) if hit_rates else 0,
            "total_token_savings": sum(token_savings),
            "total_cost_savings": sum(cost_savings),
            "alert_count": len(self.alerts),
            "latest_alerts": self.alerts[-5:] if self.alerts else []
        }
"""
AI-SE OS Cache Service
Implements prompt caching strategies for token optimization
"""

import hashlib
import json
import time
from typing import Optional, Dict, Any, List, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

# Try to import Redis, fallback to in-memory
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class CacheStrategy(str, Enum):
    """Cache strategies"""
    SYSTEM_PREFIX = "system_prefix"
    WORKSPACE_CONTEXT = "workspace_context"
    HISTORY_COMPACT = "history_compact"
    FULL_PROMPT = "full_prompt"
    MODEL_SPECIFIC = "model_specific"


@dataclass
class CacheEntry:
    """Cache entry"""
    key: str
    value: str
    strategy: CacheStrategy
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    hit_count: int = 0
    last_hit_at: Optional[datetime] = None

    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at

    def record_hit(self) -> None:
        """Record a cache hit"""
        self.hit_count += 1
        self.last_hit_at = datetime.now()


class CacheService:
    """
    Cache Service with Redis/In-Memory support
    Implements prompt caching for token efficiency
    """

    DEFAULT_TTL = 3600  # 1 hour

    def __init__(self, redis_url: Optional[str] = None):
        self.redis_client = None
        self.in_memory_cache: Dict[str, CacheEntry] = {}
        self.cache_metrics = {
            "hits": 0,
            "misses": 0,
            "total_requests": 0,
            "token_savings": 0
        }

        if redis_url and REDIS_AVAILABLE:
            try:
                self.redis_client = redis.from_url(redis_url)
                self._using_redis = True
                print(f"Connected to Redis at {redis_url}")
            except Exception as e:
                print(f"Redis connection failed: {e}. Using in-memory cache.")
                self._using_redis = False
        else:
            self._using_redis = False
            print("Using in-memory cache (Redis not available)")

    def _generate_key(self, *args, **kwargs) -> str:
        """Generate deterministic cache key"""
        sorted_kwargs = dict(sorted(kwargs.items()))
        combined = json.dumps({
            "args": args,
            "kwargs": sorted_kwargs
        }, sort_keys=True)
        return hashlib.sha256(combined.encode()).hexdigest()

    def _format_for_cache(self, content: str) -> str:
        """Format content deterministically for cache"""
        return content.strip() + "\n\n"

    def get(self, key: str) -> Optional[str]:
        """Get cached value"""
        self.cache_metrics["total_requests"] += 1

        if self._using_redis:
            value = self.redis_client.get(key)
            if value:
                self.cache_metrics["hits"] += 1
                return value.decode('utf-8')
            self.cache_metrics["misses"] += 1
            return None

        # In-memory cache
        entry = self.in_memory_cache.get(key)
        if entry and not entry.is_expired():
            entry.record_hit()
            self.cache_metrics["hits"] += 1
            return entry.value

        if entry and entry.is_expired():
            del self.in_memory_cache[key]

        self.cache_metrics["misses"] += 1
        return None

    def set(self, key: str, value: str, ttl: int = DEFAULT_TTL) -> None:
        """Set cached value"""
        if self._using_redis:
            self.redis_client.setex(key, ttl, value)
            return

        # In-memory cache
        expires_at = datetime.now() + timedelta(seconds=ttl)
        self.in_memory_cache[key] = CacheEntry(
            key=key,
            value=value,
            strategy=CacheStrategy.SYSTEM_PREFIX,
            expires_at=expires_at
        )

    def get_or_set(
        self,
        key: str,
        value_fn: Callable[[], str],
        ttl: int = DEFAULT_TTL
    ) -> str:
        """Get cached value or compute and cache"""
        cached = self.get(key)
        if cached is not None:
            return cached

        value = value_fn()
        self.set(key, value, ttl)
        return value

    def get_hit_rate(self) -> float:
        """Get cache hit rate"""
        total = self.cache_metrics["hits"] + self.cache_metrics["misses"]
        if total == 0:
            return 0.0
        return self.cache_metrics["hits"] / total

    def get_metrics(self) -> Dict[str, Any]:
        """Get cache metrics"""
        return {
            "hits": self.cache_metrics["hits"],
            "misses": self.cache_metrics["misses"],
            "total_requests": self.cache_metrics["total_requests"],
            "hit_rate": self.get_hit_rate(),
            "token_savings": self.cache_metrics["token_savings"],
            "cache_size": len(self.in_memory_cache) if not self._using_redis else 0
        }

    def clear(self) -> None:
        """Clear cache"""
        if self._using_redis:
            self.redis_client.flushdb()
        else:
            self.in_memory_cache.clear()
        self.cache_metrics = {"hits": 0, "misses": 0, "total_requests": 0, "token_savings": 0}

    def invalidate(self, key: str) -> None:
        """Invalidate specific cache key"""
        if self._using_redis:
            self.redis_client.delete(key)
        else:
            if key in self.in_memory_cache:
                del self.in_memory_cache[key]
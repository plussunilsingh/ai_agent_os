"""
Tests for Cache Service
"""

import pytest
from src.cache.cache_service import CacheService, CacheStrategy
from src.cache.cache_tracker import CacheTracker


class TestCacheService:
    def test_set_and_get(self):
        cache = CacheService()
        cache.set("test_key", "test_value")
        assert cache.get("test_key") == "test_value"

    def test_get_missing(self):
        cache = CacheService()
        assert cache.get("nonexistent") is None

    def test_get_or_set(self):
        cache = CacheService()
        result = cache.get_or_set("compute_key", lambda: "computed_value")
        assert result == "computed_value"

        # Should return cached value
        result2 = cache.get_or_set("compute_key", lambda: "new_value")
        assert result2 == "computed_value"

    def test_ttl_expiry(self):
        cache = CacheService()
        cache.set("ttl_key", "value", ttl=0)  # Expire immediately
        assert cache.get("ttl_key") is None

    def test_clear(self):
        cache = CacheService()
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        assert cache.get("key1") is None
        assert cache.get("key2") is None

    def test_invalidate(self):
        cache = CacheService()
        cache.set("key1", "value1")
        cache.invalidate("key1")
        assert cache.get("key1") is None

    def test_hit_rate(self):
        cache = CacheService()
        cache.get("miss1")
        cache.get("miss2")
        cache.set("hit1", "value")
        cache.get("hit1")
        # 1 hit, 3 total requests (2 misses + 1 hit) = 0.333...
        assert cache.get_hit_rate() == 1/3

    def test_metrics(self):
        cache = CacheService()
        cache.set("key", "value")
        cache.get("key")
        cache.get("missing")

        metrics = cache.get_metrics()
        assert metrics["hits"] == 1
        assert metrics["misses"] == 1
        assert metrics["total_requests"] == 2


class TestCacheTracker:
    def test_hit_rate_calculation(self):
        tracker = CacheTracker()
        tracker.record_hit()
        tracker.record_miss()
        assert tracker.get_hit_rate() == 0.5

    def test_token_savings(self):
        tracker = CacheTracker()
        tracker.record_hit(tokens_saved=100)
        tracker.record_hit(tokens_saved=200)
        assert tracker.token_savings == 300

    def test_divergence_detection(self):
        tracker = CacheTracker()
        # Override threshold after creation
        tracker.alert_threshold = 0.5
        tracker.record_miss()
        tracker.record_miss()
        tracker.record_miss()
        assert tracker.detect_divergence(0.5) == True

    def test_recent_ratio(self):
        tracker = CacheTracker()
        tracker.record_hit()
        tracker.record_hit()
        tracker.record_miss()
        ratio = tracker.get_hit_rate(100)
        assert ratio == 2/3

    def test_reset(self):
        tracker = CacheTracker()
        tracker.record_hit()
        tracker.record_hit()
        tracker.record_miss()
        tracker.reset()
        assert tracker.hits == 0
        assert tracker.misses == 0
        assert tracker.token_savings == 0
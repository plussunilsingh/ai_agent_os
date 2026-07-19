#!/usr/bin/env python3
"""
Cache Service for AI-SE OS
===========================
Implements the three-layer context cache:
  Layer 1 - System Prefix Cache (static)
  Layer 2 - Workspace Context Cache (semi-static)
  Layer 3 - Compacted History Cache (session-scoped)

Integrates with OpenRouter provider-side prefix caching where supported.
"""

import hashlib
import json
import os
import time
import uuid
from pathlib import Path
from typing import Any, Optional


class CacheEntry:
    """A single cache entry with provenance metadata."""

    def __init__(
        self,
        layer: str,
        cache_key: str,
        content: str,
        source_version_hashes: list[str],
        sensitivity_class: str,
        token_count: int,
        ttl: Optional[int] = None,
    ):
        self.layer = layer
        self.cache_key = cache_key
        self.content = content
        self.source_version_hashes = source_version_hashes
        self.sensitivity_class = sensitivity_class
        self.token_count = token_count
        self.created_at = time.time()
        self.ttl = ttl
        self.entry_id = str(uuid.uuid4())

    def is_expired(self) -> bool:
        if self.ttl is None:
            return False
        return (time.time() - self.created_at) > self.ttl

    def to_dict(self) -> dict:
        return {
            "entry_id": self.entry_id,
            "layer": self.layer,
            "cache_key": self.cache_key,
            "source_version_hashes": self.source_version_hashes,
            "sensitivity_class": self.sensitivity_class,
            "token_count": self.token_count,
            "created_at": self.created_at,
            "ttl": self.ttl,
        }


class CacheMetrics:
    """Tracks cache hit/miss rates and token savings."""

    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.divergence_count = 0
        self.eviction_count = 0
        self.compaction_count = 0
        self.tokens_saved = 0
        self.tokens_spent = 0
        self.by_layer = {
            "system_prefix": {"hits": 0, "misses": 0, "tokens_saved": 0},
            "workspace": {"hits": 0, "misses": 0, "tokens_saved": 0},
            "history": {"hits": 0, "misses": 0, "tokens_saved": 0},
        }
        self.alerts_raised: list[str] = []
        self._hit_history: list[tuple[str, float]] = []

    def record_hit(self, layer: str, tokens_saved: int = 0):
        self.hits += 1
        self.tokens_saved += tokens_saved
        self._hit_history.append(("hit", time.time()))
        if layer in self.by_layer:
            self.by_layer[layer]["hits"] += 1
            self.by_layer[layer]["tokens_saved"] += tokens_saved

    def record_miss(self, layer: str, tokens_spent: int = 0):
        self.misses += 1
        self.tokens_spent += tokens_spent
        self._hit_history.append(("miss", time.time()))
        if layer in self.by_layer:
            self.by_layer[layer]["misses"] += 1

    def record_divergence(self):
        self.divergence_count += 1

    def record_eviction(self):
        self.eviction_count += 1

    def record_compaction(self):
        self.compaction_count += 1

    def get_hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    def get_recent_hit_rate(self, window_seconds: int = 3600) -> float:
        now = time.time()
        recent = [h for h in self._hit_history if (now - h[1]) < window_seconds]
        if not recent:
            return 0.0
        hits = sum(1 for h in recent if h[0] == "hit")
        return hits / len(recent)

    def check_alerts(self) -> list[str]:
        alerts = []
        recent_rate = self.get_recent_hit_rate()
        if recent_rate < 0.7 and self.hits + self.misses > 10:
            alerts.append("cache_hit_rate_low")
        if self.divergence_count > 5:
            alerts.append("cache_divergence_detected")
        self.alerts_raised = alerts
        return alerts

    def to_dict(self) -> dict:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": self.get_hit_rate(),
            "divergence_count": self.divergence_count,
            "eviction_count": self.eviction_count,
            "compaction_count": self.compaction_count,
            "tokens_saved": self.tokens_saved,
            "tokens_spent": self.tokens_spent,
            "by_layer": self.by_layer,
            "alerts_raised": self.alerts_raised,
        }


class CacheService:
    """
    Three-layer context cache for AI-SE OS.

    Layer 1: System Prefix (static, no TTL expiry, invalidate on config change)
    Layer 2: Workspace Context (semi-static, content-addressed, LRU eviction)
    Layer 3: Compacted History (session-scoped, expires on session close)
    """

    def __init__(self, cache_dir: str = ".ai_os_runtime/cache"):
        self.cache_dir = Path(cache_dir)
        self.metrics = CacheMetrics()

        # Ensure cache directories exist
        for layer_dir in ["system_prefix", "workspace", "history"]:
            (self.cache_dir / layer_dir).mkdir(parents=True, exist_ok=True)

        # In-memory cache for fast lookups
        self._memory: dict[str, CacheEntry] = {}

        # LRU tracking for workspace layer
        self._lru_order: list[str] = []
        self._max_workspace_entries = 500

    def _make_key(self, layer: str, namespace: str, content_hash: str) -> str:
        """Generate a namespaced cache key."""
        return f"{layer}:{namespace}:{content_hash}"

    def _hash_content(self, content: str) -> str:
        """SHA-256 hash of canonical UTF-8 content."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _hash_sorted(self, items: list[str]) -> str:
        """Hash a sorted list of strings deterministically."""
        sorted_items = sorted(items)
        return self._hash_content(json.dumps(sorted_items, sort_keys=True))

    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (~4 chars per token)."""
        return len(text) // 4

    def _persist_entry(self, entry: CacheEntry):
        """Write cache entry to disk."""
        entry_path = self.cache_dir / entry.layer / f"{entry.cache_key}.json"
        data = entry.to_dict()
        data["content"] = entry.content
        # Atomic write via temp file + rename
        tmp_path = entry_path.with_suffix(".tmp")
        with open(tmp_path, "w") as f:
            json.dump(data, f, indent=2)
        os.rename(tmp_path, entry_path)

    def _load_entry(self, layer: str, cache_key: str) -> Optional[CacheEntry]:
        """Load cache entry from disk."""
        entry_path = self.cache_dir / layer / f"{cache_key}.json"
        if not entry_path.exists():
            return None
        try:
            with open(entry_path) as f:
                data = json.load(f)
            entry = CacheEntry(
                layer=data["layer"],
                cache_key=data["cache_key"],
                content=data["content"],
                source_version_hashes=data["source_version_hashes"],
                sensitivity_class=data["sensitivity_class"],
                token_count=data["token_count"],
                ttl=data.get("ttl"),
            )
            entry.created_at = data["created_at"]
            entry.entry_id = data["entry_id"]
            return entry
        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            return None

    def _check_divergence(self, entry: CacheEntry, current_hashes: list[str]) -> bool:
        """Check if source artifacts have changed since cache entry was created."""
        if not entry.source_version_hashes or not current_hashes:
            return False
        return set(entry.source_version_hashes) != set(current_hashes)

    def _enforce_lru(self):
        """Evict least recently used workspace entries if over limit."""
        while len(self._lru_order) > self._max_workspace_entries:
            oldest_key = self._lru_order.pop(0)
            if oldest_key in self._memory:
                del self._memory[oldest_key]
            # Remove from disk
            entry_path = self.cache_dir / "workspace" / f"{oldest_key}.json"
            if entry_path.exists():
                entry_path.unlink()
            self.metrics.record_eviction()

    # --- Layer 1: System Prefix Cache ---

    def get_system_prefix(
        self, model_id: str, tool_list: list[str], policy_version: str
    ) -> Optional[str]:
        """Get cached system prefix for a model/tool/policy combination."""
        key_parts = [model_id] + sorted(tool_list) + [policy_version]
        cache_key = self._hash_content("|".join(key_parts))
        full_key = self._make_key("system_prefix", "global", cache_key)

        entry = self._memory.get(full_key) or self._load_entry("system_prefix", cache_key)
        if entry and not entry.is_expired():
            self.metrics.record_hit("system_prefix", entry.token_count)
            return entry.content

        self.metrics.record_miss("system_prefix")
        return None

    def set_system_prefix(
        self,
        content: str,
        model_id: str,
        tool_list: list[str],
        policy_version: str,
    ):
        """Cache a system prefix."""
        key_parts = [model_id] + sorted(tool_list) + [policy_version]
        cache_key = self._hash_content("|".join(key_parts))
        full_key = self._make_key("system_prefix", "global", cache_key)

        entry = CacheEntry(
            layer="system_prefix",
            cache_key=cache_key,
            content=content,
            source_version_hashes=[policy_version],
            sensitivity_class="public",
            token_count=self._estimate_tokens(content),
        )
        self._memory[full_key] = entry
        self._persist_entry(entry)

    # --- Layer 2: Workspace Context Cache ---

    def get_workspace_context(
        self,
        dna_slice_hash: str,
        module_ids: list[str],
        policy_decision_id: str,
    ) -> Optional[str]:
        """Get cached workspace context for a DNA slice + modules + policy."""
        key_parts = [dna_slice_hash] + sorted(module_ids) + [policy_decision_id]
        cache_key = self._hash_content("|".join(key_parts))
        full_key = self._make_key("workspace", "repo", cache_key)

        entry = self._memory.get(full_key) or self._load_entry("workspace", cache_key)
        if entry and not entry.is_expired():
            # Check divergence
            current_hashes = [dna_slice_hash] + sorted(module_ids)
            if self._check_divergence(entry, current_hashes):
                self.metrics.record_divergence()
                self.invalidate(full_key)
                self.metrics.record_miss("workspace")
                return None

            self.metrics.record_hit("workspace", entry.token_count)
            # Update LRU
            if full_key in self._lru_order:
                self._lru_order.remove(full_key)
            self._lru_order.append(full_key)
            return entry.content

        self.metrics.record_miss("workspace")
        return None

    def set_workspace_context(
        self,
        content: str,
        dna_slice_hash: str,
        module_ids: list[str],
        policy_decision_id: str,
    ):
        """Cache workspace context."""
        key_parts = [dna_slice_hash] + sorted(module_ids) + [policy_decision_id]
        cache_key = self._hash_content("|".join(key_parts))
        full_key = self._make_key("workspace", "repo", cache_key)

        entry = CacheEntry(
            layer="workspace",
            cache_key=cache_key,
            content=content,
            source_version_hashes=[dna_slice_hash] + sorted(module_ids),
            sensitivity_class="repository",
            token_count=self._estimate_tokens(content),
        )
        self._memory[full_key] = entry
        self._persist_entry(entry)
        self._lru_order.append(full_key)
        self._enforce_lru()

    # --- Layer 3: Compacted History Cache ---

    def get_compacted_history(
        self, session_id: str, sequence_number: int
    ) -> Optional[str]:
        """Get cached compacted history for a session."""
        cache_key = self._hash_content(f"{session_id}:{sequence_number}")
        full_key = self._make_key("history", session_id, cache_key)

        entry = self._memory.get(full_key) or self._load_entry("history", cache_key)
        if entry and not entry.is_expired():
            self.metrics.record_hit("history", entry.token_count)
            return entry.content

        self.metrics.record_miss("history")
        return None

    def set_compacted_history(
        self,
        content: str,
        session_id: str,
        sequence_number: int,
        ttl: Optional[int] = 86400,
    ):
        """Cache compacted history (session-scoped)."""
        cache_key = self._hash_content(f"{session_id}:{sequence_number}")
        full_key = self._make_key("history", session_id, cache_key)

        entry = CacheEntry(
            layer="history",
            cache_key=cache_key,
            content=content,
            source_version_hashes=[session_id, str(sequence_number)],
            sensitivity_class="session",
            token_count=self._estimate_tokens(content),
            ttl=ttl,
        )
        self._memory[full_key] = entry
        self._persist_entry(entry)

    def invalidate_session_history(self, session_id: str):
        """Invalidate all history cache entries for a session."""
        history_dir = self.cache_dir / "history"
        for f in history_dir.glob(f"*{session_id}*"):
            f.unlink()
        keys_to_delete = [
            k for k in self._memory if k.startswith(f"history:{session_id}")
        ]
        for k in keys_to_delete:
            del self._memory[k]

    # --- General Operations ---

    def invalidate(self, cache_key: str):
        """Invalidate a specific cache entry."""
        if cache_key in self._memory:
            del self._memory[cache_key]
        # Try to find and delete from disk
        for layer_dir in ["system_prefix", "workspace", "history"]:
            entry_path = self.cache_dir / layer_dir / f"{cache_key}.json"
            if entry_path.exists():
                entry_path.unlink()

    def get_metrics_snapshot(self) -> dict:
        """Get current cache metrics."""
        self.metrics.check_alerts()
        return self.metrics.to_dict()

    def warmup_system_prefix(
        self,
        model_id: str,
        tool_list: list[str],
        policy_version: str,
        content: str,
    ):
        """Pre-warm the system prefix cache for a model."""
        self.set_system_prefix(content, model_id, tool_list, policy_version)
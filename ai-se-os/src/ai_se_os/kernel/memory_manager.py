"""
AI-SE OS Memory Manager
Manages scoped memory with TTL, namespacing, and persistence
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import json
import os
import threading
import time


@dataclass
class MemoryEntry:
    """A single memory entry with metadata"""
    id: str = field(default_factory=lambda: str(uuid4()))
    key: str = ""
    value: Any = None
    namespace: str = ""
    scope: str = "session"  # session, task, repository, global
    importance: float = 0.5  # 0.0-1.0
    ttl_seconds: Optional[int] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    accessed_at: str = field(default_factory=lambda: datetime.now().isoformat())
    access_count: int = 0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        if not self.ttl_seconds:
            return False
        created = datetime.fromisoformat(self.created_at)
        return (datetime.now() - created).total_seconds() > self.ttl_seconds

    def record_access(self) -> None:
        self.access_count += 1
        self.accessed_at = datetime.now().isoformat()


class MemoryManager:
    """
    Scoped memory manager for AI-SE OS.
    
    Supports:
    - Session-scoped memory (ephemeral)
    - Task-scoped memory (task lifecycle)
    - Repository-scoped memory (persistent)
    - Global memory (shared across all)
    - TTL-based expiration
    - Importance-based retention
    """

    def __init__(self, storage_dir: Optional[str] = None):
        self._store: Dict[str, MemoryEntry] = {}
        self._lock = threading.RLock()
        self._storage_dir = storage_dir
        self._max_entries = 10000

        # Load persisted memory
        if storage_dir:
            self._load_persisted()

    def _load_persisted(self) -> None:
        """Load persisted memory from disk"""
        memory_file = os.path.join(self._storage_dir, "memory.json")
        if os.path.exists(memory_file):
            try:
                with open(memory_file, "r") as f:
                    data = json.load(f)
                    for entry_data in data:
                        entry = MemoryEntry(
                            id=entry_data.get("id", str(uuid4())),
                            key=entry_data["key"],
                            value=entry_data["value"],
                            namespace=entry_data.get("namespace", ""),
                            scope=entry_data.get("scope", "session"),
                            importance=entry_data.get("importance", 0.5),
                            ttl_seconds=entry_data.get("ttl_seconds"),
                            created_at=entry_data.get("created_at", datetime.now().isoformat()),
                            accessed_at=entry_data.get("accessed_at", datetime.now().isoformat()),
                            access_count=entry_data.get("access_count", 0),
                            tags=entry_data.get("tags", []),
                            metadata=entry_data.get("metadata", {})
                        )
                        if not entry.is_expired():
                            self._store[entry.id] = entry
            except Exception as e:
                print(f"Error loading persisted memory: {e}")

    def _persist(self) -> None:
        """Persist memory to disk"""
        if not self._storage_dir:
            return

        os.makedirs(self._storage_dir, exist_ok=True)
        memory_file = os.path.join(self._storage_dir, "memory.json")

        try:
            data = []
            for entry in self._store.values():
                if entry.scope in ["repository", "global"] and not entry.is_expired():
                    data.append({
                        "id": entry.id,
                        "key": entry.key,
                        "value": entry.value,
                        "namespace": entry.namespace,
                        "scope": entry.scope,
                        "importance": entry.importance,
                        "ttl_seconds": entry.ttl_seconds,
                        "created_at": entry.created_at,
                        "accessed_at": entry.accessed_at,
                        "access_count": entry.access_count,
                        "tags": entry.tags,
                        "metadata": entry.metadata
                    })

            with open(memory_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error persisting memory: {e}")

    def remember(
        self,
        key: str,
        value: Any,
        namespace: str = "default",
        scope: str = "session",
        importance: float = 0.5,
        ttl_seconds: Optional[int] = None,
        tags: Optional[List[str]] = None
    ) -> str:
        """Store a memory entry"""
        with self._lock:
            # Evict if at capacity
            if len(self._store) >= self._max_entries:
                self._evict()

            entry = MemoryEntry(
                key=key,
                value=value,
                namespace=namespace,
                scope=scope,
                importance=importance,
                ttl_seconds=ttl_seconds,
                tags=tags or []
            )

            self._store[entry.id] = entry
            self._persist()
            return entry.id

    def recall(self, key: str, namespace: str = "default") -> Optional[Any]:
        """Recall a memory by key"""
        with self._lock:
            for entry in self._store.values():
                if entry.key == key and entry.namespace == namespace:
                    if entry.is_expired():
                        del self._store[entry.id]
                        return None
                    entry.record_access()
                    return entry.value
            return None

    def recall_by_id(self, memory_id: str) -> Optional[MemoryEntry]:
        """Recall a memory entry by ID"""
        with self._lock:
            entry = self._store.get(memory_id)
            if entry and entry.is_expired():
                del self._store[memory_id]
                return None
            if entry:
                entry.record_access()
            return entry

    def forget(self, memory_id: str) -> bool:
        """Forget a specific memory"""
        with self._lock:
            if memory_id in self._store:
                del self._store[memory_id]
                self._persist()
                return True
            return False

    def forget_by_key(self, key: str, namespace: str = "default") -> int:
        """Forget all memories matching a key"""
        count = 0
        with self._lock:
            ids_to_delete = [
                eid for eid, e in self._store.items()
                if e.key == key and e.namespace == namespace
            ]
            for eid in ids_to_delete:
                del self._store[eid]
                count += 1
            if count > 0:
                self._persist()
        return count

    def search(
        self,
        query: str,
        namespace: Optional[str] = None,
        scope: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_importance: float = 0.0,
        limit: int = 20
    ) -> List[MemoryEntry]:
        """Search memories by criteria"""
        results = []

        with self._lock:
            for entry in self._store.values():
                if entry.is_expired():
                    continue

                # Apply filters
                if namespace and entry.namespace != namespace:
                    continue
                if scope and entry.scope != scope:
                    continue
                if tags and not all(t in entry.tags for t in tags):
                    continue
                if entry.importance < min_importance:
                    continue

                # Text search
                if query.lower() in entry.key.lower() or \
                   (isinstance(entry.value, str) and query.lower() in entry.value.lower()):
                    results.append(entry)

        # Sort by importance and access count
        results.sort(key=lambda e: (e.importance, e.access_count), reverse=True)
        return results[:limit]

    def get_recent(self, namespace: str = "default", limit: int = 10) -> List[MemoryEntry]:
        """Get most recent memories"""
        with self._lock:
            entries = [
                e for e in self._store.values()
                if e.namespace == namespace and not e.is_expired()
            ]
            entries.sort(key=lambda e: e.created_at, reverse=True)
            return entries[:limit]

    def get_important(self, namespace: str = "default", limit: int = 10) -> List[MemoryEntry]:
        """Get most important memories"""
        with self._lock:
            entries = [
                e for e in self._store.values()
                if e.namespace == namespace and not e.is_expired()
            ]
            entries.sort(key=lambda e: e.importance, reverse=True)
            return entries[:limit]

    def clear_scope(self, scope: str) -> int:
        """Clear all memories in a scope"""
        count = 0
        with self._lock:
            ids_to_delete = [eid for eid, e in self._store.items() if e.scope == scope]
            for eid in ids_to_delete:
                del self._store[eid]
                count += 1
            if count > 0:
                self._persist()
        return count

    def clear_namespace(self, namespace: str) -> int:
        """Clear all memories in a namespace"""
        count = 0
        with self._lock:
            ids_to_delete = [eid for eid, e in self._store.items() if e.namespace == namespace]
            for eid in ids_to_delete:
                del self._store[eid]
                count += 1
            if count > 0:
                self._persist()
        return count

    def _evict(self) -> None:
        """Evict least important/accessed memories"""
        # Sort by importance * access_count, evict lowest
        sorted_entries = sorted(
            self._store.values(),
            key=lambda e: e.importance * (e.access_count + 1)
        )

        # Evict bottom 10%
        evict_count = max(1, len(sorted_entries) // 10)
        for entry in sorted_entries[:evict_count]:
            if entry.scope in ["session", "task"]:  # Only evict ephemeral scopes
                del self._store[entry.id]

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        with self._lock:
            total = len(self._store)
            by_scope = {}
            by_namespace = {}

            for entry in self._store.values():
                if entry.is_expired():
                    continue
                by_scope[entry.scope] = by_scope.get(entry.scope, 0) + 1
                by_namespace[entry.namespace] = by_namespace.get(entry.namespace, 0) + 1

            return {
                "total_entries": total,
                "by_scope": by_scope,
                "by_namespace": by_namespace,
                "avg_importance": sum(e.importance for e in self._store.values()) / total if total > 0 else 0,
                "total_accesses": sum(e.access_count for e in self._store.values()),
                "max_entries": self._max_entries
            }
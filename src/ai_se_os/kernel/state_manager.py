"""
AI-SE OS State Manager
Manages system state with namespacing and persistence
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
import json
import os
import threading


@dataclass
class NamespaceKey:
    """Fully qualified namespace key"""
    repository: str = ""
    workspace: str = ""
    worktree: str = ""
    branch: str = ""
    session: str = ""

    def to_path(self) -> str:
        """Convert to filesystem path"""
        parts = [self.repository, self.workspace, self.worktree, self.branch, self.session]
        return "/".join(p for p in parts if p)

    def to_key(self) -> str:
        """Convert to dot-separated key"""
        parts = [self.repository, self.workspace, self.worktree, self.branch, self.session]
        return ".".join(p for p in parts if p)

    @classmethod
    def from_key(cls, key: str) -> "NamespaceKey":
        """Parse from dot-separated key"""
        parts = key.split(".")
        return cls(
            repository=parts[0] if len(parts) > 0 else "",
            workspace=parts[1] if len(parts) > 1 else "",
            worktree=parts[2] if len(parts) > 2 else "",
            branch=parts[3] if len(parts) > 3 else "",
            session=parts[4] if len(parts) > 4 else ""
        )


@dataclass
class StateEntry:
    """A single state entry with metadata"""
    key: str
    value: Any
    namespace: NamespaceKey
    version: int = 1
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    created_by: Optional[str] = None
    ttl: Optional[int] = None  # Time to live in seconds
    immutable: bool = False


class StateManager:
    """
    Namespaced state manager for AI-SE OS.
    
    All state is namespaced by repository, workspace, worktree, branch, and session.
    No agent relies on an unqualified "current task".
    """

    def __init__(self, storage_dir: Optional[str] = None):
        self._store: Dict[str, StateEntry] = {}
        self._lock = threading.RLock()
        self._storage_dir = storage_dir

        # Load persisted state if available
        if storage_dir:
            self._load_persisted()

    def _load_persisted(self) -> None:
        """Load persisted state from disk"""
        state_file = os.path.join(self._storage_dir, "state.json")
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as f:
                    data = json.load(f)
                    for key, entry_data in data.items():
                        ns = NamespaceKey.from_key(entry_data.get("namespace_key", ""))
                        self._store[key] = StateEntry(
                            key=key,
                            value=entry_data["value"],
                            namespace=ns,
                            version=entry_data.get("version", 1),
                            created_at=entry_data.get("created_at", ""),
                            updated_at=entry_data.get("updated_at", ""),
                            created_by=entry_data.get("created_by"),
                            ttl=entry_data.get("ttl"),
                            immutable=entry_data.get("immutable", False)
                        )
            except Exception as e:
                print(f"Error loading persisted state: {e}")

    def _persist(self) -> None:
        """Persist state to disk"""
        if not self._storage_dir:
            return

        os.makedirs(self._storage_dir, exist_ok=True)
        state_file = os.path.join(self._storage_dir, "state.json")

        try:
            data = {}
            for key, entry in self._store.items():
                data[key] = {
                    "value": entry.value,
                    "namespace_key": entry.namespace.to_key(),
                    "version": entry.version,
                    "created_at": entry.created_at,
                    "updated_at": entry.updated_at,
                    "created_by": entry.created_by,
                    "ttl": entry.ttl,
                    "immutable": entry.immutable
                }

            with open(state_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error persisting state: {e}")

    def _make_key(self, namespace: NamespaceKey, name: str) -> str:
        """Create a fully qualified key"""
        return f"{namespace.to_key()}.{name}"

    def set(
        self,
        namespace: NamespaceKey,
        name: str,
        value: Any,
        created_by: Optional[str] = None,
        ttl: Optional[int] = None,
        immutable: bool = False
    ) -> StateEntry:
        """Set a state value"""
        key = self._make_key(namespace, name)

        with self._lock:
            existing = self._store.get(key)
            if existing and existing.immutable:
                raise ValueError(f"Cannot modify immutable state: {key}")

            now = datetime.now().isoformat()
            entry = StateEntry(
                key=key,
                value=value,
                namespace=namespace,
                version=(existing.version + 1) if existing else 1,
                created_at=existing.created_at if existing else now,
                updated_at=now,
                created_by=created_by,
                ttl=ttl,
                immutable=immutable
            )

            self._store[key] = entry
            self._persist()
            return entry

    def get(self, namespace: NamespaceKey, name: str, default: Any = None) -> Optional[Any]:
        """Get a state value"""
        key = self._make_key(namespace, name)

        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return default

            # Check TTL
            if entry.ttl:
                created = datetime.fromisoformat(entry.created_at)
                elapsed = (datetime.now() - created).total_seconds()
                if elapsed > entry.ttl:
                    del self._store[key]
                    self._persist()
                    return default

            return entry.value

    def get_entry(self, namespace: NamespaceKey, name: str) -> Optional[StateEntry]:
        """Get the full state entry with metadata"""
        key = self._make_key(namespace, name)

        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None

            # Check TTL
            if entry.ttl:
                created = datetime.fromisoformat(entry.created_at)
                elapsed = (datetime.now() - created).total_seconds()
                if elapsed > entry.ttl:
                    del self._store[key]
                    self._persist()
                    return None

            return entry

    def delete(self, namespace: NamespaceKey, name: str) -> bool:
        """Delete a state value"""
        key = self._make_key(namespace, name)

        with self._lock:
            entry = self._store.get(key)
            if entry and entry.immutable:
                raise ValueError(f"Cannot delete immutable state: {key}")

            if key in self._store:
                del self._store[key]
                self._persist()
                return True
            return False

    def list_namespace(self, namespace: NamespaceKey) -> Dict[str, Any]:
        """List all state in a namespace"""
        prefix = namespace.to_key()
        result = {}

        with self._lock:
            for key, entry in self._store.items():
                if key.startswith(prefix):
                    # Extract the name part
                    name = key[len(prefix) + 1:] if len(key) > len(prefix) else key

                    # Check TTL
                    if entry.ttl:
                        created = datetime.fromisoformat(entry.created_at)
                        elapsed = (datetime.now() - created).total_seconds()
                        if elapsed > entry.ttl:
                            continue

                    result[name] = entry.value

        return result

    def search(self, query: str) -> List[StateEntry]:
        """Search state entries by key pattern"""
        results = []

        with self._lock:
            for key, entry in self._store.items():
                if query.lower() in key.lower():
                    # Check TTL
                    if entry.ttl:
                        created = datetime.fromisoformat(entry.created_at)
                        elapsed = (datetime.now() - created).total_seconds()
                        if elapsed > entry.ttl:
                            continue
                    results.append(entry)

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Get state manager statistics"""
        with self._lock:
            total = len(self._store)
            immutable_count = sum(1 for e in self._store.values() if e.immutable)
            with_ttl = sum(1 for e in self._store.values() if e.ttl is not None)
            total_versions = sum(e.version for e in self._store.values())

            return {
                "total_entries": total,
                "immutable_entries": immutable_count,
                "entries_with_ttl": with_ttl,
                "total_versions": total_versions,
                "avg_version": total_versions / total if total > 0 else 0
            }

    def clear(self, namespace: Optional[NamespaceKey] = None) -> int:
        """Clear state, optionally for a specific namespace"""
        count = 0

        with self._lock:
            if namespace:
                prefix = namespace.to_key()
                keys_to_delete = [k for k in self._store.keys() if k.startswith(prefix)]
                for key in keys_to_delete:
                    entry = self._store.get(key)
                    if entry and entry.immutable:
                        continue
                    del self._store[key]
                    count += 1
            else:
                count = len(self._store)
                self._store.clear()

            self._persist()

        return count
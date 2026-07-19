#!/usr/bin/env python3
"""
Cache-Aware Context Compiler for AI-SE OS
==========================================
Assembles task-specific, cache-optimized context packs.

Structure:
  Layer 1 - System Prefix (cached, ~2K tokens)
  Layer 2 - Workspace Context (cached, ~3K tokens)
  Layer 3 - Compacted History (cached, ~2K tokens)
  Layer 4 - Dynamic Window (uncached, ~3.5K tokens + 1K buffer)

Targets 80-90% cache hit rate.
Default total budget: 11,500 tokens.
"""

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class CompiledContext:
    """Output of the context compiler."""

    context: str
    cache_key: str
    cache_hit: bool
    token_count: int
    layer_breakdown: dict
    cache_metrics: dict
    system_prefix: str = ""
    workspace_context: str = ""
    compacted_history: str = ""
    dynamic_content: str = ""


@dataclass
class Task:
    """Simplified task descriptor for context compilation."""

    id: str
    type: str  # planning, execution, recovery, analysis, review
    description: str
    model_id: str
    capabilities: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    files_changed: list[str] = field(default_factory=list)
    new_tokens: list[str] = field(default_factory=list)


class CacheAwareContextCompiler:
    """
    Compiles context with three-layer caching and a dynamic window.
    """

    def __init__(self, cache_service=None):
        self.cache_service = cache_service
        self.version = "1.0.0"
        self.session_id = str(uuid.uuid4())
        self.compaction_sequence = 0

    def set_cache_service(self, cache_service):
        """Inject cache service."""
        self.cache_service = cache_service

    def _hash(self, content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _estimate_tokens(self, text: str) -> int:
        return len(text) // 4

    def compile_context(self, task: Task, workspace_dna: Optional[dict] = None) -> CompiledContext:
        """
        Compile context with cache optimization.

        Args:
            task: The task descriptor
            workspace_dna: Repository DNA slice (optional)

        Returns:
            CompiledContext with cached prefix + dynamic content
        """
        # 1. Build system prefix (Layer 1 - cached)
        system_prefix = self._build_system_prefix(task)
        system_hash = self._hash(system_prefix)

        # 2. Build workspace context (Layer 2 - cached)
        workspace_json = json.dumps(workspace_dna or {}, sort_keys=True)
        workspace_context = self._build_workspace_context(task, workspace_dna)
        workspace_hash = self._hash(workspace_json)

        # 3. Get compacted history (Layer 3 - cached)
        history = self._get_compacted_history(task)
        history_hash = self._hash(json.dumps(history, sort_keys=True))

        # 4. Build dynamic changes (Layer 4 - uncached)
        dynamic_changes = self._build_dynamic_content(task)

        # 5. Cache check
        cache_key = f"ctx:{system_hash}:{workspace_hash}:{history_hash}"
        cache_hit = False

        if self.cache_service:
            # Layer 1 check
            cached_prefix = self.cache_service.get_system_prefix(
                model_id=task.model_id,
                tool_list=task.capabilities,
                policy_version=self.version,
            )

            if cached_prefix:
                # Cache hit - use cached prefix, append only dynamic
                prefix = cached_prefix
                cache_hit = True
                system_prefix_tokens = 0  # already counted in cache
            else:
                # Cache miss - build full prefix and cache it
                prefix = system_prefix
                if self.cache_service:
                    self.cache_service.set_system_prefix(
                        content=prefix,
                        model_id=task.model_id,
                        tool_list=task.capabilities,
                        policy_version=self.version,
                    )

            context = prefix + "\n" + dynamic_changes

            if cache_hit:
                self.cache_service.metrics.record_hit("system_prefix", self._estimate_tokens(prefix))
            else:
                self.cache_service.metrics.record_miss("system_prefix", self._estimate_tokens(prefix))
        else:
            # No cache service - build everything fresh
            context = system_prefix + "\n" + workspace_context + "\n" + history + "\n" + dynamic_changes

        total_tokens = self._estimate_tokens(context)

        return CompiledContext(
            context=context,
            cache_key=cache_key,
            cache_hit=cache_hit,
            token_count=total_tokens,
            system_prefix=system_prefix,
            workspace_context=workspace_context,
            compacted_history=json.dumps(history, indent=2),
            dynamic_content=dynamic_changes,
            layer_breakdown={
                "system_prefix": self._estimate_tokens(system_prefix),
                "workspace_context": self._estimate_tokens(workspace_context),
                "compacted_history": self._estimate_tokens(json.dumps(history)),
                "dynamic_content": self._estimate_tokens(dynamic_changes),
                "cache_hit": cache_hit,
            },
            cache_metrics=self.cache_service.get_metrics_snapshot() if self.cache_service else {},
        )

    def _build_system_prefix(self, task: Task) -> str:
        """Build static system prefix (deterministic, sort keys)."""
        parts = [
            f"System Role: Engineering Intelligence Agent",
            f"Model: {task.model_id}",
            f"OS Version: AI-SE OS v3 (Context Compiler v{self.version})",
            f"Session: {self.session_id}",
            f"Capabilities: {', '.join(sorted(task.capabilities))}",
            f"Constraints: {', '.join(sorted(task.constraints))}",
        ]
        return "\n".join(parts)

    def _build_workspace_context(self, task: Task, dna: Optional[dict]) -> str:
        """Build workspace context from DNA (semi-static)."""
        if not dna:
            return "Workspace Context: (not available)"

        lines = ["--- WORKSPACE CONTEXT ---"]
        for key, value in sorted(dna.items()):
            if isinstance(value, (list, tuple)):
                lines.append(f"  {key}: {', '.join(str(v) for v in value)}")
            elif isinstance(value, dict):
                lines.append(f"  {key}: (nested, {len(value)} keys)")
            else:
                lines.append(f"  {key}: {value}")
        return "\n".join(lines)

    def _get_compacted_history(self, task: Task) -> dict:
        """Get or build compacted history."""
        return {
            "session_id": self.session_id,
            "compaction_sequence": self.compaction_sequence,
            "current_task": task.id,
            "task_type": task.type,
            "description": task.description[:200],
            "files_changed": task.files_changed,
        }

    def _build_dynamic_content(self, task: Task) -> str:
        """Build uncached dynamic content for current task."""
        parts = ["--- DYNAMIC CONTEXT ---"]

        if task.description:
            parts.append(f"Task Description: {task.description}")

        if task.files_changed:
            parts.append(f"Files Changed: {', '.join(task.files_changed)}")

        if task.new_tokens:
            parts.append(f"New Information: {', '.join(task.new_tokens)}")

        return "\n".join(parts)

    def compact_history(self, session_history: list[dict]) -> str:
        """
        Compact long session history into structured summary.
        Triggered when history exceeds 80% of remaining context window.

        Args:
            session_history: List of session entry dicts

        Returns:
            Structured summary string
        """
        self.compaction_sequence += 1

        timeline = []
        decisions = []
        outcomes = []
        current_state = {
            "files_changed": [],
            "validation_status": "unknown",
            "open_blockers": [],
        }
        next_steps = []

        for entry in session_history:
            entry_type = entry.get("type", "")
            if entry_type == "decision":
                decisions.append(
                    f"[{entry.get('id', 'ADR-???')}] {entry.get('description', '')[:100]}"
                )
            elif entry_type == "outcome":
                outcomes.append(entry.get("description", "")[:100])
            elif entry_type == "task_completed":
                timeline.append(
                    f"- [{entry.get('task_id', '???')}] {entry.get('summary', '')[:100]}"
                )
            elif entry_type == "state":
                current_state.update(entry.get("state", {}))

        lines = [
            f"--- COMPACTED HISTORY [seq={self.compaction_sequence} session={self.session_id}] ---",
            "Timeline:",
        ]
        lines.extend(timeline if timeline else ["  (no completed tasks in window)"])

        lines.append("Decisions:")
        lines.extend(decisions if decisions else ["  (none recorded)"])

        lines.append("Current State:")
        lines.append(f"  files_changed: {current_state.get('files_changed', [])}")
        lines.append(f"  validation_status: {current_state.get('validation_status', 'unknown')}")
        lines.append(f"  open_blockers: {current_state.get('open_blockers', [])}")

        lines.append("Next Steps:")
        lines.extend(next_steps if next_steps else ["  (determine during current planning)"])

        summary = "\n".join(lines)

        # Cache the compacted history
        if self.cache_service:
            self.cache_service.set_compacted_history(
                content=summary,
                session_id=self.session_id,
                sequence_number=self.compaction_sequence,
            )
            self.cache_service.metrics.record_compaction()

        return summary

    def invalidate_session(self):
        """Invalidate all session-scoped caches."""
        if self.cache_service:
            self.cache_service.invalidate_session_history(self.session_id)

    def get_token_budget(self) -> dict:
        """Return the default token budget allocation."""
        return {
            "system_prefix": 2000,
            "workspace_context": 3000,
            "compacted_history": 2000,
            "dynamic_changes": 3500,
            "buffer": 1000,
            "total": 11500,
            "cache_target": "~70% cached",
        }
"""
AI-SE OS Context Compiler with Cache Optimization
Implements token optimization strategies
"""

import hashlib
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from src.cache.cache_service import CacheService, CacheStrategy
from src.cache.cache_tracker import CacheTracker


@dataclass
class CompiledContext:
    """Compiled context result"""
    context: str
    cache_key: str
    cache_hit: bool
    token_count: int
    cache_metrics: Dict[str, Any]
    provenance: List[Dict[str, Any]]


class ContextCompiler:
    """
    Context Compiler with Cache Awareness
    Builds minimal relevant context with token optimization
    """

    def __init__(self, cache_service: CacheService):
        self.cache_service = cache_service
        self.cache_tracker = CacheTracker()
        self.version = "1.0.0"

        # Token budget allocation
        self.token_budget = {
            "system_prefix": 2000,      # Cached
            "workspace_context": 3000,   # Cached
            "compacted_history": 2000,   # Cached
            "dynamic_changes": 3500,     # New
            "buffer": 1000               # Buffer
        }
        self.total_budget = sum(self.token_budget.values())

    def compile_context(
        self,
        task: Any,
        workspace: Any,
        history: Optional[List[Dict[str, Any]]] = None
    ) -> CompiledContext:
        """
        Compile context with cache optimization.

        Args:
            task: Task to compile context for
            workspace: Workspace containing repository state
            history: Optional chat history for compaction

        Returns:
            CompiledContext with optimized context
        """
        provenance = []

        # 1. Build system prefix (cached)
        system_prefix = self._build_system_prefix(task)
        system_hash = hashlib.sha256(system_prefix.encode()).hexdigest()
        cache_key_system = f"ctx:system:{system_hash}"

        cached_system = self.cache_service.get(cache_key_system)
        if cached_system:
            system_context = cached_system
            self.cache_tracker.record_hit(
                key=cache_key_system,
                strategy="system_prefix",
                tokens_saved=self.token_budget["system_prefix"]
            )
            provenance.append({
                "source": "cache",
                "key": cache_key_system,
                "type": "system_prefix"
            })
        else:
            system_context = self._format_for_cache(system_prefix)
            self.cache_service.set(cache_key_system, system_context)
            self.cache_tracker.record_miss(
                key=cache_key_system,
                strategy="system_prefix"
            )
            provenance.append({
                "source": "generated",
                "type": "system_prefix"
            })

        # 2. Build workspace context (cached)
        workspace_context = self._build_workspace_context(workspace)
        workspace_hash = hashlib.sha256(workspace_context.encode()).hexdigest()
        cache_key_workspace = f"ctx:workspace:{workspace_hash}"

        cached_workspace = self.cache_service.get(cache_key_workspace)
        if cached_workspace:
            workspace_ctx = cached_workspace
            self.cache_tracker.record_hit(
                key=cache_key_workspace,
                strategy="workspace_context",
                tokens_saved=self.token_budget["workspace_context"]
            )
            provenance.append({
                "source": "cache",
                "key": cache_key_workspace,
                "type": "workspace_context"
            })
        else:
            workspace_ctx = self._format_for_cache(workspace_context)
            self.cache_service.set(cache_key_workspace, workspace_ctx)
            self.cache_tracker.record_miss(
                key=cache_key_workspace,
                strategy="workspace_context"
            )
            provenance.append({
                "source": "generated",
                "type": "workspace_context"
            })

        # 3. Build compacted history (cached)
        if history:
            compacted_history = self._compact_history(history)
            history_hash = hashlib.sha256(compacted_history.encode()).hexdigest()
            cache_key_history = f"ctx:history:{history_hash}"

            cached_history = self.cache_service.get(cache_key_history)
            if cached_history:
                history_ctx = cached_history
                self.cache_tracker.record_hit(
                    key=cache_key_history,
                    strategy="history_compact",
                    tokens_saved=self.token_budget["compacted_history"]
                )
                provenance.append({
                    "source": "cache",
                    "key": cache_key_history,
                    "type": "history_compact"
                })
            else:
                history_ctx = self._format_for_cache(compacted_history)
                self.cache_service.set(cache_key_history, history_ctx)
                self.cache_tracker.record_miss(
                    key=cache_key_history,
                    strategy="history_compact"
                )
                provenance.append({
                    "source": "generated",
                    "type": "history_compact"
                })
        else:
            history_ctx = ""

        # 4. Build dynamic changes (new - not cached)
        dynamic_changes = self._build_dynamic_changes(task)
        dynamic_ctx = self._format_for_cache(dynamic_changes)
        provenance.append({
            "source": "generated",
            "type": "dynamic_changes"
        })

        # 5. Assemble final context
        full_context = system_context + workspace_ctx + history_ctx + dynamic_ctx

        # 6. Count tokens (approximate)
        token_count = self._count_tokens(full_context)

        # 7. Check if token budget exceeded
        if token_count > self.total_budget:
            # Compress further
            full_context = self._compress_context(full_context)
            token_count = self._count_tokens(full_context)

        return CompiledContext(
            context=full_context,
            cache_key=f"{cache_key_system}:{cache_key_workspace}",
            cache_hit=cached_system is not None and cached_workspace is not None,
            token_count=token_count,
            cache_metrics=self.cache_tracker.get_metrics(),
            provenance=provenance
        )

    def _build_system_prefix(self, task: Any) -> str:
        """Build static system prefix for caching"""
        return f"""
System Role: Engineering Intelligence Agent
Model: {getattr(task, 'model', 'default')}
Version: {self.version}
Capabilities: {getattr(task, 'capabilities', [])}
Constraints: {getattr(task, 'constraints', {})}

## System Instructions
1. Understand the repository structure using the provided Genome
2. Plan changes carefully before implementing
3. Validate all changes before completion
4. Provide provenance for all decisions

## Output Format
- Use structured JSON for responses
- Include confidence scores
- Cite evidence sources
"""

    def _build_workspace_context(self, workspace: Any) -> str:
        """Build deterministic workspace context"""
        context = {
            "repository_dna": getattr(workspace, 'dna', {}),
            "knowledge_graph": getattr(workspace, 'knowledge_graph', {}),
            "dependencies": getattr(workspace, 'dependencies', []),
            "architecture": getattr(workspace, 'architecture', {})
        }
        return json.dumps(context, indent=2, sort_keys=True)

    def _compact_history(self, history: List[Dict[str, Any]]) -> str:
        """Compact chat history into structured summary"""
        summary = {
            "timeline": [],
            "decisions": [],
            "outcomes": [],
            "current_state": {},
            "next_steps": []
        }

        for entry in history:
            entry_type = entry.get('type', '')
            if entry_type == 'decision':
                summary["decisions"].append(entry.get('adr', {}))
            elif entry_type == 'outcome':
                summary["outcomes"].append(entry.get('result', {}))
            elif entry_type == 'task':
                summary["timeline"].append(entry.get('summary', {}))
            elif entry_type == 'state':
                summary["current_state"] = entry.get('state', {})
            elif entry_type == 'next':
                summary["next_steps"].append(entry.get('step', {}))

        return f"""
--- COMPACTED HISTORY ---
Timeline: {json.dumps(summary['timeline'], indent=2)}
Decisions: {json.dumps(summary['decisions'], indent=2)}
Outcomes: {json.dumps(summary['outcomes'], indent=2)}
Current State: {json.dumps(summary['current_state'], indent=2)}
Next Steps: {json.dumps(summary['next_steps'], indent=2)}
--------------------------
"""

    def _build_dynamic_changes(self, task: Any) -> str:
        """Build dynamic changes for the current task"""
        return f"""
--- DYNAMIC CHANGES ---
Task: {getattr(task, 'name', '')}
Description: {getattr(task, 'description', '')}
Scope: {getattr(task, 'scope', {})}
Success Criteria: {getattr(task, 'success_criteria', [])}
------------------------
"""

    def _format_for_cache(self, content: str) -> str:
        """Format content deterministically for cache"""
        return content.strip() + "\n\n"

    def _count_tokens(self, text: str) -> int:
        """Approximate token count (4 chars per token)"""
        return len(text) // 4

    def _compress_context(self, context: str, target_ratio: float = 0.7) -> str:
        """Compress context if token budget exceeded"""
        # Simple compression: truncate history section
        if "--- COMPACTED HISTORY ---" in context:
            parts = context.split("--- COMPACTED HISTORY ---")
            # Keep system prefix and dynamic changes, truncate history
            return parts[0] + parts[2] if len(parts) > 2 else context
        return context

    def get_cache_metrics(self) -> Dict[str, Any]:
        """Get cache metrics"""
        return self.cache_tracker.get_metrics()
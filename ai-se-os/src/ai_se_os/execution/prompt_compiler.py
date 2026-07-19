"""
AI-SE OS Prompt Compiler
Compiles minimal, provenance-tagged context packs into optimized prompts
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
import json
import hashlib

from ..core.data_models import GenomeSnapshot
from ..cache.cache_service import CacheService


@dataclass
class PromptPacket:
    """Compiled prompt packet with metadata"""
    id: str = field(default_factory=lambda: str(uuid4()))
    system_prompt: str = ""
    context: str = ""
    instructions: str = ""
    full_prompt: str = ""
    token_count: int = 0
    provenance: List[Dict[str, Any]] = field(default_factory=list)
    policies_referenced: List[str] = field(default_factory=list)
    model: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class PromptCompiler:
    """
    Compiles minimal, provenance-tagged context packs into optimized prompts.
    
    Follows the AI-SE OS rule:
    - Prompts must reference policies instead of duplicating policy text
    - Never send an entire repository to an LLM
    - All generated artifacts must be traceable
    """

    def __init__(self, cache_service: CacheService):
        self.cache_service = cache_service
        self._token_budget = 128000

        # Policy references (not full text)
        self._policy_references = {
            "constitution": ".ai_os/docs/02_ARCHITECTURE_CONSTITUTION.md",
            "validation": ".ai_os/docs/12_VALIDATION_ENGINE.md",
            "security": ".ai_os/docs/18_SECURITY.md",
            "token_policy": ".ai_os/policies/token_policy.md"
        }

    def compile_prompt(
        self,
        task_type: str,
        context_pack: Dict[str, Any],
        genome_snapshot: Optional[GenomeSnapshot] = None,
        instructions: Optional[str] = None,
        model: str = "default"
    ) -> PromptPacket:
        """
        Compile a minimal, provenance-tagged prompt packet.
        
        Args:
            task_type: Type of task (planning, execution, validation, etc.)
            context_pack: Minimal context pack with only relevant information
            genome_snapshot: Optional genome snapshot for repository awareness
            instructions: Optional specific instructions
            model: Target model identifier
            
        Returns:
            PromptPacket with compiled prompt
        """
        provenance = []
        parts = []

        # 1. System role (cached)
        system_prompt = self._build_system_prompt(task_type, model)
        parts.append(system_prompt)
        provenance.append({"source": "compiled", "type": "system_role", "model": model})

        # 2. Policy references (not full text)
        policy_section = self._build_policy_references(task_type)
        if policy_section:
            parts.append(policy_section)
            provenance.append({"source": "compiled", "type": "policy_references", "count": len(self._policy_references)})

        # 3. Repository context (minimal - from genome)
        if genome_snapshot:
            repo_context = self._extract_minimal_context(genome_snapshot)
            parts.append(repo_context)
            provenance.append({
                "source": "genome",
                "type": "repository_context",
                "genome_version": genome_snapshot.version,
                "git_hash": genome_snapshot.git_hash
            })

        # 4. Task context (from context pack)
        task_context = self._build_task_context(context_pack)
        parts.append(task_context)
        provenance.append({"source": "context_pack", "type": "task_context"})

        # 5. Instructions
        if instructions:
            parts.append(f"\n## Instructions\n{instructions}\n")
            provenance.append({"source": "user", "type": "instructions"})

        # 6. Constitution reference (minimum)
        constitution_ref = self._build_constitution_reference(task_type)
        if constitution_ref:
            parts.append(constitution_ref)
            provenance.append({"source": "constitution", "type": "constitution_reference"})

        # Assemble
        full_prompt = "\n\n".join(p for p in parts if p)

        # Token estimation
        token_count = len(full_prompt) // 4

        # Truncate if needed
        if token_count > self._token_budget:
            full_prompt = self._truncate_prompt(full_prompt, self._token_budget)
            token_count = len(full_prompt) // 4
            provenance.append({"source": "truncation", "type": "token_budget_enforced", "limit": self._token_budget})

        return PromptPacket(
            system_prompt=system_prompt,
            context=task_context,
            instructions=instructions or "",
            full_prompt=full_prompt,
            token_count=token_count,
            provenance=provenance,
            policies_referenced=list(self._policy_references.keys()),
            model=model
        )

    def _build_system_prompt(self, task_type: str, model: str) -> str:
        """Build system role prompt"""
        role_descriptions = {
            "planning": "You are an Engineering Planning Agent. You decompose requirements into bounded, executable tasks.",
            "execution": "You are an Engineering Execution Agent. You implement planned changes with precision.",
            "validation": "You are an Engineering Validation Agent. You verify changes against quality gates.",
            "architecture": "You are an Architecture Agent. You analyze and enforce architectural patterns.",
            "security": "You are a Security Agent. You identify and mitigate security risks.",
            "review": "You are a Code Review Agent. You review changes for quality and correctness.",
            "testing": "You are a Testing Agent. You ensure comprehensive test coverage.",
            "default": "You are an Engineering Intelligence Agent. You assist with software engineering tasks."
        }

        role = role_descriptions.get(task_type, role_descriptions["default"])

        return f"""
## System Role
{role}

## Operating Constraints
1. Never send an entire repository to the LLM - only relevant context
2. Every change must be validated against quality gates
3. Reference policies by name instead of duplicating policy text
4. All artifacts must be traceable to requirements
5. Preserve user changes - do not perform unrelated refactors

## Output Requirements
- Provide clear, actionable outputs
- Include evidence and reasoning for decisions
- Flag uncertainty with appropriate confidence levels
"""
    def _build_policy_references(self, task_type: str) -> str:
        """Build policy references section (not full policy text)"""
        return """
## Policy References
The following policies apply to this task. Refer to them in `.ai_os/policies/`:
- `constitution`: Architecture Constitution - non-negotiable rules
- `validation`: Validation Engine - required quality gates
- `security`: Security Policy - security-sensitive change handling
- `token_policy`: Token Budget Policy - token usage limits

DO NOT duplicate policy text. Reference policy names and follow their rules.
"""

    def _extract_minimal_context(self, genome: GenomeSnapshot) -> str:
        """Extract only relevant context from genome"""
        return f"""
## Repository Context (Genome v{genome.version})
- Architecture: {', '.join(genome.architecture.layers)} layers
- Patterns: {', '.join(genome.architecture.patterns)}
- Build System: {genome.build.system}
- Intelligence Score: {genome.health.intelligence_score}
- Test Coverage: {genome.test.coverage}%
- Health: {genome.health.build_status}
"""

    def _build_task_context(self, context_pack: Dict[str, Any]) -> str:
        """Build task context from context pack"""
        return json.dumps(context_pack, indent=2)

    def _build_constitution_reference(self, task_type: str) -> str:
        """Build constitution reference"""
        return """
## Constitution Rules (Reference Only)
See `.ai_os/docs/02_ARCHITECTURE_CONSTITUTION.md` for full text.
Key rules applicable to all tasks:
1. Tasks must be decomposed into bounded units
2. Every task must declare validation gates
3. Generated artifacts must be traceable
4. Validate every generated change
5. Prefer deterministic tools over model guesses
"""

    def _truncate_prompt(self, prompt: str, max_tokens: int) -> str:
        """Truncate prompt to fit within token budget"""
        max_chars = max_tokens * 4
        if len(prompt) <= max_chars:
            return prompt
        return prompt[:max_chars] + "\n\n[Content truncated to meet token budget]"
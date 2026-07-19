# 02 Architecture Constitution

## Purpose

Define non-negotiable rules that every agent, subsystem, prompt, and plugin must follow.

## Rules

1. Never send an entire repository to an LLM.
2. Always gather repository intelligence before generating implementation prompts.
3. Only changed modules may be re-indexed unless the index format changes.
4. All tasks must be decomposed into bounded units before code changes.
5. Every task must declare inputs, outputs, files, risks, owner, retry budget, rollback strategy, and validation gates.
6. All generated code must pass automated validation appropriate to its risk.
7. All model calls must declare token budget, purpose, expected output, privacy class, and policy decision.
8. Every failure must be classified, fingerprinted, and recorded for future learning.
9. Security-sensitive changes require explicit risk tagging and a capability-scoped permission decision.
10. Prompts must reference policies instead of duplicating policy text.
11. Generated artifacts must be traceable to a requirement, task, context pack, source version, and audit record.
12. Agents must preserve user changes and avoid unrelated refactors.
13. The OS must prefer deterministic tools over model guesses.
14. Human escalation is required for destructive actions, credential handling, unclear production impact, or policy decisions that require it.
15. Each durable artifact has one authoritative producer defined in `24_ARTIFACT_OWNERSHIP.md`; graph projections never invent source facts.
16. Audit records are append-only. Corrections create superseding records and retain provenance.
17. Runtime state must be namespaced by repository, workspace, worktree, branch, and session. Leases prevent concurrent conflicting work.
18. Confidence is evidence metadata, not proof. Low confidence must reduce autonomy or trigger re-indexing, more context, stronger reasoning, or escalation.
19. Secrets, regulated data, and unauthorized source text must not enter prompts, memory, telemetry, audit records, or examples.
20. Identical failure fingerprints must not be retried without a material change to context, plan, model, tool, or repository state.

## Enforcement

- PEPs block protected actions when a PDP does not return `allow`.
- Prompt Compiler injects constitution and policy references into every high-risk prompt.
- Validation Intelligence checks for missing artifact lineage, validation evidence, lease ownership, and policy exceptions.
- Audit records capture governance decisions and violations without retaining secrets.

## Acceptance Criteria

- Any agent can list the rules before starting implementation.
- Any task can be rejected for violating a constitutional rule.
- Policy exceptions require a written reason, bounded expiry, and human approval.
- No privileged execution path bypasses policy enforcement.

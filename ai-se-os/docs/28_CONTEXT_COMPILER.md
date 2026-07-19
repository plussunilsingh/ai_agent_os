# 28 Context Compiler

## Purpose

Deterministically assemble a task-specific, policy-safe, cache-optimised context pack from authoritative artifacts and queryable projections. The compiler targets an 80–90 % cache hit rate by structuring every prompt as a stable cached prefix followed by a minimal dynamic window.

## Inputs

- task, requirement, impact, and risk artifacts
- Repository DNA slice and Architectural Intent/Decision records
- symbols, APIs, DTOs, SQL, tests, dependency paths, and relevant failure records
- token policy, model context limit, and policy decision

## Output Structure

1. task outcome and acceptance criteria
2. allowed scope and prohibited changes
3. task-specific DNA and architectural intent
4. relevant symbols and interfaces
5. dependency, business-rule, and data-contract evidence
6. relevant tests and validation policy
7. prior failures only when the fingerprint is materially relevant
8. policy references, source versions, provenance, and token budget

## Selection Rules

- Target 5-15 KB of context for normal implementation tasks; prefer less than 10 KB for a micro-task when evidence permits.
- Prefer symbols, signatures, DTOs, API contracts, SQL fragments, tests, and structured summaries over full files.
- Full files are prohibited by default. A small-file exception records the file, size, reason, and policy reference.
- Context items are ranked by direct target relation, symbol reference, graph distance, test relation, recency, confidence, intent relevance, and failure relevance.
- Every item carries source artifact ID, source version/hash, selection reason, sensitivity class, freshness, and estimated tokens.
- A pack is immutable. A changed source or policy creates a new pack rather than mutating an old one.

## Cache-Aware Compilation Flow

The compiler builds every prompt in four stages, delegating cache operations to `41_CACHE_INTELLIGENCE.md`:

1. **System Prefix** (Layer 1, static, ~2 000 tokens)
   - Compile once: system role, model identity, OS version, active tool list, policy version.
   - Format deterministically (sorted keys, fixed structure). Cache key: `hash(system_text + model_id + tool_list + policy_version)`.
   - Reuse from cache when key matches. Invalidate on model, tool, or policy version change.

2. **Workspace Context** (Layer 2, semi-static, ~3 000 tokens)
   - Build from task-specific Repository DNA slice, module graph edges, architecture decisions, API signatures.
   - Cache key: `hash(dna_slice_hash + module_ids_sorted + policy_decision_id)`.
   - Invalidate when any included source artifact hash changes.
   - Full files are prohibited unless a small-file exception is recorded.

3. **Compacted History** (Layer 3, session-scoped, ~2 000 tokens)
   - Compress prior turns into a structured summary (timeline, decisions, current state, next steps).
   - Compaction trigger: history exceeds 80 % of remaining context window.
   - Cache key: `hash(session_id + compaction_sequence_number)`.

4. **Dynamic Window** (uncached, ~3 500 tokens + 1 000 buffer)
   - Append only: current task delta, new edits, new tokens, current failure details.
   - Budget overflow triggers task split or compaction; never silently drops mandatory constraints.

## Default Token Budget

| Layer | Tokens | Cached? |
|---|---|---|
| System Prefix | 2 000 | ✅ Layer 1 |
| Workspace Context | 3 000 | ✅ Layer 2 |
| Compacted History | 2 000 | ✅ Layer 3 |
| Dynamic Changes | 3 500 | ❌ Always fresh |
| Buffer | 1 000 | — |
| **Total** | **11 500** | **~70 % cached** |

## Cache Rules

- Cache only content-addressed source slices and derived summaries with source version references.
- Reuse cached slices when source versions, policy, task scope, and sensitivity eligibility match.
- Divergence detection runs on every cache hit before the entry is used; a changed source hash invalidates the entry.
- Cache hit rate is measured by reusable source slices, not by reusing stale whole prompts.
- Target: 80–90 % hit rate. Alert threshold: below 70 % over a rolling 1-hour window.

## Error Handling

- missing required evidence: return an incomplete pack and block prompt compilation
- policy masking requirement: replace or remove the sensitive slice before token fitting
- budget overflow: compress lower-ranked evidence, split the task, or escalate; never silently drop mandatory constraints
- stale source: trigger incremental index

## Plan Mode vs Act Mode Context

The compiler adjusts workspace and dynamic content based on the current OS mode (see `39_OS_MODES.md`):

- **Planning mode**: heavier workspace context (architecture intent, risk graph), lighter dynamic window.
- **Implementation mode**: heavier dynamic window (current file diffs, test failures), lighter workspace context.
- **Recovery mode**: dynamic window carries failure fingerprint and root-cause evidence only.

The model router communicates the active mode in the policy decision; the compiler adjusts token allocation accordingly.

## Interfaces

- context cache entry: `schemas/context_cache.schema.json`
- cache metrics: `schemas/cache_metrics.schema.json`
- cache operations: `41_CACHE_INTELLIGENCE.md`

## Acceptance Criteria

- A pack can be reproduced from its input artifact IDs and versions.
- A reviewer can identify why every item was included or omitted.
- Pack construction never leaks content outside the policy decision's data scope.

## Future Extensions

- learned relevance ranking with deterministic fallback
- semantic cache backed by hash and embedding verification
- provider-side prefix caching (Anthropic, OpenAI, Google cache_control headers) integrated via prompt packet metadata
- cross-session workspace cache sharing when repository state and policy are identical

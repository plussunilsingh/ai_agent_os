# 41 Cache Intelligence

## Purpose

Maximize context reuse and minimize token cost by maintaining a layered, content-addressed cache of static, semi-static, and compactable context segments. Cache Intelligence is a subsystem of the Context Compiler and Token Optimizer — it does not own source facts or validation decisions.

## Responsibilities

- maintain a three-layer context cache: system prefix, workspace, and history
- generate and validate deterministic cache keys from artifact IDs and source versions
- detect cache divergence and invalidate stale entries proactively
- trigger history compaction when the dynamic context budget is exhausted
- report cache hit rate, token savings, and divergence events to Telemetry
- enforce cache policy (TTL, eviction, maximum cache size, sensitivity)

## Cache Layers

### Layer 1 — System Prefix Cache (Static)

Content: system role, model identity, OS version, active tool list, active policy references.

Properties:
- deterministic: format is fixed and sorted; same inputs always produce same bytes
- cache key: `hash(system_prompt_text + model_id + tool_list_sorted + policy_version)`
- TTL: until system configuration changes; no time-based expiry
- token budget: 2 000 tokens (reserved, not part of dynamic budget)
- invalidation trigger: model change, tool list change, policy version bump

### Layer 2 — Workspace Context Cache (Semi-Static)

Content: task-specific Repository DNA slice, relevant module graph edges, architecture intent and decision records, dependency contracts, API signatures.

Properties:
- cache key: `hash(dna_slice_hash + module_ids_sorted + policy_decision_id)`
- TTL: until any source artifact in the slice changes (content-addressed, not time-based)
- token budget: 3 000 tokens (reserved)
- invalidation trigger: incremental scanner detects file hash change in any included module
- must not include raw file content unless a small-file exception is recorded

### Layer 3 — Compacted History Cache (Compactable)

Content: structured summary of prior task decisions, ADR references, outcomes, and open blockers for the current session.

Properties:
- cache key: `hash(session_id + compaction_sequence_number)`
- TTL: session lifetime; expires on session close
- token budget: 2 000 tokens (reserved)
- compaction trigger: history exceeds 80 % of remaining context window
- compaction output format: timeline entries, decisions, outcomes, current state, next steps (see Compaction Format below)

### Dynamic Window (Uncached)

Content: current task delta — new file edits, new tokens, incremental requirement changes, current validation failure details.

Properties:
- never cached as a unit; each request appends fresh dynamic content after the cached prefix
- token budget: 3 500 tokens (target); overflow triggers task split or compaction
- buffer reserve: 1 000 tokens

Total default budget: 11 500 tokens.

## Compaction Format

When history compaction is triggered, the compiler produces a structured summary and assigns it a new cache key.

```
--- COMPACTED HISTORY [seq=N session=S] ---
Timeline:
  - [task_id] short outcome summary
Decisions:
  - [ADR-NNN] decision statement (one line)
Current State:
  files_changed: [list]
  validation_status: passed|failed|pending
  open_blockers: [list or none]
Next Steps:
  - [task_id or description]
---
```

The compacted summary replaces raw history in the prompt. Raw history is retained in `.ai_os_runtime/cache/history/` for audit; it is never re-injected into prompts.

## Cache Key Rules

- All keys are deterministic: sort all list inputs before hashing.
- Use SHA-256 of the canonical UTF-8 byte representation.
- Keys must be namespaced: `{layer}:{repo_id}:{workspace_id}:{content_hash}`.
- A cache key collision is treated as a cache miss and triggers a full rebuild.

## Divergence Detection

Divergence occurs when a cache entry is served but its source artifacts have been modified since the entry was written.

Detection:
- compare stored source_version_hash fields against current artifact hashes at compile time
- if any hash differs: invalidate the entry, log a divergence event, rebuild from source

Alert threshold: more than 5 divergence events per hour triggers a Telemetry alert.

## Cache Miss Budget

If the cache hit rate falls below 70 % over a rolling 1-hour window:
- Telemetry raises a `cache_hit_rate_low` alert
- Cache Intelligence logs the top three divergence causes
- The system does not degrade; it operates correctly on cache miss but at higher token cost

## Eviction Policy

- System prefix: evict only on invalidation (no LRU)
- Workspace: LRU eviction when cache exceeds 500 entries per repository
- History: automatic expiry on session close
- Eviction events are logged as telemetry events

## Interfaces

- context pack: `schemas/context_cache.schema.json`
- cache metrics: `schemas/cache_metrics.schema.json`
- telemetry events: `schemas/telemetry_event.schema.json`
- divergence event type: `cache_divergence_detected`
- alert event types: `cache_hit_rate_low`, `cache_eviction_budget_exceeded`

## Acceptance Criteria

- Every cached entry has: layer, cache key, source version hashes, sensitivity class, token count, created timestamp, and TTL or invalidation condition.
- A cache miss never causes incorrect context — it produces a full rebuild from source.
- Divergence detection runs on every cache hit before the entry is used.
- Cache metrics (hit rate, token savings, divergence count) are queryable from Telemetry.
- No sensitive content is cached without the originating policy decision's data scope.

## Future Extensions

- semantic similarity cache backed by embedding verification (hash must match; embedding is secondary ranking signal only)
- cross-session workspace cache sharing when repository state and policy are identical
- provider-side prefix caching integration (Anthropic, OpenAI, Google) via cache_control headers in prompt packets

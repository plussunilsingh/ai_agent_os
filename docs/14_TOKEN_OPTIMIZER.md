# 14 Token Optimizer

## Purpose

Minimize token usage while preserving enough context for correctness.

## Responsibilities

- define and enforce token budgets per OS mode
- estimate token costs before prompt compilation
- select raw versus summarized context
- direct Cache Intelligence to serve or invalidate cached layers
- trigger history compaction when dynamic budget is exhausted
- report token savings from cache hits and compaction to Telemetry
- track savings and quality impact over time

## Inputs

- task risk
- context candidates
- model limits
- historical success data
- token policy

## Outputs

- token budget
- packing plan
- compression decisions
- budget telemetry

## Strategies (Priority Order)

1. **Cache first**: serve Layer 1 (system prefix), Layer 2 (workspace), Layer 3 (compacted history) from Cache Intelligence before building anything new. A cache hit is the cheapest possible token.
2. **Provider-side prefix caching**: when routing to Anthropic, OpenAI, or Google models, include `cache_control` metadata in the prompt packet to enable server-side prefix caching. Combine with local Cache Intelligence for maximum savings.
3. **Symbol-first selection**: use graph facts, symbols, signatures, DTOs, API contracts, SQL fragments, and tests before raw code.
4. **Summary for indirect dependencies**: include summaries for modules not directly in scope.
5. **Citations over excerpts**: use artifact IDs and provenance references instead of long code blocks.
6. **Compaction**: when history exceeds 80 % of remaining context window, trigger compaction via Cache Intelligence before appending new tokens.
7. **Task split**: when the required context after all compression is still over budget, split the task at the module or layer boundary.
8. **Reuse only source-version-valid content-addressed slices**: never reuse a cached entry after its source hashes have changed.

## Interfaces

- cache metrics: `schemas/cache_metrics.schema.json`
- cache operations: `41_CACHE_INTELLIGENCE.md`
- token policy: `policies/cache_policy.md`

## Acceptance Criteria

- Every prompt packet has a token estimate before compilation.
- Budget overruns trigger compaction, then compression, then task split — in that order.
- The OS can report token spend, cache hit rate, and token savings per task and subsystem.
- Context reuse is measured without reusing stale prompts or broad repository snapshots.
- Provider-side prefix caching metadata is included in prompt packets when the model and provider support it.

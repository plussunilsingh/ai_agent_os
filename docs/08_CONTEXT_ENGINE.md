# 08 Context Engine

## Purpose

Build minimal, ranked context packs for each task. `28_CONTEXT_COMPILER.md` is the authoritative v3 compilation contract.

## Responsibilities

- retrieve task-specific DNA slices, symbols, interfaces, tests, policies, and scoped memory
- rank context by usefulness
- compress safely
- enforce token budgets
- cache reusable packs

## Inputs

- task record
- requirement brief
- knowledge graph query results
- memory records
- token policy

## Outputs

- context pack
- omitted-context report
- token estimate
- provenance list

## Interfaces

- emits `schemas/context_pack.schema.json`
- follows `policies/token_policy.md`
- feeds Prompt Compiler

## Ranking Signals

- direct symbol/interface target
- direct symbol reference
- reverse dependency distance
- test coverage relation
- recent failure relation
- architecture ownership
- recency of change
- confidence of indexed summary

## Internal Algorithms

1. Select mandatory context: task, acceptance, DNA/intent slice, target symbols, and policies.
2. Query graph for dependencies and tests.
3. Add memory snippets with confidence thresholds.
4. Rank and fit within token budget.
5. Compress lower-ranked context into summaries.
6. Emit omitted items with reasons.

## Error Handling

- budget exceeded: preserve mandatory constraints, compress lower-ranked evidence, then ask for split task
- stale context: trigger re-index
- missing file: mark blocker

## Acceptance Criteria

- Every context item has reason, provenance, source version, sensitivity, and token estimate.
- Full-file inclusion requires a recorded small-file exception.
- Context pack fits declared budget.
- Omitted relevant items are recorded.
- High-risk tasks include validation and security context.

# 05 Memory Engine

## Purpose

Persist concise, versioned engineering summaries across tasks without turning memory into an unbounded prompt dump or confusing narrative memory with graph facts.

## Responsibilities

- store summaries, decisions, patterns, pitfalls, and session compression; scanner-derived repository facts remain Repository Intelligence artifacts
- separate durable memory from temporary task context
- update memory after validated outcomes
- age out stale or contradicted facts

## Inputs

- completed task records
- validation reports
- recovery reports
- architecture decisions
- repository summaries

## Outputs

- memory snippets
- decision records
- failure playbooks
- project conventions
- stale memory alerts

## Memory Types

- Durable fact: a concise summary that references authoritative source artifacts.
- Decision: chosen approach and rationale.
- Pattern: repeated implementation style.
- Failure: problem, cause, fix, prevention.
- Session summary: task-local compressed history.

## Interfaces

- uses `schemas/memory_record.schema.json` with hash, version, timestamp, dependencies, TTL, and supersession metadata
- feeds Context Engine ranking
- receives updates from Learning Engine

## Internal Algorithms

1. Classify candidate memory.
2. Deduplicate against existing records.
3. Attach provenance and validation evidence.
4. Assign hash, version, freshness, confidence, dependency lineage, and expiry.
5. Expose only task-relevant memory to context packs.

## Error Handling

- unvalidated memory: store as tentative
- contradictory memory: mark conflict and require resolution
- outdated memory: suppress from prompts unless explicitly requested

## Token Strategy

Prefer dense, structured memory records under 200 words. Large session logs must be summarized before storage.

## Acceptance Criteria

- Memory records include type, hash, version, confidence, provenance, dependencies, and freshness.
- Failed attempts become reusable recovery knowledge.
- Stale memory is not silently injected into prompts.

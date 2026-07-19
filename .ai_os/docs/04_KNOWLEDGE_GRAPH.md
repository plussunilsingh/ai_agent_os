# 04 Knowledge Graph

## Purpose

Represent authoritative artifacts as queryable, rebuildable graph projections. The graph is not a source of truth and never invents facts.

## Responsibilities

- project modules, files, symbols, APIs, DB objects, tests, tasks, requirements, decisions, validation, and failures from source artifacts
- maintain derived edges with source lineage
- support impact queries
- preserve provenance and freshness

## Inputs

- repository index and DNA artifacts
- requirement, task, execution, validation, failure, release, and incident artifacts
- approved decision/memory artifacts only when their producer owns the fact
- audit records used for lifecycle projections

## Outputs

- graph query results with source artifact IDs and source versions
- affected entity sets
- dependency paths
- stale knowledge reports

## Interfaces

- consumes source records and derives `schemas/graph_node.schema.json` and `schemas/graph_edge.schema.json`
- links tasks from `schemas/task.schema.json` without changing task ownership
- supports context selection in `08_CONTEXT_ENGINE.md`

## Entity Types

- Repository
- Module
- File
- Symbol
- API
- DatabaseObject
- Test
- Requirement
- Task
- Decision
- Failure
- Release

## Edge Types

- imports
- exports
- calls
- owns
- tests
- implements
- depends_on
- affects
- validates
- supersedes
- failed_due_to

## Internal Algorithms

- derive entities by stable IDs, source artifact IDs, and source versions
- invalidate derived nodes and edges when source hash or artifact version changes
- retain projection lineage rather than overwriting source facts
- answer impact queries using reverse dependency traversal with depth limits
- rank graph results by distance, recency, confidence, and validation relevance

## Error Handling

- conflicting source artifacts: preserve versions, mark conflict in the projection, and request owner resolution
- stale source hash: mark the projection stale and reject it for high-risk prompts until re-indexed
- missing provenance: do not use for high-risk prompts

## Acceptance Criteria

- Every graph node and edge has source artifact provenance and is rebuildable.
- Impact analysis can trace from requirement to affected files and tests.
- Stale graph facts are detectable.
- Graph can answer "what tests validate this module?"

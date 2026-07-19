# 23 Runtime Model

## Purpose

Define the persistence and lifecycle model for AI-SE OS without prematurely requiring distributed event sourcing.

## Maturity Model

1. Level 1 - Ideas and notes.
2. Level 2 - Architecture specification.
3. Level 3 - Executable runtime specification: schemas, policies, runtime layout, and deterministic contracts exist.
4. Level 4 - Working MVP runtime: scanner, context/prompt compiler, scheduler, router, executor, and validator run locally.
5. Level 5 - Production-grade OS: multi-workspace operation, CI/CD integration, observability, enterprise policy, and measured reliability.

AI-SE OS v3 is Level 3. No document may imply that it is already a Level 4 or Level 5 system.

## Persistence Progression

1. JSON runtime artifacts under `.ai_os_runtime/`.
2. Append-only audit records for important lifecycle transitions.
3. Immutable execution history and content-addressed artifacts.
4. Derived indexes and graph projections rebuilt from artifacts when needed.
5. Optional event-store or database backend without changing artifact contracts.
6. Optional full event sourcing only when replay, scale, or integration needs justify it.

## Runtime Rules

- An artifact is immutable once published. A correction creates a new artifact with `supersedes` lineage.
- An audit event records an action that occurred. It is not a replacement for every domain object.
- Projections are disposable derived views. They can be rebuilt from authoritative artifacts and audit records.
- The runtime accepts only schema-valid, policy-authorized artifacts.
- Every artifact and event carries repository identity, correlation ID, producer, timestamp, schema version, and provenance.
- The MVP uses atomic write-then-rename for local artifact publication. Writers must never expose partially written JSON.

## Event Families

- requirement: `requirement.created`, `requirement.analyzed`, `requirement.blocked`
- repository: `repository.indexed`, `repository.dna.updated`
- planning: `task.created`, `task.queued`, `task.leased`, `task.completed`
- context and prompt: `context.compiled`, `prompt.compiled`, `route.decided`
- execution: `execution.started`, `execution.completed`, `execution.failed`
- validation: `validation.started`, `validation.completed`
- recovery: `failure.fingerprinted`, `recovery.planned`, `rollback.requested`
- governance: `policy.decided`, `policy.denied`, `human.escalated`
- learning: `knowledge.promoted`, `projection.refreshed`, `benchmark.recorded`

## Confidence Propagation

Each inferred artifact declares a `confidence` value from 0 to 1 and a basis. The runtime preserves upstream confidence values instead of fabricating certainty. A downstream component calculates its confidence from its own evidence, source freshness, deterministic-parser reliability, and relevant upstream confidence. It must retain the contributing artifact IDs.

Confidence controls autonomy according to policy: low confidence can require a re-index, more context, stronger model, independent critique, or human escalation. Validation evidence is always recorded separately; a high confidence value cannot satisfy a validation gate.

## Error Handling

- schema mismatch: reject the artifact and record a governance event
- duplicate idempotency key: return the existing result rather than re-run the action
- projection failure: mark projection stale and rebuild from authoritative artifacts
- corrupt audit record: quarantine the record, preserve bytes for diagnosis, and block dependent high-risk work

## Acceptance Criteria

- A local runtime can persist and replay artifact history without a database.
- Every projection can identify its source artifacts and source versions.
- A failed process cannot leave a partial published artifact.
- Event sourcing remains an implementation option, not an implicit dependency.

## Future Extensions

- SQLite or DuckDB projection store
- encrypted event archives
- distributed event store
- replay debugger and time-travel inspection

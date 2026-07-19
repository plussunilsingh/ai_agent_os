# 34 Continuous Repository Evolution

## Purpose

Refresh repository knowledge only from trustworthy change evidence so the OS becomes more useful over time without accumulating unverified folklore.

## Triggers

- accepted merge or verified commit
- validated task completion
- approved architecture decision
- resolved incident or postmortem
- dependency, CI, security, or deployment change
- explicit human correction of a prior record

## Update Flow

1. Detect source change and incremental index impact.
2. Publish new repository index/DNA artifacts for the affected revision.
3. Rebuild only invalidated graph projections.
4. Evaluate proposed memory, pattern, decision, and benchmark updates.
5. Promote only artifacts with source provenance and sufficient validation evidence.
6. Supersede or expire contradictory records; do not overwrite history.
7. Emit audit and telemetry records with redacted metadata.

## Promotion Rules

- code facts come from Repository Intelligence or verified source-control evidence
- decisions require an approved ADR, task evidence, or named human owner
- patterns require repeated validated examples or explicit human curation
- failures remain tentative until cause and prevention have evidence
- model performance updates require comparable benchmark/task taxonomy metadata

## Interfaces

- learning record: `schemas/learning_record.schema.json`
- memory record: `schemas/memory_record.schema.json`
- Repository DNA and repository index schemas

## Acceptance Criteria

- A merge updates only the affected index, DNA, projections, and cache entries.
- The OS can explain why a memory or pattern was promoted.
- A correction supersedes prior knowledge without deleting lineage.

## Future Extensions

- pull-request and CI event adapters
- automated ADR candidate generation
- drift detection for conventions and architecture

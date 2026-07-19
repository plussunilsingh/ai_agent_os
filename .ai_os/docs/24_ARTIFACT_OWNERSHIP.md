# 24 Artifact Ownership

## Purpose

Define who may publish each durable artifact, who may consume it, and whether a new version or an append-only record is required for changes.

## Ownership Table

| Artifact | Authoritative producer | Consumers | Lifecycle |
| --- | --- | --- | --- |
| Repository index and module record | Repository Intelligence | Knowledge, impact, context | immutable per source hash |
| Repository DNA | Repository Intelligence | Context Compiler, Engineering Governance | versioned per repository snapshot |
| Graph node and edge | Projection Builder | query consumers | derived and rebuildable |
| Requirement brief | Requirement Analyzer | Engineering Intelligence, Planner | immutable revision |
| Task DAG and task | Task Planner | Scheduler, Context Compiler, Validation | versioned plan; task state via events |
| Scheduler lease | Scheduler | Agent Manager, Execution | mutable only by Scheduler, TTL-bound |
| Context pack | Context Compiler | Prompt Compiler, Execution | immutable per task and source set |
| Prompt packet | Prompt Compiler | Model Router, Execution | immutable per context and policy decision |
| Routing decision | Model Router | Execution | immutable per routing request |
| Execution record | Execution Engine | Validation, Recovery, Learning | append-only attempt history |
| Validation report | Validation Intelligence | Recovery, Learning, Release | immutable per validation run |
| Failure record | Recovery Engine | Scheduler, Learning, Context | append-only; superseding diagnosis allowed |
| Policy decision | Policy Engine | PEP, all protected operations | immutable and expiry-bound |
| Learning record | Learning Engine | Memory, Knowledge projections | append-only after evidence review |
| Telemetry event | Observability | dashboards and benchmarks | append-only, redacted |

## Rules

- A consumer may never edit a producer's artifact in place.
- A graph is only a projection. It may index artifacts but cannot publish repository, task, validation, or policy facts.
- A corrected artifact references the prior artifact through `supersedes`; deleting history requires the retention and privacy process.
- Every artifact uses a stable ID, schema version, producer identity, repository scope, correlation ID, provenance, confidence, and published timestamp.
- An artifact that is human-authored or model-inferred declares its evidence basis. Deterministic extraction is also recorded as a producer.

## Interfaces

- Base artifact metadata: `schemas/artifact_envelope.schema.json`
- Audit history: `schemas/audit_event.schema.json`
- Runtime state and leases: `schemas/project_state.schema.json` and `schemas/scheduler_lease.schema.json`

## Acceptance Criteria

- Every persisted schema maps to one authoritative producer.
- No runtime component requires write access to a graph projection to perform its normal work.
- A reviewer can trace any completion claim to its requirement, task, execution, validation, policy, and source artifacts.

## Future Extensions

- artifact registry service
- signed producer identities
- retention labels and legal hold support

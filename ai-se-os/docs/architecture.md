# 01 Architecture

## Purpose

Define the layered architecture of AI-SE OS and the contracts between subsystems.

## System Layers

0. Governance: Constitution, Policy Engine, Permission Engine, Security Engine, and Engineering Governance.
1. Repository Intelligence: scanner, incremental indexer, repository fingerprint, and Repository DNA.
2. Knowledge System: source-backed graph projections, Project State, Architectural Intent, decisions, memory, and telemetry store.
3. Engineering Intelligence: requirement completeness, reasoning, dependency impact, architecture/risk analysis, and complexity estimation.
4. Planning and Model Intelligence: task DAGs, scheduler, deterministic context/prompt compilation, model registry, routing, and fallback.
5. Execution: Agent Manager, approved adapters, sandboxes, Git, terminal, browser, filesystem, Docker, and MCP tools.
6. Validation and Recovery: deterministic validation, independent critique, evidence evaluation, failure fingerprinting, retry, rollback, and escalation.
7. Learning and Evolution: validated knowledge updates, pattern learning, Repository DNA refresh, and benchmark history.
8. Observability: immutable audit records, metrics, dashboards, cost, latency, quality, and reliability reporting.

## Primary Flow

`RequirementCreated` -> Requirement Completeness -> Repository Intelligence -> Knowledge Query -> Engineering Reasoning and Impact -> Task DAG -> Scheduler Lease -> Context Compiler -> Prompt Compiler -> Policy Decision -> Model Router -> Execution -> Validation -> Recovery or Learning -> Audit and Projection Update.

Each transition appends an audit record. The runtime treats the audit record as the history of what happened; graphs, dashboards, and caches are derived projections. This does not require a distributed event store for the MVP.

## Interfaces

- Artifact producers and consumers are authoritative only as defined in `24_ARTIFACT_OWNERSHIP.md`.
- Runtime artifact lifecycle and audit requirements are defined in `23_RUNTIME_MODEL.md` and `36_RUNTIME_ARTIFACTS_AND_CLI.md`.
- Policy Decision Points (PDP) and Policy Enforcement Points (PEP) are defined in `25_POLICY_ENFORCEMENT.md`.
- All cross-subsystem records use `schemas/` and include a correlation ID, producer, provenance, and confidence when inferred.

## Internal Algorithms

- Prefer deterministic extraction before model inference.
- Use content hashes and commit/worktree identity for incremental indexing.
- Treat graphs as materialized views of authoritative artifacts; invalidate derived facts when their source version changes.
- Propagate confidence with provenance and freshness. Use low confidence to request context, re-index, select stronger reasoning, or escalate, never as proof of correctness.
- Decompose tasks until each task has bounded files, bounded context, lease requirements, rollback strategy, and clear validation.
- Route to the cheapest eligible model that satisfies policy, privacy, reasoning, and context needs.

## Error Handling

- classify failures as requirement, context, generation, execution, validation, permission, concurrency, or external dependency
- reject stale, schema-incompatible, or unauthorized artifacts before execution
- retry only when the failure class has a defined recovery path and a new failure fingerprint will be produced
- stop and escalate for destructive, security-sensitive, ambiguous production, or lease-conflict actions

## Token Strategy

- never send the full repository
- compile task-specific DNA and graph slices before selecting code
- prefer symbols, DTOs, tests, APIs, SQL, and structured summaries over full files
- include a full file only under a documented small-file exception
- include provenance, source version, freshness, and token cost for every context item

## Acceptance Criteria

- Every subsystem has explicit inputs, outputs, ownership, and error transitions.
- Every cross-subsystem contract points to a schema or policy.
- Every privileged action is evaluated by a PDP and enforced by a PEP.
- The architecture supports local and remote model execution, human-in-the-loop operation, and bounded autonomous modes.

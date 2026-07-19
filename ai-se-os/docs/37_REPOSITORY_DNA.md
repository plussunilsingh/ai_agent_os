# 37 Repository DNA

## Purpose

Provide a versioned, evidence-backed repository manifest that gives agents the minimum architectural orientation needed for a task.

## Contents

- architecture style, layers, entry points, and workspace topology
- languages, frameworks, build, package, test, and formatting tools
- module, API, database, ownership, technology, and validation relationships
- naming, coding, security, deployment, CI/CD, documentation, and ADR conventions
- known anti-patterns, deprecations, generated paths, and operating constraints

Every item has source artifacts, source revision/hash, confidence, freshness, and sensitivity class. DNA reports evidence and gaps; it does not claim unstated design intent.

## Production And Consumption

Repository Intelligence is the authoritative producer. Engineering Governance may attach approved conventions or ADR references, but cannot rewrite scanner-derived facts. The Context Compiler creates a task-specific DNA slice based on scope, impacted modules, risk, and policy.

No agent automatically receives the full DNA. For example, a UI task receives relevant frontend framework, style, test, route, API contract, and validation information, not unrelated payment, deployment, or customer-data details.

## Update Rules

- Rebuild per repository revision, with incremental sections reused only when their source hashes remain valid.
- A manual correction creates a superseding record with a named owner and evidence.
- Expire inferred conventions when evidence becomes stale or contradictory.

## Interfaces

- repository DNA: `schemas/repository_dna.schema.json`
- repository index: `schemas/repository_index.schema.json`
- task context: `28_CONTEXT_COMPILER.md`

## Acceptance Criteria

- A DNA artifact identifies its repository revision and evidence coverage.
- A task-specific slice is smaller and more relevant than the whole manifest.
- Agents can identify missing repository knowledge before attempting an unsupported change.

## Future Extensions

- monorepo DNA composition
- architecture drift alerts
- ownership-system adapters

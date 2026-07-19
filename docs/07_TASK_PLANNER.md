# 07 Task Planner

## Purpose

Decompose requirement briefs into bounded, dependency-aware micro-tasks.

## Responsibilities

- create versioned task DAGs; Scheduler owns runtime queue and lease state
- define task boundaries
- assign validation gates
- prevent oversized or vague implementation tasks
- sequence design, implementation, tests, and documentation

## Inputs

- requirement brief
- impact report
- architecture policies
- repository graph

## Outputs

- immutable task records and versioned task DAG
- scheduler-ready dependency metadata
- implementation order
- validation plan

## Interfaces

- emits `schemas/task.schema.json` and `schemas/task_dag.schema.json`
- hands ready tasks to `26_RUNTIME_STATE_AND_SCHEDULER.md`
- feeds Context Compiler
- receives validation results from Validation Engine

## Task Sizing Rules

- one task should modify a small, coherent file set protected by a lease
- one task should have one primary acceptance objective
- tasks must include validation evidence
- split tasks when they cross architectural layers unless the integration is the point

## Internal Algorithms

1. Convert acceptance criteria into deliverable slices.
2. Map each slice to affected modules and tests.
3. Identify dependencies and blockers.
4. Create a DAG with owner, risk, confidence, token/cost/retry budget, rollback, and validation metadata.
5. Mark tasks requiring policy or human review.

## Error Handling

- circular task dependency: merge or redefine boundaries
- task too broad: split by module, layer, or validation target
- missing validation route: add exploratory validation task first

## Token Strategy

Task descriptions must be compact. Put detailed source context in context packs, not task records.

## Acceptance Criteria

- Every task has ID, goal, inputs, outputs, files, dependencies, risks, and gates.
- The DAG can be scheduled one leased task attempt at a time.
- No implementation task lacks validation.

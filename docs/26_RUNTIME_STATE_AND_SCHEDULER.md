# 26 Runtime State And Scheduler

## Purpose

Coordinate concurrent agents and humans without treating branch, task, or modified-file state as globally unique.

## State Scope

Every runtime object is scoped by `repository_id`, `workspace_id`, `worktree_id`, `branch`, and `session_id`. A project state record distinguishes:

- durable repository facts: default branch, indexed commit, known architecture decisions
- ephemeral workspace facts: dirty files, active task, current validation run
- externally sourced facts: CI status, open pull request, release status

Each fact declares source, observed time, freshness/TTL, and confidence. The runtime never silently converts an ephemeral observation into durable project knowledge.

## Scheduler Responsibilities

- queue dependency-ready tasks
- acquire and renew file/module/resource leases
- assign one active owner per task attempt
- send heartbeats and recover expired leases
- enforce task retry, token, cost, and time budgets
- avoid conflicting work across agents and humans
- route terminal failures to recovery, rollback, or escalation

## Lease Rules

- A lease binds a task attempt, owner, resources, scope, expiry, and heartbeat interval.
- The Scheduler is the sole writer of lease records.
- A task may execute only while its lease is valid and owned by its execution attempt.
- A lease conflict pauses the task; it never overwrites the other actor's changes.
- Expiry marks work as orphaned, not failed. Reconciliation checks repository state before requeueing.

## State Machine

`planned -> queued -> leased -> executing -> validating -> validated | recovering | blocked | cancelled`.

`done` is a reporting state entered only after a validation report passes required gates. A validation failure transitions to `recovering`, `blocked`, or `cancelled`; it cannot transition directly to `done`.

## Error Handling

- duplicate queue request: use idempotency key and return existing task attempt
- missing heartbeat: reconcile source control and execution records before requeueing
- conflicting resource request: queue behind the existing lease or require a plan change
- stale state: refresh from source or block high-risk actions

## Acceptance Criteria

- Two agents cannot hold conflicting write leases simultaneously.
- A restarted scheduler can reconstruct active work from task, lease, execution, and audit artifacts.
- Human work is represented as an owner and receives the same protection from agent overwrites.

## Future Extensions

- distributed queue backend
- priority and fair-share scheduling
- CI worker and remote-agent adapters

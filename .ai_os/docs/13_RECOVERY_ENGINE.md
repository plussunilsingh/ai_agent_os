# 13 Recovery Engine

## Purpose

Recover from execution and validation failures using controlled, fingerprint-aware strategies. `33_RECOVERY_AND_FAILURES.md` is the authoritative v3 recovery contract.

## Responsibilities

- classify failures
- decide retry, re-plan, rollback, or escalate
- generate focused fix tasks
- preserve failure memory

## Inputs

- validation report
- execution record
- task record
- context pack
- memory records

## Outputs

- recovery plan, retry task, escalation report, and `schemas/failure_record.schema.json`

## Failure Classes

- requirement ambiguity
- insufficient context
- incorrect code generation
- integration breakage
- test failure
- environment/tooling failure
- permission failure
- security violation

## Internal Algorithms

1. Classify the failure and create a redacted fingerprint.
2. Determine material sameness against prior failed attempts.
3. Require a material context, plan, model, tool, environment, or repository change before retry.
4. Generate a focused recovery task, rollback plan, diagnostic task, or escalation.
5. Limit retries by task and policy budget.
6. Record hypotheses separately from confirmed causes.

## Error Handling

- repeated same fingerprint without material change: stop and escalate
- destructive recovery needed: require human approval
- uncertain root cause: create diagnostic task

## Acceptance Criteria

- Recovery never loops indefinitely.
- Every failed attempt is classified.
- Retry prompts include only failure-relevant context.

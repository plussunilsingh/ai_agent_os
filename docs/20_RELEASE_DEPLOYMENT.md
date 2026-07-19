# 20 Release And Deployment

## Purpose

Prepare validated changes for release and deployment handoff without assuming the coding agent owns production.

## Responsibilities

- create release readiness checks
- summarize changes and risks
- verify migration and configuration requirements
- produce rollback and verification plans
- generate human-readable handoff notes

## Inputs

- completed task records
- validation reports
- changed files
- security findings
- migration records
- deployment environment metadata

## Outputs

- immutable release readiness report using `schemas/release_readiness.schema.json`
- deployment checklist
- rollback plan
- smoke test plan
- change log draft

## Interfaces

- consumes `schemas/task.schema.json`
- consumes `schemas/validation_report.schema.json`
- emits telemetry through `schemas/telemetry_event.schema.json`
- requires a valid policy decision and named human approver for deployment handoff
- follows `policies/security_policy.md` and `policies/validation_policy.md`

## Release Gates

- all required validation gates passed or explicitly waived
- security-sensitive changes reviewed
- migrations identified and ordered
- environment variables documented
- rollback path exists
- smoke tests are listed
- user-facing behavior changes are summarized

## Internal Algorithms

1. Gather completed tasks for the release candidate.
2. Group changes by module, risk, and user impact.
3. Detect migrations, config changes, dependency changes, and operational changes.
4. Verify validation evidence against policy.
5. Generate deployment and rollback checklists.
6. Mark unresolved risks as release blockers or accepted residual risk.

## Error Handling

- missing validation evidence: block release readiness
- unknown migration order: create release blocker
- no rollback path for high-risk change: require human approval
- environment-specific uncertainty: require deployment owner confirmation

## Token Strategy

Use structured task and validation records instead of raw diffs unless a human release note requires exact changed behavior.

## Acceptance Criteria

- A release candidate has a clear ready/block/conditional status, source revision, validation lineage, policy decision, and rollback plan.
- Deployment handoff lists config, migration, smoke, and rollback requirements.
- Residual risk is explicit and traceable.

## Future Extensions

- CI/CD integration
- automatic release note generation from PRs
- environment drift detection
- canary analysis integration

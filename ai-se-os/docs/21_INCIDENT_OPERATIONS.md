# 21 Incident And Operations

## Purpose

Support post-release operations, incident analysis, remediation planning, and learning.

## Responsibilities

- classify incidents and operational issues
- connect symptoms to recent changes and affected modules
- plan diagnostics and remediation tasks
- define rollback or mitigation options
- update memory with postmortem learnings

## Inputs

- incident report
- logs and metrics summaries
- recent release records
- repository knowledge graph
- validation history
- user impact statements

## Outputs

- incident brief
- suspected cause map
- diagnostic task list
- mitigation plan
- remediation task plan
- postmortem memory updates
- append-only incident/recovery audit records with redacted evidence references

## Interfaces

- queries Knowledge Graph for recent changes and dependencies
- uses Recovery Engine for fix planning
- uses Release And Deployment for rollback handoff
- sends learning candidates to Memory Engine
- uses `33_RECOVERY_AND_FAILURES.md` for fingerprint-aware remediation planning

## Incident Classes

- availability
- performance
- data correctness
- security
- migration
- integration
- regression
- operational configuration

## Internal Algorithms

1. Normalize symptoms, time window, impact, and severity.
2. Correlate incident timing with releases and config changes.
3. Query graph for affected modules and reverse dependencies.
4. Create diagnostic tasks before broad code changes.
5. Propose mitigation, rollback, or forward-fix options.
6. Validate remediation with targeted and regression checks.
7. Capture postmortem facts and prevention rules.

## Error Handling

- incomplete incident data: create diagnostic questions and safe checks
- suspected security incident: stop normal workflow and follow security policy
- destructive mitigation: require human approval
- unclear root cause: avoid speculative code edits

## Token Strategy

Use summarized logs and metrics with timestamps. Do not place sensitive logs, secrets, or customer data into prompts.

## Acceptance Criteria

- Incident work starts with a severity and impact statement.
- Diagnostic tasks precede uncertain remediation.
- Remediation includes validation and rollback consideration.
- Postmortem learnings update memory after verification.

## Future Extensions

- observability provider plugins
- automatic release correlation
- incident timeline generation
- SLO-aware prioritization

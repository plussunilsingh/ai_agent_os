# 12 Validation Engine

## Purpose

Prove that a task is complete through deterministic evidence. `32_VALIDATION_INTELLIGENCE.md` is the authoritative v3 evidence and policy-matrix contract.

## Responsibilities

- run policy-selected formatting, type, build, static, test, architecture, migration, performance, security, and acceptance checks
- map validation evidence to acceptance criteria
- block completion when required gates fail

## Inputs

- task record
- changed files
- validation plan
- repository scripts
- policy requirements

## Outputs

- validation report
- pass/fail gate status
- failure classification
- residual risk

## Interfaces

- emits `schemas/validation_report.schema.json`
- sends failures to Recovery Engine
- sends successes to Learning Engine

## Gate Types

- build
- unit test
- integration test
- UI smoke
- static analysis
- type check
- security scan
- architecture conformance
- documentation check
- release readiness

## Internal Algorithms

1. Select required, optional, and prohibited checks from the validation policy matrix.
2. Run low-cost checks early and all required later checks before completion.
3. Capture source revision, environment, baseline relation, and raw evidence location.
4. Parse outputs into structured failures.
5. Map evidence and residual risk to acceptance criteria.

## Error Handling

- missing test command: record gap and use alternate evidence
- flaky test: rerun within configured limit and classify
- failing unrelated test: record separately with evidence

## Acceptance Criteria

- Completion requires validation evidence; model critique alone is advisory.
- Failed gates include command, output summary, and suspected owner.
- Residual risk is explicit.

# 32 Validation Intelligence

## Purpose

Produce deterministic, risk-appropriate evidence that a task satisfies its acceptance criteria, while keeping advisory model critique distinct from proof.

## Validation Policy Matrix

The Validation Planner maps task type, changed paths, risk, data sensitivity, and release impact to required, optional, and prohibited gates. It records unavailable gates and residual risk; it never silently skips a required gate.

Default gate order when applicable:

1. formatting
2. type check
3. compilation/build
4. static analysis
5. unit tests
6. integration tests
7. API tests
8. UI/end-to-end tests
9. architecture conformance
10. migration and data checks
11. regression/performance checks
12. security checks
13. acceptance evidence review

Risk policy may run low-cost checks first, but it may not omit a mandatory later gate merely because an early check passes.

## Evidence Model

Each gate records command/tool version, source revision, environment identity, start/end time, status, raw-output location, structured summary, baseline relation, and owner. A pass proves only the claim the gate actually tests.

The system distinguishes:

- new failure: plausibly caused by the task
- baseline failure: present before the task under comparable conditions
- flaky result: inconsistent repeated outcome under the configured rule
- unavailable evidence: gate cannot run and produces residual risk

## Self-Critic And Independent Critic

Self-Critic checks requirement coverage, unsupported claims, policy/architecture mismatch, edge cases, and regression risk. It is advisory evidence only.

An Independent Critic uses a separate model, prompt, or deterministic analysis path where policy requires it. Different model names alone are not proof of independence; the record declares the independence basis. Neither critic can override a failed deterministic gate or mark work complete without validation evidence.

## Error Handling

- missing command: record capability gap and escalate residual risk according to the policy matrix
- flaky test: rerun only within the configured limit and preserve every attempt
- unrelated baseline failure: attach comparative evidence and continue only if policy permits
- incompatible environment: block high-risk completion and create a diagnostic task

## Acceptance Criteria

- Every completed task maps acceptance criteria to evidence or explicit residual risk.
- Required gates cannot be bypassed by a model assertion.
- Validation reports are reproducible enough to distinguish task failures from pre-existing failures.

## Future Extensions

- hermetic CI environments
- mutation testing and contract testing
- evidence attestation

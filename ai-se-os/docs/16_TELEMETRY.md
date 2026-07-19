# 16 Telemetry

## Purpose

Measure engineering throughput, quality, cost, reliability, and governance outcomes. `35_ENGINEERING_BENCHMARKS.md` defines the authoritative metric methodology.

## Responsibilities

- record task lifecycle events
- track token usage and model cost
- track validation outcomes
- expose bottlenecks, repeated failure modes, policy outcomes, and benchmark evidence

## Inputs

- model routing decisions
- execution records
- validation reports
- recovery events
- learning updates

## Outputs

- redacted append-only telemetry events and benchmark metric records
- cost reports
- quality dashboards
- reliability metrics

## Metrics

- requirement-to-plan time
- plan-to-code time
- validation pass rate
- retry count
- token spend
- cost per accepted task
- context pack size
- model success rate by task type
- escaped defect count
- policy denial and unauthorized-action count
- context stale-use rate

## Interfaces

- emits `schemas/telemetry_event.schema.json`

## Acceptance Criteria

- Every task has redacted lifecycle telemetry with repository, correlation, and metric-category scope.
- Dashboard targets must reference metric numerator, denominator, source, and sample size.
- Token and validation metrics are queryable.
- Telemetry does not include secrets or sensitive source text.

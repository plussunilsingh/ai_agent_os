# 35 Engineering Benchmarks

## Purpose

Measure whether AI-SE OS improves engineering outcomes, rather than assigning ungrounded maturity scores or universal percentage targets.

## Benchmark Design

Each benchmark defines a task taxonomy, repository revision, input requirement, permitted tools/models, privacy class, budget, baseline method, acceptance oracle, evaluator, repetitions, and data-retention rules. Compare similar task classes, not unrelated tasks.

## Core Metrics

- planning completeness and human correction rate
- context relevance, reduction, cache reuse, and stale-context incidents
- token, provider, tool, and total cost per accepted task
- latency by lifecycle phase
- first-pass and final validation pass rate
- task completion, rollback, escalation, and duplicate-fingerprint rate
- regression and escaped-defect rate after merge
- policy-denial, secret-redaction, and unauthorized-action rate
- model reliability by comparable task type and evidence coverage

## Metric Rules

- Define every numerator, denominator, source, time window, sample size, and exclusion rule.
- "Hallucination" must be operationalized, for example unsupported implementation claim or failed grounded assertion, not guessed from prose quality.
- Cache-hit metrics count only source-version-valid slices.
- A duplicate failure is actionable only when plan, context, model/tool path, and repository state are materially the same.
- Targets start as baselines and are calibrated by repository and task class. They are not universal promises.

## Readiness Gates

Level 4 requires a repeatable local benchmark suite with evidence for scanner accuracy, context reproducibility, policy enforcement, scheduler collision prevention, validation reporting, and recovery deduplication.

Level 5 requires longitudinal quality, security, cost, and operational reliability evidence in the intended environment.

## Interfaces

- metric record: `schemas/benchmark_metric.schema.json`
- telemetry event: `schemas/telemetry_event.schema.json`
- model registry and routing decision schemas

## Acceptance Criteria

- No dashboard metric exists without a documented definition and source.
- Benchmark claims are reproducible from retained redacted artifacts.
- Maturity is assessed by evidence, not a subjective score alone.

## Future Extensions

- benchmark corpus management
- statistical confidence intervals
- cross-model and cross-provider evaluation

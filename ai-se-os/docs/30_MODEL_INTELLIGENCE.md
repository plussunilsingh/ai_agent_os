# 30 Model Intelligence

## Purpose

Select an eligible model and fallback strategy based on capability, policy, cost, reliability, and task evidence.

## Components

- Model Registry: provider, model, capabilities, context limits, data handling, availability, and version metadata.
- Capability Registry: tool use, coding, reasoning, vision, structured output, local execution, and privacy features.
- Cost Engine: forecast and enforce input/output token, tool, latency, and retry budgets.
- Routing Engine: select the cheapest eligible model and execution path.
- Fallback Engine: choose a materially different eligible fallback after failures.

## Routing Rules

- Policy and privacy eligibility are evaluated before cost or quality.
- Choose by task type, complexity, context size, required tool use, historical performance, uncertainty, latency target, and remaining budget.
- Reliability is scoped to comparable tasks and measured over a minimum sample size. Unknown performance is not treated as high reliability.
- A fallback must differ in model, prompt/context, tool path, or plan; it may not repeat an identical failure fingerprint.
- Hallucination risk is a decision signal derived from unsupported claims, low evidence coverage, and historical results. It is not a precise universal percentage.

## Interfaces

- model registry: `schemas/model_registry.schema.json`
- routing decision: `schemas/routing_decision.schema.json`
- policy decision: `schemas/policy_decision.schema.json`
- benchmark data: `schemas/benchmark_metric.schema.json`

## Acceptance Criteria

- Each routed call has a written eligibility, cost, and fallback rationale.
- The router cannot select a provider prohibited by policy.
- Routing records include versioned model identity and budget consumption.

## Future Extensions

- provider health probes
- portfolio optimization
- offline calibration from benchmark suites

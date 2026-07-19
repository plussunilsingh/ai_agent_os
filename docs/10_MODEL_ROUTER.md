# 10 Model Router

## Purpose

Select the cheapest eligible model and execution path for each task. `30_MODEL_INTELLIGENCE.md` is the authoritative v3 routing contract.

## Responsibilities

- match task requirements to model capabilities
- enforce budget and privacy constraints
- choose fallback models
- record cost, latency, and quality signals

## Inputs

- task record
- context pack token count
- risk rating
- policy decision, model registry, routing policy, and benchmark data

## Outputs

- immutable routing decision using `schemas/routing_decision.schema.json`
- model call budget
- fallback chain
- telemetry event

## Interfaces

- follows `policies/model_routing_policy.md`
- emits telemetry using `schemas/telemetry_event.schema.json`
- sends decisions to Execution Engine

## Routing Factors

- reasoning complexity
- context window requirement
- code generation capability
- tool-use requirement
- privacy classification
- latency target
- cost ceiling
- historical success for similar task type
- versioned model reliability and hallucination-risk signal

## Error Handling

- no eligible model: split task, compress context, or ask for human decision
- model unavailable: use fallback chain
- budget exceeded: downgrade or pause based on policy

## Acceptance Criteria

- Every model call has an explicit eligibility, routing, cost, and fallback reason.
- High-risk tasks cannot be routed to unapproved models.
- Cost and latency are recorded.

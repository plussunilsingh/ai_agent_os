# 27 Engineering Intelligence

## Purpose

Make planning decisions from structured repository evidence rather than a model's unaided interpretation of a request.

## Components

- Requirement Completeness Analyzer: finds missing outcomes, constraints, actors, data, security, migration, rollout, and acceptance criteria.
- Engineering Reasoning Engine: compares implementation options against repository conventions and explicit architectural intent.
- Dependency Impact Engine: traces direct and reverse dependencies from intended change to symbols, APIs, databases, tests, and releases.
- Architecture and Risk Analyzer: evaluates layer boundaries, ownership, compatibility, security, operational, and regression risk.
- Complexity Analyzer: estimates file breadth, integration depth, unknowns, validation cost, and token budget.

## Inputs

- requirement brief and raw request reference
- Repository DNA slice, graph projections, intent/decision records, project state, and policy requirements
- relevant historical validation and failure records

## Outputs

- completeness report and targeted questions when required
- impact report with source paths and confidence
- option analysis with trade-offs and architectural constraints
- risk/complexity assessment
- planning handoff with evidence and unresolved uncertainty

## Interfaces

- assessment record: `schemas/engineering_assessment.schema.json`
- architectural intent: `schemas/architectural_intent.schema.json`
- approved decision: `schemas/design_decision.schema.json`

## Reasoning Rules

- Evidence beats inference. A claim without source artifacts is tagged as an assumption.
- Architectural Intent and ADR-backed decisions are higher priority than inferred style patterns.
- Analysis proposes alternatives; Planning chooses a bounded plan; Governance decides whether the chosen plan is allowed.
- Low confidence in a high-risk dependency requires re-indexing, targeted discovery, or human review before execution.
- Dependency traversal has depth and confidence limits to avoid unrelated context expansion.

## Confidence Model

Record confidence for each conclusion with an evidence basis such as parser coverage, source freshness, graph path length, direct test relation, and independent corroboration. Do not multiply arbitrary confidence values. The implementation must document its aggregation rule and preserve contributing artifact IDs.

## Error Handling

- incomplete requirement: emit targeted questions or a discovery task, never invent product behavior
- contradictory intent/decision records: block architectural change until ownership resolves the conflict
- stale graph or DNA: request incremental indexing
- broad impact: split the requirement or require a human planning boundary

## Acceptance Criteria

- Every plan handoff identifies facts, assumptions, uncertainty, impact, risk, and confidence.
- A planner can explain why each target module and validation gate was selected.
- Architectural intent can veto a seemingly convenient but contradictory implementation approach.

## Future Extensions

- code-change simulation
- change-risk prediction calibrated from repository history
- requirement-to-ADR traceability

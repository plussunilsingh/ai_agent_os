# 38 Engineering Governance

## Purpose

Protect long-term maintainability by enforcing architectural intent, coding standards, decision traceability, technical-debt visibility, and modernization boundaries across the SDLC.

## Responsibilities

- enforce architecture and dependency rules through policy and validation
- maintain approved ADR/intent references and decision owners
- detect duplicate implementations, obsolete paths, dependency health issues, and convention drift
- classify and prioritize technical debt without treating every style preference as a release blocker
- guide modernization through bounded migration plans and compatibility evidence

## Boundaries

Governance is cross-cutting, not a single pipeline step. It provides rules and evidence to Repository Intelligence, Engineering Intelligence, Planning, Execution, Validation, Learning, and Release processes. It does not directly edit code, schedule tasks, or override the human owner.

## Decision Hierarchy

1. explicit legal, security, and production policy
2. approved architectural decisions and intent
3. repository contracts and compatibility guarantees
4. validated conventions and ownership rules
5. inferred patterns and agent preferences

Conflicts are recorded and escalated to the designated architecture owner. A model may propose a decision but cannot ratify it.

## Interfaces

- architectural intent: `schemas/architectural_intent.schema.json`
- design decision/ADR: `schemas/design_decision.schema.json`

## Acceptance Criteria

- Architecture checks trace violations to a rule or decision record.
- Technical-debt findings carry impact, evidence, owner, and suggested bounded action.
- Governance rules can block unsafe architecture changes without blocking harmless local edits.

## Future Extensions

- ADR repository integration
- dependency vulnerability and license policy feeds
- modernization portfolio planning

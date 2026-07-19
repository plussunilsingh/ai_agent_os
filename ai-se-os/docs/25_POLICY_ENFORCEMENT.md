# 25 Policy Enforcement

## Purpose

Turn constitution, security, token, routing, validation, and governance rules into enforceable decisions instead of advisory text.

## Components

- Policy Decision Point (PDP): evaluates an action request against policy.
- Policy Enforcement Point (PEP): blocks or permits the protected action.
- Policy registry: versioned policy documents and machine-readable rules.
- Decision record: immutable result consumed by the PEP.

## Protected Actions

- read or transmit classified repository content
- call a model or select a remote provider
- write a path, run a command, install a dependency, start Docker, or access a browser
- alter Git state, create a release artifact, deploy, or access production
- publish memory, telemetry, audit, or benchmark data

## Decision Outcomes

- `allow`: action may proceed within the issued capabilities.
- `deny`: action must not run.
- `require_human`: a named approver must create a new decision.
- `mask_data`: sanitize specified data then re-evaluate.
- `local_only`: action may use only approved local models or tools.

## Required Request Data

- action type and requested capabilities
- actor, task, repository/workspace/session scope, and correlation ID
- target paths, command, model, provider, or environment as applicable
- data classification, risk, token/cost request, and expiration requested
- referenced policy versions

## Enforcement Rules

- PEPs enforce decisions at the tool or adapter boundary; prompts alone are not enforcement.
- Decisions are least-privilege, scope-bound, expiry-bound, and non-transferable across tasks or workspaces.
- A PEP denies missing, expired, mismatched, or revoked decisions.
- A policy exception has a reason, bounded expiry, approver, and audit event.
- PDP failure defaults to deny for privileged actions and to human escalation for ambiguous actions.

## Interfaces

- policy decision: `schemas/policy_decision.schema.json`
- execution capability request: `schemas/execution_record.schema.json`
- detailed rules: `policies/security_policy.md`, `policies/token_policy.md`, `policies/model_routing_policy.md`, and `policies/validation_policy.md`

## Acceptance Criteria

- Every protected tool/model call has a valid policy decision ID.
- A denied or expired decision cannot be bypassed by an agent adapter.
- Policy decisions appear in audit history without sensitive payloads.

## Future Extensions

- OPA/Rego or Cedar adapter
- organization policy bundles
- approval workflow integration

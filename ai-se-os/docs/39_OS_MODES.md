# 39 OS Modes

## Purpose

Define explicit operating modes so agents know what they may observe, decide, or modify during each SDLC phase.

## Modes

- Discovery: read-only repository indexing, DNA refresh, and evidence gathering.
- Planning: requirement analysis, impact, task DAG creation, and policy evaluation; no source writes.
- Implementation: leased, policy-authorized task execution in bounded scope.
- Validation: evidence collection and acceptance evaluation; no scope expansion.
- Recovery: diagnosis, focused retry/replan/rollback preparation, and escalation.
- Optimization: controlled cost, context, prompt, or model improvements evaluated against benchmarks.
- Learning: promote validated knowledge and refresh derived projections.
- Release/Operations: release readiness, incident triage, and human-owned deployment handoff.

## Transition Rules

- A mode transition records an audit event and references the task or release scope.
- Mode-specific policy capabilities restrict tools. Discovery cannot write source; Implementation cannot mark completion; Validation cannot silently repair code.
- Transitions to Implementation, Recovery, and Release require valid policy and, where applicable, scheduler lease or human approval.
- A mode may request another mode but cannot assume its permissions.

## Acceptance Criteria

- An agent can determine allowed actions from mode, policy decision, and lease alone.
- Audit records show why a source change, validation run, or escalation occurred.
- Mode changes cannot hide a scope expansion.

## Future Extensions

- organization-specific modes
- incident command integration

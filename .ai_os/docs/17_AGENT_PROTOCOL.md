# 17 Agent Protocol

## Purpose

Define how agents cooperate with AI-SE OS and with each other.

## Responsibilities

- define required reading order
- define task handoff format
- define status, validation, and completion reporting
- define human escalation points

## Agent Session Protocol

1. Discover AI-SE OS through `.ai_os/README.md` or a root-level agent shim.
2. Read `docs/40_AGENT_DISCOVERY_AND_HOOKS.md`.
3. Read constitution and current subsystem document.
4. State task ID, scope, repository/workspace/worktree/session identity, and files.
5. Obtain a Scheduler lease and valid policy decision before privileged work.
6. Build or request a context pack and prompt packet.
7. Execute only the current leased task.
8. Validate using the assigned policy gates.
9. Report changes, evidence, risks, artifact IDs, and next task.

## Handoff Format

- current task ID
- AI-SE OS boot files read
- lease ID and policy decision ID
- completed work
- changed files
- validation evidence
- open risks
- next recommended task
- memory updates needed

## Prohibited Behavior

- editing outside task scope without re-planning
- hiding failed validation
- using unapproved models for sensitive code
- executing without a valid lease or policy decision
- overwriting user changes
- marking tasks complete without evidence

## Acceptance Criteria

- Any agent can resume from a handoff without reading the whole conversation.
- Multi-agent work has no ambiguous ownership, scope, or active lease.

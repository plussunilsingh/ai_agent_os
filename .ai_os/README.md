# AI Software Engineering Operating System (AI-SE OS)

## Status

AI-SE OS v3 is an executable runtime specification for the complete SDLC. It defines the artifacts, policies, state transitions, and subsystem contracts required to build an AI engineering runtime. It is not itself a running orchestrator yet; that is the Level 4 milestone in `ROADMAP.md`.

The design is deliberately practical: JSON artifacts and append-only audit records are the MVP persistence model. Derived indexes and an optional event store can be introduced later without changing the contracts.

## Purpose

AI-SE OS coordinates requirement analysis, repository intelligence, knowledge, planning, model routing, bounded execution, validation, recovery, learning, telemetry, and governance without loading an entire repository or relying on a giant prompt. It is designed for Codex, GitHub Copilot, Cline, Claude Code, local models, and compatible tool adapters.

## How Agents Must Use This OS

1. Detect `.ai_os/README.md` from root-level agent shims or repository discovery.
2. Read `docs/40_AGENT_DISCOVERY_AND_HOOKS.md`.
3. Read `docs/00_VISION.md`, `docs/01_ARCHITECTURE.md`, and `docs/02_ARCHITECTURE_CONSTITUTION.md`.
4. Read `docs/17_AGENT_PROTOCOL.md`.
5. Read `docs/23_RUNTIME_MODEL.md`, `docs/24_ARTIFACT_OWNERSHIP.md`, and `docs/25_POLICY_ENFORCEMENT.md` before building a runtime component.
6. Read `ROADMAP.md` and `IMPLEMENTATION_ORDER.md`.
7. Create a requirement brief, then a bounded task DAG, before editing code.
8. Gather repository intelligence and a task-specific Repository DNA slice before constructing context.
9. Compile a minimal, provenance-tagged context pack rather than sending broad repository context.
10. Obtain a policy decision before each privileged model or tool action.
11. Validate every generated change through the task's validation policy matrix.
12. Append an audit record and create only validated knowledge updates after completion or failure.

## Repository Structure

- `docs/` - subsystem specifications, one responsibility per file.
- `docs/diagrams/` - Mermaid diagrams for architecture and workflows.
- `prompts/` - reusable prompts for agents and subsystem sessions.
- `schemas/` - JSON schemas for contracts between subsystems.
- `policies/` - non-negotiable operating policies.
- `templates/` - implementation, planning, validation, and reporting templates.
- `examples/` - sample SDLC flows and generated artifacts.
- `hooks/` - discovery and lifecycle hook notes for current shims and future runtime adapters.
- `.ai_os_runtime/` - local runtime state, caches, events, and derived projections; ignored by Git by default.

## SDLC Coverage

AI-SE OS covers Discovery, Planning, Implementation, Validation, Recovery, Optimization, Learning, release readiness, deployment handoff, operations, and incidents.

## Layer Model

1. Governance: constitution, policy, permission, security, and engineering governance.
2. Repository Intelligence: deterministic repository facts, fingerprinting, and Repository DNA.
3. Knowledge: versioned graph projections, project state, intent, decisions, and scoped memory.
4. Engineering Intelligence: completeness, impact, reasoning, risk, and complexity analysis.
5. Planning and Model Intelligence: task DAGs, context/prompt compilation, model capability, routing, and scheduling.
6. Execution: agents, sandboxes, tool adapters, Git, terminal, browser, and filesystem actions.
7. Validation and Recovery: evidence gates, independent critique, root-cause analysis, retry, rollback, and escalation.
8. Learning and Observability: validated knowledge updates, benchmarks, telemetry, and repository evolution.

## Non-Negotiable Design Boundaries

- AI agents must auto-load AI-SE OS when `.ai_os/README.md` exists, even if the user forgets to mention it.
- A graph is a derived, queryable projection; it never invents or owns source facts.
- Every durable artifact has a schema version, producer, provenance, confidence, and lifecycle rules.
- Audit records are append-only. Full event sourcing is an optional future storage strategy, not an MVP dependency.
- Runtime state is namespaced by repository, workspace, worktree, branch, and session; no agent relies on an unqualified "current task".
- Confidence guides automation and escalation. It never replaces validation evidence.

## Contributing Rules

- Edit one subsystem file at a time.
- Every subsystem document must include purpose, responsibilities, inputs, outputs, interfaces, algorithms, errors, token strategy, acceptance criteria, and future extensions.
- Any implementation must update relevant schemas, policies, prompts, examples, and artifact ownership records in the same change set.
- Do not bypass `docs/02_ARCHITECTURE_CONSTITUTION.md`.

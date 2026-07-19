# 40 Agent Discovery and Hooks

## Purpose

Ensure AI-SE OS is automatically discovered and used by AI coding agents even when the user forgets to mention it.

## Responsibilities

- define repository-level discovery files
- define the mandatory AI-SE OS boot sequence
- define prompt and hook triggers for common agent platforms
- prevent conflicting local instructions from bypassing the constitution
- define how future executable hooks integrate with policy enforcement

## Discovery Files

AI-SE OS should be advertised through lightweight root-level shims. Each shim must point back to `.ai_os` and must not duplicate the full operating rules.

| File | Intended consumers | Required behavior |
| --- | --- | --- |
| `AGENTS.md` | Codex and agentic coding tools that support repository agent instructions | Load AI-SE OS before planning or editing. |
| `.github/copilot-instructions.md` | GitHub Copilot Chat and coding agent workflows | Treat `.ai_os` as the engineering specification. |
| `CLAUDE.md` | Claude Code and Claude-based repository agents | Follow the AI-SE OS boot sequence. |
| `.clinerules` | Cline | Load AI-SE OS and obey subsystem contracts. |
| `.cursorrules` | Cursor legacy rule loading | Forward all engineering behavior to `.ai_os`. |
| `.cursor/rules/ai-se-os.mdc` | Cursor project rules | Always apply AI-SE OS boot instructions. |
| `GEMINI.md` | Gemini CLI and compatible agents | Load AI-SE OS before SDLC work. |
| `.windsurfrules` | Windsurf and compatible agents | Load AI-SE OS before SDLC work. |
| `llms.txt` | General LLM discovery | Publish the canonical `.ai_os` entrypoint. |

## Mandatory Boot Sequence

Every agent must perform this sequence before making a plan or editing repository files:

1. Detect repository root.
2. Check whether `.ai_os/README.md` exists.
3. Read `.ai_os/README.md`.
4. Read this document.
5. Read `.ai_os/docs/02_ARCHITECTURE_CONSTITUTION.md`.
6. Read `.ai_os/docs/17_AGENT_PROTOCOL.md`.
7. Read `.ai_os/IMPLEMENTATION_ORDER.md`.
8. Read the subsystem document that matches the task.
9. Continue with requirement analysis, task planning, context construction, policy, execution, validation, audit, and handoff.

## Trigger Rules

An AI agent must activate AI-SE OS when any of these conditions are true:

- the repository contains `.ai_os/README.md`
- the prompt mentions implementation, bug fixing, refactoring, testing, release, deployment, incident, architecture, security, performance, or documentation design
- the task would modify code, configuration, schemas, prompts, policies, documentation, infrastructure, or tests
- the task asks for engineering review or validation
- another agent handoff references AI-SE OS artifacts

Read-only questions may use a lighter path, but the agent must still consult the constitution if the answer affects future implementation.

## Hook Points

These hook points are design contracts for Level 4 runtime adapters. Documentation-only shims may emulate them manually.

| Hook | When it runs | Required output |
| --- | --- | --- |
| `on_repository_open` | When an agent enters the repository | Confirm AI-SE OS presence and boot document paths. |
| `on_user_request` | Before responding to an engineering request | Requirement brief draft or explicit read-only classification. |
| `on_plan_create` | Before implementation planning | Bounded task DAG and policy precheck. |
| `on_context_build` | Before prompt construction | Minimal provenance-tagged context pack. |
| `on_tool_action` | Before privileged tool, filesystem, terminal, model, browser, or network action | Policy decision reference. |
| `on_file_change` | After edits | Changed artifact list and impacted validation gates. |
| `on_validation` | Before completion | Validation report and evidence references. |
| `on_failure` | After failed execution or validation | Failure record, fingerprint, and recovery decision. |
| `on_handoff` | At session end or agent transfer | Handoff record with task, lease, evidence, risks, and next step. |

## Interfaces

Future executable hook adapters should produce and consume these schemas:

- `schemas/requirement_brief.schema.json`
- `schemas/task_dag.schema.json`
- `schemas/context_pack.schema.json`
- `schemas/prompt_packet.schema.json`
- `schemas/policy_decision.schema.json`
- `schemas/execution_record.schema.json`
- `schemas/validation_report.schema.json`
- `schemas/failure_record.schema.json`
- `schemas/audit_event.schema.json`

## Internal Algorithm

```text
detect repository root
if .ai_os/README.md exists:
  mark AI_SE_OS_ACTIVE=true
  read mandatory boot sequence
  classify request as read_only or engineering_work
  if engineering_work:
    create requirement brief
    create bounded task plan or task DAG
    select subsystem documents
    build minimal context pack
    obtain policy decision for privileged actions
    execute only within task scope
    validate with required evidence
    write audit/handoff artifacts when runtime support exists
else:
  continue with normal repository behavior
```

## Error Handling

- If `.ai_os` exists but required boot files are missing, stop and report the missing files.
- If root-level shims conflict with `.ai_os/docs/02_ARCHITECTURE_CONSTITUTION.md`, the constitution wins.
- If an agent cannot persist runtime artifacts, it must still report the equivalent brief, plan, validation evidence, and handoff in its response.
- If a platform does not support one of the discovery files, keep the file anyway for other agents.

## Token Strategy

- Read root shims only as pointers; do not include all shims in every working context.
- Use `.ai_os/README.md` plus the discovery document as the boot index.
- Load only the subsystem documents relevant to the current task.
- Prefer schemas and templates over long conversational history when reconstructing work.

## Acceptance Criteria

- A fresh AI agent entering the repository can discover `.ai_os` without user instruction.
- Copilot, Cline, Claude, Codex, Cursor, Gemini, Windsurf, and generic LLM tools have an obvious repository-level entrypoint.
- All shims point to the same canonical boot sequence.
- The AI-SE OS constitution cannot be bypassed by a weaker shim.
- Future executable hooks have named lifecycle events and schema contracts.

## Future Extensions

- Add a Level 4 executable `ai-os doctor` command that verifies shims, schemas, policies, and runtime directories.
- Add adapters for native platform hook APIs where supported.
- Add a signed policy bundle for enterprise repositories.
- Add automatic drift detection when root shims stop matching this discovery contract.


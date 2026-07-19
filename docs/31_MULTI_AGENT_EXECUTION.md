# 31 Multi-Agent Execution

## Purpose

Execute bounded tasks through interchangeable agent and tool adapters while preserving task scope, policy enforcement, lease ownership, and user changes.

## Roles

- Agent Manager: starts, observes, and stops task attempts; it does not bypass Scheduler leases.
- Executor Agent: applies only the current leased task.
- Reviewer Agent: produces advisory analysis or independent critique; it cannot mark a task complete.
- Human Owner: can approve, reject, take ownership, or resolve a blocked task.
- Tool Adapter: translates approved capabilities into Codex, Copilot, Cline, terminal, filesystem, Git, Docker, browser, or MCP actions.

## Adapter Contract

Every adapter receives a prompt packet, routing decision, scheduler lease, and policy decision. It reports an execution record containing command/tool actions, touched paths, artifact references, normalized outputs, errors, and redacted logs.

Adapters must:

- enforce allowed paths and capabilities at the boundary
- preserve unrelated and human-owned changes
- report rather than hide failed tool actions
- support cancellation and timeouts
- avoid treating generated prose as a successful code change

## Execution Modes

- human-guided: agent proposes or executes only approved actions
- bounded autonomous: agent executes leased tasks within policy and budget
- review-only: agent produces evidence without writing
- diagnostic: agent gathers read-only evidence to unblock planning or recovery

## Operational Decisions

Execution may make only bounded operational decisions: retry a transient command inside its retry policy, refresh a safe read-only observation, or stop on timeout. It may not expand task scope, change architecture, approve itself, bypass policy, or deploy based on local reasoning.

## Error Handling

- lease expired: stop writes and reconcile with Scheduler
- dirty conflicting path: stop and report, never overwrite
- adapter output violates expected schema: classify as execution failure
- tool action denied: preserve the denial decision and escalate when required

## Acceptance Criteria

- Every file write, command, and model call is linked to a task, lease, policy decision, and execution record.
- Agents in distinct worktrees can operate concurrently without conflicting leases.
- A task can be cancelled without losing its audit history or user work.

## Future Extensions

- remote worker protocol
- isolated disposable worktree manager
- multi-agent review quorum

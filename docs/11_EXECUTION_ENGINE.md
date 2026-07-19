# 11 Execution Engine

## Purpose

Coordinate bounded code changes through approved adapters. `31_MULTI_AGENT_EXECUTION.md` is the authoritative v3 execution contract.

## Responsibilities

- execute prompt packets only with valid task lease and policy decision
- enforce file scope
- run allowed commands
- preserve user changes
- capture artifacts and logs

## Inputs

- prompt packet, routing decision, task record, Scheduler lease, policy decision, and namespaced repository state

## Outputs

- changed files, command logs, immutable `schemas/execution_record.schema.json`, and tool errors

## Interfaces

- consumes prompt packets from Prompt Engine
- sends outputs to Validation Engine
- reports failures to Recovery Engine

## Internal Algorithms

1. Verify task lease, policy decision, scope, and namespaced repository state.
2. Apply changes through the selected agent or tool.
3. Track touched files.
4. Reject unrelated edits.
5. Run local checks requested by the task.
6. Produce execution record.

## Error Handling

- permission denied: escalate according to policy
- dirty conflicting files: preserve user changes and request decision if blocked
- tool timeout: classify and retry if safe
- unrelated modifications: stop and report

## Acceptance Criteria

- Every change is tied to a task ID, lease ID, policy decision, and execution attempt.
- Touched files are recorded.
- User changes are never reverted without explicit instruction.

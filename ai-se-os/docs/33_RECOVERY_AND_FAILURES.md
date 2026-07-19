# 33 Recovery And Failures

## Purpose

Recover from failures through evidence-based diagnosis without endlessly retrying the same approach.

## Failure Fingerprint

A fingerprint includes normalized error signature, validation stage, task and plan version, prompt hash, context hash, model/version, tool path, repository/worktree revision, changed paths, policy decision, and environment identity. Secrets and sensitive raw logs are redacted before storage.

## Recovery Flow

1. Classify the failure: requirement, context, reasoning, generation, execution, validation, policy, concurrency, environment, or external dependency.
2. Compare to prior fingerprints under a material-sameness policy.
3. Identify a root-cause hypothesis and evidence level.
4. Select one action: retry with material change, re-index, recompile context, reroute model, re-plan, rollback, diagnostic task, or human escalation.
5. Publish a recovery plan and a new task attempt if authorized.
6. Promote reusable prevention guidance only after resolution evidence exists.

## Retry Rules

- Retry budgets are attached to tasks and may be tightened by policy.
- A retry requires a material change: repository state, context, plan, model, tool path, or environment.
- Replaying the same fingerprint is denied unless a human approves a documented diagnostic exception.
- Rollback preserves user changes and uses a scoped, approved strategy.

## Escalation

Escalate when root cause confidence is low, recovery could be destructive, policy is denied, a lease conflict persists, a security concern exists, or retries are exhausted. Escalation reports include evidence, failed approaches, options, and the exact decision needed.

## Interfaces

- failure record: `schemas/failure_record.schema.json`
- execution evidence: `schemas/execution_record.schema.json`
- validation evidence: `schemas/validation_report.schema.json`

## Acceptance Criteria

- Identical failed approaches cannot silently loop.
- Every retry has a recorded material difference and reason.
- Root-cause hypotheses are distinguishable from validated causes.

## Future Extensions

- causal failure clustering
- automated rollback simulation
- failure playbook recommendation

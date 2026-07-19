# AI-SE OS Roadmap

## Maturity Model

| Level | Meaning | Current state |
| --- | --- | --- |
| 1 | Ideas and notes | complete |
| 2 | Architecture specification | complete |
| 3 | Executable runtime specification | complete in v3 docs and schemas |
| 4 | Working local MVP runtime | next implementation milestone |
| 5 | Production-grade AI Engineering OS | future milestone |

AI-SE OS v3 is a Level 3 specification. Completion of this documentation does not claim that a runtime has been built or benchmarked.

## Phase 0: Runtime Foundation

- Constitution, policy/permission enforcement, security, and operating modes
- artifact ownership, append-only audit model, runtime directory, and CLI contracts
- schema validation and atomic local artifact publication

Exit criteria: a local runtime can reject invalid/unauthorized artifacts and trace every action to a task, policy decision, and audit record.

## Phase 1: Repository Understanding

- incremental scanner, content hash index, module/symbol/API/database/test facts
- Repository DNA compiler and task-specific DNA slices
- graph projection builder with provenance and freshness

Exit criteria: a repository revision produces a stable index/DNA artifact; only invalidated facts and projections are refreshed.

## Phase 2: Engineering Intelligence And Planning

- requirement completeness, impact, architecture/risk/complexity reasoning
- requirement briefs, versioned task DAGs, validation plans, and task budgets
- Scheduler queue, namespaced state, leases, heartbeats, and collision prevention

Exit criteria: ambiguous work is converted into bounded, leaseable task plans with explicit assumptions, confidence, rollback, and evidence requirements.

## Phase 3: Context, Prompt, And Model Intelligence

- deterministic context and prompt compilers
- content-addressed cache with policy/source-version checks
- model/capability registry, policy-aware router, fallback, and cost controls

Exit criteria: every model call has reproducible inputs, policy eligibility, a token/cost budget, expected output, and fallback rationale.

## Phase 4: Bounded Execution And Validation

- adapter contract for terminal/filesystem/Git first, then Codex, Cline, Copilot, and other tools
- policy enforcement at tool boundaries and task-scope/lease checks
- validation policy matrix, evidence reports, independent critique, and baseline/flaky-test handling

Exit criteria: no source change is marked complete without linked execution, validation, policy, and audit artifacts.

## Phase 5: Recovery, Learning, And Evolution

- failure fingerprints, material-change retry rules, root-cause status, rollback, and escalation
- validated knowledge promotion, DNA refresh, pattern learning, and projection rebuilds
- benchmark suite, metric definitions, and quality/cost/reliability baselines

Exit criteria: duplicate failed approaches are blocked, resolved work produces traceable learning, and local benchmark results guide improvement.

## Phase 6: Production Operation

- CI/CD, release readiness, incident, and observability adapters
- multi-workspace/remote workers, enterprise policy, data retention, access controls, and operational dashboards
- benchmarked reliability, security, cost, and recovery evidence in the intended environment

Exit criteria: Level 5 is claimed only with sustained measured evidence, not documentation completeness.

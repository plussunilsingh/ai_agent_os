# Implementation Order

This file prescribes the safe implementation order so each layer has the dependencies it needs.

## Boot Sequence

1. `40_AGENT_DISCOVERY_AND_HOOKS.md`
2. `00_VISION.md`
3. `01_ARCHITECTURE.md`
4. `02_ARCHITECTURE_CONSTITUTION.md`
5. `17_AGENT_PROTOCOL.md`
6. `23_RUNTIME_MODEL.md`
7. `24_ARTIFACT_OWNERSHIP.md`
8. `25_POLICY_ENFORCEMENT.md`
9. `36_RUNTIME_ARTIFACTS_AND_CLI.md`
10. `18_SECURITY.md`, `14_TOKEN_OPTIMIZER.md`, and `39_OS_MODES.md`

Boot exit criteria:

- repository root contains agent discovery shims for supported AI coding tools
- all shims point to the same AI-SE OS boot sequence
- discovery rules do not conflict with the architecture constitution

## Build Order

1. Runtime artifact store, schema validator, audit writer, and policy decision/PEP boundary.
2. Repository Intelligence and Repository DNA: `03_REPOSITORY_INTELLIGENCE.md`, `37_REPOSITORY_DNA.md`.
3. Graph projections and scoped Memory: `04_KNOWLEDGE_GRAPH.md`, `05_MEMORY_ENGINE.md`.
4. Namespaced Project State and Scheduler leases: `26_RUNTIME_STATE_AND_SCHEDULER.md`.
5. Engineering Intelligence and Requirement Analyzer: `27_ENGINEERING_INTELLIGENCE.md`, `06_REQUIREMENT_ANALYZER.md`.
6. Task Planner and Engineering Governance: `07_TASK_PLANNER.md`, `38_ENGINEERING_GOVERNANCE.md`.
7. Context and Prompt Compilers: `28_CONTEXT_COMPILER.md`, `29_PROMPT_COMPILER.md`.
8. Model Intelligence: `30_MODEL_INTELLIGENCE.md`.
9. Generic terminal/filesystem/Git execution adapter, then Multi-Agent adapters: `31_MULTI_AGENT_EXECUTION.md`, `11_EXECUTION_ENGINE.md`.
10. Validation Intelligence: `32_VALIDATION_INTELLIGENCE.md`, `12_VALIDATION_ENGINE.md`.
11. Recovery and failure fingerprinting: `33_RECOVERY_AND_FAILURES.md`, `13_RECOVERY_ENGINE.md`.
12. Learning, evolution, telemetry, and benchmarks: `34_CONTINUOUS_EVOLUTION.md`, `15_LEARNING_ENGINE.md`, `16_TELEMETRY.md`, `35_ENGINEERING_BENCHMARKS.md`.
13. Plugins, releases, incidents, and deferred extensions: `19_PLUGIN_SYSTEM.md`, `20_RELEASE_DEPLOYMENT.md`, `21_INCIDENT_OPERATIONS.md`, `22_FUTURE.md`.

## Per-Subsystem Implementation Loop

1. Read the subsystem document.
2. Read only referenced schemas and policies, then declare artifact producer/consumer ownership.
3. Obtain a policy decision before privileged work and a Scheduler lease before source writes.
4. Create an implementation brief from `templates/implementation_brief.md`.
5. Generate or modify code in the smallest useful increment.
6. Run validation gates from `templates/validation_report.md` and append audit/telemetry records.
7. Promote learning only from validated evidence and supersede stale artifacts rather than overwriting them.
8. Mark acceptance criteria only when evidence exists.

## Rationale

Start with policy-enforced, schema-valid artifacts and a small accurate model of the codebase. All later autonomy depends on reliable repository intelligence, bounded context, exclusive task leases, and evidence-based validation.

# 36 Runtime Artifacts And CLI

## Purpose

Define the local runtime layout and CLI boundary for an MVP implementation while keeping storage and tool adapters replaceable.

## Runtime Layout

```text
.ai_os_runtime/
  artifacts/
    requirements/
    plans/
    context/
    prompts/
    routes/
    execution/
    validation/
    failures/
    learning/
    policy/
  indexes/
  projections/
    graph/
    state/
    telemetry/
  audit/
  scheduler/
    queue/
    leases/
  cache/
  reports/
  quarantine/
```

The directory is local and ignored by Git. Curated, redacted fixtures belong under `examples/`, never in the runtime directory.

## Publication Rules

- Write new artifacts to a same-directory temporary file, validate schema, then atomically publish.
- Use content hash plus artifact ID for immutable artifacts.
- Create derived indexes only from published artifacts and audit records.
- Quarantine malformed, unknown-version, or policy-violating artifacts; do not load them into projections.
- Do not store secrets, raw credentials, or prohibited source text in any runtime path.

## CLI Contract

The first implementation exposes a small deterministic CLI:

```text
ai-se init
ai-se scan [--changed]
ai-se dna show [--scope <task-or-path>]
ai-se requirement analyze <input>
ai-se plan create <requirement-id>
ai-se context compile <task-id>
ai-se prompt compile <task-id>
ai-se route decide <prompt-packet-id>
ai-se task lease <task-id>
ai-se execute <task-id>
ai-se validate <task-id>
ai-se recover <failure-id>
ai-se status [--workspace <id>]
ai-se audit verify
```

Every command accepts `--repository`, `--workspace`, `--worktree`, `--branch`, `--session`, and `--correlation-id` where relevant. Commands print a schema-valid result or a structured error with an exit code. Commands never infer a globally current task.

## Exit Codes

- `0`: requested operation completed
- `2`: invalid input or schema
- `3`: policy denied or approval required
- `4`: stale/missing prerequisite artifact
- `5`: lease or concurrency conflict
- `6`: validation failed
- `7`: external tool or environment failure

## Acceptance Criteria

- A clean workspace can initialize runtime storage and produce a scan artifact without external services.
- Runtime state can be deleted and rebuilt from repository source plus retained artifacts where policy allows.
- Every CLI command has deterministic input/output contracts and audit lineage.

## Future Extensions

- daemon/API server
- SQLite/DuckDB store
- remote worker and CI adapters

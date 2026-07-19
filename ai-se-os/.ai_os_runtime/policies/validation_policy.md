# Validation Policy

## Rules

- No task is complete without validation evidence.
- Validation must match task risk.
- Shared modules require broader test selection.
- Failed validation must be reported honestly.
- Missing validation commands are a residual risk, not a pass.
- A policy matrix must define required, optional, and prohibited gates from task type, changed paths, risk, and release impact.
- Record source revision, environment, baseline relation, and evidence location for each gate.
- Self-critique is advisory and cannot override a failed deterministic gate.

## Minimum Gates

- documentation only: link and format check
- code edit: compile or type check when available
- behavior change: targeted tests
- shared behavior: targeted plus broader tests
- security-sensitive: security review and relevant scans

## Default Order

When applicable: formatting, type check, build, static analysis, unit, integration, API, UI, architecture, migration, regression/performance, security, and acceptance evidence review.

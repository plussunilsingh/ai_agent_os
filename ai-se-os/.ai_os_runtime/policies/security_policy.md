# Security Policy

## Rules

- No secrets in prompts, memory, logs, telemetry, or examples.
- Redact tokens, keys, passwords, private URLs, and customer data.
- Validate auth, input parsing, file IO, network, crypto, dependency, and migration changes.
- Require human approval for production, credentials, destructive operations, and access control changes.
- Store only provenance references for sensitive files unless approved.
- Protected model and tool actions require a Policy Decision Point (PDP) result and a Policy Enforcement Point (PEP) at the adapter boundary.
- Decisions are least-privilege, task/workspace scoped, expiry-bound, and denied by default when missing or stale.
- Apply retention, access, redaction, and deletion rules to audit, memory, learning, benchmark, and telemetry artifacts.

# 18 Security

## Purpose

Protect source code, credentials, infrastructure, users, and production systems during AI-assisted engineering.

## Responsibilities

- classify sensitive files and tasks
- define model privacy constraints
- prevent secret exposure
- require security validation for risky changes
- govern tool permissions
- require PDP decisions and PEP enforcement for protected actions

## Sensitive Data

- secrets and tokens
- production credentials
- customer data
- private keys
- regulated data
- proprietary source code outside approved execution paths

## Security Rules

- never paste secrets into prompts
- redact sensitive values in telemetry
- require human approval for credential, auth, payment, or production deployment changes
- run security gates for auth, input handling, crypto, dependency, and network changes
- deny privileged actions when policy decisions are missing, expired, or scope-mismatched

## Error Handling

- suspected secret exposure: stop, rotate if required, and record incident
- insecure generated code: fail validation and create recovery task
- unauthorized model route: block execution

## Acceptance Criteria

- Sensitive tasks are tagged before model routing and policy decisions are enforced at the adapter boundary.
- Security gates are part of validation for relevant changes.
- Telemetry and memory do not store secrets.

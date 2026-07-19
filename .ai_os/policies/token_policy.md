# Token Policy

## Purpose

Control context size, cost, and model usage.

## Rules

- Never send full repositories.
- Every prompt packet must have an estimated token count.
- Prefer task-specific Repository DNA, symbols, DTOs, APIs, SQL fragments, and tests before raw code.
- Full files require a documented small-file exception with source size, relevance, and policy reference.
- Indirect dependencies should be summaries unless risk requires source.
- If context exceeds budget, compress first, then split the task.
- Memory snippets must include confidence and freshness.
- Context items must include source version, provenance, sensitivity, selection reason, and token estimate.
- Reuse cache entries only when source versions and policy eligibility still match.

## Default Budgets

- requirement analysis: small
- task planning: small to medium
- implementation: medium
- architecture refactor: large with explicit approval
- recovery: small and failure-focused

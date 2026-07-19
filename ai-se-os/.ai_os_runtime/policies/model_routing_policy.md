# Model Routing Policy

## Purpose

Route tasks to appropriate models based on capability, cost, privacy, and risk.

## Rules

- Use the cheapest capable model for low-risk summarization and classification.
- Use stronger reasoning models for architecture, recovery, security, and multi-file refactors.
- Do not send sensitive code or secrets to unapproved external models.
- Prefer local or approved private routes for sensitive tasks.
- Record routing reason, fallback, cost estimate, and actual usage.
- Require a valid PDP decision before provider/model selection and enforce it at the adapter boundary.
- Record versioned model identity, context limit, data-handling class, and comparable-task reliability where available.
- A fallback must make a material change to model, context, prompt, plan, or tool path after a failure.

## Risk Routing

- Low: documentation, summaries, simple single-file edits.
- Medium: feature implementation, tests, adapters, UI changes.
- High: auth, security, data loss, migrations, payments, production operations.

High-risk work requires explicit validation gates, approved model routes, and a policy decision with bounded expiry.

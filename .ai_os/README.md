AI Software Engineering Operating System (AI-SE-OS)
=================================================

Purpose
-------
This repository contains the design, policies, templates, and schemas for an AI Software Engineering Operating System — an orchestration layer that coordinates Repository Intelligence, Knowledge Graphs, Task Planning, Model Routing, and Execution Engines (e.g., GitHub Copilot, Cline, OpenRouter).

How to use
----------
- Place this `.ai_os` folder next to a project you want to operate on.
- Ask an agent to read `ROADMAP.md` then `IMPLEMENTATION_ORDER.md`.
- For implementation tasks, point the agent to a single document under `docs/` and require an update to that document's acceptance criteria before coding.

Structure
---------
- `docs/` — subsystem specifications (one responsibility per file).
- `prompts/` — prompt templates and example interactions.
- `schemas/` — JSON schemas for module records, tasks, metrics.
- `policies/` — routing, token, and architecture policies.
- `templates/` — file and commit templates for generator usage.
- `examples/` — example workflows and sample outputs.

Contributing
------------
Edit one subsystem file at a time. Each file must have Acceptance Criteria and a single small implementation checklist.

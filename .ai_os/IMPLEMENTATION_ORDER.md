Implementation Order
====================

This file prescribes the safe order to implement subsystems so each layer has the dependencies it needs.

Priority (short-term)
---------------------
1. Repository Intelligence (module graph, module JSONs, project DNA)
2. Incremental Context Engine (hashing, change detection)
3. Knowledge Graph & Memory Store (store module JSONs, indexes)
4. Requirement Analyzer (reads Knowledge Graph)
5. Task Planner (uses Requirement Analyzer outputs)
6. Prompt Engineering Engine (templates for micro-tasks)
7. Model Router (policies + cheapest-capable mapping)

Secondary (integration & quality)
--------------------------------
8. Architecture Guardrails
9. Execution Engine Integrations (Cline, Copilot, OpenRouter)
10. Validation Engine (compile/tests/static analysis)
11. Execution Recovery Engine
12. Learning Engine
13. Token Optimizer & Cache
14. Metrics & Telemetry

Rationale
---------
Start by building a small, accurate, and persistent model of the codebase. All later orchestration depends on a reliable Repository Intelligence layer.

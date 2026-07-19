I think you're solving the right problem, but I would change the goal slightly.

Your goal should **not** be:

> "Build another AI coding agent."

Your goal should be:

> **"Build an AI Software Engineering Operating System (SEOS) that orchestrates Cline, GitHub Copilot, and LLMs efficiently."**

Since you're already using:

* ✅ VS Code
* ✅ Cline
* ✅ GitHub Copilot Agent
* ✅ OpenRouter free models
* ✅ Local project

the orchestrator should **not generate code**.

Instead it should answer:

> **Which model should do what, with which context, in which order, while spending the fewest tokens possible?**

---

# Current Pain Points

From all our discussions, your actual problems are these:

| Problem            | Current Situation                     |
| ------------------ | ------------------------------------- |
| Token limit        | Huge codebase                         |
| Context overflow   | Entire files repeatedly sent          |
| Hallucination      | Model invents architecture            |
| Repetition         | Same files loaded again and again     |
| Large tasks        | Requirement not decomposed            |
| No orchestration   | Copilot/Cline both work independently |
| Validation         | Coding ≠ correctness                  |
| Testing            | Usually after implementation          |
| Long conversations | Lose earlier decisions                |
| Multi-project      | Backend + React + DB                  |

So the orchestrator should solve these instead of writing code.

---

# What the orchestrator should become

```
Developer

↓

Requirement

↓

Requirement Analyzer

↓

Architecture Analyzer

↓

Knowledge Graph

↓

Planner

↓

Task Splitter

↓

Context Builder

↓

Model Selector

↓

Execution

↓

Compile

↓

Test

↓

Review

↓

Fix

↓

Commit
```

Notice that **LLM is only one component**.

---

# What should happen after you type ONE sentence

Suppose you type

```
Implement Inventory Reservation.
```

Instead of immediately asking Cline...

The orchestrator should do:

```
Requirement Analysis

↓

Understand domain

↓

Locate affected modules

↓

Read architecture

↓

Read database

↓

Read APIs

↓

Dependency graph

↓

Generate plan

↓

Split task

↓

Estimate complexity

↓

Choose model

↓

Execute

↓

Compile

↓

Integration Test

↓

Review

↓

Update memory
```

Exactly like a Senior Tech Lead.

---

# Phase 1

Requirement Understanding Agent

Input

```
Implement reservation
```

Output

```
Feature

Reservation

Business Goal

Reserve stock before dispatch.

Affected Modules

Inventory

Batch

Sales

Movement

Warehouse

Affected APIs

Reserve Inventory

Release Reservation

Confirm Reservation

Files

Inventory.java

InventoryService.java

ReservationService.java

InventoryMovement.java

Risk

Deadlock

Concurrency

Required Tests

Reservation

Release

Concurrent Reservation

Rollback
```

This alone saves lots of tokens.

---

# Phase 2

Knowledge Graph

Instead of

```
Send 800 files
```

Agent knows

```
Reservation

↓

Inventory

↓

Movement

↓

Batch

↓

Sales Allocation

↓

Warehouse
```

Only these files go to LLM.

---

# Phase 3

Planning Agent

Instead of

```
Implement reservation.
```

LLM gets

```
Task 1

Create Entity

Task 2

Repository

Task 3

Service

Task 4

API

Task 5

Tests

Task 6

Compile

Task 7

Integration

Task 8

Documentation
```

Tiny tasks.

Much fewer hallucinations.

---

# Phase 4

Context Builder

Never send

```
Inventory.java

1000 lines
```

Instead

```
Relevant methods

Relevant DTOs

Repository

Business rules

Architecture notes

Tests
```

Around 5–10 KB instead of hundreds of KB.

---

# Phase 5

Model Router

Don't use the same model for everything.

Example policy:

| Task                 | Model                 |
| -------------------- | --------------------- |
| Requirement analysis | GPT-5 / Claude        |
| Code search          | Local embedding model |
| Simple CRUD          | Qwen                  |
| Refactoring          | Claude                |
| Java reasoning       | DeepSeek              |
| Documentation        | GPT-5                 |
| Tests                | Qwen                  |
| Review               | Claude                |

The orchestrator decides automatically.

---

# Phase 6

Execution

Cline receives

```
ONLY

Implement ReservationRepository.

Files allowed

ReservationRepository.java

InventoryRepository.java

Do not touch other files.

Success

Compile

No warnings

No failing tests
```

Much better than

```
Implement reservation
```

---

# Phase 7

Verification

Never trust generated code.

Automatically run

```
Gradle

↓

SpotBugs

↓

JUnit

↓

Integration

↓

Playwright

↓

Performance

↓

Architecture Rules

↓

Security

↓

Done
```

---

# Phase 8

Reflection

Ask another model

```
Did implementation satisfy requirement?

Any missing validation?

Any race condition?

Architecture broken?

Duplicate code?

Missing tests?

Any deadlock?

Missing transaction?

N+1 queries?
```

Very effective.

---

# Phase 9

Memory

Don't resend

```
Inventory rules
```

Store

```
Inventory

↓

Reservation

↓

Movement

↓

Sales Allocation

↓

Concurrency

↓

Architecture decisions
```

Retrieve only when needed.

---

# Phase 10

Project Summaries

Maintain automatically generated summaries like:

```
Backend

120 files

Responsibilities

APIs

Dependencies

Architecture

Last modified

Summary

400 tokens
```

instead of

```
120 Java files
```

---

# The biggest token saver

Don't summarize files.

Summarize **modules**.

Example

```
Inventory Module

Purpose

Maintain stock.

Public APIs

reserve()

release()

deduct()

adjust()

Dependencies

Movement

Batch

Warehouse

Business Rules

Never negative.

Only InventoryService updates stock.

Pessimistic locking.

Movement append only.

Tests

45

Summary

300 tokens
```

Every LLM can understand the whole module from this.

---

# Proposed architecture for your orchestrator

```
┌────────────────────────────────────────────┐
│ VS Code                                    │
└────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────┐
│ AI Software Engineering Orchestrator       │
├────────────────────────────────────────────┤
│ Requirement Analyzer                       │
│ Architecture Analyzer                      │
│ Dependency Graph                           │
│ Project Knowledge Graph                    │
│ Context Builder                            │
│ Token Optimizer                            │
│ Planner                                    │
│ Task Splitter                              │
│ Model Router                               │
│ Memory Manager                             │
│ Verification Engine                        │
│ Reflection Engine                          │
└────────────────────────────────────────────┘
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
   Cline       GitHub Copilot   OpenRouter
      │
      ▼
 Build → Test → Fix → Commit
```

## A concise master prompt for your orchestrator

This is the kind of instruction I'd give the orchestrator itself:

> **You are an AI Software Engineering Orchestrator, not a coding assistant. Before generating code, analyze the requirement, identify affected modules, retrieve only relevant project context, decompose the work into independently verifiable tasks, choose the most appropriate model for each task, execute tasks incrementally, validate every change by compiling and testing, perform a self-review against architecture and business rules, and update project memory with any new decisions. Optimize for minimal token usage, deterministic execution, minimal file modifications, and autonomous completion. Never send the entire codebase when targeted context is sufficient. Never proceed to the next task until the current task satisfies its acceptance criteria.**

That gives you an orchestration layer focused on **planning, context management, execution control, and validation**, while continuing to use Cline, Copilot, and OpenRouter as the execution engines rather than replacing them.

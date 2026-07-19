# 06 Requirement Analyzer

## Purpose

Transform user requests into structured, testable requirement briefs.

## Responsibilities

- detect intent, scope, constraints, and success criteria
- identify ambiguity and missing information
- perform preliminary impact analysis
- classify risk, complexity, confidence, rollback impact, token budget, and SDLC phase

## Inputs

- raw user request
- project knowledge graph
- project memory
- architecture policies

## Outputs

- immutable requirement brief revision
- requirement completeness report
- assumptions
- open questions
- affected modules
- acceptance criteria
- risk rating

## Interfaces

- emits `schemas/requirement_brief.schema.json` and follows `27_ENGINEERING_INTELLIGENCE.md`
- passes impact hints to Task Planner
- requests context candidates from Knowledge Graph

## Internal Algorithms

1. Normalize the request into user-visible outcomes.
2. Detect SDLC phase: discovery, design, implementation, test, refactor, release, incident, documentation.
3. Extract constraints: files, frameworks, deadlines, tools, policies.
4. Query Knowledge Graph for likely impacted modules and tests.
5. Generate acceptance criteria with observable evidence.
6. Classify risk, complexity, confidence, rollback impact, token budget, and unknowns.

## Error Handling

- incomplete or ambiguous requirement: ask targeted questions or create a Discovery task; do not invent product behavior
- missing repository knowledge: trigger Repository Intelligence
- conflicting requirements: produce conflict report

## Token Strategy

Use graph summaries and memory records first. Include raw source only when a requirement references specific code behavior.

## Acceptance Criteria

- Every brief has scope, non-scope, assumptions, risks, complexity, confidence, and acceptance criteria.
- High-risk ambiguity is not hidden.
- The brief can be handed to Task Planner without the original conversation.

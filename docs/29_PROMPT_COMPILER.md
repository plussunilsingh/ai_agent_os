# 29 Prompt Compiler

## Purpose

Compile reproducible prompt packets from a task, context pack, policies, and expected machine-readable output instead of manually assembled agent instructions.

## Responsibilities

- select a versioned prompt template by task and execution mode
- bind task scope, context, policy references, allowed capabilities, and validation requirements
- emit a deterministic prompt packet with hashes of all source artifacts
- reject missing, stale, or policy-incompatible inputs

## Prompt Packet Requirements

- packet ID, compiler/template version, task/context IDs, and correlation ID
- allowed files, forbidden changes, tool capabilities, and output schema
- model-independent instructions plus model-specific adapter additions
- validation gates, retry metadata, token budget, and policy decision ID
- source artifact hashes and a prompt hash

## Determinism Rules

- Given identical compiler version, ordered inputs, policy decision, and template, the normalized packet must have the same prompt hash.
- Dynamic timestamps, unbounded chat history, and hidden system state are excluded from normalized prompt content.
- Provider-specific wrappers are adapters; they do not change task semantics.

## Error Handling

- missing acceptance criteria or context pack: reject compilation
- policy decision expired or insufficient: request a new decision
- output schema incompatible with adapter: fail before model routing
- prompt budget exceeded: return a structured compression request to Context Compiler

## Acceptance Criteria

- A packet is reproducible, inspectable, and traceable to its source artifacts.
- An executor can act without reading the full conversation.
- The packet clearly states success evidence and forbidden behavior.

## Future Extensions

- signed templates
- prompt-diff inspection
- controlled A/B template evaluation

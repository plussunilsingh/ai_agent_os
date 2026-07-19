# 09 Prompt Engine

## Purpose

Compile reproducible, policy-aware prompt packets from task records and context packs. `29_PROMPT_COMPILER.md` is the authoritative v3 compiler contract.

## Responsibilities

- compile prompts deterministically from versioned templates
- inject task scope, acceptance criteria, context, policies, and validation requirements
- prevent prompt bloat
- define expected output format

## Inputs

- task record
- context pack
- architecture constitution
- policy decision and model-independent execution mode
- execution mode

## Outputs

- immutable prompt packet using `schemas/prompt_packet.schema.json`
- tool instructions
- expected response schema
- validation checklist

## Interfaces

- uses templates in `prompts/`
- follows `policies/token_policy.md`
- hands prompt packet to Model Router or Execution Engine

## Internal Algorithms

1. Select prompt template by task type.
2. Insert task and acceptance criteria.
3. Insert bounded context in ranked order.
4. Bind a valid policy decision and only relevant policy references.
5. Specify allowed files, capabilities, and forbidden behavior.
6. Require validation output.

## Error Handling

- missing context pack: reject prompt generation
- prompt exceeds model limit: ask Context Engine to compress
- missing acceptance criteria: reject implementation prompt

## Acceptance Criteria

- Prompt packets are reproducible from task, context pack, policy decision, compiler version, and template.
- Prompts never duplicate large policy text unnecessarily.
- Prompts clearly state what not to change.

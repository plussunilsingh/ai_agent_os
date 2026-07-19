# 03 Repository Intelligence

## Purpose

Build a deterministic, incremental understanding of the target repository.

## Responsibilities

- detect languages, frameworks, packages, build systems, and entry points
- produce authoritative module, dependency, symbol, API, route, database, configuration, test, ownership, and technology facts
- identify ownership boundaries and architectural layers
- detect changed files and affected modules

## Inputs

- repository root
- ignore rules
- package manifests
- build files
- source files
- test files
- previous index snapshots

## Outputs

- immutable module and symbol records
- repository index for a source revision
- Repository DNA artifact
- source-backed dependency, API, route, database, ownership, and technology facts
- audit event identifying indexed source revision and changed paths

## Interfaces

- emits module records using `schemas/module_record.schema.json` and index records using `schemas/repository_index.schema.json`
- is the authoritative producer of scanner-derived repository facts; Projection Builder alone derives graph nodes and edges from those records
- publishes Repository DNA using `schemas/repository_dna.schema.json`
- provides impact hints to `06_REQUIREMENT_ANALYZER.md`

## Internal Algorithms

1. Discover project roots and manifests.
2. Apply ignore rules and max-file safeguards.
3. Hash files and compare against previous index.
4. Parse changed files with language-aware parsers when available.
5. Extract imports, exports, symbols, APIs, routes, models, migrations, and tests.
6. Publish source-backed facts and reverse dependency relationships with stable IDs.
7. Produce module summaries and DNA sections with confidence, source revision, and evidence coverage.

## Error Handling

- unreadable file: record skipped file with reason
- parser failure: fall back to lexical extraction and mark low confidence
- huge file: summarize by section and avoid raw inclusion
- generated file: classify and exclude unless directly required

## Token Strategy

Repository Intelligence should create compact facts. It should not ask a model to read the repository directly except for summary refinement after deterministic extraction.

## Acceptance Criteria

- Changed-file indexing works without reprocessing the whole repository.
- Every module record has path, language, dependencies, exports, tests, source revision, and confidence.
- Every index/DNA result identifies its source revision and can be superseded by a later revision.
- Reverse dependency lookup works for impact analysis.
- Generated and vendor files are excluded by default.

## Future Extensions

- Tree-sitter parser adapters
- monorepo workspace support
- service ownership inference
- API contract diffing

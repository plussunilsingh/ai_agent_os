# AI-SE OS - Engineering Intelligence Platform

Central AI-powered engineering intelligence service that provides intelligent assistance to all your repositories.

## Architecture

AI-SE OS runs as a **central service**. Each repository contains only a thin SDK.

```
ai-os/                          ⭐ CENTRAL SERVICE (this repo)
├── src/
│   ├── core/           # Data models, state machines, events
│   ├── kernel/         # State manager, scheduler, memory, resources
│   ├── intelligence/   # Genome, knowledge graph, reasoning, decisions
│   ├── execution/      # Context/prompt compilers, runtime, validation, recovery
│   ├── cache/          # Cache service with token optimization
│   ├── api/            # FastAPI routes and handlers
│   └── plugins/        # Plugin system
├── sdk-python/         # Thin Python SDK for repositories
├── docker/             # Docker compose for deployment
└── tests/              # Unit tests
```

## Quick Start

### Prerequisites
- Python 3.10+
- Docker & Docker Compose

### Run with Docker

```bash
cd .ai_os/docker
cp .env.example .env
# Edit .env with your configuration

docker-compose up -d
```

### Run Locally

```bash
cd .ai_os
pip install -r requirements.txt
python -m src.main
```

API docs: http://localhost:8000/docs
Health: http://localhost:8000/api/v1/health

## SDK Installation

```bash
pip install ai-se-os-client
```

## Key Features

- **Repository Intelligence**: Genome snapshots with 15 DNA dimensions
- **Knowledge Graph**: Versioned graph projections of repository knowledge
- **Planning**: Task decomposition from natural language requirements
- **Execution**: Agent runtime with lease management and policy enforcement
- **Validation**: 8-layer validation (build, static, test, architecture, security, policy, runtime, acceptance)
- **Recovery**: Failure fingerprinting and automated recovery strategies
- **Cache Intelligence**: Prompt caching with token optimization
- **Decision Engine**: Policy-based decisions with trust explanations

## Documentation

- `.ai_os/README.md` - Full specification
- `.ai_os/docs/` - Subsystem specifications
- `.ai_os/policies/` - Operating policies
- `.ai_os/schemas/` - JSON schemas
- `.ai_os/templates/` - Implementation templates

## License

MIT
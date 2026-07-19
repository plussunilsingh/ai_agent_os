# AI-SE OS Python SDK

Thin client for the AI-SE OS Engineering Intelligence Platform.

## Installation

```bash
pip install ai-se-os-client
```

## Quick Start

```python
from ai_se_os import AISeOSClient, Repository

# Initialize client (loads from environment variables)
client = AISeOSClient()

# Or configure manually
from ai_se_os import Config
config = Config(
    endpoint="https://ai-os.company.com",
    api_key="sk-xxxxxxxxxxxxxxxx"
)
client = AISeOSClient(config)

# Register a repository
repo = Repository(
    id="my-repo",
    name="My Repository",
    language="python",
    framework="django",
    owner="team-core",
    git_url="https://github.com/company/my-repo.git"
)
client.register_repository(repo)

# Generate a plan
plan = client.generate_plan(
    requirement="Add discount validation to order processing",
    repository_id="my-repo"
)

# Execute the plan
execution = client.execute_plan(plan.id)

# Run validation
result = client.run_validation("my-repo")

# Get intelligence score
score = client.get_intelligence_score("my-repo")
print(f"Intelligence Score: {score.overall}")
```

## Environment Variables

- `AI_OS_ENDPOINT` - AI-SE OS service endpoint (default: https://ai-os.company.com)
- `AI_OS_API_KEY` - API key for authentication
- `AI_OS_TIMEOUT` - Request timeout in seconds (default: 60)
- `AI_OS_MAX_RETRIES` - Maximum retries (default: 3)

## Key Features

- **Repository Management**: Register, analyze, and get genome snapshots
- **Planning**: Generate task plans from natural language requirements
- **Execution**: Execute plans and track progress
- **Validation**: Run multi-layer validation
- **Experience**: Search and recommend engineering experiences
- **Physics**: Predict change impact
- **Simulation**: Run what-if scenarios
- **Economics**: Analyze decision economics
- **Intelligence Score**: Track repository intelligence
- **Trust**: Explain decisions with full audit trail
- **Knowledge Graph**: Query and trace intent

## API Reference

See the full API reference at https://ai-os.company.com/docs
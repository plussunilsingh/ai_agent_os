FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ✅ Copy pyproject.toml first
COPY pyproject.toml setup.py README.md ./

# ✅ Install dependencies only (not the package itself)
RUN pip install --no-cache-dir \
    pydantic>=2.0.0 \
    redis>=5.0.0 \
    sqlalchemy>=2.0.0 \
    fastapi>=0.104.0 \
    uvicorn>=0.24.0 \
    opentelemetry-api>=1.20.0 \
    prometheus-client>=0.19.0 \
    openai>=1.0.0 \
    anthropic>=0.7.0 \
    click>=8.1.0 \
    rich>=13.0.0 \
    neo4j>=5.14.0 \
    asyncpg>=0.29.0

# ✅ Copy source code
COPY src/ /app/src/

# ✅ Install the package normally (not editable)
RUN pip install --no-cache-dir .

# Create non-root user
RUN useradd -m -u 1000 ai-os && \
    chown -R ai-os:ai-os /app
USER ai-os

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "ai_se_os.main:app", "--host", "0.0.0.0", "--port", "8000"]
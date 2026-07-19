FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN apt-get update && apt-get install -y gcc curl && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml setup.py README.md ./
RUN pip install --no-cache-dir -e ".[dev]"
COPY src/ /app/src/
RUN pip install -e .
RUN useradd -m -u 1000 ai-os && chown -R ai-os:ai-os /app
USER ai-os
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD curl -f http://localhost:8000/api/v1/health || exit 1
CMD ["uvicorn", "ai_se_os.main:app", "--host", "0.0.0.0", "--port", "8000"]

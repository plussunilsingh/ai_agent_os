FROM python:3.11-slim

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies (including curl for healthcheck)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy configuration, metadata, and source directory
COPY pyproject.toml README.md ./
COPY src/ /app/src/

# Install application package with dev dependencies
RUN pip install --no-cache-dir .[dev]

# Create non-root user for security
RUN useradd -m -u 1000 ai-os && \
    chown -R ai-os:ai-os /app
USER ai-os

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Run the application
CMD ["uvicorn", "ai_se_os.main:app", "--host", "0.0.0.0", "--port", "8000"]
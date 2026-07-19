FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc curl && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip
RUN pip install -e ".[dev]"

RUN useradd -m ai-os
USER ai-os

EXPOSE 8000

CMD ["uvicorn","ai_se_os.main:app","--host","0.0.0.0","--port","8000"]
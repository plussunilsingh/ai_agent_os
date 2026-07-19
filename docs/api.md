# AI-SE OS - API Documentation

## Overview
AI-SE OS provides RESTful HTTP APIs built with FastAPI for context management, intelligence queries, execution, and health monitoring.

## Base Endpoints

- `GET /`: Service identification and status.
- `GET /health`: Service health check.
- `GET /docs`: Interactive Swagger OpenAPI documentation.
- `GET /redoc`: ReDoc documentation.

## API Routes (`/api/v1`)

### Health & Status
- `GET /api/v1/health`: Detailed subsystem health.

### Context Engine
- `POST /api/v1/context/compile`: Compiles repo context into prompt packets.

### Intelligence & Cache
- `GET /api/v1/cache/stats`: Cache hit/miss metrics and token savings.
- `POST /api/v1/cache/invalidate`: Cache invalidation endpoint.

### Execution Engine
- `POST /api/v1/execution/run`: Execute agent tasks.

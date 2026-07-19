"""
AI-SE OS - Central Engineering Intelligence Service
FastAPI application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from .api.routes import router
from .api.handlers import APIHandlers
from .core.events import Event, EventType, get_event_bus

# Create FastAPI app
app = FastAPI(
    title="AI-SE OS",
    description="Engineering Intelligence Platform - Central Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Global handlers instance
handlers: APIHandlers = None


@app.on_event("startup")
async def startup():
    """Initialize AI-SE OS on startup"""
    global handlers
    handlers = APIHandlers()

    event_bus = get_event_bus()
    event_bus.publish(Event(
        type=EventType.SYSTEM_STARTUP,
        source="main",
        producer="system",
        payload={"version": "1.0.0"}
    ))

    print("AI-SE OS v1.0.0 started successfully")
    print(f"API docs: http://localhost:8000/docs")
    print(f"Health: http://localhost:8000/api/v1/health")


@app.on_event("shutdown")
async def shutdown():
    """Clean shutdown"""
    event_bus = get_event_bus()
    event_bus.publish(Event(
        type=EventType.SYSTEM_SHUTDOWN,
        source="main",
        producer="system",
        payload={}
    ))
    print("AI-SE OS shutdown complete")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "AI-SE OS",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


def start():
    """Start the AI-SE OS server"""
    host = os.getenv("AI_OS_HOST", "0.0.0.0")
    port = int(os.getenv("AI_OS_PORT", "8000"))
    uvicorn.run("src.main:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    start()
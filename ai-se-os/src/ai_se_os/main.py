"""
AI-SE OS Main Application
"""

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime

from .api.routes import router
from .version import get_version

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI-SE OS",
    description="Engineering Intelligence Platform",
    version=get_version(),
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(router, prefix="/api/v1", tags=["api"])

# Health check endpoint
@app.get("/")
async def root():
    return {
        "service": "AI-SE OS",
        "version": get_version(),
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "AI-SE OS",
        "version": get_version()
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("AI-SE OS starting up...")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("AI-SE OS shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

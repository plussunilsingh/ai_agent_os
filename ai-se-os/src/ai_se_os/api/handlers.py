"""
API Handlers for AI-SE OS
"""

from typing import Dict, Any, List, Optional
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

class APIHandlers:
    """API Handlers class"""
    
    @staticmethod
    async def handle_not_found(request, exc):
        """Handle 404 errors."""
        return {"error": "Resource not found", "status": 404}
    
    @staticmethod
    async def handle_validation_error(request, exc):
        """Handle validation errors."""
        return {"error": "Validation error", "status": 400}
    
    @staticmethod
    async def handle_internal_error(request, exc):
        """Handle internal errors."""
        logger.error(f"Internal error: {exc}")
        return {"error": "Internal server error", "status": 500}
    
    @staticmethod
    def create_response(data: Any, message: str = "Success", status: int = 200) -> Dict[str, Any]:
        """Create a standard API response."""
        return {
            "status": status,
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }

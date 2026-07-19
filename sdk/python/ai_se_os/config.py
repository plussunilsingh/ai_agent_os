"""
AI-SE OS Configuration
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """AI-SE OS client configuration"""
    
    endpoint: str = "https://ai-os.company.com"
    api_key: str = ""
    timeout: int = 60
    max_retries: int = 3
    
    @classmethod
    def from_env(cls) -> "Config":
        """
        Load configuration from environment variables.
        
        Environment variables:
        - AI_OS_ENDPOINT: AI-SE OS service endpoint
        - AI_OS_API_KEY: API key for authentication
        - AI_OS_TIMEOUT: Request timeout in seconds
        - AI_OS_MAX_RETRIES: Maximum retries
        """
        return cls(
            endpoint=os.getenv("AI_OS_ENDPOINT", "https://ai-os.company.com"),
            api_key=os.getenv("AI_OS_API_KEY", ""),
            timeout=int(os.getenv("AI_OS_TIMEOUT", "60")),
            max_retries=int(os.getenv("AI_OS_MAX_RETRIES", "3"))
        )
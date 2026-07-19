"""
AI-SE OS Python SDK
Thin client for the Engineering Intelligence Platform
"""

from .client import AISeOSClient
from .config import Config
from .models import (
    Repository,
    Task,
    Plan,
    Execution,
    ValidationResult,
    Experience,
    GenomeSnapshot,
    SimulationResult,
    EconomicsAnalysis,
    IntelligenceScore,
    TrustExplanation
)
from .exceptions import (
    AISeOSError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError
)

__version__ = "1.0.0"
__all__ = [
    "AISeOSClient",
    "Config",
    "Repository",
    "Task",
    "Plan",
    "Execution",
    "ValidationResult",
    "Experience",
    "GenomeSnapshot",
    "SimulationResult",
    "EconomicsAnalysis",
    "IntelligenceScore",
    "TrustExplanation",
    "AISeOSError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
]
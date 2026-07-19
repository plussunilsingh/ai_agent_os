"""
AI-SE OS SDK Exceptions
"""


class AISeOSError(Exception):
    """Base exception for AI-SE OS SDK"""
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class AuthenticationError(AISeOSError):
    """Authentication failed"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class NotFoundError(AISeOSError):
    """Resource not found"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ValidationError(AISeOSError):
    """Validation failed"""
    def __init__(self, message: str = "Validation failed", details: dict = None):
        super().__init__(message, status_code=422, details=details)


class RateLimitError(AISeOSError):
    """Rate limit exceeded"""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429)
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from fastapi import HTTPException, status

# Keep your existing response model
class ErrorResponse(BaseModel):
    """
    Base class for error responses.
    """
    status_code: int
    message: str
    error: Optional[str] = None
    timestamp: datetime = datetime.now()

# Add the base exception class
class FlowworkException(HTTPException):
    """
    Base exception class for all custom exceptions in the Flowwork application.
    """
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        self.error_code = error_code
        super().__init__(status_code=status_code, detail=detail, headers=headers)

# Add some common specific exceptions
class ResourceNotFoundException(FlowworkException):
    """Exception raised when a requested resource is not found."""
    def __init__(
        self,
        detail: str = "Resource not found",
        error_code: str = "RESOURCE_NOT_FOUND",
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code=error_code,
            headers=headers,
        )

class ValidationException(FlowworkException):
    """Exception raised for validation errors."""
    def __init__(
        self,
        detail: str = "Validation error",
        error_code: str = "VALIDATION_ERROR",
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code=error_code,
            headers=headers,
        )
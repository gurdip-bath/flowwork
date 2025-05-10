
# app/core/error_handlers.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import FlowworkException, ErrorResponse
from datetime import datetime

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Validation error",
            "error": "VALIDATION_ERROR",
            "details": exc.errors(),
            "timestamp": datetime.now().isoformat()
        }
    )

async def flowwork_exception_handler(request: Request, exc: FlowworkException):
    """Handle custom application exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status_code=exc.status_code,
            message=exc.detail,
            error=exc.error_code,
            timestamp=datetime.now()
        ).model_dump()
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Database error",
            "error": "DATABASE_ERROR",
            "timestamp": datetime.now().isoformat()
        }
    )

# Add more exception handlers as needed TODO
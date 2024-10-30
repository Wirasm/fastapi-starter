"""Module for custom exception classes and exception handlers.

This module defines custom exception classes and exception handlers
used throughout the application for consistent error handling.
"""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class AppException(HTTPException):
    """Base exception class for application-specific exceptions."""

    def __init__(self, status_code: int, detail: str):
        """Initialize the AppException."""
        super().__init__(status_code=status_code, detail=detail)


class DatabaseException(AppException):
    """Exception raised for database-related errors."""

    def __init__(self, detail: str):
        """Initialize the DatabaseException."""
        super().__init__(status_code=500, detail=detail)


class AuthenticationException(AppException):
    """Exception raised for authentication-related errors."""

    def __init__(self, detail: str):
        """Initialize the AuthenticationException."""
        super().__init__(status_code=401, detail=detail)


class NotFoundException(AppException):
    """Exception raised when a requested resource is not found."""

    def __init__(self, detail: str):
        """Initialize the NotFoundException."""
        super().__init__(status_code=404, detail=detail)


async def app_exception_handler(request: Request, exc: AppException):
    """Handle AppExceptions and return appropriate JSON responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    """Handle unhandled exceptions and return a generic error response."""
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )


def add_exception_handlers(app):
    """Add exception handlers to the FastAPI application."""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

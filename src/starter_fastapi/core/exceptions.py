"""Custom exception classes and exception handlers."""

from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from starter_fastapi.core.logging import get_logger

logger = get_logger(__name__)


class AppException(Exception):
    """Base exception class for application-specific exceptions."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            status_code: HTTP status code
            details: Additional error details
        """
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(AppException):
    """Exception raised when a resource is not found."""

    def __init__(self, message: str = "Resource not found", details: dict[str, Any] | None = None) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND, details=details)


class ValidationError(AppException):
    """Exception raised when validation fails."""

    def __init__(
        self,
        message: str = "Validation error",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, details=details)


class UnauthorizedError(AppException):
    """Exception raised when authentication fails."""

    def __init__(self, message: str = "Unauthorized", details: dict[str, Any] | None = None) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED, details=details)


class ForbiddenError(AppException):
    """Exception raised when access is forbidden."""

    def __init__(self, message: str = "Forbidden", details: dict[str, Any] | None = None) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN, details=details)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle application exceptions.

    Args:
        request: The request that caused the exception
        exc: The exception instance

    Returns:
        JSON response with error details
    """
    logger.error(
        "Application exception occurred",
        exc_info=exc,
        path=request.url.path,
        method=request.method,
        status_code=exc.status_code,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "details": exc.details,
            "path": request.url.path,
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions.

    Args:
        request: The request that caused the exception
        exc: The exception instance

    Returns:
        JSON response with error details
    """
    logger.warning(
        "HTTP exception occurred",
        path=request.url.path,
        method=request.method,
        status_code=exc.status_code,
        detail=exc.detail,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "path": request.url.path,
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions.

    Args:
        request: The request that caused the exception
        exc: The exception instance

    Returns:
        JSON response with error details
    """
    logger.error(
        "Unexpected exception occurred",
        exc_info=exc,
        path=request.url.path,
        method=request.method,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "path": request.url.path,
        },
    )

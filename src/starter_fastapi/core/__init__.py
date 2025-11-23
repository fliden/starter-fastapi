"""Core functionality for the application."""

from starter_fastapi.core.config import settings
from starter_fastapi.core.exceptions import AppException, NotFoundError, ValidationError

__all__ = ["AppException", "NotFoundError", "ValidationError", "settings"]

"""Structured logging configuration using structlog."""

import logging
import sys
from typing import Any, cast

import structlog
from structlog.types import EventDict, Processor

from starter_fastapi.core.config import settings


def add_app_context(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    """Add application context to log events."""
    event_dict["app_name"] = settings.app_name
    event_dict["environment"] = settings.environment
    return event_dict


def setup_logging() -> None:
    """Configure structured logging for the application."""
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )

    # Determine processors based on log format
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        add_app_context,
    ]

    # Add format-specific processors
    if settings.log_format == "json":
        processors.extend(
            [
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer(),
            ]
        )
    else:
        # Console format for development
        processors.extend(
            [
                structlog.processors.ExceptionPrettyPrinter(),
                structlog.dev.ConsoleRenderer(colors=True),
            ]
        )

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Get a configured logger instance.

    Args:
        name: Logger name. If None, uses the default logger.

    Returns:
        Configured structlog logger instance.
    """
    return cast("structlog.stdlib.BoundLogger", structlog.get_logger(name))

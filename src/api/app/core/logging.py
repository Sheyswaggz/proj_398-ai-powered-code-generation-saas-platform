"""Structured logging configuration using loguru."""

import sys
from typing import Any

from loguru import logger

from app.core.config import settings


def configure_logging() -> None:
    """Configure loguru logger with structured output and appropriate log levels.

    Sets up logging based on the environment:
    - Development: DEBUG level, colorized console output
    - Staging/Production: INFO level, JSON-structured output

    Includes request ID in logs for distributed tracing when available.
    """
    # Remove default handler
    logger.remove()

    # Determine log level based on environment
    log_level = "DEBUG" if settings.DEBUG else "INFO"

    # Configure format based on environment
    if settings.ENVIRONMENT == "development":
        # Human-readable format for development
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
        logger.add(
            sys.stderr,
            format=log_format,
            level=log_level,
            colorize=True,
            backtrace=True,
            diagnose=True,
        )
    else:
        # JSON-structured format for production/staging
        logger.add(
            sys.stderr,
            format="{message}",
            level=log_level,
            serialize=True,  # Output as JSON
            backtrace=False,
            diagnose=False,
        )

    # Add extra context to all logs
    logger.configure(
        extra={
            "environment": settings.ENVIRONMENT,
            "app_name": settings.APP_NAME,
            "app_version": settings.APP_VERSION,
        }
    )

    logger.info(
        "Logging configured",
        environment=settings.ENVIRONMENT,
        log_level=log_level,
        debug_mode=settings.DEBUG,
    )


def log_request(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    request_id: str | None = None,
) -> None:
    """Log HTTP request with structured context.

    Args:
        method: HTTP method (GET, POST, etc.)
        path: Request path
        status_code: HTTP status code
        duration_ms: Request duration in milliseconds
        request_id: Optional request ID for tracing
    """
    log_context: dict[str, Any] = {
        "http_method": method,
        "http_path": path,
        "http_status": status_code,
        "duration_ms": round(duration_ms, 2),
    }

    if request_id:
        log_context["request_id"] = request_id

    # Use appropriate log level based on status code
    if status_code >= 500:
        logger.error("HTTP request failed", **log_context)
    elif status_code >= 400:
        logger.warning("HTTP client error", **log_context)
    else:
        logger.info("HTTP request completed", **log_context)


def log_exception(
    exc: Exception,
    context: dict[str, Any] | None = None,
    request_id: str | None = None,
) -> None:
    """Log exception with full context and traceback.

    Args:
        exc: The exception to log
        context: Additional context dict
        request_id: Optional request ID for tracing
    """
    log_context: dict[str, Any] = {
        "exception_type": type(exc).__name__,
        "exception_message": str(exc),
    }

    if request_id:
        log_context["request_id"] = request_id

    if context:
        log_context.update(context)

    logger.exception("Unhandled exception occurred", **log_context)


def get_logger_with_context(**context: Any) -> Any:
    """Get a logger instance with bound context for request-scoped logging.

    Args:
        **context: Key-value pairs to bind to the logger

    Returns:
        Logger instance with bound context

    Example:
        >>> log = get_logger_with_context(request_id="abc123", user_id="user456")
        >>> log.info("Processing request")
    """
    return logger.bind(**context)

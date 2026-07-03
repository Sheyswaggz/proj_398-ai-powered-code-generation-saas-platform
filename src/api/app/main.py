"""FastAPI application factory and initialization."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.health import router as health_router
from app.core.config import settings
from app.core.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager for startup and shutdown events.

    Handles:
    - Logging configuration on startup
    - Resource initialization
    - Graceful shutdown and cleanup

    Args:
        app: FastAPI application instance

    Yields:
        None during application runtime
    """
    # Startup
    configure_logging()
    logger.info(
        "Application starting up",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
    )

    # TODO: Initialize database connection pool (added in database task)
    # TODO: Initialize Redis connection (added in caching task)
    # TODO: Initialize background task queue (added in celery task)

    yield

    # Shutdown
    logger.info("Application shutting down")
    # TODO: Close database connections
    # TODO: Close Redis connections
    # TODO: Cleanup background tasks


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI-Powered Code Generation SaaS Platform - Backend API",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )

    # Include routers
    app.include_router(health_router, tags=["Health"])
    # TODO: Include auth router (added in auth task)
    # TODO: Include projects router (added in projects task)
    # TODO: Include code generation router (added in generation task)

    logger.info(
        "FastAPI application created",
        docs_enabled=settings.DEBUG,
        cors_origins=[settings.FRONTEND_URL],
    )

    return app


# Application instance for uvicorn
app = create_app()

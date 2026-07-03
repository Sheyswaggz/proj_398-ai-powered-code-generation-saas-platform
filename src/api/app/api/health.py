"""Health check endpoints for service monitoring."""

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter(prefix="")


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    service: str
    version: str
    timestamp: str


class ReadinessResponse(BaseModel):
    """Readiness check response model with dependency checks."""

    status: str
    checks: dict[str, str]


@router.get("/health", response_model=HealthResponse, status_code=200)
async def health_check() -> dict[str, Any]:
    """Liveness probe endpoint.

    Returns basic service health information without checking dependencies.
    Used by Kubernetes/Docker to determine if the container should be restarted.

    Returns:
        dict: Service health status with name, version, and timestamp
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/ready", response_model=ReadinessResponse, status_code=200)
async def readiness_check() -> dict[str, Any]:
    """Readiness probe endpoint.

    Checks if the service is ready to accept traffic by verifying dependencies.
    Currently returns stubs - real checks will be added in database/redis tasks.

    Returns:
        dict: Readiness status with dependency health checks

    Note:
        Real database and Redis connectivity checks will be implemented in
        their respective tasks. Current implementation returns 'pending' status
        to indicate checks are not yet active.
    """
    # TODO: Add real database connectivity check (database task)
    # Example: await db.execute("SELECT 1")
    database_status = "pending"

    # TODO: Add real Redis connectivity check (redis/caching task)
    # Example: await redis.ping()
    redis_status = "pending"

    return {
        "status": "ready",
        "checks": {
            "database": database_status,
            "redis": redis_status,
        },
    }

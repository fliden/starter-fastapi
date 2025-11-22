"""Health check endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel, Field

from starter_fastapi.core.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Service status")
    app_name: str = Field(..., description="Application name")
    version: str = Field(..., description="Application version")
    environment: str = Field(..., description="Current environment")
    timestamp: datetime = Field(..., description="Current server timestamp")


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check if the service is healthy and running",
)
async def health_check() -> HealthResponse:
    """Perform a health check.

    Returns:
        Health status information
    """
    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
        timestamp=datetime.now(timezone.utc),
    )


@router.get(
    "/ready",
    summary="Readiness check",
    description="Check if the service is ready to accept requests",
)
async def readiness_check() -> dict[str, str]:
    """Check if the service is ready.

    This endpoint can be used by orchestration systems (Kubernetes, etc.)
    to determine if the service is ready to accept traffic.

    Returns:
        Readiness status
    """
    # Add checks for database connections, external services, etc.
    # For now, just return ready
    return {"status": "ready"}


@router.get(
    "/live",
    summary="Liveness check",
    description="Check if the service is alive",
)
async def liveness_check() -> dict[str, str]:
    """Check if the service is alive.

    This endpoint can be used by orchestration systems (Kubernetes, etc.)
    to determine if the service should be restarted.

    Returns:
        Liveness status
    """
    return {"status": "alive"}

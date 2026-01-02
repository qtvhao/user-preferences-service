"""Health check endpoints.

Associated Frontend Files:
  - None (infrastructure endpoint)
"""
from fastapi import APIRouter, status
from pydantic import BaseModel

from ..config import get_settings

router = APIRouter(tags=["Health"])
settings = get_settings()


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    service: str
    version: str


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Basic health check."""
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        version=settings.app_version,
    )


@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def ready():
    """Readiness probe - service is ready to accept traffic."""
    return {"status": "ready"}


@router.get("/health/live", status_code=status.HTTP_200_OK)
async def live():
    """Liveness probe - service is running."""
    return {"status": "alive"}

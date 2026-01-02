"""API routes."""
from .health import router as health_router
from .settings import router as settings_router

__all__ = ["health_router", "settings_router"]

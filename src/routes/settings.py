"""Settings endpoints.

Associated Frontend Files:
  - web/app/src/pages/SettingsPage.tsx (main settings page)
  - web/app/src/pages/settings/NotificationSettings.tsx (notification toggle UI)
  - web/app/src/config/notificationConfig.ts (API calls for notifications)
"""
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas import (
    UserSettingsResponse,
    UserSettingsUpdate,
    NotificationSettingsResponse,
    NotificationPreferencesUpdate,
    ThemeSettingsResponse,
    ThemeSettingsUpdate,
)
from ..services import SettingsService

router = APIRouter(prefix="/api/v1/user-preferences", tags=["User Preferences"])


async def get_user_id(x_user_id: str = Header(None, alias="X-User-ID")) -> str:
    """Extract user ID from header (set by API Gateway after JWT validation)."""
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "UNAUTHORIZED",
                    "message": "User not authenticated",
                }
            },
        )
    return x_user_id


# ============================================
# General Settings Endpoints
# ============================================


@router.get("", response_model=UserSettingsResponse)
async def get_settings(
    user_id: str = Depends(get_user_id),
    db: AsyncSession = Depends(get_db),
) -> UserSettingsResponse:
    """Get user's general settings (language, timezone, locale)."""
    service = SettingsService(db)
    return await service.get_user_settings(user_id)


@router.put("", response_model=UserSettingsResponse)
async def update_settings(
    update: UserSettingsUpdate,
    user_id: str = Depends(get_user_id),
    db: AsyncSession = Depends(get_db),
) -> UserSettingsResponse:
    """Update user's general settings."""
    service = SettingsService(db)
    return await service.update_user_settings(user_id, update)


# ============================================
# Notification Settings Endpoints
# ============================================


@router.get("/notifications", response_model=NotificationSettingsResponse)
async def get_notification_settings(
    user_id: str = Depends(get_user_id),
    db: AsyncSession = Depends(get_db),
) -> NotificationSettingsResponse:
    """Get notification settings with available items and user preferences."""
    service = SettingsService(db)
    return await service.get_notification_settings(user_id)


@router.put("/notifications")
async def update_notification_settings(
    update: NotificationPreferencesUpdate,
    user_id: str = Depends(get_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Update notification preferences."""
    service = SettingsService(db)
    preferences = await service.update_notification_settings(user_id, update)
    return {"preferences": preferences}


# ============================================
# Theme Settings Endpoints
# ============================================


@router.get("/theme", response_model=ThemeSettingsResponse)
async def get_theme_settings(
    user_id: str = Depends(get_user_id),
    db: AsyncSession = Depends(get_db),
) -> ThemeSettingsResponse:
    """Get user's theme settings (mode, accent color)."""
    service = SettingsService(db)
    return await service.get_theme_settings(user_id)


@router.put("/theme", response_model=ThemeSettingsResponse)
async def update_theme_settings(
    update: ThemeSettingsUpdate,
    user_id: str = Depends(get_user_id),
    db: AsyncSession = Depends(get_db),
) -> ThemeSettingsResponse:
    """Update user's theme settings."""
    # Validate mode if provided
    if update.mode and update.mode not in ("light", "dark", "system"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "INVALID_THEME_MODE",
                    "message": "Theme mode must be 'light', 'dark', or 'system'",
                }
            },
        )

    service = SettingsService(db)
    return await service.update_theme_settings(user_id, update)

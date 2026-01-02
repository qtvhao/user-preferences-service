"""Settings service for business logic.

Associated Frontend Files:
  - web/app/src/pages/SettingsPage.tsx (main settings page)
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import UserSettings, NotificationPreferences, ThemeSettings
from ..schemas import (
    UserSettingsResponse,
    UserSettingsUpdate,
    NotificationSettingsResponse,
    NotificationPreferencesUpdate,
    NotificationItem,
    ThemeSettingsResponse,
    ThemeSettingsUpdate,
)


# Default notification items
DEFAULT_NOTIFICATION_ITEMS = [
    NotificationItem(
        key="email",
        label="Email Notifications",
        description="Receive notifications via email",
    ),
    NotificationItem(
        key="push",
        label="Push Notifications",
        description="Receive browser push notifications",
    ),
    NotificationItem(
        key="assignments",
        label="Assignment Updates",
        description="Get notified when assignments change",
    ),
    NotificationItem(
        key="skillUpdates",
        label="Skill Updates",
        description="Get notified about skill taxonomy changes",
    ),
]


class SettingsService:
    """Service for managing user settings."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_settings(self, user_id: str) -> UserSettingsResponse:
        """Get user's general settings."""
        result = await self.db.execute(
            select(UserSettings).where(UserSettings.user_id == user_id)
        )
        settings = result.scalar_one_or_none()

        if settings:
            return UserSettingsResponse.model_validate(settings)

        # Return defaults
        return UserSettingsResponse()

    async def update_user_settings(
        self, user_id: str, update: UserSettingsUpdate
    ) -> UserSettingsResponse:
        """Update user's general settings."""
        result = await self.db.execute(
            select(UserSettings).where(UserSettings.user_id == user_id)
        )
        settings = result.scalar_one_or_none()

        if not settings:
            # Create new settings
            settings = UserSettings(
                user_id=user_id,
                language=update.language or "en",
                timezone=update.timezone or "UTC",
                locale=update.locale or "en-US",
            )
            self.db.add(settings)
        else:
            # Update existing
            if update.language is not None:
                settings.language = update.language
            if update.timezone is not None:
                settings.timezone = update.timezone
            if update.locale is not None:
                settings.locale = update.locale

        await self.db.flush()
        return UserSettingsResponse.model_validate(settings)

    async def get_notification_settings(self, user_id: str) -> NotificationSettingsResponse:
        """Get user's notification preferences."""
        result = await self.db.execute(
            select(NotificationPreferences).where(
                NotificationPreferences.user_id == user_id
            )
        )
        prefs = result.scalar_one_or_none()

        if prefs:
            preferences = {
                "email": prefs.email_enabled,
                "push": prefs.push_enabled,
                "assignments": prefs.assignments_enabled,
                "skillUpdates": prefs.skill_updates_enabled,
            }
        else:
            # Return defaults
            preferences = {
                "email": False,
                "push": True,
                "assignments": False,
                "skillUpdates": True,
            }

        return NotificationSettingsResponse(
            items=DEFAULT_NOTIFICATION_ITEMS,
            preferences=preferences,
        )

    async def update_notification_settings(
        self, user_id: str, update: NotificationPreferencesUpdate
    ) -> dict[str, bool]:
        """Update user's notification preferences."""
        result = await self.db.execute(
            select(NotificationPreferences).where(
                NotificationPreferences.user_id == user_id
            )
        )
        prefs = result.scalar_one_or_none()

        if not prefs:
            prefs = NotificationPreferences(user_id=user_id)
            self.db.add(prefs)

        # Update preferences from the map
        if "email" in update.preferences:
            prefs.email_enabled = update.preferences["email"]
        if "push" in update.preferences:
            prefs.push_enabled = update.preferences["push"]
        if "assignments" in update.preferences:
            prefs.assignments_enabled = update.preferences["assignments"]
        if "skillUpdates" in update.preferences:
            prefs.skill_updates_enabled = update.preferences["skillUpdates"]

        await self.db.flush()

        return {
            "email": prefs.email_enabled,
            "push": prefs.push_enabled,
            "assignments": prefs.assignments_enabled,
            "skillUpdates": prefs.skill_updates_enabled,
        }

    async def get_theme_settings(self, user_id: str) -> ThemeSettingsResponse:
        """Get user's theme settings."""
        result = await self.db.execute(
            select(ThemeSettings).where(ThemeSettings.user_id == user_id)
        )
        theme = result.scalar_one_or_none()

        if theme:
            return ThemeSettingsResponse(
                mode=theme.mode,
                accent_color=theme.accent_color,
            )

        # Return defaults
        return ThemeSettingsResponse()

    async def update_theme_settings(
        self, user_id: str, update: ThemeSettingsUpdate
    ) -> ThemeSettingsResponse:
        """Update user's theme settings."""
        result = await self.db.execute(
            select(ThemeSettings).where(ThemeSettings.user_id == user_id)
        )
        theme = result.scalar_one_or_none()

        if not theme:
            theme = ThemeSettings(
                user_id=user_id,
                mode=update.mode or "system",
                accent_color=update.accentColor or "#3b82f6",
            )
            self.db.add(theme)
        else:
            if update.mode is not None:
                theme.mode = update.mode
            if update.accentColor is not None:
                theme.accent_color = update.accentColor

        await self.db.flush()

        return ThemeSettingsResponse(
            mode=theme.mode,
            accent_color=theme.accent_color,
        )

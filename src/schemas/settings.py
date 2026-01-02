"""Pydantic schemas for settings endpoints."""
from typing import Literal
from pydantic import BaseModel, Field


class UserSettingsResponse(BaseModel):
    """Response schema for user settings."""

    language: str = Field(default="en", description="Language code (e.g., 'en', 'es', 'fr')")
    timezone: str = Field(default="UTC", description="Timezone (e.g., 'UTC', 'America/New_York')")
    locale: str = Field(default="en-US", description="Locale code (e.g., 'en-US', 'es-ES')")

    class Config:
        from_attributes = True


class UserSettingsUpdate(BaseModel):
    """Request schema for updating user settings."""

    language: str | None = Field(default=None, min_length=2, max_length=10)
    timezone: str | None = Field(default=None, max_length=50)
    locale: str | None = Field(default=None, max_length=10)


class NotificationItem(BaseModel):
    """Schema for a notification setting item."""

    key: str = Field(description="Unique key for the notification type")
    label: str = Field(description="Display label")
    description: str = Field(description="Description of the notification type")


class NotificationPreferencesUpdate(BaseModel):
    """Request schema for updating notification preferences."""

    preferences: dict[str, bool] = Field(
        description="Map of notification key to enabled status"
    )


class NotificationSettingsResponse(BaseModel):
    """Response schema for notification settings."""

    items: list[NotificationItem] = Field(
        description="Available notification types"
    )
    preferences: dict[str, bool] = Field(
        description="User's current preferences"
    )


class ThemeSettingsResponse(BaseModel):
    """Response schema for theme settings."""

    mode: Literal["light", "dark", "system"] = Field(
        default="system",
        description="Theme mode"
    )
    accentColor: str = Field(
        default="#3b82f6",
        alias="accent_color",
        description="Primary accent color (hex)"
    )

    class Config:
        from_attributes = True
        populate_by_name = True


class ThemeSettingsUpdate(BaseModel):
    """Request schema for updating theme settings."""

    mode: Literal["light", "dark", "system"] | None = Field(default=None)
    accentColor: str | None = Field(default=None, alias="accent_color")

    class Config:
        populate_by_name = True

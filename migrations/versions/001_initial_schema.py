"""Initial schema for user preferences.

Revision ID: 001
Revises:
Create Date: 2026-01-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # User Settings table
    op.create_table(
        "user_settings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("language", sa.String(10), nullable=False, default="en"),
        sa.Column("timezone", sa.String(50), nullable=False, default="UTC"),
        sa.Column("locale", sa.String(10), nullable=False, default="en-US"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )

    # Notification Preferences table
    op.create_table(
        "notification_preferences",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("email_enabled", sa.Boolean(), nullable=False, default=False),
        sa.Column("push_enabled", sa.Boolean(), nullable=False, default=True),
        sa.Column("assignments_enabled", sa.Boolean(), nullable=False, default=False),
        sa.Column("skill_updates_enabled", sa.Boolean(), nullable=False, default=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )

    # Theme Settings table
    op.create_table(
        "theme_settings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("mode", sa.String(10), nullable=False, default="system"),
        sa.Column("accent_color", sa.String(20), nullable=False, default="#3b82f6"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("theme_settings")
    op.drop_table("notification_preferences")
    op.drop_table("user_settings")

"""Application configuration using pydantic-settings."""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "preferences-service"
    app_version: str = "1.0.0"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8071

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@host.docker.internal:5432/user_preferences"
    database_pool_size: int = 5
    database_max_overflow: int = 10

    # JWT (for token validation - shared with API Gateway)
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

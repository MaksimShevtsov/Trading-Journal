"""Centralized application configuration using Pydantic Settings."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    app_name: str = "Trading Journal"
    debug: bool = False
    log_level: str = "INFO"

    # Trading-Journal-specific settings (placeholders for future stories)
    encryption_key: str = "dev-only-key-never-use-in-production"
    clerk_jwks_url: str = ""
    clerk_webhook_secret: str = ""

    # Admin panel
    admin_enabled: bool = False
    admin_session_secret: str = "change-me-in-production"
    admin_https_only: bool = False

    # Database
    db_driver: str = "postgresql"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "trading_journal"
    db_user: str = "postgres"
    db_password: str = "postgres"

    @property
    def database_url(self) -> str:
        """Build the database connection URL."""
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

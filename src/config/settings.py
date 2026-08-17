"""Global settings and environment variable loading via Pydantic."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "AI Project Template"
    app_env: str = "development"
    debug: bool = True
    api_prefix: str = "/api/v1"


@lru_cache
def get_settings() -> Settings:
    """Returns cached settings instance."""
    return Settings()

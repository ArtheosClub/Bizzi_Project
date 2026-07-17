"""Typed application settings.

Fails fast at startup if a required environment variable is missing —
pydantic-settings raises a ValidationError before the app can serve traffic,
rather than surfacing a confusing failure the first time the value is used.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: str = "development"
    port: int = 8000
    database_url: str


@lru_cache
def get_settings() -> Settings:
    return Settings()

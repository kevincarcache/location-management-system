from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="API_", extra="ignore")

    env: str = "development"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/locations"
    secret_key: str = "change-me-at-least-32-characters"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    bootstrap_on_startup: bool = True
    storefront_slug: str | None = None
    admin_email: str = "admin@example.com"
    admin_password: str = "ChangeMe123!"
    admin_full_name: str = "Platform Admin"
    geocoding_base_url: str = "https://nominatim.openstreetmap.org/search"
    geocoding_user_agent: str = "location-management-system/0.1"
    geocoding_timeout_seconds: int = 10
    geocoding_limit: int = 5
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:3100",
            "http://localhost:5173",
            "http://localhost:4173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3100",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:4173",
        ]
    )

    @field_validator("database_url")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

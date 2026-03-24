from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="API_", extra="ignore")

    env: str = "development"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/locations"
    secret_key: str = "change-me-at-least-32-characters"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    bootstrap_on_startup: bool = True
    admin_email: str = "admin@example.com"
    admin_password: str = "ChangeMe123!"
    admin_full_name: str = "Platform Admin"
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5173",
        ]
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

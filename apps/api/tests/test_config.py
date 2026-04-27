from app.core.config import Settings


def test_database_url_uses_psycopg_driver_for_plain_postgres_urls() -> None:
    settings = Settings(database_url="postgresql://user:pass@example.com:5432/locations")

    assert settings.database_url == "postgresql+psycopg://user:pass@example.com:5432/locations"


def test_database_url_keeps_explicit_driver() -> None:
    settings = Settings(database_url="postgresql+psycopg://user:pass@example.com:5432/locations")

    assert settings.database_url == "postgresql+psycopg://user:pass@example.com:5432/locations"

# API

Backend FastAPI para autenticación de admin, gestión de localizaciones y futuras importaciones CSV.

## Scripts sugeridos
- `uv sync`
- `uv run uvicorn app.main:app --reload`
- `uv run alembic upgrade head`
- `uv run python -m app.scripts.bootstrap_db`
- `uv run pytest`

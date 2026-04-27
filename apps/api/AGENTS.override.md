# API Scope Guide

## Local Rules
- Keep FastAPI routes thin. HTTP translation belongs in routes, orchestration belongs in services.
- Services serialize schema responses; repositories return persistence objects or query results, not API payloads.
- Repositories may `flush()`, but they must not own transaction boundaries.
- Any SQLAlchemy model change must ship with an Alembic migration in `apps/api/alembic/versions`.
- Admin routes must use the reusable admin auth dependency.
- External HTTP integrations must go through provider or adapter modules, not direct inline calls from routes.

## Anti-patterns
- Serializing API response shapes inside repositories.
- Calling providers or raw network clients from route handlers.
- Performing auth checks ad hoc inside route bodies instead of reusable dependencies.
- Mixing preview/import business rules directly into CSV transport parsing when a service helper can isolate them.

## Validation
- `cd apps/api && UV_CACHE_DIR=.uv-cache uv run ruff check app tests`
- `cd apps/api && UV_CACHE_DIR=.uv-cache uv run pytest`
- `cd apps/api && UV_CACHE_DIR=.uv-cache uv run alembic upgrade head` when models or migrations change

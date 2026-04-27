---
name: backend-fastapi-crud
description: Use when implementing or changing FastAPI routes, services, repositories, schemas, models, migrations, or backend tests in apps/api.
---

# Backend FastAPI CRUD

## Purpose
- Implement or modify backend CRUD behavior following the repository's canonical layering.

## Use when
- Touching routes, services, repositories, schemas, models or backend tests.

## Workflow
1. Identify the boundary being changed first: route, service, repository, schema, model or test.
2. Read the adjacent canonical modules before editing:
   - `apps/api/app/api/routes`
   - `apps/api/app/services`
   - `apps/api/app/repositories`
3. Keep route handlers thin:
   - parse request
   - call service
   - translate domain failures to HTTP errors
4. Put orchestration, transaction ownership and response serialization in services.
5. Keep repositories focused on persistence reads and writes; use `flush()` when needed, never `commit()`.
6. If a model or schema changes, check whether:
   - Alembic migration is required
   - seeds or imports depend on that shape
   - shared contracts in `packages/types` must be updated
7. Add or update tests nearest to the changed behavior before closing the task.

## MCP and references
- Prefer Git or filesystem context to inspect nearby patterns before introducing a new one.
- If the change affects database behavior, pair this skill with `migrations-safe`.
- If the change crosses consumers, pair this skill with `testing-matrix`.

## Common mistakes to avoid
- Writing business logic directly in route handlers.
- Returning API payload dicts from repositories.
- Introducing a new auth pattern instead of the reusable admin dependency.
- Changing persistence shape without checking migrations, seeds and shared contracts.

## Required validation
- `cd apps/api && UV_CACHE_DIR=.uv-cache uv run ruff check app tests`
- `cd apps/api && UV_CACHE_DIR=.uv-cache uv run pytest`
- `cd apps/api && UV_CACHE_DIR=.uv-cache uv run alembic upgrade head` if models changed

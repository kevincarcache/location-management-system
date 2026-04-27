---
name: migrations-safe
description: Use when editing SQLAlchemy models, Alembic migrations, or schema-dependent seeds and you need to preserve database reproducibility and upgrade safety.
---

# Migrations Safe

## Purpose
- Apply schema changes without losing reproducibility.

## Use when
- Editing SQLAlchemy models, seeds that depend on schema, or Alembic config.

## Workflow
1. Confirm whether the change is:
   - schema-changing
   - seed-dependent
   - contract-affecting
2. Update SQLAlchemy models first, then create or adjust the Alembic migration in `apps/api/alembic/versions`.
3. Check whether the change affects:
   - admin seed data
   - CSV import assumptions
   - public or admin response contracts
4. Validate the upgrade path locally.
5. If the migration is destructive or risky, document the compatibility concern in the final handoff.

## MCP and references
- Pair this skill with Postgres MCP when you need to inspect the live schema, seed rows or import output after a migration.
- Pair with `backend-fastapi-crud` when the migration accompanies service or route changes.

## Common mistakes to avoid
- Changing models without a migration.
- Treating seed or import breakage as an unrelated follow-up.
- Forgetting to validate the upgrade path after editing an existing migration.

## Required validation
- `cd apps/api && UV_CACHE_DIR=.uv-cache uv run alembic upgrade head`
- `cd apps/api && UV_CACHE_DIR=.uv-cache uv run pytest`

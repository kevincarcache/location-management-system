---
name: postgres-debugging
description: Use when debugging database-backed issues in this project, especially schema drift, seed data, imports, migration outcomes, or inconsistencies between the API and PostgreSQL state.
---

# Postgres Debugging

## Purpose
- Investigate database-backed bugs without guessing from application code alone.

## Use when
- Debugging migrations, seed data, CSV imports, missing rows, schema drift or API responses that do not match expected database state.

## Workflow
1. Identify whether the issue is schema, data, import, or query-shape related.
2. Inspect the relevant model, migration and service before querying the database.
3. Use Postgres MCP when available to inspect:
   - table shape
   - relevant rows
   - seed output
   - import side effects
4. Compare database truth against:
   - SQLAlchemy models
   - Alembic migration history
   - service/repository query code
5. If the problem spans API behavior too, pair this skill with `backend-fastapi-crud` or `integration-triage`.

## Common mistakes to avoid
- Treating stale seed data as an application bug without checking DB state.
- Debugging import output only from logs without inspecting inserted rows and errors.
- Changing migrations before confirming whether the issue is actually bad data or bad queries.

## Required validation
- `cd apps/api && UV_CACHE_DIR=.uv-cache uv run alembic upgrade head` when schema is involved
- `cd apps/api && UV_CACHE_DIR=.uv-cache uv run pytest` when behavior changes follow from the investigation

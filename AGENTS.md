# Repository Operating Guide

## Purpose
- This repository hosts a location-management platform with three executable apps:
  - `apps/api`: FastAPI backend, auth, seeds, migrations, imports
  - `apps/admin`: internal Vue + Vuetify admin
  - `apps/web`: public Nuxt + Vuetify storefront
- The repo is optimized for small, verifiable changes. Do not widen scope unless the current task explicitly requires it.

## Sources of Truth
- Database schema and behavior: `apps/api/app/models`, `apps/api/alembic/versions`
- Backend request/response contracts: FastAPI schemas in `apps/api/app/schemas`
- Shared TypeScript contracts: `packages/types/src/index.ts`
- Public storefront data orchestration: `apps/web/composables/useStorefrontPage.ts`
- Admin API client boundary: `apps/admin/src/lib/admin-api.ts`

## Global Rules
- If you change SQLAlchemy models, also add/update Alembic migrations and run `uv run alembic upgrade head`.
- Admin routes must require auth. Do not add admin endpoints without the reusable admin auth dependency.
- Repositories do not own transaction boundaries. They may `flush()`, but services own `commit()` and `rollback()`.
- Do not redefine shared API contracts inside app-local files when the contract belongs in `packages/types`.
- API wire format stays `snake_case`. Client-facing models may use `camelCase`, but the mapping must be explicit and centralized.
- Put orchestration in boundaries dedicated to orchestration, not inside presentation components or persistence helpers.
- If logic needs independent tests, extract it to a pure helper or service boundary instead of hiding it inside framework lifecycle code.
- Prefer extending existing patterns over creating a parallel abstraction.

## Validation Matrix
| Change type | Required validation |
|---|---|
| Backend Python code | `cd apps/api && UV_CACHE_DIR=.uv-cache uv run ruff check app tests` and `cd apps/api && UV_CACHE_DIR=.uv-cache uv run pytest` |
| Models or migrations | Backend validation plus `cd apps/api && UV_CACHE_DIR=.uv-cache uv run alembic upgrade head` |
| Admin code | `pnpm --filter @lms/admin lint`, `pnpm --filter @lms/admin test`, `pnpm --filter @lms/admin build` |
| Web code | `pnpm --filter @lms/web lint`, `pnpm --filter @lms/web test`, `pnpm --filter @lms/web build` |
| Shared contracts | Validate every consumer touched by the contract change |
| CI/workflow changes | Run the relevant commands locally where feasible and ensure the workflow mirrors them |
| Docs-only changes | Manual consistency review of referenced commands and paths |

## Definition of Done
- The modified layer passes the validation matrix above.
- Contracts remain aligned between backend and consumers.
- No new parallel pattern was introduced where a canonical one already exists.
- If behavior changed, tests or documentation changed with it.
- If a limitation remains, it is called out explicitly in the final handoff.

## Anti-patterns
- Adding new admin routes without auth.
- Calling `commit()` in repository helpers.
- Defining duplicate TS contract types in app-local files.
- Hiding data flow in framework lifecycle hooks when a dedicated orchestration boundary already exists.
- Using undocumented one-off scripts or workflows when a standard command exists.
- Editing generated directories (`.nuxt`, `.output`, `dist`, caches) as if they were source.

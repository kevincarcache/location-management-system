---
name: testing-matrix
description: Use when a change touches code, contracts, CI, or docs and you need to determine the correct validation commands before considering the task done.
---

# Testing Matrix

## Purpose
- Select the correct validation commands for a change before closing it.

## Use when
- Any code, CI, contract or docs change is made.

## Workflow
1. Map the touched files to impacted layers before choosing commands.
2. Run the narrowest relevant checks first, then expand to all affected consumers.
3. If a change touches shared contracts, validate every consumer instead of only the edited package.
4. If a change touches schema or imports, include migration validation.
5. If a change touches visual or route-driven behavior, add a browser sanity pass when feasible.

## Command selection
- Backend only:
  - `cd apps/api && UV_CACHE_DIR=.uv-cache uv run ruff check app tests`
  - `cd apps/api && UV_CACHE_DIR=.uv-cache uv run pytest`
- Backend schema or migrations:
  - backend commands above
  - `cd apps/api && UV_CACHE_DIR=.uv-cache uv run alembic upgrade head`
- Web:
  - `pnpm --filter @lms/web lint`
  - `pnpm --filter @lms/web test`
  - `pnpm --filter @lms/web build`
- Admin:
  - `pnpm --filter @lms/admin lint`
  - `pnpm --filter @lms/admin test`
  - `pnpm --filter @lms/admin build`
- Shared contracts:
  - validate each touched consumer after contract changes

## MCP and references
- Pair with Playwright MCP for UI sanity when route state, hydration, auth or responsive behavior changes.
- Pair with Git MCP when the impacted area is unclear and you need to inspect adjacent patterns or recent regressions.

## Common mistakes to avoid
- Stopping at lint when build or tests exist for that layer.
- Validating only the edited app after changing shared contracts.
- Treating migration checks as optional after schema changes.

## Output
- End with a concise list of commands run, commands intentionally skipped and remaining validation risk.

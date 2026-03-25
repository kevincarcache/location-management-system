---
name: admin-vue-vuetify
description: Use when modifying the Vue and Vuetify admin app, especially auth flow, routing, session state, navigation, forms, or the admin HTTP boundary in apps/admin.
---

# Admin Vue Vuetify

## Purpose
- Modify the admin app while keeping auth, routing and API consumption consistent.

## Use when
- Editing `apps/admin` pages, session flow, navigation or admin HTTP integration.

## Workflow
1. Decide whether the change belongs in:
   - `src/pages` for route-level orchestration and submit flows
   - `src/components` for reusable UI
   - `src/lib/admin-api.ts` for HTTP
   - `src/stores` for shared persistent state
2. Keep auth and session flow in shared state plus router guards; do not recreate per-page access checks.
3. When a form grows beyond one page or repeats transformation logic, extract helpers to `src/lib` or state to `src/stores`.
4. Import shared API contracts from `@lms/types` unless the type is purely local UI state.
5. Before adding a new page-level pattern, compare with the existing page files in `src/pages`.
6. Treat the admin as `Vuetify-first`: prefer Vuetify components, defaults, theme tokens and documented patterns before adding custom wrappers or bespoke styling.

## MCP and references
- Pair this skill with Playwright MCP for auth, navigation, form and responsive debugging.
- Consult `vuetify_mcp` when the correct Vuetify component API, composition pattern, theming approach or best practice is unclear.
- Use Git or filesystem context to inspect existing page and store patterns before introducing new helpers.
- Pair with `testing-matrix` whenever the change crosses auth, routes and API consumers.

## Common mistakes to avoid
- Fetching directly from page or component files instead of `admin-api.ts`.
- Reading `localStorage` at module import time.
- Mixing auth/session state with transient form state.
- Replacing a solvable Vuetify pattern with a custom abstraction before checking `vuetify_mcp` or existing app patterns.
- Leaving page-specific transformation logic buried inside template-heavy `.vue` files.

## Required validation
- `pnpm --filter @lms/admin lint`
- `pnpm --filter @lms/admin test`
- `pnpm --filter @lms/admin build`

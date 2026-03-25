# Admin Scope Guide

## Local Rules
- `src/lib/admin-api.ts` is the only approved HTTP boundary.
- Session state must not read or write `localStorage` at module import time.
- Route protection belongs in router guards or shared auth state, not in ad hoc per-page checks.
- Page components own route-level orchestration, data loading and submit flows.
- Reusable UI or field logic should move to `src/components`, `src/lib` or `src/stores` once it would otherwise be duplicated.
- Shared contracts should come from `@lms/types` unless the type is purely local UI state.

## Anti-patterns
- Fetching directly from page or component files when `admin-api.ts` can own the call.
- Mixing persistent auth state with page-local form state.
- Hiding testable transformation logic inside template-heavy page components.

## Validation
- `pnpm --filter @lms/admin lint`
- `pnpm --filter @lms/admin test`
- `pnpm --filter @lms/admin build`

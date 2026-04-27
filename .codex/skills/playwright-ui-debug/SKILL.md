---
name: playwright-ui-debug
description: Use when debugging browser-visible issues in the admin or storefront, especially hydration, auth flows, navigation, responsive layout, and map-driven interactions.
---

# Playwright UI Debug

## Purpose
- Reproduce UI bugs in a real browser flow instead of reasoning only from source code.

## Use when
- Investigating layout regressions, hydration mismatch, auth flows, route/query state, responsive issues, map interactions or end-to-end breakages.

## Workflow
1. Reproduce the issue in the narrowest realistic flow first.
2. Capture the failure using:
   - browser snapshot or screenshot
   - console errors
   - network requests when relevant
3. Decide whether the root cause is:
   - markup or hydration mismatch
   - route or query state
   - API or data issue
   - styling or layout issue
4. Once narrowed down, inspect the owning boundary:
   - storefront orchestration
   - admin page, store or router
   - API response or auth
5. After the fix, rerun the exact browser flow that originally failed.

## MCP and references
- Pair with Playwright MCP for browser automation.
- Pair with `frontend-storefront-vuetify` or `admin-vue-vuetify` depending on the affected app.
- Pair with `integration-triage` when the UI bug may actually come from API or DB state.

## Common mistakes to avoid
- Assuming a visual bug is CSS-only without checking console and network signals.
- Verifying only the initial render when the bug appears after hydration or interaction.
- Fixing symptoms in components when the real issue is route state or backend data.

## Required validation
- Rerun the failing browser flow after the fix.
- Run the relevant app validation commands from `testing-matrix`.

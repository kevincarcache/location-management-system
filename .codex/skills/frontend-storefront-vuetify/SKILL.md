---
name: frontend-storefront-vuetify
description: Use when editing the Nuxt and Vuetify public storefront in apps/web, including layout, components, composables, URL state, and shared storefront behavior.
---

# Frontend Storefront Vuetify

## Purpose
- Change the public storefront without reintroducing parallel data-loading patterns.

## Use when
- Editing `apps/web` layout, components, composables or shared storefront behavior.

## Workflow
1. Decide whether the change belongs in:
   - `useStorefrontPage.ts` for orchestration, route/query sync and fetch state
   - `storefront-state.ts` or another pure helper for testable business logic
   - a component for presentation and emitted events
2. Keep shareable URL state centralized in the page orchestration layer.
3. If a component starts owning filtering, selection or hydration-sensitive logic, extract that logic before expanding the component further.
4. Use Vuetify for structure and stateful UI first; keep custom CSS focused on branding, map integration or targeted polish.
5. If SSR or hydration can change, validate the server/client shape mentally before changing markup or route-bound state.
6. If contracts change, import shared types from `@lms/types` instead of redefining local versions.

## MCP and references
- Pair this skill with Playwright MCP when validating layout, hydration, responsive bugs or query-state flows.
- Use Nuxt docs MCP when a Nuxt behavior or deployment detail is unclear.
- Use filesystem or Git context to compare against `StorefrontHeader.vue`, `StorefrontHero.vue` and `useStorefrontPage.ts`.

## Common mistakes to avoid
- Reintroducing a second fetch/orchestration pattern.
- Reading or mutating route query state from multiple components.
- Solving a Vuetify layout issue with a competing manual layout system.
- Hiding testable selection/filter logic inside a large component.

## Required validation
- `pnpm --filter @lms/web lint`
- `pnpm --filter @lms/web test`
- `pnpm --filter @lms/web build`

# Web Scope Guide

## Local Rules
- `composables/useStorefrontPage.ts` is the canonical data orchestration layer for the public storefront.
- Do not introduce a second fetch or composable pattern for the same store config and locations flow unless replacing the canonical one.
- Shared URL state belongs in the page orchestration layer.
- Components should focus on presentation and emitted events; extracted state logic belongs in composables or pure helpers.
- Web is `Vuetify-first`. Prefer Vuetify primitives, theme tokens, defaults and documented component patterns over bespoke UI abstractions or parallel layout systems.
- When a Nuxt runtime, routing, hydration, `useAsyncData`, or deployment behavior is unclear, consult `nuxt_mcp`.
- When the correct Vuetify pattern, API or best practice is unclear, consult `vuetify_mcp` before inventing a custom solution.
- Shared contracts should come from `@lms/types` unless the type is purely local presentation state.

## Anti-patterns
- Reading route query state directly from multiple components.
- Hiding filtering, selection or URL sync logic inside presentational components.
- Reintroducing HTML/CSS layout systems that fight Vuetify for the same structure.

## Validation
- `pnpm --filter @lms/web lint`
- `pnpm --filter @lms/web test`
- `pnpm --filter @lms/web build`

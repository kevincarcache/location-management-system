# Web Scope Guide

## Local Rules
- `composables/useStorefrontPage.ts` is the canonical data orchestration layer for the public storefront.
- Do not introduce a second fetch or composable pattern for the same store config and locations flow unless replacing the canonical one.
- Shared URL state belongs in the page orchestration layer.
- Components should focus on presentation and emitted events; extracted state logic belongs in composables or pure helpers.
- Use Vuetify-first structure for layout and stateful UI, and keep custom CSS focused on branding or technical integration details.
- Shared contracts should come from `@lms/types` unless the type is purely local presentation state.

## Anti-patterns
- Reading route query state directly from multiple components.
- Hiding filtering, selection or URL sync logic inside presentational components.
- Reintroducing HTML/CSS layout systems that fight Vuetify for the same structure.

## Validation
- `pnpm --filter @lms/web lint`
- `pnpm --filter @lms/web test`
- `pnpm --filter @lms/web build`

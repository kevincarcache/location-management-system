---
name: integration-triage
description: Use when a bug or task crosses backend, admin, web, contracts, or data state and you need to identify the owning boundary before implementing a fix.
---

# Integration Triage

## Purpose
- Localize cross-layer failures before editing multiple parts of the repo blindly.

## Use when
- A bug spans backend, admin, storefront, shared types, auth, migrations or seeded data.

## Workflow
1. State the failing symptom in one sentence.
2. Identify the first observable boundary where the failure appears:
   - database state
   - backend response
   - shared contract mapping
   - admin behavior
   - storefront behavior
3. Use the smallest useful tool mix:
   - Git or filesystem for code-path inspection
   - Postgres MCP for schema or data truth
   - Playwright MCP for browser reproduction
   - Fetch or docs tools for external contract clarification
4. Decide the owner of the fix before editing:
   - backend
   - shared types
   - admin
   - storefront
5. Only after the owner is clear, switch to the specialized skill for that layer.

## Common mistakes to avoid
- Editing both frontend and backend before confirming the real owner.
- Treating shared contract drift as a UI-only bug.
- Skipping DB or browser inspection when the failure signal already points there.

## Required validation
- Reproduce the failure before the fix.
- Validate the owning layer after the fix.
- Re-run one cross-layer sanity check for the original symptom.

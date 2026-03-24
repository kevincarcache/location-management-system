# Agent Execution Guide

## Purpose
- Define clear ownership for contributors or agents working on the Location Management System in parallel.
- Reduce overlap, avoid accidental rework, and keep interfaces aligned across backend, admin, and public web.

## Team Topology

### Agent 1: Platform / Monorepo
- Owns repository bootstrap and shared development ergonomics.
- Responsibilities:
  - create monorepo structure
  - configure `pnpm workspaces` and `turbo`
  - set up root scripts, formatting, linting, and environment conventions
  - add Docker and local development defaults
  - define shared package conventions

### Agent 2: Backend / API
- Owns the Python backend and persistence layer.
- Responsibilities:
  - implement `FastAPI` project structure
  - define models and migrations
  - build admin auth
  - build public and admin location endpoints
  - implement CSV import pipeline
  - add backend tests

### Agent 3: Admin Frontend
- Owns the operational interface for internal users.
- Responsibilities:
  - build the `Vue 3 + Vite + Vuetify` admin app
  - implement login flow and protected navigation
  - build location CRUD screens
  - build the CSV import user flow
  - apply the admin visual system and theming

### Agent 4: Public Web
- Owns the customer-facing locator experience.
- Responsibilities:
  - build the `Nuxt` store-locator UI
  - integrate search, filters, sidebar, and map
  - synchronize selected location between list and map
  - support responsive layouts and shareable URLs
  - deliver a product-grade presentation layer

### Agent 5: QA / Integration
- Owns cross-app validation and release readiness.
- Responsibilities:
  - validate API contracts across consumers
  - configure end-to-end tests
  - verify seed data and startup flows
  - catch integration issues across apps
  - maintain a release-readiness checklist

## Collaboration Rules
- Each agent owns its scope and should not overwrite unrelated work from other agents.
- Shared contracts must be agreed before downstream implementation diverges.
- Changes in `packages/*` require coordination with affected app owners.
- Backend should expose stable API contracts for both frontends.
- Any data model change must include:
  - migration updates
  - contract updates
  - seed updates when needed
  - minimum test coverage

## Recommended Delivery Order
1. Platform sets up the monorepo, tooling, and local environment.
2. Backend defines the schema, auth, and core endpoints.
3. Admin frontend consumes auth and CRUD endpoints.
4. Backend finalizes CSV import behavior and reporting.
5. Public web consumes the public API and completes the store-locator experience.
6. QA validates end-to-end flows and closes integration gaps.

## Key Handoffs
- Platform to Backend/Admin/Web:
  - workspace structure
  - shared scripts
  - environment conventions
- Backend to Admin/Web:
  - API contract
  - auth flow
  - data shape for locations
  - import job response shape
- QA to all teams:
  - integration bugs
  - missing edge cases
  - release blockers

## Deliverables by Agent

### Platform
- Executable monorepo skeleton
- Shared tooling and documented startup flow

### Backend
- FastAPI service with migrations, auth, seed, CRUD, import pipeline, and tests

### Admin Frontend
- Usable admin app for login, location management, and CSV imports

### Public Web
- Public locator app with search, list, map, filters, and responsive polish

### QA / Integration
- Minimum E2E suite
- Smoke-test checklist
- Release validation notes

## Definition of Done
- Seeded admin can log in in deployed environments.
- Locations can be created manually or through CSV.
- Public frontend reflects active locations from the backend.
- List and map interactions remain synchronized.
- Visual design is cohesive and product-ready.
- Local setup is reproducible and documented.

## Working Assumptions
- The system is single-organization per deployment in v1.
- The admin seed creates the first admin user only.
- CSV import is a first-class feature in v1.
- The public map stack is `MapLibre + OpenStreetMap`.
- Product polish matters as much as basic functionality for the initial release.

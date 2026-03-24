# Location Management System Plan

## Product Goal
- Build a reusable Location Management System for different business types: branches, nearby events, recycling points, academies, and technical service centers.
- Let administrators manage locations in an admin panel and publish them to a public-facing map experience.
- Deliver a polished product feel, not a demo, with a custom visual identity and a Vuetify theme that moves away from default Material Design colors.

## Target Architecture
- Monorepo managed with `pnpm workspaces` and `turbo`.
- Primary apps:
  - `apps/api`: Python backend with `FastAPI`
  - `apps/web`: public-facing `Nuxt` application
  - `apps/admin`: admin panel built with `Vue 3 + Vite + Vuetify`
- Shared packages:
  - `packages/ui`: shared tokens, theme primitives, and reusable components when beneficial
  - `packages/types`: shared contracts and typed API models
  - `packages/config`: shared linting, TypeScript, and build configuration
- Data layer:
  - `PostgreSQL` as the primary database
  - `SQLAlchemy 2.x`, `Alembic`, `Pydantic v2`, `psycopg`
- Local development:
  - `docker compose` for `postgres`
  - optional API container for full local parity
- Public map stack:
  - `MapLibre + OpenStreetMap`

## Core Functional Model

### Main Entity: `Location`
- `id`
- `slug`
- `name`
- `business_type`
- `status`
- `description_short`
- `description_long`
- `address_line_1`
- `address_line_2`
- `city`
- `region`
- `country`
- `postal_code`
- `latitude`
- `longitude`
- `phone`
- `email`
- `website`
- `opening_hours`
- `services` or `tags`
- `featured`
- `visible_from`
- `visible_until`
- `external_id`
- `created_at`
- `updated_at`

### Supporting Entities
- `AdminUser`
- `LocationImportJob`
- `LocationImportRowError`

### Business Flexibility
- The system is multi-category and generic by design.
- `business_type` must be configurable so the same product can be adapted to different business contexts without changing the core data model.
- Multi-tenant support is out of scope for v1. Each deployment serves a single organization.

## Backend Plan

### Modules
- `auth`
- `locations`
- `imports`
- `taxonomy`
- `health`

### Authentication
- Custom auth for admin users.
- Email/password login.
- Access token + refresh token flow using JWT.
- Initial seeded admin user created from environment variables or a bootstrap command.
- Production seed focuses on the initial admin account only.

### Public API
- `GET /api/public/locations`
  - supports search by name, city, or address
  - supports filtering by `business_type`, tags, city, and active status
  - supports geospatial filtering for nearby searches
- `GET /api/public/locations/:slug`
  - returns location detail for public rendering
- Optional geospatial support:
  - radius-based or bounding-box filtering when needed for map view performance

### Admin API
- `POST /api/admin/auth/login`
- `POST /api/admin/auth/refresh`
- `GET /api/admin/locations`
- `POST /api/admin/locations`
- `PATCH /api/admin/locations/:id`
- `DELETE /api/admin/locations/:id`
- `POST /api/admin/imports/locations/csv`
- `GET /api/admin/imports/:id`

### CSV Import
- Upload CSV from the admin panel.
- Validate required columns before import.
- Process rows idempotently using `external_id` or a fallback matching strategy.
- Track import job summaries and row-level errors.
- Support:
  - template download
  - preview validation
  - create/update/reject counts

### CSV Contract
- Required columns:
  - `external_id`
  - `name`
  - `business_type`
  - `address_line_1`
  - `city`
  - `country`
  - `latitude`
  - `longitude`
- Optional columns:
  - contact fields
  - opening hours
  - tags or services

## Public Frontend Plan

### Stack
- `Nuxt` latest stable release
- SSR or hybrid rendering
- `MapLibre` for map rendering

### UX Structure
- Left sidebar with a searchable, filterable list of locations
- Top search bar for quick lookup
- Right-side map panel
- Synchronized interactions between list items and map markers
- On selection:
  - center the map
  - highlight the selected card
  - highlight the selected pin

### Required Behaviors
- Search by name, city, or address
- Filter by business type
- Display empty states and API error states cleanly
- Persist state in query params for shareable deep links
- Render responsively on desktop and mobile

### Product Feel
- Use a custom palette distinct from default Material colors
- Visual design should feel like a production product, not a generic prototype
- Focus on clarity, trust, and usability

## Admin Frontend Plan

### Stack
- `Vue 3 + Vite + Vuetify`

### Initial Sections
- Login
- Basic dashboard
- Locations list
- Create/edit location form
- CSV import flow
- Admin session or profile area

### CSV Flow
- Download CSV template
- Upload file
- Preview validation feedback
- Confirm import
- Show import results:
  - created rows
  - updated rows
  - rejected rows

### Design Direction
- Keep the UI clear and operationally efficient
- Define a custom Vuetify theme with brand-oriented colors
- Treat the admin as a real internal tool, not a temporary back office

## Implementation Phases

### Phase 1: Monorepo Bootstrap
- Create workspace structure
- Configure `pnpm`, `turbo`, shared config, and scripts
- Add Docker and environment templates
- Establish CI baseline

### Phase 2: Backend Foundation
- Implement FastAPI app structure
- Create database schema and initial migrations
- Add admin auth
- Add `Location` model and CRUD foundation
- Add admin seed flow

### Phase 3: Admin App
- Build admin shell
- Implement login and protected routes
- Build CRUD screens for locations
- Apply shared visual system and theme

### Phase 4: CSV Imports
- Implement backend import pipeline
- Build admin CSV workflow
- Add validation and import result reporting

### Phase 5: Public Locator
- Build Nuxt store-locator experience
- Integrate map, list, search, filters, and selection sync
- Add query-param persistence and responsive behavior

### Phase 6: Hardening
- Add representative seed data
- Expand tests and E2E coverage
- Polish product presentation
- Close integration gaps for initial deployment

## Testing and Acceptance

### Backend
- Unit tests for validation, auth, and import parsing
- API tests for:
  - login
  - refresh token flow
  - location CRUD
  - CSV import

### Admin
- Form tests for critical fields and validation
- Login flow coverage
- CSV import flow coverage

### Public Web
- Search behavior
- Location selection behavior
- List/map synchronization
- Persistent query params

### End-to-End
- Seeded admin can log in
- Admin can create a location manually
- Admin can import locations via CSV
- Imported or created locations appear on the public frontend

## Acceptance Criteria
- A seeded admin user can access the admin in deployed environments.
- Locations can be created manually or imported through CSV.
- Public frontend displays active locations from the API.
- Map and list stay synchronized during interaction.
- The visual system feels consistent and product-ready.
- The full solution can run locally with repeatable setup steps.

## Assumptions and Defaults
- `pnpm + Turbo` is the default monorepo tooling.
- Authentication is implemented in-house for v1.
- The public map uses `MapLibre + OpenStreetMap`.
- `Nuxt` powers the public site and `Vue 3 + Vuetify` powers the admin.
- No mobile app is included in v1.
- No multi-organization support is included in v1.

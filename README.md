# Location Management System

Monorepo base para un Location Management System genérico con backend en FastAPI, frontend público en Nuxt y panel de administración en Vue 3 + Vuetify.

## Apps
- `apps/api`: API, auth, seeds y lógica de importación
- `apps/web`: experiencia pública tipo store locator
- `apps/admin`: panel de administración

## Packages
- `packages/config`: configuraciones compartidas
- `packages/types`: contratos y tipos compartidos
- `packages/ui`: tokens y primitivas de diseño compartidas

## Requisitos
- `pnpm` 10+
- `node` 20+
- `python` 3.12+
- `uv` 0.10+
- `docker` y `docker compose`

## Inicio rápido
1. Copia `.env.example` a `.env`.
2. Levanta PostgreSQL con `docker compose up -d`.
3. Instala dependencias de frontend con `pnpm install`.
4. Sincroniza dependencias Python con `cd apps/api && uv sync`.
5. Aplica migraciones con `cd apps/api && uv run alembic upgrade head`.
6. Ejecuta los proyectos con `pnpm dev`.

## URLs locales
- Web pública: `http://localhost:3000`
- Admin: `http://localhost:5173`
- API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

## Credenciales seed
- Email: `admin@example.com`
- Password: `ChangeMe123!`

## Scripts raíz
- `pnpm dev`
- `pnpm dev:api`
- `pnpm dev:web`
- `pnpm dev:admin`
- `pnpm build`
- `pnpm lint`
- `pnpm typecheck`
- `pnpm test`
- `pnpm test:e2e`

## End-to-end
1. Instala navegadores de Playwright:
   - `pnpm exec playwright install`
2. Ejecuta la suite:
   - `pnpm test:e2e`

## Estado actual
- Fase 1 del monorepo creada
- Estructura inicial del backend FastAPI lista
- Shells iniciales para Nuxt y Vue/Vuetify creados
- Configuración base de Docker y entornos incluida
- Locator público conectado a API real con MapLibre
- Flujo admin de importación CSV con preview y confirmación
- Cobertura E2E inicial para login, creación manual e importación CSV

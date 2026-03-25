# Location Management System

Monorepo para administrar y publicar localizaciones comerciales con backend en FastAPI, storefront público en Nuxt y panel de administración en Vue + Vuetify.

## Workspace
- `apps/api`: API, auth, seeds, importación CSV, migraciones
- `apps/admin`: panel de operación interna
- `apps/web`: storefront público y mapa
- `packages/types`: contratos TypeScript compartidos
- `packages/ui`: tokens visuales compartidos ligeros
- `packages/config`: configuración TypeScript compartida

## Requisitos
- `pnpm` 10+
- `node` 20+
- `python` 3.12+
- `uv`
- `docker compose`

## Inicio rápido
1. Copia `.env.example` a `.env`.
2. Levanta PostgreSQL con `docker compose up -d`.
3. Instala dependencias JS con `pnpm install`.
4. Sincroniza Python con `cd apps/api && uv sync`.
5. Aplica migraciones con `cd apps/api && UV_CACHE_DIR=.uv-cache uv run alembic upgrade head`.
6. Inicia las apps con `pnpm dev`.

## URLs locales
- Web pública: `http://localhost:3000`
- Admin: `http://localhost:5173`
- API: `http://localhost:8000`
- OpenAPI: `http://localhost:8000/docs`

## Credenciales seed
- Email: `admin@example.com`
- Password: `ChangeMe123!`

## Scripts raíz
- `pnpm dev`
- `pnpm build`
- `pnpm lint`
- `pnpm typecheck`
- `pnpm test`
- `pnpm test:e2e`

## Validación rápida
- Backend: `cd apps/api && UV_CACHE_DIR=.uv-cache uv run pytest`
- Web: `pnpm --filter @lms/web lint && pnpm --filter @lms/web test && pnpm --filter @lms/web build`
- Admin: `pnpm --filter @lms/admin lint && pnpm --filter @lms/admin test && pnpm --filter @lms/admin build`

## Documentación operativa
- [Plan de ejecución de auditoría](docs/plan-ejecucion-auditoria.md)
- [Auditoría técnica y de contexto IA](docs/auditoria-hallazgos.md)
- [Arquitectura](docs/architecture.md)
- [Convenciones](docs/conventions.md)
- [Testing y matriz de validación](docs/testing.md)
- [Ejemplos y anti-patrones](docs/examples.md)
- [Toolkit MCP recomendado](docs/mcp-tooling.md)
- [Contribución](CONTRIBUTING.md)

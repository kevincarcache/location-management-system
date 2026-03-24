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
5. Ejecuta los proyectos con `pnpm dev`.

## Scripts raíz
- `pnpm dev`
- `pnpm build`
- `pnpm lint`
- `pnpm typecheck`
- `pnpm test`

## Estado actual
- Fase 1 del monorepo creada
- Estructura inicial del backend FastAPI lista
- Shells iniciales para Nuxt y Vue/Vuetify creados
- Configuración base de Docker y entornos incluida


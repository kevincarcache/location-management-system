# Arquitectura

## Vista general
- `apps/api` expone contratos HTTP y persiste el dominio.
- `apps/admin` consume contratos admin autenticados.
- `apps/web` consume contratos públicos para el storefront.
- `packages/types` contiene la fuente de verdad de contratos TypeScript compartidos.

## Backend
### Capas
- `api/routes`: superficie HTTP y traducción a status codes.
- `services`: orquestación, reglas de aplicación, transacciones y serialización.
- `repositories`: acceso a datos y queries. No hacen `commit()`.
- `models`: esquema SQLAlchemy.
- `schemas`: contratos Pydantic de request/response.

### Reglas de dependencia
- Routes -> Services -> Repositories -> Models
- Schemas pueden ser usados por routes y services.
- Repositories no importan routes ni lógica HTTP.

### Transacciones
- Los servicios son dueños de `commit`, `rollback` y `refresh`.
- Los repositorios pueden hacer `flush()` para materializar IDs.
- La importación CSV es el caso de referencia para operaciones compuestas.

## Frontend admin
- `lib/admin-api.ts`: boundary HTTP único.
- `stores/session.ts`: auth/session.
- `router/guards.ts`: control de acceso.
- `pages/*`: composición de pantallas.

## Frontend público
- `app.vue`: composición de shell.
- `composables/useStorefrontPage.ts`: orquestación de store config, locations y sync de URL.
- `components/*`: presentación.

## Contratos
- Backend emite `snake_case`.
- `packages/types` define contratos compartidos TypeScript.
- Si un cliente usa `camelCase`, el mapping debe ser explícito en helpers/composables.

## Integraciones externas
- Geocoding se encapsula detrás de un provider configurable.
- No se permiten llamadas de red ad hoc desde routes.

## Packages compartidos
- `packages/types`: obligatorio para contratos TS compartidos.
- `packages/config`: base TS compartida.
- `packages/ui`: tokens compartidos ligeros; no es todavía un design system completo.

# Ejemplos y anti-patrones

## Haz esto
- Backend:
  - route -> service -> repository
  - auth admin reusable aplicada al router
  - repositorio con `flush()`, service con `commit()`
- Frontend:
  - tipos compartidos importados desde `@lms/types`
  - boundary HTTP centralizado en `admin-api.ts`
  - helper puro testeable para mapear contratos

## No hagas esto
- Crear una nueva ruta admin sin auth.
- Hacer `commit()` directamente en el repositorio.
- Duplicar `StoreConfig`, `ApiLocation` o `TokenPair` dentro de una app.
- Reintroducir un segundo patrón de fetch en `apps/web` para la misma pantalla.
- Acceder a `localStorage` al importar un módulo.

## Ejemplos canónicos actuales
- Auth admin reusable:
  - `apps/api/app/api/dependencies/auth.py`
- Patrón transaccional en services:
  - `apps/api/app/services/locations.py`
  - `apps/api/app/services/store_configs.py`
- Import modularizado:
  - `apps/api/app/services/imports.py`
- Boundary HTTP admin:
  - `apps/admin/src/lib/admin-api.ts`
- Orquestación storefront:
  - `apps/web/composables/useStorefrontPage.ts`
- Helpers puros testeables:
  - `apps/web/composables/storefront-state.ts`

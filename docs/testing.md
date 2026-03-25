# Testing y validación

## Matriz de validación
| Tipo de cambio | Validación mínima |
|---|---|
| Backend | `cd apps/api && UV_CACHE_DIR=.uv-cache uv run ruff check app tests` + `cd apps/api && UV_CACHE_DIR=.uv-cache uv run pytest` |
| Modelos/migraciones | Backend + `cd apps/api && UV_CACHE_DIR=.uv-cache uv run alembic upgrade head` |
| Web | `pnpm --filter @lms/web lint` + `pnpm --filter @lms/web test` + `pnpm --filter @lms/web build` |
| Admin | `pnpm --filter @lms/admin lint` + `pnpm --filter @lms/admin test` + `pnpm --filter @lms/admin build` |
| Tipos compartidos | Validar todos los consumidores impactados |
| CI | Reproducir localmente los comandos del workflow cuando sea viable |

## Cobertura inicial esperada
- Backend:
  - auth
  - store config resolution
  - import preview/import
  - autorización admin
- Web:
  - helpers/mappers de storefront
  - estado y sync de query crítica
- Admin:
  - session store
  - guards/helpers críticos

## Definition of Done técnica
- La validación mínima del área modificada pasa completa.
- Los tests agregados cubren el comportamiento nuevo o el bug corregido.
- No se cierran cambios importantes solo con lint si el área tiene build/test disponibles.

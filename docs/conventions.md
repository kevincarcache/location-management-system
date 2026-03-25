# Convenciones

## Naming
- Backend Python:
  - módulos en `snake_case`
  - schemas y modelos con nombres de dominio claros
- Frontend TypeScript/Vue:
  - componentes en `PascalCase`
  - composables en `useX`
  - helpers puros con nombre funcional y descriptivo

## Contratos y tipos
- Fuente de verdad TypeScript: `packages/types/src/index.ts`
- Formato wire API: `snake_case`
- Modelos UI pueden usar `camelCase`, pero solo mediante mappers explícitos
- No redefinir el mismo contrato en:
  - `apps/admin/src/lib/admin-api.ts`
  - `apps/web/composables/*`
  - `packages/types`

## Backend
- Routes finas, services gruesos, repositories delgados.
- Toda mutación de modelo debe ir con migración Alembic.
- Toda ruta admin debe exigir auth reusable.
- Las integraciones externas deben usar adapters/providers.

## Frontend
- `apps/admin` usa `admin-api.ts` como boundary HTTP.
- `apps/web` usa `useStorefrontPage.ts` como patrón canónico de carga.
- Evitar side effects a nivel de módulo, sobre todo para storage o dependencias browser-only.

## Testing
- Backend: pytest + ruff
- Web/Admin: Vitest para lógica y componentes críticos, además de build/typecheck
- E2E no reemplaza pruebas locales de unidad/composición

## Documentación
- Si se adopta un nuevo patrón canónico, actualizar la documentación correspondiente.
- Si un cambio modifica la validación requerida, actualizar `docs/testing.md`.
- Si cambian los flujos de debugging o validación asistida por herramientas, actualizar `docs/mcp-tooling.md` o la skill afectada.

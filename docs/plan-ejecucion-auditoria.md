# Plan de Ejecución de la Auditoría Técnica

## 1. Resumen de estrategia de ejecución

### Criterio general del plan
- El plan prioriza primero riesgo sistémico, luego estabilidad estructural, después estandarización de contratos y validación, y finalmente contexto operativo para IA y escalabilidad.
- El orden evita documentar o “formalizar” patrones que todavía están técnicamente inestables.
- Los cambios de contexto para IA se posponen hasta que las reglas más importantes del repositorio sean reales y verificables.

### Por qué este orden es el correcto
- No tiene sentido mejorar `AGENTS.md` o crear skills si las rutas admin siguen sin auth, las migraciones no se versionan y la CI no detecta roturas críticas.
- La consolidación de contratos debe ocurrir después de fijar seguridad, reproducibilidad y patrón transaccional básico.
- La documentación operativa y el contexto IA deben construirse encima de patrones ya estabilizados, no sobre deuda viva.

### Principales desbloqueadores
- Corregir `.gitignore` y versionar migraciones.
- Aplicar auth real a rutas admin.
- Reforzar CI mínima para validar backend y frontends.
- Definir patrón canónico de contratos compartidos.
- Limpiar artefactos generados y patrones obsoletos.

### Principales riesgos de implementación
- Romper el flujo actual del admin al endurecer auth.
- Introducir un refactor transaccional demasiado amplio de una sola vez.
- Consolidar contratos antes de decidir claramente la fuente de verdad.
- Reescribir `AGENTS.md` antes de estabilizar convenciones reales.
- Mezclar limpieza de repositorio con cambios funcionales y dificultar revisión.

## 2. Plan de ejecución por fases

### Fase 0: Preparación

#### Objetivo
- Preparar el repositorio para cambios seguros y visibles.

#### Resultado esperado
- Base mínima de trabajo limpia, con trazabilidad y sin confusión operativa básica.

#### Tareas incluidas
- Corregir `.gitignore` para no ignorar migraciones.
- Verificar qué artefactos generados están presentes y limpiar el árbol de trabajo.
- Añadir scripts de limpieza o pautas mínimas de exclusión.
- Confirmar estado actual de Alembic y migraciones existentes.

#### Dependencias
- Ninguna.

#### Riesgos
- Confundir limpieza local con cambios de producto.
- Perder visibilidad de archivos generados útiles para debugging.

#### Criterio de cierre
- `.gitignore` corregido.
- Directorios generados identificados y política de limpieza definida.
- Migraciones listas para quedar versionadas.

---

### Fase 1: Riesgos críticos

#### Objetivo
- Eliminar riesgos de seguridad y reproducibilidad.

#### Resultado esperado
- API admin protegida.
- Esquema reproducible entre entornos.
- CI mínima capaz de detectar roturas obvias.

#### Tareas incluidas
- Implementar dependencia de autenticación para rutas admin.
- Aplicar auth a `admin_locations`, `admin_store_configs`, `admin_imports`, `admin_geocoding`.
- Añadir tests de autorización.
- Versionar migraciones existentes.
- Reforzar CI para correr builds básicos de frontends además de lint y pytest.

#### Dependencias
- Fase 0 completada.

#### Riesgos
- Romper login/refresh o flujos actuales del admin.
- Introducir fallos en pruebas y seeds al endurecer auth.

#### Criterio de cierre
- Ningún endpoint admin responde sin credenciales válidas.
- Migraciones versionadas y aplicables.
- CI valida backend, web y admin al menos a nivel build/typecheck.

---

### Fase 2: Estabilización estructural

#### Objetivo
- Reducir deuda técnica que afecta evolución segura del código.

#### Resultado esperado
- Patrón backend más controlable.
- Menos duplicación estructural.
- Menos rutas ambiguas para cambios futuros.

#### Tareas incluidas
- Definir patrón transaccional canónico backend.
- Refactorizar repositorios para quitar `commit()` internos.
- Reestructurar importación CSV alrededor de responsabilidades separadas.
- Encapsular geocoding en adapter configurable y testeable.
- Corregir store de sesión del admin para eliminar side effects a nivel de módulo.
- Retirar o consolidar composables obsoletos del storefront.

#### Dependencias
- Fase 1 completada.

#### Riesgos
- Refactors amplios en backend con regresiones sutiles.
- Cambios de estado en admin que afecten navegación y guards.

#### Criterio de cierre
- Repositorios sin `commit()` internos en el flujo principal.
- CSV import organizado en capas más claras.
- Geocoding desacoplado de red directa.
- Admin session store sin side effects globales.

---

### Fase 3: Estandarización de contratos y validación

#### Objetivo
- Eliminar drift entre apps y crear validación más útil.

#### Resultado esperado
- Contratos compartidos claros.
- Menos duplicación de tipos.
- Testing y validación mejor alineados con la arquitectura.

#### Tareas incluidas
- Elegir fuente de verdad de contratos.
- Consolidar tipos compartidos entre backend, web y admin.
- Documentar política snake_case/camelCase.
- Añadir Vitest a web y admin.
- Crear matriz de validación por tipo de cambio.
- Expandir pruebas clave de frontend/admin.

#### Dependencias
- Fase 2 completada o lo suficientemente avanzada para no reescribir contratos dos veces.

#### Riesgos
- Congelar contratos demasiado pronto.
- Introducir refactor transversal sin plan de migración.

#### Criterio de cierre
- Una sola estrategia oficial de contratos compartidos.
- Scripts de test reales en `web` y `admin`.
- Validación por tipo de cambio documentada y ejecutable.

---

### Fase 4: Contexto IA

#### Objetivo
- Traducir patrones estabilizados a guardrails operativos para agentes.

#### Resultado esperado
- Repositorio preparado para trabajo intensivo con IA sin improvisación estructural.

#### Tareas incluidas
- Reescribir `AGENTS.md`.
- Crear `AGENTS.override.md` por app.
- Crear docs canónicas de arquitectura, convenciones, testing y ejemplos.
- Crear skill pack inicial del repositorio.
- Añadir plantillas de tarea y PR.

#### Dependencias
- Fase 2 y 3 suficientemente estabilizadas.

#### Riesgos
- Documentar reglas que luego cambien.
- Sobredocumentar sin ejemplos útiles.

#### Criterio de cierre
- Un agente puede identificar qué hacer, dónde hacerlo y cómo validarlo sin inferencias amplias.

---

### Fase 5: Escalabilidad y endurecimiento

#### Objetivo
- Preparar el repositorio para crecimiento sostenido y menor drift a futuro.

#### Resultado esperado
- Mejor trazabilidad, mejor observabilidad y menor riesgo de divergencia entre apps.

#### Tareas incluidas
- Evaluar generación de tipos desde OpenAPI.
- Añadir logging estructurado y observabilidad mínima.
- Mejorar cobertura E2E y smoke tests.
- Revisar packages compartidos para fortalecerlos o simplificarlos.
- Documentar políticas de compatibilidad, refactor vs parche y evolución del repo.

#### Dependencias
- Fases anteriores cerradas o suficientemente maduras.

#### Riesgos
- Hacer abstracciones compartidas prematuras.
- Sobre-optimizar tooling antes de cerrar patrones reales.

#### Criterio de cierre
- El repositorio tiene reglas, contratos y tooling suficientemente estables para evolución continua.

## 3. Backlog ejecutable

| ID | Título | Descripción | Tipo | Prioridad | Esfuerzo | Riesgo | Dependencias | Archivos tentativos a modificar | Definición de terminado | Validaciones requeridas |
|---|---|---|---|---|---|---|---|---|---|---|
| T-000 | Corregir exclusiones críticas en `.gitignore` | Retirar exclusión de migraciones y revisar exclusiones de artefactos generados | docs / repositorio | P0 | XS | bajo | ninguna | `.gitignore` | Alembic versions ya no se ignora y política de exclusión es coherente | revisión manual + `git status` |
| T-001 | Versionar migraciones existentes | Asegurar que las migraciones actuales queden en control de versiones | código | P0 | S | medio | T-000 | `apps/api/alembic/versions/*` | Migraciones versionadas y aplicables | `uv run alembic upgrade head` |
| T-002 | Implementar dependencia auth admin | Crear `get_current_admin_user()` y validación JWT | código | P0 | M | medio | ninguna | `apps/api/app/core/security.py`, nuevas dependencias auth, routers admin | Existe dependencia reusable para auth admin | `uv run pytest` |
| T-003 | Proteger rutas admin | Aplicar auth a routers admin | código | P0 | M | alto | T-002 | `apps/api/app/api/routes/admin_*.py` | Todas las rutas admin exigen token válido | tests 401/200 |
| T-004 | Añadir tests de autorización | Cubrir acceso sin token, con token inválido y válido | testing | P0 | M | medio | T-003 | `apps/api/tests/*` | Tests auth pasan y cubren rutas críticas | `uv run pytest` |
| T-005 | Reforzar CI básica | Añadir build/typecheck de web y admin al workflow | CI | P0 | S | bajo | ninguna | `.github/workflows/ci.yml` | CI detecta roturas de backend, admin y web | ejecutar workflow localmente o por PR |
| T-006 | Limpiar artefactos generados y agregar estrategia de limpieza | Definir scripts o guía para limpiar `.nuxt`, `.output`, `.venv`, `--host`, caches locales | repositorio / DX | P1 | S | bajo | T-000 | `package.json`, `README.md`, docs | Política de limpieza clara y repetible | revisión manual |
| T-007 | Definir patrón transaccional backend | Establecer dónde viven `commit`, `rollback`, `flush` y errores | arquitectura / código | P1 | M | medio | T-003 | `apps/api/app/repositories/*`, `apps/api/app/services/*`, docs | Patrón documentado y aplicado en primer dominio | lint + pytest |
| T-008 | Refactorizar repositorios para quitar `commit()` internos | Empezar por locations/imports/store_configs/admin_users | código | P1 | L | alto | T-007 | `apps/api/app/repositories/*.py`, `apps/api/app/services/*.py` | Repositorios no hacen commit en flujo principal | `uv run pytest` |
| T-009 | Reestructurar importación CSV | Separar parser, validator, matcher, preview/import runner | arquitectura / código | P1 | XL | alto | T-008 | `apps/api/app/services/imports.py`, nuevos módulos | Import flow más modular y menos duplicado | tests de preview/import |
| T-010 | Encapsular geocoding en adapter | Introducir provider configurable y testeable | código | P1 | M | medio | T-007 | `apps/api/app/services/geocoding.py`, nuevos módulos, settings, tests | Red externa desacoplada | tests con mocks |
| T-011 | Rehacer session store del admin | Eliminar `localStorage` en nivel de módulo y formalizar inicialización | código | P1 | S | medio | ninguna | `apps/admin/src/stores/session.ts`, quizá router/guards | Store sin side effects globales | `pnpm --filter @lms/admin lint` |
| T-012 | Eliminar o consolidar composables obsoletos de web | Definir patrón único de carga SSR-safe | código | P1 | S | medio | ninguna | `apps/web/composables/*`, docs | Solo queda un patrón canónico | `pnpm --filter @lms/web lint` + build |
| T-013 | Elegir fuente de verdad de contratos | Decidir entre OpenAPI generated types o `packages/types` reforzado | arquitectura | P1 | M | medio | T-008 | `packages/types`, `apps/admin/src/lib/admin-api.ts`, `apps/web/composables/*`, docs | Decisión explícita y documentada | revisión arquitectónica |
| T-014 | Consolidar tipos compartidos | Mover duplicaciones a fuente oficial y actualizar consumidores | código / arquitectura | P1 | L | alto | T-013 | `packages/types/*`, `apps/admin/src/lib/admin-api.ts`, `apps/web/*` | Sin duplicación principal de tipos | lint + build + tests |
| T-015 | Documentar política de mapping API/domain | Establecer snake_case vs camelCase y mappers canónicos | docs | P1 | S | bajo | T-013 | `docs/conventions.md`, ejemplos | Regla clara y reusable | revisión manual |
| T-016 | Añadir Vitest a `web` | Introducir tests unitarios/composables/componentes críticos | testing | P1 | M | medio | ninguna | `apps/web/package.json`, config de test, tests nuevos | `test` deja de ser echo y corre suite real | `pnpm --filter @lms/web test` |
| T-017 | Añadir Vitest a `admin` | Cobertura básica de stores, helpers y componentes | testing | P1 | M | medio | ninguna | `apps/admin/package.json`, config de test, tests nuevos | `test` deja de ser echo y corre suite real | `pnpm --filter @lms/admin test` |
| T-018 | Crear matriz de validación por tipo de cambio | Definir qué comandos correr en backend/web/admin/docs/CI | docs / contexto IA | P1 | S | bajo | T-005, T-016, T-017 | `AGENTS.md`, `docs/testing.md`, `README.md` | Validación obligatoria documentada | revisión manual |
| T-019 | Reescribir README | Convertirlo en quickstart veraz y mapa de documentación | docs | P1 | S | bajo | T-005 | `README.md` | README alineado con repo real | revisión manual |
| T-020 | Crear `docs/architecture.md` | Documentar capas, dominios y dependencias permitidas | docs | P1 | M | bajo | T-007, T-013 | `docs/architecture.md` | Arquitectura trazable | revisión manual |
| T-021 | Crear `docs/conventions.md` | Naming, casing, reglas por capa, contratos, errores | docs | P1 | M | bajo | T-013, T-015 | `docs/conventions.md` | Convenciones explícitas | revisión manual |
| T-022 | Reescribir `AGENTS.md` | Convertirlo en manual operativo del repo | contexto IA | P1 | M | medio | T-018, T-020, T-021 | `AGENTS.md` | Contiene reglas accionables y no genéricas | revisión manual |
| T-023 | Crear `AGENTS.override.md` por app | Introducir reglas locales por stack usando el mecanismo nativo de Codex | contexto IA | P2 | S | bajo | T-022 | `apps/api/AGENTS.override.md`, `apps/admin/AGENTS.override.md`, `apps/web/AGENTS.override.md` | Reglas locales claras y no contradictorias | revisión manual |
| T-024 | Crear `docs/examples.md` | Ejemplos canónicos y anti-patrones | docs / contexto IA | P2 | M | bajo | T-007, T-013, T-022 | `docs/examples.md` | IA y humanos tienen ejemplos fuente de verdad | revisión manual |
| T-025 | Crear skill pack inicial | Skills para backend, frontend, admin, migrations y testing | contexto IA | P2 | L | medio | T-022, T-024 | `.codex/skills/**` | Skills versionadas y accionables | revisión manual |
| T-026 | Añadir logging estructurado básico | Instrumentar requests, auth e imports | código / ops | P2 | M | medio | T-008, T-009 | `apps/api/app/core/*`, `apps/api/app/services/*` | Logging mínimo útil para debugging | pytest + smoke manual |
| T-027 | Evaluar OpenAPI/codegen | Decidir si conviene mover tipos a generación automática | arquitectura | P2 | M | medio | T-014 | docs, tooling, quizá scripts | Decisión documentada y ADR simple | revisión manual |
| T-028 | Revisar packages compartidos | Fortalecer `packages/ui`/`config` o reducirlos | arquitectura | P3 | M | medio | T-020, T-021 | `packages/*`, docs | Shared packages con propósito claro | lint/build |

## 4. Agrupación por workstreams

### Seguridad
- Objetivo:
  - cerrar brechas críticas de acceso y endurecer la superficie admin.
- Tareas incluidas:
  - T-002
  - T-003
  - T-004
- Orden recomendado:
  - dependencia auth
  - aplicación a rutas
  - pruebas de autorización

### Reproducibilidad y repositorio
- Objetivo:
  - asegurar trazabilidad de esquema y limpieza operativa del repo.
- Tareas incluidas:
  - T-000
  - T-001
  - T-006
  - T-019
- Orden recomendado:
  - `.gitignore`
  - migraciones
  - limpieza
  - README

### Backend architecture
- Objetivo:
  - volver el backend más mantenible y menos frágil.
- Tareas incluidas:
  - T-007
  - T-008
  - T-009
  - T-010
  - T-026
- Orden recomendado:
  - patrón transaccional
  - repositorios
  - CSV import
  - geocoding
  - logging

### API contracts
- Objetivo:
  - evitar drift entre backend y consumidores.
- Tareas incluidas:
  - T-013
  - T-014
  - T-015
  - T-027
- Orden recomendado:
  - decidir fuente de verdad
  - consolidar tipos
  - documentar mapping
  - evaluar codegen

### Frontend consistency
- Objetivo:
  - simplificar patrones y reducir side effects.
- Tareas incluidas:
  - T-011
  - T-012
- Orden recomendado:
  - store del admin
  - composables obsoletos del storefront

### Testing and CI
- Objetivo:
  - crear una red de seguridad útil para humanos e IA.
- Tareas incluidas:
  - T-005
  - T-016
  - T-017
  - T-018
- Orden recomendado:
  - CI mínima
  - Vitest web
  - Vitest admin
  - matriz de validación

### Documentation
- Objetivo:
  - hacer explícita la arquitectura y las reglas del repo.
- Tareas incluidas:
  - T-019
  - T-020
  - T-021
  - T-024
- Orden recomendado:
  - README
  - arquitectura
  - convenciones
  - ejemplos

### AI operating context
- Objetivo:
  - diseñar guardrails operativos reales para agentes.
- Tareas incluidas:
  - T-022
  - T-023
  - T-025
- Orden recomendado:
  - AGENTS nuevo
- `AGENTS.override.md` por subárbol
  - skills

## 5. Secuencia recomendada de implementación

1. Corregir `.gitignore` y dejar de ignorar migraciones.
2. Versionar las migraciones existentes.
3. Crear dependencia de autenticación para admin.
4. Proteger rutas admin.
5. Añadir pruebas de autorización.
6. Reforzar CI mínima con builds de web/admin.
7. Limpiar artefactos generados y documentar estrategia de limpieza.
8. Definir patrón transaccional backend.
9. Refactorizar repositorios para quitar `commit()` internos.
10. Reestructurar importación CSV.
11. Encapsular geocoding en adapter testeable.
12. Corregir store de sesión del admin.
13. Eliminar o consolidar composables obsoletos del storefront.
14. Elegir fuente de verdad para contratos.
15. Consolidar tipos compartidos.
16. Documentar mapping snake_case/camelCase.
17. Añadir Vitest a `web`.
18. Añadir Vitest a `admin`.
19. Crear matriz de validación por tipo de cambio.
20. Reescribir README.
21. Crear `docs/architecture.md`.
22. Crear `docs/conventions.md`.
23. Reescribir `AGENTS.md`.
24. Crear `AGENTS.override.md` por app.
25. Crear `docs/examples.md`.
26. Crear skill pack inicial.
27. Añadir logging estructurado básico.
28. Evaluar OpenAPI/codegen.
29. Revisar packages compartidos.

## 6. Matriz de dependencias

| Tarea | Depende de | Desbloquea | ¿Paralela? |
|---|---|---|---|
| T-000 | - | T-001, T-006 | sí |
| T-001 | T-000 | Fase de reproducibilidad | no |
| T-002 | - | T-003, T-004 | sí |
| T-003 | T-002 | T-004, hardening backend | no |
| T-004 | T-003 | cierre de seguridad | no |
| T-005 | - | T-018, confianza de CI | sí |
| T-006 | T-000 | DX y contexto más limpio | sí |
| T-007 | T-003 idealmente | T-008, T-009, T-010 | no |
| T-008 | T-007 | T-009, T-026 | no |
| T-009 | T-008 | estabilidad import | no |
| T-010 | T-007 | testabilidad integraciones | sí |
| T-011 | - | mejor testing admin | sí |
| T-012 | - | menor ambigüedad frontend | sí |
| T-013 | T-008 recomendado | T-014, T-015, T-027 | no |
| T-014 | T-013 | menor drift y docs IA | no |
| T-015 | T-013 | T-021, T-024 | sí |
| T-016 | - | T-018 | sí |
| T-017 | - | T-018 | sí |
| T-018 | T-005, T-016, T-017 | T-022 | no |
| T-019 | T-005 recomendado | onboarding mejorado | sí |
| T-020 | T-007, T-013 | T-022, T-024 | no |
| T-021 | T-013, T-015 | T-022, T-024 | no |
| T-022 | T-018, T-020, T-021 | T-023, T-025 | no |
| T-023 | T-022 | mejor segmentación de contexto | sí |
| T-024 | T-007, T-013, T-022 | T-025 | no |
| T-025 | T-022, T-024 | operación IA madura | no |
| T-026 | T-008, T-009 recomendado | ops/debug | sí |
| T-027 | T-014 | decisiones de largo plazo | sí |
| T-028 | T-020, T-021 | simplificación o fortalecimiento shared | sí |

## 7. Entregables por fase

### Al final de Fase 0
- `.gitignore` corregido
- migraciones listas para versionarse
- criterio de limpieza del repo documentado o script definido

### Al final de Fase 1
- rutas admin protegidas
- tests de auth
- migraciones versionadas
- CI reforzada

### Al final de Fase 2
- patrón transaccional backend documentado y aplicado
- import CSV modularizado
- geocoding con adapter
- session store del admin corregido
- patrón canónico del storefront definido

### Al final de Fase 3
- contratos compartidos consolidados
- policy de mapping documentada
- Vitest en web/admin
- matriz de validación operativa

### Al final de Fase 4
- `AGENTS.md` reescrito
- `apps/api/AGENTS.override.md`, `apps/admin/AGENTS.override.md`, `apps/web/AGENTS.override.md`
- `docs/architecture.md`
- `docs/conventions.md`
- `docs/examples.md`
- skills iniciales

### Al final de Fase 5
- logging estructurado mínimo
- decisión sobre OpenAPI/codegen
- revisión final de `packages/*`
- base lista para escalar

## 8. Riesgos de implementación

### Riesgo: romper compatibilidad al endurecer auth
- Mitigación:
  - introducir dependencia auth y actualizar tests/admin en la misma fase
  - validar manualmente login, CRUD e imports

### Riesgo: refactor backend demasiado amplio
- Mitigación:
  - no refactorizar todos los dominios a la vez
  - empezar por `locations` e `imports`
  - cerrar una vertical antes de abrir otra

### Riesgo: consolidar contratos demasiado pronto
- Mitigación:
  - decidir primero la fuente de verdad
  - hacer inventario de contratos antes de migrar consumidores

### Riesgo: documentar antes de estabilizar patrones
- Mitigación:
  - retrasar `AGENTS.md`, skills y docs canónicas hasta después de Fase 2/3

### Riesgo: sobre-documentación sin utilidad operativa
- Mitigación:
  - cada documento debe responder a una decisión concreta del agente:
    - dónde editar
    - cómo validar
    - qué patrón seguir

### Riesgo: CI demasiado pesada demasiado pronto
- Mitigación:
  - empezar por build/typecheck y smoke tests
  - dejar E2E completos para milestone posterior si cuesta demasiado estabilizarlos

## 9. Recomendación de milestones

### Milestone 1: Seguridad y reproducibilidad mínima
- Objetivo:
  - eliminar riesgos críticos del repo
- Tareas incluidas:
  - T-000, T-001, T-002, T-003, T-004, T-005
- Criterio de cierre:
  - auth admin funcionando, migraciones versionadas y CI mínima activa

### Milestone 2: Backend durable
- Objetivo:
  - estabilizar backend para evolucionar sin deuda creciente
- Tareas incluidas:
  - T-007, T-008, T-009, T-010
- Criterio de cierre:
  - patrón transaccional claro, imports refactorizados y geocoding desacoplado

### Milestone 3: Contratos y validación
- Objetivo:
  - reducir drift entre apps y aumentar seguridad de cambios
- Tareas incluidas:
  - T-011, T-012, T-013, T-014, T-015, T-016, T-017, T-018
- Criterio de cierre:
  - contratos consolidados, tests reales en frontends y matriz de validación definida

### Milestone 4: Contexto operativo para IA
- Objetivo:
  - convertir el repo en una base usable por agentes con menor ambigüedad
- Tareas incluidas:
  - T-019, T-020, T-021, T-022, T-023, T-024, T-025
- Criterio de cierre:
  - docs canónicas y sistema de instrucciones operativas listos

### Milestone 5: Escalabilidad y endurecimiento
- Objetivo:
  - consolidar base de largo plazo
- Tareas incluidas:
  - T-026, T-027, T-028
- Criterio de cierre:
  - observabilidad mínima, estrategia de contratos a futuro y packages compartidos resueltos

## 10. Archivo de salida obligatorio

- Este plan debe vivir en `docs/plan-ejecucion-auditoria.md`.
- Debe mantenerse como documento vivo hasta cerrar el roadmap de remediación.

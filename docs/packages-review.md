# Revisión de packages compartidos

## `packages/types`
- Decisión: mantener y fortalecer.
- Motivo: ya es la fuente de verdad TS compartida entre admin y web.

## `packages/config`
- Decisión: mantener.
- Motivo: aporta una base TS compartida útil y de bajo costo.

## `packages/ui`
- Decisión: mantener como paquete de tokens ligeros, no como design system completo.
- Motivo: hoy aporta theme/tokens, pero aún no justifica una capa de componentes compartidos más grande.

## Regla
- No expandir `packages/ui` a librería completa salvo tarea explícita de consolidación visual.

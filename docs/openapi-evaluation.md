# Evaluación inicial de OpenAPI/codegen

## Estado actual
- La campaña actual adopta `packages/types` como fuente de verdad operativa para contratos TypeScript.
- No se implementa codegen automático en esta fase.

## Motivo
- Primero se estabilizaron auth, transacciones, contratos compartidos básicos y testing.
- Introducir codegen antes de cerrar esos patrones aumentaría la complejidad y el riesgo de doble migración.

## Criterios para reevaluar
- El backend cambia contratos con frecuencia y genera drift repetido.
- `packages/types` empieza a duplicar demasiado shape del backend.
- Se necesita cliente tipado generado para más de dos consumidores o más endpoints complejos.

## Decisión actual
- Mantener `packages/types` manual.
- Reabrir evaluación cuando el contrato público/admin esté más estable o el costo de mantenimiento manual crezca.

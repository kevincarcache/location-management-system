# Contributing

## Flujo recomendado
1. Identifica el área afectada.
2. Revisa la documentación específica del área antes de editar.
3. Implementa el cambio en la capa correcta.
4. Ejecuta la matriz de validación correspondiente.
5. Actualiza docs o ejemplos si se adoptó un patrón nuevo.

## Reglas prácticas
- Mantén los cambios pequeños y revisables.
- No mezcles refactor estructural con cambios de producto sin necesidad.
- Si cambias modelos o contratos, actualiza consumidores y documentación.
- Si tocas una integración externa, usa adapter/provider.

## Branching
- Prefiere branches pequeñas por milestone o workstream.
- Usa nombres descriptivos y orientados a tarea.

## Checklist antes de cerrar
- Tests y builds relevantes en verde
- Contratos compartidos alineados
- Sin artefactos generados añadidos por error
- Docs actualizadas cuando aplica

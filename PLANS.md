# PLANS.md

## Visión actual del producto
- El frontend público debe comportarse como el sitio real de un negocio específico, no como un "Location Management System" genérico.
- El admin es el único lugar donde debe vivir el branding técnico del producto y desde donde se administran localizaciones, configuración del negocio, importaciones y reportes.
- El contexto del negocio se resuelve por `storeview` con esta precedencia:
  - variable de entorno
  - parámetro en la URL
  - primer storeview existente en base de datos
- El seed inicial debe garantizar que siempre exista un storeview `default`.

## Estado general
- Estado: En implementación avanzada
- Base técnica completada:
  - monorepo con `pnpm + turbo`
  - backend `FastAPI + PostgreSQL + SQLAlchemy + Alembic`
  - frontend público en `Nuxt`
  - panel admin en `Vue 3 + Vite + Vuetify`
  - importación CSV con preview y confirmación
  - mapa público con `MapLibre + OpenStreetMap`

## Decisiones rectoras

### Storeview y storefront
- El frontend público usa `StoreConfig` como fuente principal de identidad visual y contenido.
- `Location.business_type` se mantiene como dato interno y filtro operativo.
- Si el storefront ya fija un solo tipo de localización, el frontend no debe exponer ese tipo como filtro visible principal.
- El storeview `default` se crea automáticamente en seed.

### Backend
- Se incorpora `StoreConfig` como entidad persistida.
- Se expone configuración pública del storefront y configuración editable desde admin.
- La resolución de storeview se hace con:
  - `API_STOREFRONT_SLUG`
  - `storeview` en request
  - primer registro disponible
- El backend sigue persistiendo `latitude` y `longitude`, pero el admin deja de capturarlas como campos manuales.

### Frontend público
- El layout público debe parecerse a un sitio comercial:
  - header
  - contenido principal
  - footer
- La columna izquierda conserva el listado de localizaciones.
- El mapa ocupa todo el espacio restante en la derecha.
- Al seleccionar una ubicación se muestra una tarjeta superpuesta sobre el mapa.
- No se muestran latitud/longitud ni copy técnico obvio.

### Admin
- El admin debe verse como panel convencional:
  - menú lateral izquierdo
  - header superior
  - footer
- La creación y edición de localizaciones ocurre en página dedicada, no en modal.
- Los campos del formulario deben ir en flujo vertical.
- La ubicación se define con:
  - búsqueda geográfica
  - ajuste manual de pin sobre el mapa

## Modelo funcional

### Entidades activas
- `AdminUser`
- `Location`
- `LocationImportJob`
- `LocationImportRowError`
- `StoreConfig`

### `StoreConfig`
- `slug`
- `brand_name`
- `business_description`
- `theme_preset`
- `business_type`
- `logo_url`
- `hero_title`
- `hero_subtitle`
- `menu_label`
- `footer_text`

## APIs clave

### Públicas
- `GET /api/public/store-config`
- `GET /api/public/locations`
- `GET /api/public/locations/:slug`

### Admin
- `POST /api/admin/auth/login`
- `POST /api/admin/auth/refresh`
- `GET /api/admin/locations`
- `GET /api/admin/locations/:id`
- `POST /api/admin/locations`
- `PATCH /api/admin/locations/:id`
- `DELETE /api/admin/locations/:id`
- `GET /api/admin/store-configs`
- `POST /api/admin/store-configs`
- `PATCH /api/admin/store-configs/:id`
- `GET /api/admin/geocoding/search`
- `POST /api/admin/imports/locations/csv/preview`
- `POST /api/admin/imports/locations/csv`
- `GET /api/admin/imports/locations/csv/template`

## Fases de esta nueva etapa

### Fase A: Fundaciones de storefront
- Estado: Completada
- Entregables:
  - modelo `StoreConfig`
  - seed de storeview `default`
  - resolución por env, URL y fallback a primer registro
  - endpoint público de configuración
  - filtrado público de localizaciones por `business_type` del storefront

### Fase B: Rediseño del admin
- Estado: Completada
- Entregables:
  - shell con menú lateral, header y footer
  - dashboard realineado
  - páginas separadas para:
    - listado de localizaciones
    - editor de localizaciones
    - tipos de localización
    - reportes
    - configuración de la tienda

### Fase C: Editor de localizaciones con mapa
- Estado: Completada
- Entregables:
  - formulario vertical en página completa
  - búsqueda geográfica desde admin
  - selección de coordenadas con pin en mapa
  - remoción de inputs manuales de latitud/longitud

### Fase D: Reenfoque del frontend público
- Estado: Completada en su alcance actual
- Entregables listos:
  - branding y contenido cargados desde `StoreConfig`
  - resolución de storeview desde frontend
  - header y footer orientados a storefront
  - shell público migrado a componentes base de Vuetify
  - sidebar izquierda + mapa dominante a la derecha
  - tarjeta superpuesta de la ubicación seleccionada
  - eliminación de texto técnico innecesario y lat/lng visibles
- Pendiente de pulido:
  - ampliar presets visuales y profundidad del tema por storefront
  - refinar la tarjeta del mapa para anclarla con mayor precisión visual al marcador seleccionado

### Fase E: Hardening y polish
- Estado: En progreso
- Pendiente:
  - ampliar E2E del nuevo flujo de configuración de tienda
  - cubrir creación/edición con mapa en navegador
  - endurecer reportes y métricas del admin
  - completar documentación visual y operativa de storeviews

## Sitemap objetivo del admin
- Dashboard
- Gestión de localizaciones
  - Lista de localizaciones
  - Gestionar tipos de localizaciones
- Reportes
- Configuración de la tienda

## Criterios de aceptación de esta etapa
- Existe un storeview `default` luego del seed.
- El frontend público puede resolver el storeview por env, por URL o por fallback.
- El branding y el contenido del storefront se pueden editar desde admin.
- El branding técnico "Location Management System" solo aparece en admin.
- El formulario de localizaciones funciona en página completa.
- La ubicación de una localización se define con mapa y no con inputs de lat/lng.
- El mapa público muestra una tarjeta contextual al seleccionar una ubicación.

## Validación actual
- `pnpm lint`: pasando
- `uv run pytest`: pasando
- Cobertura backend añadida para:
  - seed de `StoreConfig`
  - precedencia de resolución del storeview

## Siguiente foco recomendado
- Completar el pulido visual final del storefront público.
- Ampliar presets y tokens de tema por storefront.
- Añadir E2E del flujo completo:
  - editar configuración de tienda
  - crear localización con mapa
  - verificar render correcto en el storefront resuelto

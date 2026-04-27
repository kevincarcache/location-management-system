<template>
  <v-sheet rounded="lg" border color="background">
    <v-sheet color="surface" border rounded="lg" class="ma-3 overflow-hidden">
      <div class="position-relative">
        <v-sheet v-if="!mapUnavailable" :height="mapHeight" color="surface">
          <div ref="mapContainer" class="w-100 h-100" />
        </v-sheet>
        <v-sheet
          v-else
          :height="mapHeight"
          color="surface"
          class="d-flex align-center justify-center w-100"
        >
          <v-empty-state
            icon="mdi-map-search-outline"
            title="Mapa no disponible"
            text="Puedes seguir explorando las ubicaciones desde el registro lateral."
          />
        </v-sheet>

        <v-card
          v-if="mapUnavailable"
          rounded="lg"
          border
          color="surface"
          class="position-absolute top-0 left-0 ma-4"
          max-width="380"
        >
          <v-card-item>
            <template #prepend>
              <v-avatar size="40" color="secondary" variant="tonal">
                <v-icon icon="mdi-map-marker-radius" />
              </v-avatar>
            </template>
            <template #title>
              <span class="text-overline text-secondary d-block mb-1">
                Vista editorial del lugar
              </span>
              <span class="text-h6">
                {{ selectedLocation?.name || 'Selecciona una ubicación' }}
              </span>
            </template>
            <template #subtitle>
              <span class="text-body-2 text-medium-emphasis">
                {{ selectedLocation ? `${selectedLocation.city}, ${selectedLocation.country}` : 'Explora la lista para ver detalles.' }}
              </span>
            </template>
          </v-card-item>

          <v-card-text class="pt-0">
            <p class="text-body-2 text-medium-emphasis mb-4">
              {{
                selectedLocation?.descriptionShort ||
                'Explora la lista y selecciona una ubicación para centrar el mapa.'
              }}
            </p>

            <div v-if="selectedLocation" class="d-flex flex-wrap ga-2 mb-4">
              <v-chip size="small" color="secondary" variant="tonal">
                {{ businessTypeLabel(selectedLocation.businessType) }}
              </v-chip>
              <v-chip size="small" color="primary" variant="outlined">
                {{ selectedLocation.featured ? 'Lugar destacado' : 'Lugar activo' }}
              </v-chip>
            </div>

            <v-alert
              v-if="mapUnavailable"
              type="warning"
              variant="tonal"
              rounded="lg"
              density="comfortable"
              class="mb-4"
            >
              El mapa interactivo no está disponible en este entorno, pero puedes seguir explorando
              la ubicación seleccionada desde el listado.
            </v-alert>

            <v-list
              v-if="selectedLocation"
              density="compact"
              class="bg-transparent pa-0"
            >
              <v-list-item class="px-0">
                <template #prepend>
                  <v-icon icon="mdi-map-marker-outline" color="secondary" />
                </template>
                <v-list-item-title>Dirección</v-list-item-title>
                <v-list-item-subtitle>{{ selectedLocation.addressLine1 }}</v-list-item-subtitle>
              </v-list-item>

              <v-list-item class="px-0">
                <template #prepend>
                  <v-icon icon="mdi-city-variant-outline" color="secondary" />
                </template>
                <v-list-item-title>Ubicación</v-list-item-title>
                <v-list-item-subtitle>
                  {{ selectedLocation.city }}, {{ selectedLocation.country }}
                </v-list-item-subtitle>
              </v-list-item>

              <v-list-item class="px-0">
                <template #prepend>
                  <v-icon icon="mdi-crosshairs-gps" color="secondary" />
                </template>
                <v-list-item-title>Coordenadas</v-list-item-title>
                <v-list-item-subtitle>
                  {{ selectedLocation.latitude.toFixed(4) }}, {{ selectedLocation.longitude.toFixed(4) }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </div>
    </v-sheet>
  </v-sheet>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, shallowRef, watch } from 'vue'

import type { LocationSummary } from '@lms/types'

type MapLibreModule = typeof import('maplibre-gl')
type MarkerInstance = {
  marker: {
    remove: () => void
    setLngLat: (coordinates: [number, number]) => void
    getElement: () => HTMLElement
  }
  remove: () => void
  setLngLat: (coordinates: [number, number]) => void
}
type MapLibrePopup = InstanceType<MapLibreModule['Popup']>

const props = withDefaults(defineProps<{
  locations: LocationSummary[]
  selectedSlug: string | null
}>(), {
  locations: () => [],
  selectedSlug: null
})

const emit = defineEmits<{
  select: [slug: string]
}>()

const mapContainer = ref<HTMLDivElement | null>(null)
const map = ref<any>(null)
const maplibre = ref<MapLibreModule | null>(null)
const mapUnavailable = ref(false)
const selectedPopup = shallowRef<MapLibrePopup | null>(null)
const markers = new Map<string, MarkerInstance>()

const selectedLocation = computed(() =>
  props.locations.find((location) => location.slug === props.selectedSlug)
)
const mapHeight = 680

async function initializeMap() {
  if (!import.meta.client || map.value || !mapContainer.value) {
    return
  }

  try {
    maplibre.value = await import('maplibre-gl')

    map.value = new maplibre.value.Map({
      container: mapContainer.value,
      style: {
        version: 8,
        sources: {
          osm: {
            type: 'raster',
            tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
            tileSize: 256,
            attribution: '&copy; OpenStreetMap contributors'
          }
        },
        layers: [
          {
            id: 'osm',
            type: 'raster',
            source: 'osm'
          }
        ]
      },
      center: [-79.5199, 8.9824],
      zoom: 10.5
    })

    map.value.addControl(
      new maplibre.value.NavigationControl({ visualizePitch: true }),
      'top-right'
    )
    syncMarkers()
    fitToLocations()
    updateSelectedPopup()
  } catch (error) {
    console.warn('Map initialization failed, falling back to static location panel.', error)
    mapUnavailable.value = true
    removeSelectedPopup()
    map.value?.remove()
    map.value = null
    maplibre.value = null
    markers.clear()
  }
}

function syncMarkers() {
  if (!map.value || !maplibre.value || !import.meta.client || mapUnavailable.value) {
    return
  }

  const knownSlugs = new Set(props.locations.map((location) => location.slug))

  for (const [slug, marker] of markers.entries()) {
    if (!knownSlugs.has(slug)) {
      marker.remove()
      markers.delete(slug)
    }
  }

  for (const location of props.locations) {
    const existingMarker = markers.get(location.slug)
    if (existingMarker) {
      existingMarker.remove()
      markers.delete(location.slug)
    }

    const marker = new maplibre.value.Marker({
      color: location.slug === props.selectedSlug ? '#b26a3d' : '#1d5c63',
      scale: location.slug === props.selectedSlug ? 1.15 : 1
    })
      .setLngLat([location.longitude, location.latitude])
      .addTo(map.value)

    marker.getElement().setAttribute('aria-label', location.name)
    marker.getElement().addEventListener('click', () => emit('select', location.slug))

    markers.set(location.slug, {
      marker,
      remove: () => marker.remove(),
      setLngLat: (coordinates: [number, number]) => {
        marker.setLngLat(coordinates)
      }
    })
  }
}

function focusSelectedLocation() {
  if (!map.value || !selectedLocation.value || mapUnavailable.value) {
    return
  }

  map.value.flyTo({
    center: [selectedLocation.value.longitude, selectedLocation.value.latitude],
    zoom: 12.5,
    essential: true
  })
}

function createSelectedPopupContent(location: LocationSummary) {
  const content = document.createElement('div')
  content.className = 'location-map-popup'

  const eyebrow = document.createElement('div')
  eyebrow.className = 'location-map-popup__eyebrow'
  eyebrow.textContent = `${location.city}, ${location.country}`

  const title = document.createElement('div')
  title.className = 'location-map-popup__title'
  title.textContent = location.name

  const description = document.createElement('p')
  description.className = 'location-map-popup__description'
  description.textContent =
    location.descriptionShort || 'Selecciona la sucursal para ver mas detalles.'

  const chips = document.createElement('div')
  chips.className = 'location-map-popup__chips'

  const typeChip = document.createElement('span')
  typeChip.className = 'location-map-popup__chip location-map-popup__chip--secondary'
  typeChip.textContent = businessTypeLabel(location.businessType)
  chips.append(typeChip)

  const statusChip = document.createElement('span')
  statusChip.className = 'location-map-popup__chip'
  statusChip.textContent = location.featured ? 'Lugar destacado' : 'Lugar activo'
  chips.append(statusChip)

  content.append(eyebrow, title, description, chips)

  return content
}

function removeSelectedPopup() {
  selectedPopup.value?.remove()
  selectedPopup.value = null
}

function updateSelectedPopup() {
  if (!map.value || !maplibre.value || !import.meta.client || mapUnavailable.value) {
    removeSelectedPopup()
    return
  }

  const location = selectedLocation.value

  if (!location) {
    removeSelectedPopup()
    return
  }

  const coordinates: [number, number] = [location.longitude, location.latitude]

  if (!selectedPopup.value) {
    selectedPopup.value = new maplibre.value.Popup({
      anchor: 'bottom',
      closeButton: false,
      closeOnClick: false,
      className: 'location-map-popup-shell',
      maxWidth: '320px',
      offset: [0, -42]
    })
  }

  const popup = selectedPopup.value

  popup
    .setLngLat(coordinates)
    .setDOMContent(createSelectedPopupContent(location))
    .addTo(map.value)
}

function fitToLocations() {
  if (!map.value || !maplibre.value || !props.locations.length || mapUnavailable.value) {
    return
  }

  if (selectedLocation.value) {
    focusSelectedLocation()
    return
  }

  if (props.locations.length === 1) {
    const singleLocation = props.locations[0]
    if (!singleLocation) {
      return
    }
    map.value.flyTo({
      center: [singleLocation.longitude, singleLocation.latitude],
      zoom: 12,
      essential: true
    })
    return
  }

  const bounds = new maplibre.value.LngLatBounds()
  for (const location of props.locations) {
    bounds.extend([location.longitude, location.latitude])
  }
  map.value.fitBounds(bounds, { padding: 60, maxZoom: 12, duration: 800 })
}

onMounted(async () => {
  await initializeMap()
})

onBeforeUnmount(() => {
  removeSelectedPopup()
  for (const marker of markers.values()) {
    marker.remove()
  }
  markers.clear()
  map.value?.remove()
})

watch(
  () => props.locations,
  () => {
    syncMarkers()
    fitToLocations()
    updateSelectedPopup()
  },
  { deep: true }
)

watch(
  () => props.selectedSlug,
  () => {
    for (const [slug, marker] of markers.entries()) {
      marker.remove()
      markers.delete(slug)
    }
    syncMarkers()
    focusSelectedLocation()
    updateSelectedPopup()
  },
  { immediate: true }
)

const businessTypeLabels: Record<string, string> = {
  academy: 'Academia',
  'nearby-event': 'Evento',
  'recycling-point': 'Reciclaje',
  'technical-service': 'Servicio tecnico',
  'virtual-store': 'Sucursal'
}

function businessTypeLabel(value: string) {
  return businessTypeLabels[value] || value
}
</script>

<style scoped>
:deep(.location-map-popup-shell .maplibregl-popup-content) {
  border-radius: 8px;
  box-shadow: 0 12px 32px rgba(36, 30, 24, 0.16);
  padding: 0;
}

:deep(.location-map-popup-shell .maplibregl-popup-tip) {
  border-top-color: rgb(var(--v-theme-surface));
}

:deep(.location-map-popup) {
  background: rgb(var(--v-theme-surface));
  border-radius: 8px;
  color: rgba(var(--v-theme-on-surface), 0.88);
  max-width: 320px;
  padding: 14px 16px 16px;
}

:deep(.location-map-popup__eyebrow) {
  color: rgb(var(--v-theme-secondary));
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0;
  line-height: 1.2;
  margin-bottom: 4px;
  text-transform: uppercase;
}

:deep(.location-map-popup__title) {
  font-size: 1rem;
  font-weight: 700;
  line-height: 1.3;
  margin-bottom: 8px;
}

:deep(.location-map-popup__description) {
  color: rgba(var(--v-theme-on-surface), 0.68);
  font-size: 0.875rem;
  line-height: 1.45;
  margin: 0 0 12px;
}

:deep(.location-map-popup__chips) {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

:deep(.location-map-popup__chip) {
  align-items: center;
  border: 1px solid rgb(var(--v-theme-primary));
  border-radius: 999px;
  color: rgb(var(--v-theme-primary));
  display: inline-flex;
  font-size: 0.75rem;
  font-weight: 600;
  min-height: 24px;
  padding: 2px 9px;
}

:deep(.location-map-popup__chip--secondary) {
  background: rgba(var(--v-theme-secondary), 0.12);
  border-color: transparent;
  color: rgb(var(--v-theme-secondary));
}
</style>

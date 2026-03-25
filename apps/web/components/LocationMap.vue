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
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useDisplay } from 'vuetify'

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
const markers = new Map<string, MarkerInstance>()
const { mdAndUp } = useDisplay()

const selectedLocation = computed(() =>
  props.locations.find((location) => location.slug === props.selectedSlug)
)
const mapHeight = computed(() => (mdAndUp.value ? 680 : 560))

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
  } catch (error) {
    console.warn('Map initialization failed, falling back to static location panel.', error)
    mapUnavailable.value = true
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

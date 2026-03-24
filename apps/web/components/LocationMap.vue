<template>
  <v-sheet rounded="md" class="map-card">
    <div class="map-shell">
      <div class="map-surface">
        <div v-if="!mapUnavailable" ref="mapContainer" class="map-canvas" />
        <div v-else class="map-fallback-surface" aria-hidden="true" />
      </div>

      <div class="map-summary">
        <v-card
          rounded="md"
          elevation="0"
          class="map-summary-card"
        >
          <v-card-item>
            <template #prepend>
              <v-avatar size="40" color="secondary" variant="tonal">
                <v-icon icon="mdi-map-marker-radius" />
              </v-avatar>
            </template>
            <template #title>
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

            <v-alert
              v-if="mapUnavailable"
              type="warning"
              variant="tonal"
              rounded="md"
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
            </v-list>
          </v-card-text>
        </v-card>
      </div>
    </div>
  </v-sheet>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

import type { LocationSummary } from '@lms/types'

type MapLibreModule = typeof import('maplibre-gl')
type MarkerInstance = {
  remove: () => void
  setLngLat: (coordinates: [number, number]) => MarkerInstance
  getElement: () => HTMLElement
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

const selectedLocation = computed(() =>
  props.locations.find((location) => location.slug === props.selectedSlug)
)

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
      updateMarkerElement(existingMarker.getElement(), location.slug === props.selectedSlug)
      existingMarker.setLngLat([location.longitude, location.latitude])
      continue
    }

    const markerElement = document.createElement('button')
    markerElement.type = 'button'
    markerElement.className = 'map-marker'
    markerElement.setAttribute('aria-label', location.name)
    updateMarkerElement(markerElement, location.slug === props.selectedSlug)
    markerElement.addEventListener('click', () => emit('select', location.slug))

    const marker = new maplibre.value.Marker({ element: markerElement, anchor: 'bottom' })
      .setLngLat([location.longitude, location.latitude])
      .addTo(map.value)

    markers.set(location.slug, marker as MarkerInstance)
  }
}

function updateMarkerElement(element: HTMLElement, isActive: boolean) {
  element.classList.toggle('active', isActive)
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
      updateMarkerElement(marker.getElement(), slug === props.selectedSlug)
    }
    focusSelectedLocation()
  },
  { immediate: true }
)
</script>

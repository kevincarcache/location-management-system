<template>
  <section class="map-panel">
    <div class="map-layout">
      <div class="map-stage">
        <div ref="mapContainer" class="map-canvas" />
        <div class="map-overlay">
          <p class="eyebrow">Mapa interactivo</p>
          <h2>{{ selectedLocation?.name || 'Selecciona una ubicación' }}</h2>
          <p>
            {{
              selectedLocation?.descriptionShort ||
              'Explora la lista y selecciona una ubicación para centrar el mapa.'
            }}
          </p>
        </div>
      </div>

      <div class="map-sidebar">
        <p class="eyebrow">Mapa interactivo</p>
        <h2>{{ selectedLocation?.name || 'Selecciona una ubicación' }}</h2>
        <p>
          {{
            selectedLocation?.descriptionShort ||
            'Explora la lista y selecciona una ubicación para centrar el mapa.'
          }}
        </p>
        <dl v-if="selectedLocation" class="map-details">
          <div>
            <dt>Dirección</dt>
            <dd>{{ selectedLocation.addressLine1 }}</dd>
          </div>
          <div>
            <dt>Ciudad</dt>
            <dd>{{ selectedLocation.city }}, {{ selectedLocation.country }}</dd>
          </div>
        </dl>

        <ul class="map-list">
          <li
            v-for="location in locations"
            :key="location.id"
            :class="{ active: location.slug === selectedSlug }"
          >
            <span>{{ location.name }}</span>
            <small>{{ location.latitude }}, {{ location.longitude }}</small>
          </li>
        </ul>
      </div>
    </div>
  </section>
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

const props = defineProps<{
  locations: LocationSummary[]
  selectedSlug: string | null
}>()

const emit = defineEmits<{
  select: [slug: string]
}>()

const mapContainer = ref<HTMLDivElement | null>(null)
const map = ref<any>(null)
const maplibre = ref<MapLibreModule | null>(null)
const markers = new Map<string, MarkerInstance>()

const selectedLocation = computed(() =>
  props.locations.find((location) => location.slug === props.selectedSlug)
)

async function initializeMap() {
  if (!import.meta.client || map.value || !mapContainer.value) {
    return
  }

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

  map.value.addControl(new maplibre.value.NavigationControl({ visualizePitch: true }), 'top-right')
  syncMarkers()
  fitToLocations()
}

function syncMarkers() {
  if (!map.value || !maplibre.value || !import.meta.client) {
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
  if (!map.value || !selectedLocation.value) {
    return
  }

  map.value.flyTo({
    center: [selectedLocation.value.longitude, selectedLocation.value.latitude],
    zoom: 12.5,
    essential: true
  })
}

function fitToLocations() {
  if (!map.value || !maplibre.value || !props.locations.length) {
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

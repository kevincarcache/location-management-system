<template>
  <div class="map-picker-card">
    <div class="map-picker-header">
      <div>
        <p class="eyebrow">Ubicación en mapa</p>
        <h2>Selecciona el punto exacto</h2>
      </div>
      <p class="copy">
        Usa la búsqueda para aproximar la dirección y luego ajusta el pin manualmente sobre el mapa.
      </p>
    </div>

    <div ref="mapContainer" class="admin-map-canvas" />
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

type MapPoint = {
  latitude: number
  longitude: number
}

type MapLibreModule = typeof import('maplibre-gl')

const props = defineProps<{
  modelValue: MapPoint
}>()

const emit = defineEmits<{
  'update:modelValue': [value: MapPoint]
}>()

const mapContainer = ref<HTMLDivElement | null>(null)
const map = ref<any>(null)
const marker = ref<any>(null)
const maplibre = ref<MapLibreModule | null>(null)

async function initializeMap() {
  if (!import.meta.env.SSR && mapContainer.value && !map.value) {
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
        layers: [{ id: 'osm', type: 'raster', source: 'osm' }]
      },
      center: [props.modelValue.longitude, props.modelValue.latitude],
      zoom: 12
    })

    marker.value = new maplibre.value.Marker({ draggable: true })
      .setLngLat([props.modelValue.longitude, props.modelValue.latitude])
      .addTo(map.value)

    marker.value.on('dragend', syncFromMarker)
    map.value.on('click', ({ lngLat }: { lngLat: { lat: number; lng: number } }) => {
      emit('update:modelValue', { latitude: lngLat.lat, longitude: lngLat.lng })
    })
  }
}

function syncFromMarker() {
  if (!marker.value) {
    return
  }

  const coordinates = marker.value.getLngLat()
  emit('update:modelValue', { latitude: coordinates.lat, longitude: coordinates.lng })
}

function updateMarker() {
  if (!map.value || !marker.value) {
    return
  }

  marker.value.setLngLat([props.modelValue.longitude, props.modelValue.latitude])
  map.value.flyTo({
    center: [props.modelValue.longitude, props.modelValue.latitude],
    essential: true,
    duration: 600
  })
}

onMounted(async () => {
  await initializeMap()
})

onBeforeUnmount(() => {
  marker.value?.remove()
  map.value?.remove()
})

watch(
  () => props.modelValue,
  () => {
    updateMarker()
  },
  { deep: true }
)
</script>

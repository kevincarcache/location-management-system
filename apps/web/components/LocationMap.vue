<template>
  <section class="map-panel">
    <div class="map-placeholder">
      <div>
        <p class="eyebrow">Mapa interactivo</p>
        <h2>{{ selectedLocation?.name || 'Selecciona una ubicación' }}</h2>
        <p>
          Aquí se integrará MapLibre con markers sincronizados con la lista y filtros del
          sidebar.
        </p>
      </div>

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
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import type { LocationSummary } from '@lms/types'

const props = defineProps<{
  locations: LocationSummary[]
  selectedSlug: string | null
}>()

const selectedLocation = computed(() =>
  props.locations.find((location) => location.slug === props.selectedSlug)
)
</script>

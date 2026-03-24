<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <h2>Ubicaciones</h2>
      <span>{{ props.locations.length }} resultados</span>
    </div>

    <div v-if="!props.locations.length" class="empty-state">
      No encontramos ubicaciones con ese criterio de búsqueda.
    </div>

    <button
      v-for="location in props.locations"
      :key="location.id"
      class="location-card"
      :class="{ active: location.slug === props.selectedSlug }"
      @click="emit('select', location.slug)"
    >
      <div class="location-card-top">
        <strong>{{ location.name }}</strong>
        <span>{{ location.businessType }}</span>
      </div>
      <p>{{ location.addressLine1 }}</p>
      <small>{{ location.city }}, {{ location.country }}</small>
    </button>
  </aside>
</template>

<script setup lang="ts">
import type { LocationSummary } from '@lms/types'

const props = defineProps<{
  locations: LocationSummary[]
  selectedSlug: string | null
}>()

const emit = defineEmits<{
  select: [slug: string]
}>()
</script>

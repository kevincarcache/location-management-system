<template>
  <div class="shell">
    <header class="hero">
      <div>
        <p class="eyebrow">Location Management System</p>
        <h1>Encuentra la ubicación correcta para cada necesidad.</h1>
        <p class="lede">
          Explora sucursales, eventos, puntos de reciclaje, academias y servicios técnicos
          desde una experiencia unificada.
        </p>
      </div>
      <input
        v-model="query"
        class="search"
        type="search"
        placeholder="Buscar por nombre, ciudad o dirección"
      />
    </header>

    <main class="locator">
      <LocationSidebar
        :locations="filteredLocations"
        :selected-slug="selectedSlug"
        @select="selectedSlug = $event"
      />
      <LocationMap :locations="filteredLocations" :selected-slug="selectedSlug" />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'

import { useLocations } from './composables/useLocations'

const { locations } = useLocations()
const query = ref('')
const selectedSlug = ref<string | null>(null)

const filteredLocations = computed(() => {
  const normalized = query.value.trim().toLowerCase()
  if (!normalized) {
    return locations.value
  }

  return locations.value.filter((location) => {
    return (
      location.name.toLowerCase().includes(normalized) ||
      location.city.toLowerCase().includes(normalized) ||
      location.addressLine1.toLowerCase().includes(normalized)
    )
  })
})

watch(
  filteredLocations,
  (items) => {
    if (!items.length) {
      selectedSlug.value = null
      return
    }

    const firstItem = items[0]
    if (!selectedSlug.value || !items.some((item) => item.slug === selectedSlug.value)) {
      selectedSlug.value = firstItem?.slug ?? null
    }
  },
  { immediate: true }
)
</script>

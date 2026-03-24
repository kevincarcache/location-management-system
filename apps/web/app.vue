<template>
  <div class="shell">
    <header class="hero">
      <div class="hero-copy">
        <p class="eyebrow">Location Management System</p>
        <h1>Encuentra la ubicación correcta para cada necesidad.</h1>
        <p class="lede">
          Explora sucursales, eventos, puntos de reciclaje, academias y servicios técnicos
          desde una experiencia unificada.
        </p>
      </div>
      <div class="filters">
        <input
          v-model="query"
          class="search"
          type="search"
          placeholder="Buscar por nombre, ciudad o dirección"
        />
        <select v-model="businessType" class="search search-select">
          <option value="all">Todos los tipos</option>
          <option
            v-for="option in businessTypeFilterOptions"
            :key="option.value"
            :value="option.value"
          >
            {{ option.label }}
          </option>
        </select>
      </div>
    </header>

    <section v-if="pending" class="hero-card state-card">
      <p class="eyebrow">Cargando</p>
      <h2>Estamos preparando las ubicaciones disponibles.</h2>
      <p class="lede">El catálogo se está consultando desde la API pública.</p>
    </section>

    <section v-else-if="error" class="hero-card state-card">
      <p class="eyebrow">Conexión</p>
      <h2>No pudimos cargar las ubicaciones.</h2>
      <p class="lede">
        Verifica que la API esté corriendo en {{ apiBase }} y vuelve a intentarlo.
      </p>
      <button class="primary-button" @click="refresh()">Reintentar</button>
    </section>

    <main v-else class="locator">
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
import { computed, watch } from 'vue'

import type { BusinessType } from '@lms/types'
import { businessTypeLabels } from '@lms/ui'
import { useLocations } from './composables/useLocations'

const route = useRoute()
const router = useRouter()
const config = useRuntimeConfig()

const query = ref(typeof route.query.q === 'string' ? route.query.q : '')
const businessType = ref<BusinessType | 'all'>(
  typeof route.query.type === 'string' &&
    route.query.type in businessTypeLabels
    ? (route.query.type as BusinessType)
    : 'all'
)
const selectedSlug = ref<string | null>(
  typeof route.query.selected === 'string' ? route.query.selected : null
)

const { locations, pending, error, refresh } = await useLocations()
const apiBase = config.public.apiBase

const businessTypeFilterOptions = Object.entries(businessTypeLabels).map(([value, label]) => ({
  value: value as BusinessType,
  label
}))

const filteredLocations = computed(() => {
  const normalized = query.value.trim().toLowerCase()
  return locations.value.filter((location) => {
    const matchesQuery =
      !normalized ||
      location.name.toLowerCase().includes(normalized) ||
      location.city.toLowerCase().includes(normalized) ||
      location.addressLine1.toLowerCase().includes(normalized)

    const matchesType =
      businessType.value === 'all' || location.businessType === businessType.value

    return matchesQuery && matchesType
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

watch(
  [query, businessType, selectedSlug],
  async ([nextQuery, nextType, nextSelected]) => {
    await router.replace({
      query: {
        ...(nextQuery ? { q: nextQuery } : {}),
        ...(nextType !== 'all' ? { type: nextType } : {}),
        ...(nextSelected ? { selected: nextSelected } : {})
      }
    })
  },
  { flush: 'post' }
)
</script>

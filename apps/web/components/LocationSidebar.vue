<template>
  <v-sheet rounded="md" class="location-sidebar h-100">
    <v-card-item class="pb-2 px-4 px-md-5 pt-4 pt-md-5">
      <template #title>
        <span class="text-h6">{{ title }}</span>
      </template>
      <template #append>
        <v-chip size="small" variant="outlined" color="secondary">
          {{ props.locations.length }} resultados
        </v-chip>
      </template>
    </v-card-item>

    <v-divider />

    <v-card-text class="pa-2 pa-md-3">
      <v-alert
        v-if="!props.locations.length"
        type="info"
        variant="tonal"
        rounded="md"
      >
        No encontramos ubicaciones con ese criterio de búsqueda.
      </v-alert>

      <v-list v-else nav class="bg-transparent d-flex flex-column ga-2">
        <v-list-item
          v-for="location in props.locations"
          :key="location.id"
          rounded="md"
          :active="location.slug === props.selectedSlug"
          color="primary"
          class="location-list-item py-5 px-5"
          @click="emit('select', location.slug)"
        >
          <template #prepend>
            <v-avatar size="36" color="primary" variant="tonal">
              <v-icon icon="mdi-map-marker" />
            </v-avatar>
          </template>

          <v-list-item-title class="font-weight-semibold text-body-1 mb-1">
            {{ location.name }}
          </v-list-item-title>
          <v-list-item-subtitle class="text-body-2 text-medium-emphasis">
            {{ location.addressLine1 }}
          </v-list-item-subtitle>
          <v-list-item-subtitle class="text-body-2 text-medium-emphasis mt-1">
            {{ location.city }}, {{ location.country }}
          </v-list-item-subtitle>

          <div v-if="location.descriptionShort" class="text-body-2 text-medium-emphasis mt-3">
            {{ location.descriptionShort }}
          </div>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-sheet>
</template>

<script setup lang="ts">
import type { LocationSummary } from '@lms/types'

const props = withDefaults(defineProps<{
  locations: LocationSummary[]
  selectedSlug: string | null
  title: string
}>(), {
  locations: () => [],
  selectedSlug: null,
  title: 'Ubicaciones'
})

const emit = defineEmits<{
  select: [slug: string]
}>()
</script>

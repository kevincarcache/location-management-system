<template>
  <v-sheet
    rounded="lg"
    border
    color="background"
    class="location-sidebar h-100 pa-2 pa-md-3"
  >
    <div class="d-flex align-center justify-space-between px-2 px-md-3 pt-2 pb-4 flex-shrink-0">
      <div>
        <div class="text-overline text-secondary">Registro</div>
        <div class="text-h6">{{ title }}</div>
      </div>
      <v-chip size="small" variant="outlined" color="secondary">
        {{ props.locations.length }} resultados
      </v-chip>
    </div>

    <v-divider class="mb-3 flex-shrink-0" />

    <div class="location-sidebar__body">
      <v-alert
        v-if="!props.locations.length"
        type="info"
        variant="tonal"
        rounded="lg"
      >
        No encontramos ubicaciones con ese criterio de búsqueda.
      </v-alert>

      <v-list v-else nav bg-color="transparent" class="d-flex flex-column ga-2 pa-0">
        <v-list-item
          v-for="location in props.locations"
          :key="location.id"
          rounded="lg"
          :active="location.slug === props.selectedSlug"
          :base-color="location.slug === props.selectedSlug ? 'secondary' : 'primary'"
          border
          class="py-4 px-4"
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
          <div class="d-flex align-center flex-wrap ga-2 mb-2">
            <span class="text-overline text-secondary">{{ location.city }}, {{ location.country }}</span>
            <v-chip
              size="x-small"
              variant="tonal"
              color="secondary"
            >
              {{ businessTypeLabel(location.businessType) }}
            </v-chip>
            <v-chip
              v-if="location.featured"
              size="x-small"
              variant="outlined"
              color="primary"
            >
              Destacado
            </v-chip>
          </div>
          <v-list-item-subtitle class="text-body-2 text-medium-emphasis">
            {{ location.addressLine1 }}
          </v-list-item-subtitle>

          <div v-if="location.descriptionShort" class="text-body-2 text-medium-emphasis mt-3">
            {{ location.descriptionShort }}
          </div>
        </v-list-item>
      </v-list>
    </div>
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
.location-sidebar {
  display: flex;
  flex-direction: column;
  max-height: 560px;
  min-height: 0;
}

.location-sidebar__body {
  flex: 1 1 auto;
  min-height: 0;
  overflow-y: auto;
  padding-right: 4px;
}

@media (min-width: 1280px) {
  .location-sidebar {
    max-height: 680px;
  }
}
</style>

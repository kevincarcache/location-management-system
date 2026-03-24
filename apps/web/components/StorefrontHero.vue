<template>
  <v-sheet
    rounded="md"
    class="storefront-hero mb-5 mb-md-7"
  >
    <v-row align="center" class="ga-0">
      <v-col cols="12" md="8" lg="7" class="pa-6 pa-md-9">
        <div class="text-overline text-secondary mb-4">
          {{ storeConfig?.brand_name || 'Negocio' }}
        </div>
        <h1 class="storefront-hero-title font-weight-bold text-high-emphasis mb-4">
          {{ storeConfig?.hero_title || 'Encuentra nuestras ubicaciones' }}
        </h1>
        <p class="text-body-1 text-medium-emphasis mb-0 storefront-lede">
          {{
            storeConfig?.hero_subtitle ||
            'Consulta nuestras ubicaciones, horarios y puntos de atención en un solo lugar.'
          }}
        </p>
      </v-col>

      <v-col cols="12" md="4" lg="5" class="pa-4 pa-md-7 d-flex align-center justify-md-end">
        <v-sheet rounded="md" class="storefront-search-panel pa-5 pa-md-6">
          <div class="storefront-search-copy">
            <div class="text-overline text-secondary mb-2">Búsqueda rápida</div>
            <p class="text-body-2 text-medium-emphasis mb-0">
              {{
                storeConfig?.business_description ||
                'Información del negocio cargada desde configuración.'
              }}
            </p>
          </div>
          <div class="storefront-search-field">
            <v-text-field
              :model-value="query"
              rounded="md"
              variant="solo-filled"
              flat
              prepend-inner-icon="mdi-magnify"
              label="Buscar por nombre, ciudad o dirección"
              @update:model-value="emit('update:query', $event ?? '')"
            />
          </div>
        </v-sheet>
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script setup lang="ts">
import type { StoreConfig } from '../composables/useStoreConfig'

withDefaults(defineProps<{
  query: string
  storeConfig: StoreConfig | null | undefined
}>(), {
  query: '',
  storeConfig: undefined
})

const emit = defineEmits<{
  'update:query': [value: string]
}>()
</script>

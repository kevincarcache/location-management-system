<template>
  <v-sheet
    rounded="lg"
    color="surface"
    border
    class="mb-5 mb-md-7"
  >
    <v-row align="stretch">
      <v-col cols="12" md="7" lg="7" class="pa-6 pa-md-9">
        <div class="text-overline text-secondary mb-3">
          {{ storeConfig?.brand_name || 'Negocio' }}
        </div>
        <h1 class="text-h2 text-md-h1 font-weight-black mb-4">
          {{ storeConfig?.hero_title || 'Encuentra nuestras ubicaciones' }}
        </h1>
        <p class="text-body-1 text-medium-emphasis mb-0">
          {{
            storeConfig?.hero_subtitle ||
            'Consulta nuestras ubicaciones, horarios y puntos de atención en un solo lugar.'
          }}
        </p>

        <v-row class="mt-4">
          <v-col cols="12" sm="6">
            <v-sheet rounded="lg" border color="background" class="pa-4 h-100">
              <div class="text-overline text-secondary">Ubicaciones visibles</div>
              <div class="text-h5 font-weight-bold">{{ totalLocations }}</div>
            </v-sheet>
          </v-col>
          <v-col cols="12" sm="6">
            <v-sheet rounded="lg" border color="background" class="pa-4 h-100">
              <div class="text-overline text-secondary">Destacadas</div>
              <div class="text-h5 font-weight-bold">{{ featuredCount }}</div>
            </v-sheet>
          </v-col>
        </v-row>
      </v-col>

      <v-col cols="12" md="5" lg="5" class="pa-4 pa-md-7 d-flex align-center">
        <v-sheet
          rounded="lg"
          color="background"
          border
          class="pa-5 pa-md-6 d-flex flex-column ga-5 w-100"
        >
          <div>
            <div class="text-overline text-secondary mb-2">Comienza el recorrido</div>
            <p class="text-body-2 text-medium-emphasis mb-4">
              {{
                storeConfig?.business_description ||
                'Información del negocio cargada desde configuración.'
              }}
            </p>
            <div class="d-flex flex-wrap ga-2 mb-4">
              <v-btn variant="flat" color="primary" @click="emit('navigate', 'locations')">
                Ver registro
              </v-btn>
              <v-btn variant="text" color="secondary" @click="emit('navigate', 'mapa')">
                Abrir mapa
              </v-btn>
            </div>
          </div>

          <div class="d-flex justify-center">
            <v-text-field
              :model-value="query"
              max-width="520"
              prepend-inner-icon="mdi-magnify"
              label="Buscar por nombre, ciudad o dirección"
              class="w-100"
              @update:model-value="emit('update:query', $event ?? '')"
            />
          </div>
        </v-sheet>
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script setup lang="ts">
import type { StoreConfig } from '@lms/types'

withDefaults(defineProps<{
  featuredCount: number
  query: string
  resolvedStoreview: string | null | undefined
  storeConfig: StoreConfig | null | undefined
  totalLocations: number
}>(), {
  featuredCount: 0,
  query: '',
  resolvedStoreview: undefined,
  storeConfig: undefined,
  totalLocations: 0
})

const emit = defineEmits<{
  navigate: [id: string]
  'update:query': [value: string]
}>()
</script>

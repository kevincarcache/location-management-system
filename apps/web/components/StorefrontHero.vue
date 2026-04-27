<template>
  <v-sheet
    rounded="lg"
    color="surface"
    border
    class="mb-5 mb-md-7"
  >
    <v-row align="stretch">
      <v-col cols="12" md="9" lg="8" class="pa-6 pa-md-9">
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
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script setup lang="ts">
import type { StoreConfig } from '@lms/types'

withDefaults(defineProps<{
  storeConfig: StoreConfig | null | undefined
}>(), {
  storeConfig: undefined,
})
</script>

<template>
  <v-footer id="contacto" border color="surface">
    <v-container max-width="1480" class="px-4 px-md-6 py-8">
      <v-row>
        <v-col cols="12" md="7">
          <div class="text-subtitle-1 font-weight-bold mb-1">
            {{ storeConfig?.brand_name || 'Storefront' }}
          </div>
          <p class="text-body-2 text-medium-emphasis mb-4 mb-md-0">
            {{ storeConfig?.footer_text || 'Consulta nuestras ubicaciones y servicios.' }}
          </p>
        </v-col>
        <v-col cols="12" md="5" class="d-flex flex-column align-md-end justify-center">
          <div class="d-flex flex-wrap ga-2 mb-3">
            <v-btn variant="text" color="accent" href="#locations">Registro</v-btn>
            <v-btn variant="text" color="accent" href="#mapa">Mapa</v-btn>
            <v-btn variant="text" color="accent" href="#contacto">Contacto</v-btn>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script setup lang="ts">
import type { StoreConfig } from '@lms/types'

defineProps<{
  storeConfig: StoreConfig | null | undefined
}>()
</script>

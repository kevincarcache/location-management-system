<template>
  <v-footer id="contacto" border color="surface" class="storefront-footer">
    <v-container max-width="1480" class="px-4 px-md-6">
      <v-row align="center" class="ga-0">
        <v-col cols="12" md="8">
          <div class="text-subtitle-1 font-weight-bold mb-1">
            {{ storeConfig?.brand_name || 'Storefront' }}
          </div>
          <p class="text-body-2 text-medium-emphasis mb-0">
            {{ storeConfig?.footer_text || 'Consulta nuestras ubicaciones y servicios.' }}
          </p>
        </v-col>
        <v-col cols="12" md="4" class="text-md-right mt-3 mt-md-0">
          <span class="text-caption text-medium-emphasis">
            Storeview: {{ resolvedStoreview || storeConfig?.slug || 'default' }}
          </span>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script setup lang="ts">
import type { StoreConfig } from '@lms/types'

defineProps<{
  resolvedStoreview: string | null | undefined
  storeConfig: StoreConfig | null | undefined
}>()
</script>

<template>
  <div>
    <v-app-bar
      color="surface"
      border
      flat
      height="76"
      scroll-behavior="elevate"
      class="px-2 px-md-6"
    >
      <v-app-bar-title>
        <div class="d-flex flex-column py-2">
          <span class="text-overline text-secondary">{{ brandName }}</span>
          <span class="text-subtitle-1 font-weight-bold">{{ menuLabel }}</span>
        </div>
      </v-app-bar-title>
    </v-app-bar>
  </div>
</template>

<script setup lang="ts">
import type { StoreConfig } from '@lms/types'
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  storeConfig: StoreConfig | null | undefined
}>(), {
  storeConfig: undefined
})

const brandName = computed(() => props.storeConfig?.brand_name || 'Storefront')
const menuLabel = computed(() => props.storeConfig?.menu_label || 'Ubicaciones')
</script>

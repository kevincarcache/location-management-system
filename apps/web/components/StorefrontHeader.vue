<template>
  <div>
    <v-toolbar flat height="72" class="storefront-app-bar px-2 px-md-5">
      <template #prepend>
        <v-btn
          class="d-md-none"
          icon="mdi-menu"
          variant="text"
          @click="emit('toggle-drawer')"
        />
      </template>

      <v-toolbar-title class="storefront-title">
        <div class="storefront-brand">
          <span class="storefront-brand-name text-secondary">{{ brandName }}</span>
          <span class="storefront-brand-context text-high-emphasis">{{ menuLabel }}</span>
        </div>
      </v-toolbar-title>

      <v-spacer />

      <div class="d-none d-md-flex align-center ga-1">
        <v-btn variant="text" color="accent" @click="emit('navigate', 'locations')">{{ menuLabel }}</v-btn>
        <v-btn variant="text" color="accent" @click="emit('navigate', 'mapa')">Mapa</v-btn>
        <v-btn variant="text" color="accent" @click="emit('navigate', 'contacto')">Contacto</v-btn>
      </div>
    </v-toolbar>

    <ClientOnly>
      <v-navigation-drawer
        :model-value="drawer"
        location="right"
        temporary
        width="300"
        class="storefront-drawer"
        @update:model-value="emit('update:drawer', $event)"
      >
        <v-list nav class="py-4">
          <v-list-subheader class="text-secondary">
            {{ brandName }}
          </v-list-subheader>
          <v-list-item
            :title="menuLabel"
            prepend-icon="mdi-format-list-bulleted-square"
            @click="emit('navigate', 'locations')"
          />
          <v-list-item title="Mapa" prepend-icon="mdi-map-marker-radius" @click="emit('navigate', 'mapa')" />
          <v-list-item title="Contacto" prepend-icon="mdi-email-outline" @click="emit('navigate', 'contacto')" />
        </v-list>
      </v-navigation-drawer>
    </ClientOnly>
  </div>
</template>

<script setup lang="ts">
import type { StoreConfig } from '@lms/types'
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  drawer: boolean
  storeConfig: StoreConfig | null | undefined
}>(), {
  drawer: false,
  storeConfig: undefined
})

const emit = defineEmits<{
  'toggle-drawer': []
  'update:drawer': [value: boolean]
  navigate: [id: string]
}>()

const brandName = computed(() => props.storeConfig?.brand_name || 'Storefront')
const menuLabel = computed(() => props.storeConfig?.menu_label || 'Ubicaciones')
</script>

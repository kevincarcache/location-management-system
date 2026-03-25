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
      <template #prepend>
        <v-btn
          class="d-md-none"
          icon="mdi-menu"
          variant="text"
          @click="emit('toggle-drawer')"
        />
      </template>

      <v-app-bar-title>
        <div class="d-flex flex-column py-2">
          <span class="text-overline text-secondary">{{ brandName }}</span>
          <span class="text-subtitle-1 font-weight-bold">{{ menuLabel }}</span>
        </div>
      </v-app-bar-title>

      <v-spacer />

      <div class="d-none d-md-flex align-center ga-2">
        <v-btn variant="text" color="accent" @click="emit('navigate', 'locations')">
          {{ menuLabel }}
        </v-btn>
        <v-btn variant="text" color="accent" @click="emit('navigate', 'mapa')">
          Mapa
        </v-btn>
        <v-btn variant="text" color="accent" @click="emit('navigate', 'contacto')">
          Contacto
        </v-btn>
        <v-chip
          v-if="resolvedStoreview"
          size="small"
          color="secondary"
          variant="outlined"
          class="ms-2"
        >
          {{ resolvedStoreview }}
        </v-chip>
      </div>
    </v-app-bar>

    <ClientOnly>
      <v-navigation-drawer
        :model-value="drawer"
        location="right"
        temporary
        width="320"
        @update:model-value="emit('update:drawer', $event)"
      >
        <v-list nav class="py-4">
          <v-list-subheader class="text-secondary text-overline">
            {{ brandName }}
          </v-list-subheader>
          <v-list-item
            :title="menuLabel"
            prepend-icon="mdi-format-list-bulleted-square"
            @click="emit('navigate', 'locations')"
          />
          <v-list-item title="Mapa" prepend-icon="mdi-map-marker-radius" @click="emit('navigate', 'mapa')" />
          <v-list-item title="Contacto" prepend-icon="mdi-email-outline" @click="emit('navigate', 'contacto')" />
          <v-divider class="my-3" />
          <v-list-item
            v-if="resolvedStoreview"
            :title="resolvedStoreview"
            subtitle="Contexto activo"
            prepend-icon="mdi-compass-outline"
          />
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
  resolvedStoreview: string | null | undefined
  storeConfig: StoreConfig | null | undefined
}>(), {
  drawer: false,
  resolvedStoreview: undefined,
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

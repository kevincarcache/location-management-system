<template>
  <div class="page-shell">
    <header class="page-header">
      <div>
        <p class="eyebrow">Resumen general</p>
        <h1>Dashboard</h1>
        <p class="copy">
          Vista inicial de la operación, el storefront activo y el estado del catálogo.
        </p>
      </div>
      <div class="header-actions">
        <v-btn color="primary" to="/locations">Gestionar localizaciones</v-btn>
        <v-btn variant="outlined" to="/store-settings">Configurar tienda</v-btn>
      </div>
    </header>

    <section class="stats-grid">
      <v-card class="stat-card" elevation="0">
        <span>Localizaciones activas</span>
        <strong>{{ activeCount }}</strong>
      </v-card>
      <v-card class="stat-card" elevation="0">
        <span>Total del catálogo</span>
        <strong>{{ totalCount }}</strong>
      </v-card>
      <v-card class="stat-card" elevation="0">
        <span>Storeview activo</span>
        <strong>{{ storeSlug }}</strong>
      </v-card>
    </section>

    <div class="dashboard-grid">
      <v-card elevation="0" class="panel-card">
        <v-card-text>
          <p class="eyebrow">Storefront</p>
          <h2>{{ storeName }}</h2>
          <p class="copy">{{ storeDescription }}</p>
        </v-card-text>
      </v-card>

      <v-card elevation="0" class="panel-card">
        <v-card-text>
          <p class="eyebrow">Siguientes acciones</p>
          <h2>Atajos de operación</h2>
          <div class="quick-actions">
            <v-btn variant="outlined" to="/locations/new">Nueva localización</v-btn>
            <v-btn variant="outlined" to="/reports">Ver reportes</v-btn>
            <v-btn variant="outlined" to="/location-types">Revisar tipos</v-btn>
          </div>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import { getLocations, getStoreConfigs, type ApiLocation, type StoreConfig } from '../lib/admin-api'
import { useSessionStore } from '../stores/session'

const session = useSessionStore()
const locations = ref<ApiLocation[]>([])
const storeConfig = ref<StoreConfig | null>(null)

const activeCount = computed(() => locations.value.filter((item) => item.status === 'active').length)
const totalCount = computed(() => locations.value.length)
const storeSlug = computed(() => storeConfig.value?.slug ?? 'default')
const storeName = computed(() => storeConfig.value?.brand_name ?? 'Storefront principal')
const storeDescription = computed(
  () => storeConfig.value?.business_description ?? 'Configura el mensaje comercial desde el panel.'
)

async function loadDashboard() {
  if (!session.accessToken.value) {
    return
  }

  const [locationData, storeConfigs] = await Promise.all([
    getLocations(session.accessToken.value),
    getStoreConfigs(session.accessToken.value)
  ])

  locations.value = locationData
  storeConfig.value = storeConfigs[0] ?? null
}

onMounted(loadDashboard)
</script>

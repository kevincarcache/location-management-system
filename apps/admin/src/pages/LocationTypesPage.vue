<template>
  <div class="page-shell">
    <header class="page-header">
      <div>
        <p class="eyebrow">Catálogo</p>
        <h1>Gestionar tipos de localización</h1>
        <p class="copy">
          El sistema mantiene el catálogo base y la tienda activa define cuál es el tipo principal
          que verá el frontend público.
        </p>
      </div>
      <div class="header-actions">
        <v-btn color="primary" to="/store-settings">Configurar storefront</v-btn>
      </div>
    </header>

    <div class="types-grid">
      <v-card v-for="option in businessTypeOptions" :key="option.value" elevation="0" class="panel-card">
        <v-card-text>
          <p class="eyebrow">Tipo disponible</p>
          <h2>{{ option.title }}</h2>
          <p class="copy">
            {{ descriptions[option.value] }}
          </p>
          <v-chip
            v-if="storeBusinessType === option.value"
            color="primary"
            size="small"
            variant="flat"
          >
            Tipo activo del storefront
          </v-chip>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { businessTypeOptions } from '../constants/business'
import { getStoreConfigs } from '../lib/admin-api'
import { useSessionStore } from '../stores/session'

const session = useSessionStore()
const storeBusinessType = ref<string | null>(null)

const descriptions: Record<string, string> = {
  'virtual-store': 'Ideal para cadenas con sucursales o puntos de atención estables.',
  'nearby-event': 'Pensado para agendas de eventos con presencia temporal o itinerante.',
  'recycling-point': 'Útil para campañas ambientales y centros de recolección especializados.',
  academy: 'Enfocado en academias, campus y centros de formación con distintas sedes.',
  'technical-service': 'Adecuado para talleres, laboratorios y puntos de soporte técnico.'
}

async function loadStoreConfig() {
  if (!session.accessToken.value) {
    return
  }

  const configs = await getStoreConfigs(session.accessToken.value)
  storeBusinessType.value = configs[0]?.business_type ?? null
}

onMounted(loadStoreConfig)
</script>

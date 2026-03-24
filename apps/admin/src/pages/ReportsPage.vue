<template>
  <div class="page-shell">
    <header class="page-header">
      <div>
        <p class="eyebrow">Analítica</p>
        <h1>Reportes</h1>
        <p class="copy">Resumen operativo del catálogo para tomar decisiones rápidas.</p>
      </div>
    </header>

    <section class="stats-grid">
      <v-card elevation="0" class="stat-card">
        <span>Activas</span>
        <strong>{{ activeCount }}</strong>
      </v-card>
      <v-card elevation="0" class="stat-card">
        <span>Destacadas</span>
        <strong>{{ featuredCount }}</strong>
      </v-card>
      <v-card elevation="0" class="stat-card">
        <span>En borrador</span>
        <strong>{{ draftCount }}</strong>
      </v-card>
    </section>

    <v-card elevation="0" class="panel-card">
      <v-card-text>
        <div class="section-heading">
          <div>
            <p class="eyebrow">Distribución</p>
            <h2>Ubicaciones por tipo</h2>
          </div>
        </div>

        <v-table>
          <thead>
            <tr>
              <th>Tipo</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in byType" :key="row.type">
              <td>{{ row.title }}</td>
              <td>{{ row.total }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import { businessTypeOptions } from '../constants/business'
import { getLocations, type ApiLocation } from '../lib/admin-api'
import { useSessionStore } from '../stores/session'

const session = useSessionStore()
const locations = ref<ApiLocation[]>([])

const activeCount = computed(() => locations.value.filter((item) => item.status === 'active').length)
const featuredCount = computed(() => locations.value.filter((item) => item.featured).length)
const draftCount = computed(() => locations.value.filter((item) => item.status === 'draft').length)
const byType = computed(() =>
  businessTypeOptions.map((option) => ({
    type: option.value,
    title: option.title,
    total: locations.value.filter((item) => item.business_type === option.value).length
  }))
)

async function loadLocations() {
  if (!session.accessToken.value) {
    return
  }

  locations.value = await getLocations(session.accessToken.value)
}

onMounted(loadLocations)
</script>

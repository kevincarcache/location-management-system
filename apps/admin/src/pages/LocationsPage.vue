<template>
  <div class="page-shell">
    <header class="page-header">
      <div>
        <p class="eyebrow">Catalog</p>
        <h1>Ubicaciones</h1>
      </div>
      <div class="header-actions">
        <v-btn variant="outlined">Descargar CSV</v-btn>
        <v-btn color="primary">Importar CSV</v-btn>
      </div>
    </header>

    <v-card elevation="0" class="table-card">
      <v-table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Tipo</th>
            <th>Ciudad</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="location in locations" :key="location.slug">
            <td>{{ location.name }}</td>
            <td>{{ location.businessType }}</td>
            <td>{{ location.city }}</td>
            <td>{{ location.status }}</td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import type { LocationSummary } from '@lms/types'

const locations: LocationSummary[] = [
  {
    id: 'seed-001',
    slug: 'panama-city-hub',
    name: 'Panama City Hub',
    businessType: 'virtual-store',
    status: 'active',
    city: 'Panama City',
    country: 'Panama',
    latitude: 8.9824,
    longitude: -79.5199,
    addressLine1: 'Avenida Balboa, Torre Central',
    featured: true
  },
  {
    id: 'seed-002',
    slug: 'recycling-costa-del-este',
    name: 'Punto Verde Costa del Este',
    businessType: 'recycling-point',
    status: 'active',
    city: 'Panama City',
    country: 'Panama',
    latitude: 9.0075,
    longitude: -79.4818,
    addressLine1: 'Boulevard Costa del Este',
    featured: false
  }
]
</script>


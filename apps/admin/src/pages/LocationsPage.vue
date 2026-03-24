<template>
  <div class="page-shell">
    <header class="page-header">
      <div>
        <p class="eyebrow">Catálogo</p>
        <h1>Lista de localizaciones</h1>
        <p class="copy">
          Administra el catálogo activo, abre fichas individuales y ejecuta importaciones masivas.
        </p>
      </div>
      <div class="header-actions">
        <v-btn color="primary" data-testid="new-location-button" to="/locations/new">
          Nueva localización
        </v-btn>
        <v-btn variant="outlined" data-testid="download-template-button" @click="downloadTemplate">
          Descargar plantilla
        </v-btn>
        <v-btn variant="outlined" data-testid="open-import-dialog-button" @click="isImportDialogOpen = true">
          Importar CSV
        </v-btn>
      </div>
    </header>

    <v-alert v-if="errorMessage" type="error" variant="tonal" class="mb-4">
      {{ errorMessage }}
    </v-alert>

    <v-card elevation="0" class="panel-card">
      <v-card-text>
        <div class="table-toolbar">
          <v-text-field
            v-model="search"
            label="Buscar por nombre o ciudad"
            variant="outlined"
            density="comfortable"
            hide-details
          />
          <v-btn variant="text" :loading="isLoading" @click="loadLocations">Recargar</v-btn>
        </div>

        <v-table>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Tipo</th>
              <th>Ciudad</th>
              <th>Estado</th>
              <th class="text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="location in filteredLocations" :key="location.id">
              <td>{{ location.name }}</td>
              <td>{{ businessTypeTitle(location.business_type) }}</td>
              <td>{{ location.city }}</td>
              <td>{{ statusTitle(location.status) }}</td>
              <td class="text-right">
                <v-btn size="small" variant="text" :to="`/locations/${location.id}/edit`">Editar</v-btn>
                <v-btn size="small" variant="text" color="error" @click="remove(location.id)">
                  Eliminar
                </v-btn>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card-text>
    </v-card>

    <v-card v-if="lastImportJob" elevation="0" class="panel-card import-summary-card">
      <v-card-text>
        <div class="summary-grid">
          <div>
            <span class="eyebrow">Última importación</span>
            <strong>{{ lastImportJob.filename }}</strong>
          </div>
          <div>
            <span class="eyebrow">Creadas</span>
            <strong>{{ lastImportJob.created }}</strong>
          </div>
          <div>
            <span class="eyebrow">Actualizadas</span>
            <strong>{{ lastImportJob.updated }}</strong>
          </div>
          <div>
            <span class="eyebrow">Rechazadas</span>
            <strong>{{ lastImportJob.rejected }}</strong>
          </div>
        </div>

        <v-table v-if="lastImportJob.errors.length">
          <thead>
            <tr>
              <th>Fila</th>
              <th>Error</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="error in lastImportJob.errors" :key="error.id">
              <td>{{ error.row_number }}</td>
              <td>{{ error.message }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-card-text>
    </v-card>

    <v-dialog v-model="isImportDialogOpen" max-width="720">
      <v-card class="dialog-card">
        <v-card-title>Importar localizaciones</v-card-title>
        <v-card-text>
          <p class="copy">
            Requeridos: <code>external_id</code>, <code>name</code>, <code>business_type</code>,
            <code>address_line_1</code>, <code>city</code>, <code>country</code>,
            <code>latitude</code>, <code>longitude</code>.
          </p>
          <v-file-input
            v-model="importFile"
            accept=".csv,text/csv"
            label="Archivo CSV"
            variant="outlined"
            prepend-icon=""
            data-testid="import-file-input"
          />
          <div v-if="importPreview" class="import-preview">
            <div class="summary-grid">
              <div>
                <span class="eyebrow">Filas</span>
                <strong>{{ importPreview.total_rows }}</strong>
              </div>
              <div>
                <span class="eyebrow">Crear</span>
                <strong>{{ importPreview.create_candidates }}</strong>
              </div>
              <div>
                <span class="eyebrow">Actualizar</span>
                <strong>{{ importPreview.update_candidates }}</strong>
              </div>
              <div>
                <span class="eyebrow">Rechazar</span>
                <strong>{{ importPreview.rejected_rows }}</strong>
              </div>
            </div>

            <v-table>
              <thead>
                <tr>
                  <th>Fila</th>
                  <th>Acción</th>
                  <th>Nombre</th>
                  <th>Detalle</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in importPreview.rows" :key="`${row.row_number}-${row.slug}`">
                  <td>{{ row.row_number }}</td>
                  <td>{{ row.action }}</td>
                  <td>{{ row.name || row.slug || '-' }}</td>
                  <td>{{ row.message || row.business_type || '-' }}</td>
                </tr>
              </tbody>
            </v-table>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="closeImportDialog">Cancelar</v-btn>
          <v-btn variant="outlined" data-testid="preview-import-button" :loading="isPreviewing" @click="previewImport">
            Preview
          </v-btn>
          <v-btn
            color="primary"
            data-testid="confirm-import-button"
            :loading="isImporting"
            :disabled="!importPreview || importPreview.valid_rows === 0"
            @click="submitImport"
          >
            Confirmar importación
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import { businessTypeOptions, locationStatusOptions } from '../constants/business'
import {
  deleteLocation,
  downloadLocationsTemplate,
  getLocations,
  importLocationsCsv,
  previewLocationsCsv,
  type ApiLocation,
  type LocationImportJob,
  type LocationImportPreview
} from '../lib/admin-api'
import { useSessionStore } from '../stores/session'

const session = useSessionStore()

const locations = ref<ApiLocation[]>([])
const search = ref('')
const errorMessage = ref('')
const isLoading = ref(false)
const isImportDialogOpen = ref(false)
const isImporting = ref(false)
const isPreviewing = ref(false)
const importFile = ref<File | null>(null)
const lastImportJob = ref<LocationImportJob | null>(null)
const importPreview = ref<LocationImportPreview | null>(null)

const filteredLocations = computed(() => {
  const normalized = search.value.trim().toLowerCase()
  if (!normalized) {
    return locations.value
  }

  return locations.value.filter((location) => {
    return (
      location.name.toLowerCase().includes(normalized) ||
      location.city.toLowerCase().includes(normalized)
    )
  })
})

function businessTypeTitle(value: ApiLocation['business_type']) {
  return businessTypeOptions.find((option) => option.value === value)?.title ?? value
}

function statusTitle(value: ApiLocation['status']) {
  return locationStatusOptions.find((option) => option.value === value)?.title ?? value
}

async function loadLocations() {
  if (!session.accessToken.value) {
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    locations.value = await getLocations(session.accessToken.value)
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No se pudieron cargar las localizaciones.'
  } finally {
    isLoading.value = false
  }
}

async function remove(locationId: string) {
  if (!session.accessToken.value) {
    return
  }

  try {
    await deleteLocation(session.accessToken.value, locationId)
    await loadLocations()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No se pudo eliminar la localización.'
  }
}

async function submitImport() {
  if (!session.accessToken.value || !importFile.value) {
    return
  }

  isImporting.value = true
  errorMessage.value = ''

  try {
    lastImportJob.value = await importLocationsCsv(session.accessToken.value, importFile.value)
    closeImportDialog()
    await loadLocations()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No se pudo importar el CSV.'
  } finally {
    isImporting.value = false
  }
}

async function previewImport() {
  if (!session.accessToken.value || !importFile.value) {
    return
  }

  isPreviewing.value = true
  errorMessage.value = ''

  try {
    importPreview.value = await previewLocationsCsv(session.accessToken.value, importFile.value)
  } catch (error) {
    importPreview.value = null
    errorMessage.value =
      error instanceof Error ? error.message : 'No se pudo generar el preview del CSV.'
  } finally {
    isPreviewing.value = false
  }
}

async function downloadTemplate() {
  if (!session.accessToken.value) {
    return
  }

  try {
    const blob = await downloadLocationsTemplate(session.accessToken.value)
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'locations-template.csv'
    link.click()
    URL.revokeObjectURL(url)
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'No se pudo descargar la plantilla CSV.'
  }
}

function closeImportDialog() {
  isImportDialogOpen.value = false
  importFile.value = null
  importPreview.value = null
}

onMounted(loadLocations)
</script>

<template>
  <div class="page-shell">
    <header class="page-header">
      <div>
        <p class="eyebrow">Gestión de localizaciones</p>
        <h1>{{ isEditing ? 'Editar localización' : 'Nueva localización' }}</h1>
        <p class="copy">
          Completa la información comercial y define la posición exacta usando búsqueda y mapa.
        </p>
      </div>
      <div class="header-actions">
        <v-btn variant="text" to="/locations">Volver al listado</v-btn>
      </div>
    </header>

    <v-alert v-if="errorMessage" type="error" variant="tonal" class="mb-4">
      {{ errorMessage }}
    </v-alert>

    <div class="editor-grid">
      <v-card elevation="0" class="panel-card">
        <v-card-text class="stacked-form">
          <v-text-field v-model="form.name" label="Nombre" variant="outlined" data-testid="location-name" />
          <v-text-field v-model="form.slug" label="Slug" variant="outlined" data-testid="location-slug" />
          <v-select
            v-model="form.business_type"
            :items="businessTypeOptions"
            item-title="title"
            item-value="value"
            label="Tipo de localización"
            variant="outlined"
          />
          <v-select
            v-model="form.status"
            :items="locationStatusOptions"
            item-title="title"
            item-value="value"
            label="Estado"
            variant="outlined"
          />
          <v-text-field
            v-model="form.address_line_1"
            label="Dirección principal"
            variant="outlined"
            data-testid="location-address"
          />
          <v-text-field v-model="form.address_line_2" label="Complemento" variant="outlined" />
          <v-text-field v-model="form.city" label="Ciudad" variant="outlined" data-testid="location-city" />
          <v-text-field v-model="form.region" label="Región" variant="outlined" />
          <v-text-field v-model="form.country" label="País" variant="outlined" data-testid="location-country" />
          <v-text-field v-model="form.postal_code" label="Código postal" variant="outlined" />
          <v-textarea
            v-model="form.description_short"
            label="Descripción corta"
            variant="outlined"
            rows="2"
          />
          <v-textarea
            v-model="form.description_long"
            label="Descripción extendida"
            variant="outlined"
            rows="4"
          />
          <v-text-field v-model="form.phone" label="Teléfono" variant="outlined" />
          <v-text-field v-model="form.email" label="Correo" variant="outlined" />
          <v-text-field v-model="form.website" label="Sitio web" variant="outlined" />
          <v-text-field v-model="servicesInput" label="Servicios (separados por coma)" variant="outlined" />
          <v-text-field v-model="externalIdInput" label="Identificador externo" variant="outlined" />
          <v-switch v-model="form.featured" color="primary" label="Destacar en el frontend" />
        </v-card-text>
      </v-card>

      <div class="editor-side">
        <v-card elevation="0" class="panel-card">
          <v-card-text class="stacked-form">
            <div>
              <p class="eyebrow">Búsqueda geográfica</p>
              <h2>Busca una dirección</h2>
            </div>
            <div class="search-inline">
              <v-text-field
                v-model="searchQuery"
                label="Buscar dirección o referencia"
                variant="outlined"
                hide-details
              />
              <v-btn color="primary" :loading="isSearching" @click="searchPlaces">Buscar</v-btn>
            </div>
            <v-list v-if="searchResults.length" class="search-results">
              <v-list-item
                v-for="result in searchResults"
                :key="`${result.latitude}-${result.longitude}-${result.name}`"
                :title="result.name"
                :subtitle="result.address"
                @click="selectResult(result)"
              />
            </v-list>
          </v-card-text>
        </v-card>

        <AdminMapPicker v-model="coordinates" />

        <div class="form-actions">
          <v-btn variant="outlined" to="/locations">Cancelar</v-btn>
          <v-btn color="primary" data-testid="save-location-button" :loading="isSaving" @click="submit">
            {{ isEditing ? 'Guardar cambios' : 'Crear localización' }}
          </v-btn>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import AdminMapPicker from '../components/AdminMapPicker.vue'
import { businessTypeOptions, locationStatusOptions } from '../constants/business'
import {
  createLocation,
  getLocation,
  searchGeocoding,
  updateLocation,
  type GeocodingResult,
  type LocationFormPayload
} from '../lib/admin-api'
import { useSessionStore } from '../stores/session'

const route = useRoute()
const router = useRouter()
const session = useSessionStore()

const locationId = computed(() =>
  typeof route.params.locationId === 'string' ? route.params.locationId : null
)
const isEditing = computed(() => Boolean(locationId.value))

const errorMessage = ref('')
const isSaving = ref(false)
const isLoading = ref(false)
const isSearching = ref(false)
const searchQuery = ref('')
const searchResults = ref<GeocodingResult[]>([])
const servicesInput = ref('')
const externalIdInput = ref('')

const form = ref<LocationFormPayload>({
  slug: '',
  name: '',
  business_type: 'virtual-store',
  status: 'active',
  description_short: '',
  description_long: '',
  address_line_1: '',
  address_line_2: '',
  city: '',
  region: '',
  country: 'Panama',
  postal_code: '',
  latitude: 8.9824,
  longitude: -79.5199,
  phone: '',
  email: '',
  website: '',
  opening_hours: {},
  services: [],
  featured: false,
  external_id: ''
})

const coordinates = computed({
  get: () => ({
    latitude: form.value.latitude,
    longitude: form.value.longitude
  }),
  set: (value: { latitude: number; longitude: number }) => {
    form.value.latitude = value.latitude
    form.value.longitude = value.longitude
  }
})

async function loadLocation() {
  if (!session.accessToken.value || !locationId.value) {
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    const location = await getLocation(session.accessToken.value, locationId.value)
    form.value = {
      slug: location.slug,
      name: location.name,
      business_type: location.business_type,
      status: location.status,
      description_short: location.description_short ?? '',
      description_long: location.description_long ?? '',
      address_line_1: location.address_line_1,
      address_line_2: location.address_line_2 ?? '',
      city: location.city,
      region: location.region ?? '',
      country: location.country,
      postal_code: location.postal_code ?? '',
      latitude: location.latitude,
      longitude: location.longitude,
      phone: location.phone ?? '',
      email: location.email ?? '',
      website: location.website ?? '',
      opening_hours: location.opening_hours,
      services: location.services,
      featured: location.featured,
      external_id: location.external_id ?? ''
    }
    servicesInput.value = location.services.join(', ')
    externalIdInput.value = location.external_id ?? ''
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No se pudo cargar la localización.'
  } finally {
    isLoading.value = false
  }
}

async function searchPlaces() {
  if (!session.accessToken.value || searchQuery.value.trim().length < 3) {
    return
  }

  isSearching.value = true
  errorMessage.value = ''

  try {
    searchResults.value = await searchGeocoding(session.accessToken.value, searchQuery.value)
  } catch (error) {
    searchResults.value = []
    errorMessage.value =
      error instanceof Error ? error.message : 'No se pudo consultar direcciones.'
  } finally {
    isSearching.value = false
  }
}

function selectResult(result: GeocodingResult) {
  form.value.address_line_1 = result.address
  coordinates.value = {
    latitude: result.latitude,
    longitude: result.longitude
  }
  searchResults.value = []
}

async function submit() {
  if (!session.accessToken.value) {
    return
  }

  isSaving.value = true
  errorMessage.value = ''

  const payload: LocationFormPayload = {
    ...form.value,
    services: servicesInput.value
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean),
    external_id: externalIdInput.value.trim() || null
  }

  try {
    if (locationId.value) {
      await updateLocation(session.accessToken.value, locationId.value, payload)
    } else {
      await createLocation(session.accessToken.value, payload)
    }

    await router.push('/locations')
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No se pudo guardar la localización.'
  } finally {
    isSaving.value = false
  }
}

watch(
  () => form.value.name,
  (name) => {
    if (!isEditing.value && name && !form.value.slug) {
      form.value.slug = name
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/(^-|-$)/g, '')
    }
  }
)

onMounted(loadLocation)
</script>

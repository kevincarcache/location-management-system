<template>
  <div class="page-shell">
    <header class="page-header">
      <div>
        <p class="eyebrow">Storefront</p>
        <h1>Configuración de la tienda</h1>
        <p class="copy">
          Define el branding, los textos comerciales y el tipo de localización que verá el frontend.
        </p>
      </div>
    </header>

    <v-alert v-if="errorMessage" type="error" variant="tonal" class="mb-4">
      {{ errorMessage }}
    </v-alert>

    <div class="store-settings-grid">
      <v-card elevation="0" class="panel-card">
        <v-card-text class="stacked-form">
          <v-text-field v-model="form.slug" label="Slug del storefront" variant="outlined" />
          <v-text-field v-model="form.brand_name" label="Nombre comercial" variant="outlined" />
          <v-textarea
            v-model="form.business_description"
            label="Descripción del negocio"
            variant="outlined"
            rows="3"
          />
          <v-text-field v-model="form.hero_title" label="Título principal" variant="outlined" />
          <v-textarea
            v-model="form.hero_subtitle"
            label="Subtítulo principal"
            variant="outlined"
            rows="3"
          />
          <v-select
            v-model="form.business_type"
            :items="businessTypeOptions"
            item-title="title"
            item-value="value"
            label="Tipo visible en storefront"
            variant="outlined"
          />
          <v-select
            v-model="form.theme_preset"
            :items="themeOptions"
            label="Tema visual"
            variant="outlined"
          />
          <v-text-field v-model="form.menu_label" label="Etiqueta del menú" variant="outlined" />
          <v-text-field v-model="form.logo_url" label="URL del logo" variant="outlined" />
          <v-textarea v-model="form.footer_text" label="Texto del footer" variant="outlined" rows="2" />
        </v-card-text>
      </v-card>

      <v-card elevation="0" class="panel-card">
        <v-card-text class="store-preview">
          <div>
            <p class="eyebrow">Preview de marca</p>
            <h2>{{ form.brand_name || 'Nombre comercial' }}</h2>
            <p class="copy">{{ form.business_description || 'Describe aquí el negocio.' }}</p>
          </div>

          <div class="preview-banner" :data-theme="form.theme_preset">
            <strong>{{ form.hero_title || 'Título principal del storefront' }}</strong>
            <span>{{ form.hero_subtitle || 'Mensaje principal para contextualizar el mapa y el listado.' }}</span>
          </div>

          <div class="preview-chip-row">
            <v-chip color="primary" variant="flat">{{ menuLabel }}</v-chip>
            <v-chip variant="outlined">{{ businessTypeLabel }}</v-chip>
          </div>

          <div class="form-actions">
            <v-btn color="primary" :loading="isSaving" @click="submit">
              Guardar configuración
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import { businessTypeOptions } from '../constants/business'
import {
  createStoreConfig,
  getStoreConfigs,
  updateStoreConfig,
  type StoreConfig,
  type StoreConfigPayload
} from '../lib/admin-api'
import { useSessionStore } from '../stores/session'

const session = useSessionStore()

const errorMessage = ref('')
const isSaving = ref(false)
const currentId = ref<string | null>(null)
const form = ref<StoreConfigPayload>({
  slug: 'default',
  brand_name: 'Demo Business',
  business_description: 'Describe el propósito principal del negocio y su alcance geográfico.',
  theme_preset: 'serious-teal',
  business_type: 'virtual-store',
  logo_url: '',
  hero_title: 'Encuentra nuestra red de atención',
  hero_subtitle: 'Ubica rápidamente la sucursal, evento o punto de servicio más conveniente.',
  menu_label: 'Ubicaciones',
  footer_text: 'Encuentra nuestras ubicaciones activas y planifica tu visita.'
})

const themeOptions = ['serious-teal', 'graphite-sand', 'coastal-slate']
const businessTypeLabel = computed(
  () => businessTypeOptions.find((item) => item.value === form.value.business_type)?.title ?? 'Sin definir'
)
const menuLabel = computed(() => form.value.menu_label || 'Ubicaciones')

async function loadStoreConfig() {
  if (!session.accessToken.value) {
    return
  }

  errorMessage.value = ''

  try {
    const configs = await getStoreConfigs(session.accessToken.value)
    const config = configs[0]
    if (!config) {
      return
    }

    currentId.value = config.id
    form.value = {
      slug: config.slug,
      brand_name: config.brand_name,
      business_description: config.business_description,
      theme_preset: config.theme_preset,
      business_type: config.business_type,
      logo_url: config.logo_url ?? '',
      hero_title: config.hero_title,
      hero_subtitle: config.hero_subtitle,
      menu_label: config.menu_label,
      footer_text: config.footer_text
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No se pudo cargar la configuración.'
  }
}

async function submit() {
  if (!session.accessToken.value) {
    return
  }

  isSaving.value = true
  errorMessage.value = ''

  try {
    let saved: StoreConfig
    if (currentId.value) {
      saved = await updateStoreConfig(session.accessToken.value, currentId.value, form.value)
    } else {
      saved = await createStoreConfig(session.accessToken.value, form.value)
    }
    currentId.value = saved.id
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No se pudo guardar la configuración.'
  } finally {
    isSaving.value = false
  }
}

onMounted(loadStoreConfig)
</script>

<template>
  <v-layout class="admin-shell">
    <v-navigation-drawer
      v-model="drawerOpen"
      :permanent="mdAndUp"
      :temporary="!mdAndUp"
      width="272"
      color="surface"
      class="admin-drawer"
    >
      <div class="admin-brand">
        <p class="eyebrow">Platform</p>
        <strong>Location Management System</strong>
        <span>Panel central para operar tiendas, eventos y puntos de servicio.</span>
      </div>

      <v-list nav class="admin-nav">
        <v-list-item title="Dashboard" to="/" exact />
        <v-list-item title="Lista de localizaciones" to="/locations" />
        <v-list-item title="Gestionar tipos" to="/location-types" />
        <v-list-item title="Reportes" to="/reports" />
        <v-list-item title="Configuración de la tienda" to="/store-settings" />
      </v-list>
    </v-navigation-drawer>

    <v-app-bar flat color="surface" class="admin-topbar">
      <v-btn
        v-if="!mdAndUp"
        icon="mdi-menu"
        variant="text"
        class="mr-3"
        @click="drawerOpen = !drawerOpen"
      />
      <div>
        <p class="eyebrow">Administración</p>
        <strong>{{ currentSection }}</strong>
      </div>
      <v-spacer />
      <v-btn variant="text" to="/store-settings">Configuración</v-btn>
      <v-btn variant="outlined" @click="handleLogout">Cerrar sesión</v-btn>
    </v-app-bar>

    <v-main class="admin-main">
      <div class="admin-main-inner">
        <div class="admin-content">
          <div class="content-frame">
            <router-view />
          </div>
        </div>

        <v-footer class="admin-footer">
          <span>{{ currentYear }} Location Management System</span>
          <span>Operación centralizada del catálogo de localizaciones.</span>
        </v-footer>
      </div>
    </v-main>
  </v-layout>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDisplay } from 'vuetify'

import { useSessionStore } from '../stores/session'

const route = useRoute()
const router = useRouter()
const session = useSessionStore()
const { mdAndUp } = useDisplay()
const drawerOpen = ref(true)

const sectionTitles: Record<string, string> = {
  '/': 'Dashboard',
  '/locations': 'Gestión de localizaciones',
  '/location-types': 'Tipos de localización',
  '/reports': 'Reportes',
  '/store-settings': 'Configuración de la tienda'
}

const currentSection = computed(() => {
  if (route.path.startsWith('/locations/')) {
    return 'Edición de localizaciones'
  }
  return sectionTitles[route.path] ?? 'Panel de administración'
})

const currentYear = new Date().getFullYear()

watch(
  mdAndUp,
  (isDesktop) => {
    drawerOpen.value = isDesktop
  },
  { immediate: true }
)

function handleLogout() {
  session.logout()
  router.push('/login')
}
</script>

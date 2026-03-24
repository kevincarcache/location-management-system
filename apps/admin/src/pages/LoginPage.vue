<template>
  <div class="auth-shell">
    <v-card class="auth-card" elevation="0">
      <p class="eyebrow">Panel de administración</p>
      <h1>Ingresa al centro de operación</h1>
      <p class="copy">
        Accede al panel desde donde se administra el storefront, las localizaciones y las importaciones.
      </p>

      <v-alert v-if="errorMessage" type="error" variant="tonal" class="mb-4">
        {{ errorMessage }}
      </v-alert>

      <v-form class="auth-form" @submit.prevent="submit">
        <v-text-field v-model="email" label="Email" variant="outlined" />
        <v-text-field v-model="password" type="password" label="Password" variant="outlined" />
        <v-btn color="primary" size="large" block type="submit" :loading="isSubmitting">
          Entrar
        </v-btn>
      </v-form>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useSessionStore } from '../stores/session'

const route = useRoute()
const router = useRouter()
const session = useSessionStore()

const email = ref('admin@example.com')
const password = ref('ChangeMe123!')
const errorMessage = ref('')
const isSubmitting = ref(false)

async function submit() {
  errorMessage.value = ''
  isSubmitting.value = true

  try {
    await session.login({
      email: email.value,
      password: password.value
    })

    const redirect =
      typeof route.query.redirect === 'string' && route.query.redirect ? route.query.redirect : '/'
    await router.push(redirect)
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No se pudo iniciar sesión.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <v-alert
    v-if="mode === 'loading'"
    rounded="md"
    border="start"
    type="info"
    variant="tonal"
    class="mb-6"
  >
    <div class="text-subtitle-1 font-weight-bold mb-1">Cargando la experiencia de la tienda</div>
    <div class="text-body-2">Estamos preparando el catálogo visible para este storeview.</div>
  </v-alert>

  <v-alert
    v-else-if="mode === 'error'"
    rounded="md"
    border="start"
    type="error"
    variant="tonal"
    class="mb-6"
  >
    <div class="text-subtitle-1 font-weight-bold mb-2">No pudimos cargar esta tienda</div>
    <div class="text-body-2 mb-4">
      Verifica la configuración del storeview y la disponibilidad de la API.
    </div>
    <v-btn color="primary" @click="emit('retry')">Reintentar</v-btn>
  </v-alert>
</template>

<script setup lang="ts">
defineProps<{
  mode: 'loading' | 'error'
}>()

const emit = defineEmits<{
  retry: []
}>()
</script>

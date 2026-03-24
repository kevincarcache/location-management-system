import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  compatibilityDate: '2026-03-24',
  css: ['maplibre-gl/dist/maplibre-gl.css', '~/assets/css/main.css'],
  app: {
    head: {
      title: 'Location Management System',
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content: 'Store locator experience for branches, events, recycling points, academies, and technical services.'
        }
      ]
    }
  },
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000'
    }
  }
})

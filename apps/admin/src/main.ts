import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

import App from './App.vue'
import { configureAuthSessionHandlers } from './lib/admin-api'
import { router } from './router'
import { useSessionStore } from './stores/session'
import './styles/main.css'
import 'maplibre-gl/dist/maplibre-gl.css'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi
    }
  },
  theme: {
    defaultTheme: 'lms',
    themes: {
      lms: {
        dark: false,
        colors: {
          background: '#f3f4f6',
          surface: '#ffffff',
          primary: '#1f4b6e',
          secondary: '#a35b31',
          accent: '#0f172a',
          info: '#3a7ca5',
          success: '#4f7d4f',
          warning: '#c7912c',
          error: '#b54747'
        }
      }
    }
  }
})

const session = useSessionStore()

configureAuthSessionHandlers({
  async refreshAccessToken() {
    const tokens = await session.refreshSession()
    return tokens?.access_token ?? null
  },
  async onSessionExpired() {
    session.logout()
    await router.push({
      path: '/login',
      query: {
        redirect: router.currentRoute.value.fullPath
      }
    })
  }
})

createApp(App).use(router).use(vuetify).mount('#app')

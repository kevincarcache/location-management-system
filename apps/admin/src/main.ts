import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

import App from './App.vue'
import { router } from './router'
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

createApp(App).use(router).use(vuetify).mount('#app')

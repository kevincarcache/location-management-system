import { createApp } from 'vue'
import { createVuetify } from 'vuetify'

import App from './App.vue'
import { router } from './router'
import './styles/main.css'
import 'vuetify/styles'

const vuetify = createVuetify({
  theme: {
    defaultTheme: 'lms',
    themes: {
      lms: {
        dark: false,
        colors: {
          background: '#f4efe5',
          surface: '#fffdf7',
          primary: '#0f766e',
          secondary: '#c26d38',
          accent: '#194759',
          info: '#3a7ca5',
          success: '#3f8f5f',
          warning: '#d7a94b',
          error: '#b74d4d'
        }
      }
    }
  }
})

createApp(App).use(router).use(vuetify).mount('#app')


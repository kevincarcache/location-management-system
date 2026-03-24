import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

export default defineNuxtPlugin((nuxtApp) => {
  const vuetify = createVuetify({
    components,
    directives,
    icons: {
      defaultSet: 'mdi',
      aliases,
      sets: {
        mdi
      }
    },
    theme: {
      defaultTheme: 'storefront',
      themes: {
        storefront: {
          dark: false,
          colors: {
            background: '#f4efe6',
            surface: '#fcfaf5',
            primary: '#1d5c63',
            secondary: '#b26a3d',
            accent: '#233847',
            info: '#476c89',
            success: '#4d6d4f',
            warning: '#b88628',
            error: '#ab4c4c'
          }
        }
      }
    },
    defaults: {
      VAppBar: {
        elevation: 0
      },
      VCard: {
        rounded: 'md',
        elevation: 0
      },
      VSheet: {
        rounded: 'md'
      },
      VTextField: {
        variant: 'outlined',
        density: 'comfortable',
        hideDetails: true
      },
      VBtn: {
        rounded: 'md'
      },
      VChip: {
        rounded: 'md'
      },
      VNavigationDrawer: {
        elevation: 0
      },
      VListItem: {
        rounded: 'md'
      }
    }
  })

  nuxtApp.vueApp.use(vuetify)
})

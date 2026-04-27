import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

const branchTeal = {
  dark: false,
  colors: {
    background: '#f4efe6',
    surface: '#fffaf2',
    primary: '#1d5c63',
    secondary: '#b26a3d',
    accent: '#233847',
    info: '#476c89',
    success: '#4d6d4f',
    warning: '#b88628',
    error: '#ab4c4c'
  }
}

const serviceSlate = {
  dark: false,
  colors: {
    background: '#eef3f7',
    surface: '#ffffff',
    primary: '#25516b',
    secondary: '#0f766e',
    accent: '#17212b',
    info: '#3b6f8f',
    success: '#40715f',
    warning: '#b88728',
    error: '#a84949'
  }
}

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
      defaultTheme: 'branch-teal',
      themes: {
        storefront: branchTeal,
        'branch-teal': branchTeal,
        'event-indigo': {
          dark: false,
          colors: {
            background: '#f3f0ff',
            surface: '#ffffff',
            primary: '#4f46e5',
            secondary: '#db2777',
            accent: '#1e1b4b',
            info: '#6366f1',
            success: '#2f855a',
            warning: '#c98216',
            error: '#b4235a'
          }
        },
        'recycling-green': {
          dark: false,
          colors: {
            background: '#eef7ef',
            surface: '#fbfffb',
            primary: '#2f6f4e',
            secondary: '#8a9a2f',
            accent: '#143828',
            info: '#3f7f72',
            success: '#2f6f4e',
            warning: '#9a7a20',
            error: '#a34747'
          }
        },
        'academy-amber': {
          dark: false,
          colors: {
            background: '#fff7e6',
            surface: '#fffdf7',
            primary: '#8a4f12',
            secondary: '#d97706',
            accent: '#2f2417',
            info: '#6a6f8f',
            success: '#557a3d',
            warning: '#d97706',
            error: '#a54735'
          }
        },
        'service-slate': serviceSlate,
        'serious-teal': branchTeal,
        'graphite-sand': serviceSlate,
        'coastal-slate': serviceSlate
      }
    },
    defaults: {
      VAppBar: {
        elevation: 0
      },
      VCard: {
        rounded: 'lg',
        elevation: 0
      },
      VSheet: {
        rounded: 'lg'
      },
      VTextField: {
        variant: 'outlined',
        density: 'comfortable',
        hideDetails: true,
        rounded: 'lg'
      },
      VBtn: {
        rounded: 'lg'
      },
      VChip: {
        rounded: 'lg'
      },
      VNavigationDrawer: {
        elevation: 0
      },
      VListItem: {
        rounded: 'lg'
      }
    }
  })

  nuxtApp.vueApp.use(vuetify)
})

import type { Router } from 'vue-router'

import { useSessionStore } from '../stores/session'

export function registerRouterGuards(router: Router) {
  router.beforeEach(async (to) => {
    const session = useSessionStore()

    if (session.isAuthenticated.value && to.path === '/login') {
      return '/'
    }

    if (to.meta.public) {
      return true
    }

    if (session.isAuthenticated.value) {
      return true
    }

    const refreshed = await session.refreshSession()
    if (refreshed) {
      return true
    }

    return { path: '/login', query: { redirect: to.fullPath } }
  })
}

import { computed, ref } from 'vue'

import {
  login as loginRequest,
  refresh as refreshRequest,
  type LoginPayload,
  type TokenPair
} from '../lib/admin-api'

const ACCESS_TOKEN_KEY = 'lms.admin.accessToken'
const REFRESH_TOKEN_KEY = 'lms.admin.refreshToken'

const accessToken = ref<string | null>(null)
const refreshToken = ref<string | null>(null)
let hydrated = false

function ensureHydrated() {
  if (hydrated || typeof window === 'undefined') {
    hydrated = true
    return
  }

  accessToken.value = localStorage.getItem(ACCESS_TOKEN_KEY)
  refreshToken.value = localStorage.getItem(REFRESH_TOKEN_KEY)
  hydrated = true
}

function persistTokens(tokens: TokenPair) {
  ensureHydrated()
  accessToken.value = tokens.access_token
  refreshToken.value = tokens.refresh_token
  localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access_token)
  localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token)
}

function clearTokens() {
  ensureHydrated()
  accessToken.value = null
  refreshToken.value = null
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
}

export function useSessionStore() {
  ensureHydrated()
  const isAuthenticated = computed(() => Boolean(accessToken.value))

  async function login(payload: LoginPayload) {
    const tokens = await loginRequest(payload)
    persistTokens(tokens)
    return tokens
  }

  async function refreshSession() {
    if (!refreshToken.value) {
      clearTokens()
      return null
    }

    try {
      const tokens = await refreshRequest(refreshToken.value)
      persistTokens(tokens)
      return tokens
    } catch {
      clearTokens()
      return null
    }
  }

  function logout() {
    clearTokens()
  }

  return {
    accessToken,
    refreshToken,
    isAuthenticated,
    login,
    logout,
    refreshSession
  }
}

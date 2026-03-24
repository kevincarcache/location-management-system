import { computed, ref } from 'vue'

import {
  login as loginRequest,
  refresh as refreshRequest,
  type LoginPayload,
  type TokenPair
} from '../lib/admin-api'

const ACCESS_TOKEN_KEY = 'lms.admin.accessToken'
const REFRESH_TOKEN_KEY = 'lms.admin.refreshToken'

const accessToken = ref<string | null>(localStorage.getItem(ACCESS_TOKEN_KEY))
const refreshToken = ref<string | null>(localStorage.getItem(REFRESH_TOKEN_KEY))

function persistTokens(tokens: TokenPair) {
  accessToken.value = tokens.access_token
  refreshToken.value = tokens.refresh_token
  localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access_token)
  localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token)
}

function clearTokens() {
  accessToken.value = null
  refreshToken.value = null
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
}

export function useSessionStore() {
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

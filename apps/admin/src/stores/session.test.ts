import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const { loginMock, refreshMock } = vi.hoisted(() => ({
  loginMock: vi.fn(),
  refreshMock: vi.fn(),
}))

vi.mock('../lib/admin-api', () => ({
  login: loginMock,
  refresh: refreshMock,
}))

function createStorage() {
  const store = new Map<string, string>()

  return {
    clear: () => store.clear(),
    getItem: (key: string) => store.get(key) ?? null,
    key: (index: number) => Array.from(store.keys())[index] ?? null,
    removeItem: (key: string) => {
      store.delete(key)
    },
    setItem: (key: string, value: string) => {
      store.set(key, value)
    },
    get length() {
      return store.size
    },
  }
}

describe('useSessionStore', () => {
  beforeEach(() => {
    vi.resetModules()
    loginMock.mockReset()
    refreshMock.mockReset()
    vi.stubGlobal('localStorage', createStorage())
    vi.stubGlobal('window', {})
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('hydrates lazily from storage and persists login tokens', async () => {
    loginMock.mockResolvedValue({
      access_token: 'access-1',
      refresh_token: 'refresh-1',
      token_type: 'bearer',
    })

    const { useSessionStore } = await import('./session')
    const store = useSessionStore()

    expect(store.isAuthenticated.value).toBe(false)

    await store.login({
      email: 'admin@example.com',
      password: 'ChangeMe123!',
    })

    expect(store.accessToken.value).toBe('access-1')
    expect(store.refreshToken.value).toBe('refresh-1')
    expect(store.isAuthenticated.value).toBe(true)
    expect(localStorage.getItem('lms.admin.accessToken')).toBe('access-1')
  })

  it('clears session when refresh fails', async () => {
    localStorage.setItem('lms.admin.accessToken', 'stale-access')
    localStorage.setItem('lms.admin.refreshToken', 'stale-refresh')
    refreshMock.mockRejectedValue(new Error('expired'))

    const { useSessionStore } = await import('./session')
    const store = useSessionStore()

    const refreshed = await store.refreshSession()

    expect(refreshed).toBeNull()
    expect(store.accessToken.value).toBeNull()
    expect(store.refreshToken.value).toBeNull()
    expect(localStorage.getItem('lms.admin.accessToken')).toBeNull()
  })

  it('persists refreshed tokens', async () => {
    localStorage.setItem('lms.admin.accessToken', 'stale-access')
    localStorage.setItem('lms.admin.refreshToken', 'refresh-1')
    refreshMock.mockResolvedValue({
      access_token: 'access-2',
      refresh_token: 'refresh-2',
      token_type: 'bearer',
    })

    const { useSessionStore } = await import('./session')
    const store = useSessionStore()

    const refreshed = await store.refreshSession()

    expect(refreshed?.access_token).toBe('access-2')
    expect(store.accessToken.value).toBe('access-2')
    expect(store.refreshToken.value).toBe('refresh-2')
    expect(localStorage.getItem('lms.admin.accessToken')).toBe('access-2')
    expect(localStorage.getItem('lms.admin.refreshToken')).toBe('refresh-2')
  })

  it('deduplicates concurrent refresh attempts', async () => {
    localStorage.setItem('lms.admin.accessToken', 'stale-access')
    localStorage.setItem('lms.admin.refreshToken', 'refresh-1')
    refreshMock.mockResolvedValue({
      access_token: 'access-2',
      refresh_token: 'refresh-2',
      token_type: 'bearer',
    })

    const { useSessionStore } = await import('./session')
    const store = useSessionStore()

    const [first, second] = await Promise.all([store.refreshSession(), store.refreshSession()])

    expect(first?.access_token).toBe('access-2')
    expect(second?.access_token).toBe('access-2')
    expect(refreshMock).toHaveBeenCalledTimes(1)
    expect(localStorage.getItem('lms.admin.accessToken')).toBe('access-2')
  })
})

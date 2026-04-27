import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

function textResponse(body: string, status: number) {
  return new Response(body, { status })
}

describe('admin-api auth retry', () => {
  const fetchMock = vi.fn()

  beforeEach(() => {
    vi.resetModules()
    fetchMock.mockReset()
    vi.stubGlobal('fetch', fetchMock)
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('does not refresh a successful authenticated request', async () => {
    fetchMock.mockResolvedValueOnce(jsonResponse([]))

    const refreshAccessToken = vi.fn()
    const onSessionExpired = vi.fn()
    const { configureAuthSessionHandlers, getStoreConfigs } = await import('./admin-api')

    configureAuthSessionHandlers({ refreshAccessToken, onSessionExpired })

    await expect(getStoreConfigs('access-1')).resolves.toEqual([])

    expect(refreshAccessToken).not.toHaveBeenCalled()
    expect(onSessionExpired).not.toHaveBeenCalled()
    expect(fetchMock).toHaveBeenCalledTimes(1)
  })

  it('refreshes and retries an authenticated request after a 401', async () => {
    fetchMock.mockResolvedValueOnce(textResponse('expired', 401))
    fetchMock.mockResolvedValueOnce(jsonResponse([]))

    const refreshAccessToken = vi.fn().mockResolvedValue('access-2')
    const onSessionExpired = vi.fn()
    const { configureAuthSessionHandlers, getStoreConfigs } = await import('./admin-api')

    configureAuthSessionHandlers({ refreshAccessToken, onSessionExpired })

    await expect(getStoreConfigs('access-1')).resolves.toEqual([])

    expect(refreshAccessToken).toHaveBeenCalledTimes(1)
    expect(onSessionExpired).not.toHaveBeenCalled()
    expect(fetchMock).toHaveBeenCalledTimes(2)
    expect(fetchMock.mock.calls[0][1].headers.Authorization).toBe('Bearer access-1')
    expect(fetchMock.mock.calls[1][1].headers.Authorization).toBe('Bearer access-2')
  })

  it('calls the session-expired handler when refresh cannot recover a 401', async () => {
    fetchMock.mockResolvedValueOnce(textResponse('expired', 401))

    const refreshAccessToken = vi.fn().mockResolvedValue(null)
    const onSessionExpired = vi.fn()
    const { configureAuthSessionHandlers, getStoreConfigs } = await import('./admin-api')

    configureAuthSessionHandlers({ refreshAccessToken, onSessionExpired })

    await expect(getStoreConfigs('access-1')).rejects.toThrow('expired')

    expect(refreshAccessToken).toHaveBeenCalledTimes(1)
    expect(onSessionExpired).toHaveBeenCalledTimes(1)
    expect(fetchMock).toHaveBeenCalledTimes(1)
  })

  it('does not retry infinitely when the retried request also fails', async () => {
    fetchMock.mockResolvedValueOnce(textResponse('expired', 401))
    fetchMock.mockResolvedValueOnce(textResponse('still expired', 401))

    const refreshAccessToken = vi.fn().mockResolvedValue('access-2')
    const onSessionExpired = vi.fn()
    const { configureAuthSessionHandlers, getStoreConfigs } = await import('./admin-api')

    configureAuthSessionHandlers({ refreshAccessToken, onSessionExpired })

    await expect(getStoreConfigs('access-1')).rejects.toThrow('still expired')

    expect(refreshAccessToken).toHaveBeenCalledTimes(1)
    expect(onSessionExpired).not.toHaveBeenCalled()
    expect(fetchMock).toHaveBeenCalledTimes(2)
  })

  it('uses auth retry for CSV uploads', async () => {
    fetchMock.mockResolvedValueOnce(textResponse('expired', 401))
    fetchMock.mockResolvedValueOnce(jsonResponse({ id: 'job-1' }))

    const refreshAccessToken = vi.fn().mockResolvedValue('access-2')
    const onSessionExpired = vi.fn()
    const { configureAuthSessionHandlers, importLocationsCsv } = await import('./admin-api')

    configureAuthSessionHandlers({ refreshAccessToken, onSessionExpired })

    await expect(importLocationsCsv('access-1', new File(['a,b'], 'locations.csv'))).resolves.toEqual({
      id: 'job-1'
    })

    expect(refreshAccessToken).toHaveBeenCalledTimes(1)
    expect(fetchMock.mock.calls[1][1].headers.Authorization).toBe('Bearer access-2')
  })

  it('uses auth retry for template downloads', async () => {
    fetchMock.mockResolvedValueOnce(textResponse('expired', 401))
    fetchMock.mockResolvedValueOnce(new Response(new Blob(['template'])))

    const refreshAccessToken = vi.fn().mockResolvedValue('access-2')
    const onSessionExpired = vi.fn()
    const { configureAuthSessionHandlers, downloadLocationsTemplate } = await import('./admin-api')

    configureAuthSessionHandlers({ refreshAccessToken, onSessionExpired })

    const blob = await downloadLocationsTemplate('access-1')

    expect(await blob.text()).toBe('template')
    expect(refreshAccessToken).toHaveBeenCalledTimes(1)
    expect(fetchMock.mock.calls[1][1].headers.Authorization).toBe('Bearer access-2')
  })
})

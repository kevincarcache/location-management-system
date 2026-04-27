import type {
  ApiLocation,
  BusinessType as ApiBusinessType,
  GeocodingResult,
  LocationFormPayload,
  LocationImportJob,
  LocationImportPreview,
  LocationStatus as ApiLocationStatus,
  LoginPayload,
  StoreConfig,
  StoreConfigPayload,
  TokenPair
} from '@lms/types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

interface AuthSessionHandlers {
  refreshAccessToken: () => Promise<string | null>
  onSessionExpired: () => void | Promise<void>
}

let authSessionHandlers: AuthSessionHandlers | null = null
let sessionExpirationInFlight: Promise<void> | null = null

export type {
  ApiLocation,
  ApiBusinessType,
  ApiLocationStatus,
  GeocodingResult,
  LocationFormPayload,
  LocationImportJob,
  LocationImportPreview,
  LoginPayload,
  StoreConfig,
  StoreConfigPayload,
  TokenPair
}

export function configureAuthSessionHandlers(handlers: AuthSessionHandlers) {
  authSessionHandlers = handlers
}

function getErrorMessage(response: Response, fallback: string): Promise<string> {
  return response.text().then((detail) => detail || fallback)
}

async function handleUnauthorized(): Promise<string | null> {
  if (!authSessionHandlers) {
    return null
  }

  const refreshedToken = await authSessionHandlers.refreshAccessToken()
  if (refreshedToken) {
    return refreshedToken
  }

  if (!sessionExpirationInFlight) {
    sessionExpirationInFlight = Promise.resolve(authSessionHandlers.onSessionExpired()).finally(() => {
      sessionExpirationInFlight = null
    })
  }

  await sessionExpirationInFlight
  return null
}

async function withAuthRetry<T>(
  token: string | undefined,
  fetcher: (token?: string) => Promise<Response>,
  parser: (response: Response) => Promise<T>,
  errorMessage: (status: number) => string
): Promise<T> {
  const response = await fetcher(token)

  if (response.status === 401 && token) {
    const refreshedToken = await handleUnauthorized()
    if (refreshedToken) {
      const retryResponse = await fetcher(refreshedToken)
      if (retryResponse.ok) {
        return parser(retryResponse)
      }

      throw new Error(await getErrorMessage(retryResponse, errorMessage(retryResponse.status)))
    }
  }

  if (!response.ok) {
    throw new Error(await getErrorMessage(response, errorMessage(response.status)))
  }

  return parser(response)
}

async function request<T>(path: string, init: RequestInit = {}, token?: string): Promise<T> {
  return withAuthRetry(
    token,
    (currentToken) =>
      fetch(`${API_BASE_URL}${path}`, {
        ...init,
        headers: {
          'Content-Type': 'application/json',
          ...(currentToken ? { Authorization: `Bearer ${currentToken}` } : {}),
          ...(init.headers || {})
        }
      }),
    async (response) => {
      if (response.status === 204) {
        return undefined as T
      }

      return response.json() as Promise<T>
    },
    (status) => `Request failed with status ${status}`
  )
}

async function upload<T>(path: string, file: File, token: string): Promise<T> {
  return withAuthRetry(
    token,
    (currentToken) => {
      const formData = new FormData()
      formData.append('file', file)

      return fetch(`${API_BASE_URL}${path}`, {
        method: 'POST',
        headers: {
          ...(currentToken ? { Authorization: `Bearer ${currentToken}` } : {})
        },
        body: formData
      })
    },
    (response) => response.json() as Promise<T>,
    (status) => `Upload failed with status ${status}`
  )
}

async function download(path: string, token: string): Promise<Blob> {
  return withAuthRetry(
    token,
    (currentToken) =>
      fetch(`${API_BASE_URL}${path}`, {
        headers: {
          ...(currentToken ? { Authorization: `Bearer ${currentToken}` } : {})
        }
      }),
    (response) => response.blob(),
    (status) => `Template download failed with status ${status}`
  )
}

async function requestWithoutAuthRetry<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init.headers || {})
    }
  })

  if (!response.ok) {
    const detail = await response.text()
    throw new Error(detail || `Request failed with status ${response.status}`)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json() as Promise<T>
}

export function login(payload: LoginPayload): Promise<TokenPair> {
  return requestWithoutAuthRetry<TokenPair>('/api/admin/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function refresh(refreshToken: string): Promise<TokenPair> {
  return requestWithoutAuthRetry<TokenPair>('/api/admin/auth/refresh', {
    method: 'POST',
    body: JSON.stringify({ refresh_token: refreshToken })
  })
}

export function getLocations(token: string): Promise<ApiLocation[]> {
  return request<ApiLocation[]>('/api/admin/locations', {}, token)
}

export function getLocation(token: string, locationId: string): Promise<ApiLocation> {
  return request<ApiLocation>(`/api/admin/locations/${locationId}`, {}, token)
}

export function createLocation(token: string, payload: LocationFormPayload): Promise<ApiLocation> {
  return request<ApiLocation>(
    '/api/admin/locations',
    {
      method: 'POST',
      body: JSON.stringify(payload)
    },
    token
  )
}

export function updateLocation(
  token: string,
  locationId: string,
  payload: Partial<LocationFormPayload>
): Promise<ApiLocation> {
  return request<ApiLocation>(
    `/api/admin/locations/${locationId}`,
    {
      method: 'PATCH',
      body: JSON.stringify(payload)
    },
    token
  )
}

export function deleteLocation(token: string, locationId: string): Promise<void> {
  return request<void>(
    `/api/admin/locations/${locationId}`,
    {
      method: 'DELETE'
    },
    token
  )
}

export function importLocationsCsv(token: string, file: File): Promise<LocationImportJob> {
  return upload<LocationImportJob>('/api/admin/imports/locations/csv', file, token)
}

export function previewLocationsCsv(token: string, file: File): Promise<LocationImportPreview> {
  return upload<LocationImportPreview>('/api/admin/imports/locations/csv/preview', file, token)
}

export async function downloadLocationsTemplate(token: string): Promise<Blob> {
  return download('/api/admin/imports/locations/csv/template', token)
}

export function getStoreConfigs(token: string): Promise<StoreConfig[]> {
  return request<StoreConfig[]>('/api/admin/store-configs', {}, token)
}

export function createStoreConfig(token: string, payload: StoreConfigPayload): Promise<StoreConfig> {
  return request<StoreConfig>(
    '/api/admin/store-configs',
    {
      method: 'POST',
      body: JSON.stringify(payload)
    },
    token
  )
}

export function updateStoreConfig(
  token: string,
  storeConfigId: string,
  payload: Partial<StoreConfigPayload>
): Promise<StoreConfig> {
  return request<StoreConfig>(
    `/api/admin/store-configs/${storeConfigId}`,
    {
      method: 'PATCH',
      body: JSON.stringify(payload)
    },
    token
  )
}

export function searchGeocoding(token: string, query: string): Promise<GeocodingResult[]> {
  const params = new URLSearchParams({ query })
  return request<GeocodingResult[]>(`/api/admin/geocoding/search?${params.toString()}`, {}, token)
}

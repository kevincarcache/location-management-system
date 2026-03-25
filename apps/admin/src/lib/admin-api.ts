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

async function request<T>(path: string, init: RequestInit = {}, token?: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
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

async function upload<T>(path: string, file: File, token: string): Promise<T> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`
    },
    body: formData
  })

  if (!response.ok) {
    const detail = await response.text()
    throw new Error(detail || `Upload failed with status ${response.status}`)
  }

  return response.json() as Promise<T>
}

export function login(payload: LoginPayload): Promise<TokenPair> {
  return request<TokenPair>('/api/admin/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function refresh(refreshToken: string): Promise<TokenPair> {
  return request<TokenPair>('/api/admin/auth/refresh', {
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
  const response = await fetch(`${API_BASE_URL}/api/admin/imports/locations/csv/template`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })

  if (!response.ok) {
    const detail = await response.text()
    throw new Error(detail || `Template download failed with status ${response.status}`)
  }

  return response.blob()
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

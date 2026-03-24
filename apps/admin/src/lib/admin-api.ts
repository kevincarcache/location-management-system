const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export type ApiBusinessType =
  | 'virtual-store'
  | 'nearby-event'
  | 'recycling-point'
  | 'academy'
  | 'technical-service'

export type ApiLocationStatus = 'draft' | 'active' | 'archived'

export interface LoginPayload {
  email: string
  password: string
}

export interface TokenPair {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface ApiLocation {
  id: string
  slug: string
  name: string
  business_type: ApiBusinessType
  status: ApiLocationStatus
  description_short?: string | null
  description_long?: string | null
  address_line_1: string
  address_line_2?: string | null
  city: string
  region?: string | null
  country: string
  postal_code?: string | null
  latitude: number
  longitude: number
  phone?: string | null
  email?: string | null
  website?: string | null
  opening_hours: Record<string, string[]>
  services: string[]
  featured: boolean
  external_id?: string | null
}

export interface LocationFormPayload {
  slug: string
  name: string
  business_type: ApiBusinessType
  status: ApiLocationStatus
  description_short?: string | null
  description_long?: string | null
  address_line_1: string
  address_line_2?: string | null
  city: string
  region?: string | null
  country: string
  postal_code?: string | null
  latitude: number
  longitude: number
  phone?: string | null
  email?: string | null
  website?: string | null
  opening_hours: Record<string, string[]>
  services: string[]
  featured: boolean
  external_id?: string | null
}

export interface LocationImportRowError {
  id: string
  row_number: number
  message: string
  raw_row: string
}

export interface LocationImportJob {
  id: string
  filename: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  created: number
  updated: number
  rejected: number
  errors: LocationImportRowError[]
}

export interface LocationImportPreviewRow {
  row_number: number
  action: 'create' | 'update' | 'reject'
  slug?: string | null
  name?: string | null
  business_type?: string | null
  message?: string | null
}

export interface LocationImportPreview {
  filename: string
  required_columns: string[]
  optional_columns: string[]
  total_rows: number
  valid_rows: number
  create_candidates: number
  update_candidates: number
  rejected_rows: number
  rows: LocationImportPreviewRow[]
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

export type BusinessType =
  | 'virtual-store'
  | 'nearby-event'
  | 'recycling-point'
  | 'academy'
  | 'technical-service'

export type LocationStatus = 'draft' | 'active' | 'archived'

export interface TokenPair {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface LoginPayload {
  email: string
  password: string
}

export interface ApiLocation {
  id: string
  slug: string
  name: string
  business_type: BusinessType
  status: LocationStatus
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

export interface LocationSummary {
  id: string
  slug: string
  name: string
  businessType: BusinessType
  status: LocationStatus
  city: string
  country: string
  latitude: number
  longitude: number
  addressLine1: string
  descriptionShort?: string | null
  featured: boolean
}

export interface LocationDetail extends LocationSummary {
  addressLine2?: string | null
  region?: string | null
  postalCode?: string | null
  phone?: string | null
  email?: string | null
  website?: string | null
  descriptionLong?: string | null
  services: string[]
  openingHours: Record<string, string[]>
}

export interface PublicLocationFilters {
  query?: string
  businessType?: BusinessType | 'all'
}

export interface StoreConfig {
  id: string
  slug: string
  brand_name: string
  business_description: string
  theme_preset: string
  business_type: BusinessType
  logo_url?: string | null
  hero_title: string
  hero_subtitle: string
  menu_label: string
  footer_text: string
}

export interface StoreConfigPayload {
  slug: string
  brand_name: string
  business_description: string
  theme_preset: string
  business_type: BusinessType
  logo_url?: string | null
  hero_title: string
  hero_subtitle: string
  menu_label: string
  footer_text: string
}

export interface GeocodingResult {
  name: string
  address: string
  latitude: number
  longitude: number
}

export interface LocationFormPayload {
  slug: string
  name: string
  business_type: BusinessType
  status: LocationStatus
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

export type BusinessType =
  | 'virtual-store'
  | 'nearby-event'
  | 'recycling-point'
  | 'academy'
  | 'technical-service'

export type LocationStatus = 'draft' | 'active' | 'archived'

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


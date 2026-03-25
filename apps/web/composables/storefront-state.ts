import type { ApiLocation, LocationSummary } from '@lms/types'

export interface StorefrontRouteQueryInput {
  configuredStoreview: string | null
  query: string
  resolvedStoreview: string | null
  selectedSlug: string | null
}

export function mapLocationSummary(location: ApiLocation): LocationSummary {
  return {
    id: location.id,
    slug: location.slug,
    name: location.name,
    businessType: location.business_type,
    status: location.status,
    city: location.city,
    country: location.country,
    latitude: location.latitude,
    longitude: location.longitude,
    addressLine1: location.address_line_1,
    descriptionShort: location.description_short ?? null,
    featured: location.featured,
  }
}

export function buildStorefrontRouteQuery(input: StorefrontRouteQueryInput) {
  return {
    ...(input.resolvedStoreview && !input.configuredStoreview
      ? { storeview: input.resolvedStoreview }
      : {}),
    ...(input.query ? { q: input.query } : {}),
    ...(input.selectedSlug ? { selected: input.selectedSlug } : {}),
  }
}

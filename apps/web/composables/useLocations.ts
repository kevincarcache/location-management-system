import { computed } from 'vue'

import type { BusinessType, LocationSummary } from '@lms/types'

interface ApiLocation {
  id: string
  slug: string
  name: string
  business_type: BusinessType
  status: 'draft' | 'active' | 'archived'
  description_short?: string | null
  address_line_1: string
  city: string
  country: string
  latitude: number
  longitude: number
  featured: boolean
}

function mapLocation(location: ApiLocation): LocationSummary {
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
    featured: location.featured
  }
}

export async function useLocations(storeview: MaybeRefOrGetter<string | null>) {
  const config = useRuntimeConfig()
  const requestedSlug = computed(() => toValue(storeview) || null)

  const { data, pending, error, refresh } = await useFetch<ApiLocation[]>('/api/public/locations', {
    baseURL: config.public.apiBase,
    query: computed(() => {
      const slug = requestedSlug.value
      return slug ? { storeview: slug } : {}
    }),
    default: () => [],
    key: computed(() => `locations:${requestedSlug.value ?? 'default'}`),
    watch: [requestedSlug]
  })

  const locations = computed<LocationSummary[]>(() => (data.value ?? []).map(mapLocation))

  return {
    locations,
    pending,
    error,
    refresh
  }
}

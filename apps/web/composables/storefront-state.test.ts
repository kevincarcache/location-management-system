import { describe, expect, it } from 'vitest'

import type { ApiLocation } from '@lms/types'

import { buildStorefrontRouteQuery, mapLocationSummary } from './storefront-state'

describe('storefront-state', () => {
  it('maps api locations into storefront summaries', () => {
    const location: ApiLocation = {
      id: 'loc-1',
      slug: 'panama-city-hub',
      name: 'Panama City Hub',
      business_type: 'virtual-store',
      status: 'active',
      description_short: 'Sucursal principal',
      description_long: null,
      address_line_1: 'Avenida Balboa',
      address_line_2: null,
      city: 'Panama City',
      region: null,
      country: 'Panama',
      postal_code: null,
      latitude: 8.98,
      longitude: -79.52,
      phone: null,
      email: null,
      website: null,
      opening_hours: {},
      services: [],
      featured: true,
      external_id: 'seed-001',
    }

    expect(mapLocationSummary(location)).toEqual({
      id: 'loc-1',
      slug: 'panama-city-hub',
      name: 'Panama City Hub',
      businessType: 'virtual-store',
      status: 'active',
      city: 'Panama City',
      country: 'Panama',
      latitude: 8.98,
      longitude: -79.52,
      addressLine1: 'Avenida Balboa',
      descriptionShort: 'Sucursal principal',
      featured: true,
    })
  })

  it('omits configured storeview from shareable route query', () => {
    expect(
      buildStorefrontRouteQuery({
        configuredStoreview: 'default',
        resolvedStoreview: 'default',
        query: 'balboa',
        selectedSlug: 'panama-city-hub',
      }),
    ).toEqual({
      q: 'balboa',
      selected: 'panama-city-hub',
    })
  })

  it('includes resolved storeview when it comes from the url', () => {
    expect(
      buildStorefrontRouteQuery({
        configuredStoreview: null,
        resolvedStoreview: 'events',
        query: '',
        selectedSlug: 'innovation-weekend-marbella',
      }),
    ).toEqual({
      storeview: 'events',
      selected: 'innovation-weekend-marbella',
    })
  })
})

import { ref } from 'vue'

import type { LocationSummary } from '@lms/types'

const seedLocations: LocationSummary[] = [
  {
    id: 'seed-001',
    slug: 'panama-city-hub',
    name: 'Panama City Hub',
    businessType: 'virtual-store',
    status: 'active',
    city: 'Panama City',
    country: 'Panama',
    latitude: 8.9824,
    longitude: -79.5199,
    addressLine1: 'Avenida Balboa, Torre Central',
    descriptionShort: 'Centro principal para retiros, asesoría y soporte.',
    featured: true
  },
  {
    id: 'seed-002',
    slug: 'recycling-costa-del-este',
    name: 'Punto Verde Costa del Este',
    businessType: 'recycling-point',
    status: 'active',
    city: 'Panama City',
    country: 'Panama',
    latitude: 9.0075,
    longitude: -79.4818,
    addressLine1: 'Boulevard Costa del Este',
    descriptionShort: 'Recepción de plásticos, cartón y electrónicos.',
    featured: false
  }
]

export const useLocations = () => {
  const locations = ref<LocationSummary[]>(seedLocations)
  return { locations }
}

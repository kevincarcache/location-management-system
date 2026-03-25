import { computed, watch } from 'vue'

import type { ApiLocation, LocationSummary, StoreConfig } from '@lms/types'
import { buildStorefrontRouteQuery, mapLocationSummary } from './storefront-state'

export async function useStorefrontPage() {
  const route = useRoute()
  const router = useRouter()
  const runtimeConfig = useRuntimeConfig()

  const routeStoreview = computed(() =>
    typeof route.query.storeview === 'string' && route.query.storeview ? route.query.storeview : null
  )
  const configuredStoreview = computed(() =>
    runtimeConfig.public.storefrontSlug ? String(runtimeConfig.public.storefrontSlug) : null
  )
  const requestedStoreview = computed(() => configuredStoreview.value || routeStoreview.value)

  const query = ref(typeof route.query.q === 'string' ? route.query.q : '')
  const selectedSlug = ref<string | null>(
    typeof route.query.selected === 'string' ? route.query.selected : null
  )
  const drawer = ref(false)

  const { data, pending, error, refresh } = await useAsyncData(
    computed(() => `storefront-page:${requestedStoreview.value ?? 'default'}`),
    async () => {
      const storeConfig = await $fetch<StoreConfig>('/api/public/store-config', {
        baseURL: runtimeConfig.public.apiBase,
        query: requestedStoreview.value ? { storeview: requestedStoreview.value } : undefined
      })

      const resolvedStoreview =
        configuredStoreview.value || storeConfig.slug || routeStoreview.value || null

      const locations = await $fetch<ApiLocation[]>('/api/public/locations', {
        baseURL: runtimeConfig.public.apiBase,
        query: resolvedStoreview ? { storeview: resolvedStoreview } : undefined
      })

      return {
        locations: locations.map(mapLocationSummary),
        resolvedStoreview,
        storeConfig
      }
    },
    {
      watch: [requestedStoreview]
    }
  )

  const storeConfig = computed<StoreConfig | undefined>(() => data.value?.storeConfig)
  const resolvedStoreview = computed<string | null>(
    () => data.value?.resolvedStoreview ?? configuredStoreview.value ?? routeStoreview.value ?? null
  )
  const locations = computed<LocationSummary[]>(() => data.value?.locations ?? [])

  if (!selectedSlug.value && locations.value.length > 0) {
    selectedSlug.value = locations.value[0]?.slug ?? null
  }

  const filteredLocations = computed(() => {
    const normalized = query.value.trim().toLowerCase()
    return locations.value.filter((location) => {
      return (
        !normalized ||
        location.name.toLowerCase().includes(normalized) ||
        location.city.toLowerCase().includes(normalized) ||
        location.addressLine1.toLowerCase().includes(normalized)
      )
    })
  })

  function buildRouteQuery() {
    return buildStorefrontRouteQuery({
      configuredStoreview: configuredStoreview.value,
      resolvedStoreview: resolvedStoreview.value,
      query: query.value,
      selectedSlug: selectedSlug.value
    })
  }

  async function syncRouteState() {
    const nextQueryState = buildRouteQuery()
    const currentQueryState = {
      ...(typeof route.query.storeview === 'string' && route.query.storeview
        ? { storeview: route.query.storeview }
        : {}),
      ...(typeof route.query.q === 'string' && route.query.q ? { q: route.query.q } : {}),
      ...(typeof route.query.selected === 'string' && route.query.selected
        ? { selected: route.query.selected }
        : {})
    }

    if (JSON.stringify(currentQueryState) === JSON.stringify(nextQueryState)) {
      return
    }

    await router.replace({
      query: nextQueryState
    })
  }

  function updateQuery(value: string) {
    query.value = value
    void syncRouteState()
  }

  function updateSelectedSlug(value: string | null) {
    selectedSlug.value = value
  }

  function toggleDrawer() {
    drawer.value = !drawer.value
  }

  function updateDrawer(value: boolean) {
    drawer.value = value
  }

  function navigateToSection(id: string) {
    drawer.value = false

    if (!import.meta.client) {
      return
    }

    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  watch(
    filteredLocations,
    (items) => {
      if (!items.length) {
        selectedSlug.value = null
        return
      }
      const match = items.find((item) => item.slug === selectedSlug.value)
      if (!match) {
        selectedSlug.value = items[0]?.slug ?? null
      }
    },
    { immediate: true }
  )

  watch(
    [selectedSlug, resolvedStoreview],
    () => {
      void syncRouteState()
    },
    { flush: 'post' }
  )

  async function retryAll() {
    await refresh()
  }

  return {
    configError: error,
    drawer,
    filteredLocations,
    locationsError: error,
    navigateToSection,
    pendingConfig: pending,
    pendingLocations: pending,
    query,
    resolvedStoreview,
    retryAll,
    selectedSlug,
    storeConfig,
    toggleDrawer,
    updateDrawer,
    updateQuery,
    updateSelectedSlug
  }
}

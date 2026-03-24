import { computed } from 'vue'

import type { BusinessType } from '@lms/types'

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

export async function useStoreConfig(storeview: MaybeRefOrGetter<string | null>) {
  const config = useRuntimeConfig()
  const requestedSlug = computed(() => toValue(storeview) || null)

  const { data, pending, error, refresh } = await useFetch<StoreConfig>('/api/public/store-config', {
    baseURL: config.public.apiBase,
    query: computed(() => {
      const slug = requestedSlug.value
      return slug ? { storeview: slug } : {}
    }),
    key: computed(() => `store-config:${requestedSlug.value ?? 'default'}`),
    watch: [requestedSlug]
  })

  return {
    storeConfig: data,
    pending,
    error,
    refresh
  }
}

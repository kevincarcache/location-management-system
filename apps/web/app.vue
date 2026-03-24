<template>
  <v-app class="storefront-app" :data-theme="storeConfig?.theme_preset || 'storefront'">
    <div class="storefront-layout">
      <StorefrontHeader
        :drawer="drawer ?? false"
        :store-config="storeConfig"
        @toggle-drawer="toggleDrawer"
        @update:drawer="updateDrawer"
        @navigate="navigateToSection"
      />

      <v-sheet tag="main" color="transparent" class="storefront-main">
        <v-container class="storefront-stage py-4 py-md-8" fluid>
          <v-container class="px-0 px-md-4" max-width="1480">
            <StorefrontHero
              :query="query ?? ''"
              :store-config="storeConfig"
              @update:query="updateQuery"
            />

            <StorefrontStatus
              v-if="pendingConfig || pendingLocations"
              mode="loading"
            />

            <StorefrontStatus
              v-else-if="configError || locationsError"
              mode="error"
              @retry="retryAll"
            />

            <v-sheet
              v-else
              id="locations"
              rounded="md"
              class="locator-workspace pa-3 pa-md-4"
            >
              <v-row class="ga-0">
                <v-col cols="12" lg="4" xl="3" class="pe-lg-4 mb-4 mb-lg-0">
                  <LocationSidebar
                    :locations="filteredLocations ?? []"
                    :selected-slug="selectedSlug ?? null"
                    :title="storeConfig?.menu_label || 'Ubicaciones'"
                    @select="updateSelectedSlug"
                  />
                </v-col>

                <v-col id="mapa" cols="12" lg="8" xl="9">
                  <LocationMap
                    :locations="filteredLocations ?? []"
                    :selected-slug="selectedSlug ?? null"
                    @select="updateSelectedSlug"
                  />
                </v-col>
              </v-row>
            </v-sheet>
          </v-container>
        </v-container>
      </v-sheet>

      <StorefrontFooter
        :resolved-storeview="resolvedStoreview"
        :store-config="storeConfig"
      />
    </div>
  </v-app>
</template>

<script setup lang="ts">
const {
  configError,
  drawer,
  filteredLocations,
  locationsError,
  navigateToSection,
  pendingConfig,
  pendingLocations,
  query,
  resolvedStoreview,
  retryAll,
  selectedSlug,
  storeConfig,
  toggleDrawer,
  updateDrawer,
  updateQuery,
  updateSelectedSlug
} = await useStorefrontPage()

useHead(
  computed(() => ({
    title: storeConfig.value?.brand_name || 'Storefront',
    meta: [
      {
        name: 'description',
        content: storeConfig.value?.business_description || 'Ubicaciones y puntos de atención.'
      }
    ]
  }))
)
</script>

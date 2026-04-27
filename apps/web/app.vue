<template>
  <v-app :data-theme="storeConfig?.theme_preset || 'storefront'">
    <v-layout class="d-flex flex-column">
      <StorefrontHeader
        :store-config="storeConfig"
      />

      <v-main>
        <v-container fluid class="py-4 py-md-8">
          <v-container max-width="1480">
            <StorefrontHero
              :store-config="storeConfig"
            />

            <v-sheet
              rounded="lg"
              color="surface"
              border
              class="mb-5 mb-md-7 pa-4 pa-md-5"
            >
              <v-text-field
                :model-value="query ?? ''"
                prepend-inner-icon="mdi-magnify"
                label="Buscar por nombre, ciudad o dirección"
                hide-details
                class="w-100"
                @update:model-value="updateQuery($event ?? '')"
              />
            </v-sheet>

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
              rounded="lg"
              color="surface"
              border
              class="pa-3 pa-md-4"
            >
              <v-row>
                <v-col cols="12" lg="4" xl="3">
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
      </v-main>

      <StorefrontFooter
        :store-config="storeConfig"
      />
    </v-layout>
  </v-app>
</template>

<script setup lang="ts">
const {
  configError,
  filteredLocations,
  locationsError,
  pendingConfig,
  pendingLocations,
  query,
  retryAll,
  selectedSlug,
  storeConfig,
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

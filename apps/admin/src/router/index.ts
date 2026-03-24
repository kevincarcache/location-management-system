import { createRouter, createWebHistory } from 'vue-router'

import AdminShell from '../layouts/AdminShell.vue'
import DashboardPage from '../pages/DashboardPage.vue'
import LocationEditorPage from '../pages/LocationEditorPage.vue'
import LocationTypesPage from '../pages/LocationTypesPage.vue'
import LoginPage from '../pages/LoginPage.vue'
import LocationsPage from '../pages/LocationsPage.vue'
import ReportsPage from '../pages/ReportsPage.vue'
import StoreSettingsPage from '../pages/StoreSettingsPage.vue'
import { registerRouterGuards } from './guards'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: LoginPage, meta: { public: true } },
    {
      path: '/',
      component: AdminShell,
      children: [
        { path: '', component: DashboardPage },
        { path: 'locations', component: LocationsPage },
        { path: 'locations/new', component: LocationEditorPage },
        { path: 'locations/:locationId/edit', component: LocationEditorPage, props: true },
        { path: 'location-types', component: LocationTypesPage },
        { path: 'reports', component: ReportsPage },
        { path: 'store-settings', component: StoreSettingsPage }
      ]
    }
  ]
})

registerRouterGuards(router)

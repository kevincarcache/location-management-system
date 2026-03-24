import { createRouter, createWebHistory } from 'vue-router'

import DashboardPage from '../pages/DashboardPage.vue'
import LoginPage from '../pages/LoginPage.vue'
import LocationsPage from '../pages/LocationsPage.vue'
import { registerRouterGuards } from './guards'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: DashboardPage },
    { path: '/login', component: LoginPage, meta: { public: true } },
    { path: '/locations', component: LocationsPage }
  ]
})

registerRouterGuards(router)

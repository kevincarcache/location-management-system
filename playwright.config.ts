import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 60_000,
  fullyParallel: false,
  retries: 0,
  reporter: 'list',
  use: {
    baseURL: 'http://localhost:3100',
    trace: 'on-first-retry'
  },
  webServer: [
    {
      command: 'pnpm dev:api',
      port: 8000,
      reuseExistingServer: true,
      timeout: 120_000,
      cwd: '.'
    },
    {
      command: 'pnpm --filter @lms/web exec nuxt dev --host localhost --port 3100',
      port: 3100,
      reuseExistingServer: true,
      timeout: 120_000,
      cwd: '.'
    },
    {
      command: 'pnpm --filter @lms/admin exec vite --host localhost --port 4173',
      port: 4173,
      reuseExistingServer: true,
      timeout: 120_000,
      cwd: '.'
    }
  ],
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    }
  ]
})

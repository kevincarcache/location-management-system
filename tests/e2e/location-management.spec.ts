import { expect, test } from '@playwright/test'

async function loginToAdmin(page: Parameters<typeof test>[0]['page']) {
  await page.goto('http://localhost:4173/login')

  await page.getByLabel('Email').fill('admin@example.com')
  await page.getByLabel('Password').fill('ChangeMe123!')
  await page.getByRole('button', { name: /entrar/i }).click()
  await expect(page).toHaveURL('http://localhost:4173/')
}

test('public locator renders seeded locations and search state', async ({ page }) => {
  await page.goto('/')

  await expect(
    page.getByRole('heading', { name: /encuentra la sucursal ideal para tu próxima visita/i })
  ).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Panama City Hub' })).toBeVisible()
  await expect(page.getByText(/storeview: default/i)).toBeVisible()

  await page.getByLabel(/buscar por nombre, ciudad o dirección/i).fill('balboa')
  await expect(page).toHaveURL(/q=balboa/i)
  await expect(page.getByRole('heading', { name: 'Panama City Hub' })).toBeVisible()
})

test('admin login works with seeded credentials', async ({ page }) => {
  await loginToAdmin(page)
  await expect(page.getByRole('heading', { name: /dashboard/i })).toBeVisible()
})

test('admin can create a location and it appears on the public site', async ({ page }) => {
  const suffix = Date.now().toString().slice(-6)
  const locationName = `E2E Service ${suffix}`
  const locationSlug = `e2e-service-${suffix}`

  await loginToAdmin(page)
  await page.goto('http://localhost:4173/locations')

  await page.getByTestId('new-location-button').click()
  await page.getByLabel('Nombre').fill(locationName)
  await page.getByLabel('Slug').fill(locationSlug)
  await page.getByLabel('Dirección principal').fill('Calle 50, Torre E2E')
  await page.getByLabel('Ciudad').fill('Panama City')
  await page.getByLabel('País').fill('Panama')
  await page.getByTestId('save-location-button').click()

  await expect(page.getByText(locationName)).toBeVisible()

  await page.goto('/')
  await page.getByLabel(/buscar por nombre, ciudad o dirección/i).fill(locationName)
  await expect(page.getByText(locationName)).toBeVisible()
})

test('admin can preview and import csv data that becomes public', async ({ page }) => {
  const suffix = Date.now().toString().slice(-6)
  const locationName = `E2E Import ${suffix}`
  const locationSlug = `e2e-import-${suffix}`

  const csvContent = [
    'external_id,slug,name,business_type,address_line_1,city,country,latitude,longitude',
    `e2e-${suffix},${locationSlug},${locationName},virtual-store,Avenida Central,Panama City,Panama,8.99,-79.52`
  ].join('\n')

  await loginToAdmin(page)
  await page.goto('http://localhost:4173/locations')

  await page.getByTestId('open-import-dialog-button').click()
  await page.locator('input[type="file"]').setInputFiles({
    name: 'locations.csv',
    mimeType: 'text/csv',
    buffer: Buffer.from(csvContent, 'utf-8')
  })
  await page.getByTestId('preview-import-button').click()

  await expect(page.getByText(locationName)).toBeVisible()
  await page.getByTestId('confirm-import-button').click()

  await expect(page.getByText('locations.csv')).toBeVisible()
  await page.goto('/')
  await page.getByLabel(/buscar por nombre, ciudad o dirección/i).fill(locationName)
  await expect(page.getByText(locationName)).toBeVisible()
})

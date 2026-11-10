// frontend/e2e/orders.spec.ts
import { test, expect } from '@playwright/test';

test('commander décrémente le stock', async ({ page, request }) => {
  // Crée un drop via l'API pour être indépendant
  const res = await request.post('http://localhost:8000/api/drops', {
    data: { name: 'E2E Drop', price: 90, stock: 2, start_time: new Date().toISOString() }
  });
  const drop = await res.json();

  await page.goto(`/drops/${drop.id}`);
  const remainingEl = page.locator('[data-testid="remaining"]');
  await expect(remainingEl).toHaveText('2');

  await page.getByRole('button', { name: /commander|acheter/i }).click();
  await expect(remainingEl).toHaveText('1');
});

test('un drop épuisé désactive le bouton', async ({ page, request }) => {
  const res = await request.post('http://localhost:8000/api/drops', {
    data: { name: 'Soldout Drop', price: 90, stock: 0, start_time: new Date().toISOString() }
  });
  const drop = await res.json();

  await page.goto(`/drops/${drop.id}`);
  const button = page.getByRole('button', { name: /épuisé|sold out|commander/i });
  await expect(button).toBeDisabled();
});

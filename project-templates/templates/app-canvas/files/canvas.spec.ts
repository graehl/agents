import { test, expect } from "@playwright/test";
import { createStaticServer } from "../../scripts/serve.mjs";
import type { Server } from "node:http";

let server: Server;
let url: string;
test.beforeAll(async () => {
  server = await createStaticServer();
  await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address();
  if (!address || typeof address === "string")
    throw new Error("Missing test server port");
  url = `http://127.0.0.1:${address.port}`;
});
test.afterAll(async () => {
  if (!server) return;
  server.closeAllConnections();
  await new Promise<void>((resolve) => server.close(() => resolve()));
});

test("draw, resize, undo, and type without losing characters", async ({ page }) => {
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto(url);
  const canvas = page.getByLabel("Drawing canvas.", { exact: false });
  const box = (await canvas.boundingBox())!;
  await page.mouse.move(box.x + 30, box.y + 35);
  await page.mouse.down();
  await page.mouse.move(box.x + box.width - 35, box.y + 150, { steps: 12 });
  await page.mouse.up();
  await expect(page.locator("#status")).toHaveText("1 stroke");
  expect(
    await canvas.evaluate((element: HTMLCanvasElement) =>
      element
        .getContext("2d")!
        .getImageData(0, 0, element.width, element.height)
        .data.some((value, index) => index % 4 === 3 && value > 0),
    ),
  ).toBe(true);
  const size = page.viewportSize()!;
  await page.setViewportSize({ width: size.width - 10, height: size.height });
  await expect(page.locator("#status")).toHaveText("1 stroke");
  await page.getByRole("button", { name: "Undo" }).click();
  await expect(page.locator("#status")).toHaveText("0 strokes");
  for (let stroke = 0; stroke < 20; stroke++) {
    await page.mouse.move(box.x + 30, box.y + 40 + stroke * 4);
    await page.mouse.down();
    await page.mouse.move(box.x + box.width - 45, box.y + 100 + stroke * 4, { steps: 6 });
    await page.mouse.up();
  }
  await expect(page.locator("#status")).toHaveText("20 strokes");
  const resizeTimer = await page.evaluate(() =>
    window.setInterval(() => {
      const element = document.querySelector("canvas")!;
      element.style.height = element.style.height === "250px" ? "260px" : "250px";
    }, 16),
  );
  const input = page.getByLabel("Sketch name");
  await input.clear();
  const text = "My canvas 0123456789";
  try {
    for (let index = 0; index < text.length; index++) {
      await input.pressSequentially(text[index]);
      await expect(input).toHaveValue(text.slice(0, index + 1), { timeout: 100 });
    }
  } finally {
    await page.evaluate((timer) => window.clearInterval(timer), resizeTimer);
  }
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth),
  ).toBe(true);
  expect(errors).toEqual([]);
});

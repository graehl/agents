import { test, expect } from "@playwright/test";
import { createStaticServer } from "../../scripts/serve.mjs";
import type { Server } from "node:http";

let server: Server;
let url: string;
test.beforeAll(async () => {
  server = await createStaticServer();
  await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address();
  if (!address || typeof address === "string") throw new Error("Missing preview port");
  url = `http://127.0.0.1:${address.port}`;
});
test.afterAll(async () => {
  if (!server) return;
  server.closeAllConnections();
  await new Promise<void>((resolve) => server.close(() => resolve()));
});

test("navigate, filter and type without losing characters", async ({ page }) => {
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto(url);
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "A place foryour next idea.",
  );
  await page.getByRole("link", { name: /Take a look/ }).click();
  await expect(page).toHaveURL(/#collection$/);
  await expect(page.getByRole("article")).toHaveCount(3);
  await page.getByRole("button", { name: "Make", exact: true }).click();
  await expect(page.getByRole("article")).toHaveCount(2);
  const search = page.getByRole("searchbox", { name: "Find an idea" });
  let query = "";
  for (const character of "share") {
    await search.pressSequentially(character);
    query += character;
    await expect(search).toHaveValue(query, { timeout: 100 });
  }
  await expect(page.getByRole("article")).toHaveCount(1);
  await expect(page.getByRole("heading", { name: "Made to share" })).toBeVisible();
  await page.getByRole("button", { name: "Explore", exact: true }).click();
  await expect(page.getByText("No ideas match yet.", { exact: false })).toBeVisible();
  await search.fill("");
  await page.getByRole("button", { name: "All ideas" }).click();
  await expect(page.getByRole("article")).toHaveCount(3);
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth),
  ).toBe(true);
  expect(errors).toEqual([]);
});

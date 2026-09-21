import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "test/browser",
  use: { headless: true },
  projects: [
    { name: "desktop", use: { viewport: { width: 1200, height: 600 } } },
    {
      name: "phone",
      use: { viewport: { width: 375, height: 812 }, hasTouch: true },
    },
  ],
});

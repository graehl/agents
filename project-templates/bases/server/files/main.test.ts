import assert from "node:assert/strict";
import test from "node:test";
import { createBackendServer } from "./main.ts";

test("the added server serves the app and its API on one origin", async () => {
  const server = await createBackendServer();
  try {
    await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
    const address = server.address();
    if (!address || typeof address === "string")
      throw new Error("Missing server address");
    const url = `http://127.0.0.1:${address.port}`;
    const page = await fetch(url);
    assert.equal(page.status, 200);
    assert.match(await page.text(), /<html/);
    const health = await fetch(`${url}/api/health`);
    assert.deepEqual(await health.json(), { ok: true, service: "app-canvas" });
    assert.equal((await fetch(`${url}/api/health`, { method: "POST" })).status, 405);
    assert.equal((await fetch(`${url}/package.json`)).status, 404);
  } finally {
    server.closeAllConnections();
    await new Promise<void>((resolve) => server.close(() => resolve()));
  }
});

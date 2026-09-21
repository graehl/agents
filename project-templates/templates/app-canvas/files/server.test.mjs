import assert from "node:assert/strict";
import { request } from "node:http";
import { mkdtemp, mkdir, writeFile, rm } from "node:fs/promises";
import path from "node:path";
import test from "node:test";

test("preview serves only dist and rejects traversal and writes", async () => {
  // The server module locates its project from its own path, so exercise it in a fresh tree.
  const fixture = await mkdtemp(path.resolve(".server-test-"));
  let server;
  try {
    await mkdir(path.join(fixture, "scripts"));
    await mkdir(path.join(fixture, "dist"));
    const { copyFile } = await import("node:fs/promises");
    await copyFile("scripts/serve.mjs", path.join(fixture, "scripts/serve.mjs"));
    await writeFile(path.join(fixture, "dist/index.html"), "<h1>Built app</h1>");
    await writeFile(path.join(fixture, "secret.txt"), "outside");
    const { pathToFileURL } = await import("node:url");
    const { createStaticServer } = await import(
      pathToFileURL(path.join(fixture, "scripts/serve.mjs"))
    );
    server = await createStaticServer();
    await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
    const query = (url, method = "GET") =>
      new Promise((resolve, reject) => {
        const req = request(
          { host: "127.0.0.1", port: server.address().port, path: url, method },
          (res) => {
            let body = "";
            res.on("data", (chunk) => (body += chunk));
            res.on("end", () => resolve({ status: res.statusCode, body }));
          },
        );
        req.on("error", reject);
        req.end();
      });
    assert.deepEqual(await query("/"), {
      status: 200,
      body: "<h1>Built app</h1>",
    });
    assert.equal((await query("/%2e%2e/secret.txt")).status, 400);
    assert.equal((await query("/secret.txt")).status, 404);
    assert.equal((await query("/", "POST")).status, 405);
    assert.equal((await query("/%ZZ")).status, 400);
  } finally {
    server?.closeAllConnections();
    if (server) await new Promise((resolve) => server.close(resolve));
    await rm(fixture, { recursive: true });
  }
});

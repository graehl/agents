import type { IncomingMessage, ServerResponse } from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createStaticServer, listen } from "../scripts/serve.mjs";

export const createBackendServer = () =>
  createStaticServer((request: IncomingMessage, response: ServerResponse) => {
    if (request.url?.split("?")[0] !== "/api/health") return false;
    if (request.method !== "GET") {
      response.writeHead(405, { Allow: "GET" }).end();
      return true;
    }
    response.writeHead(200, {
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
    });
    response.end(JSON.stringify({ ok: true, service: "app-canvas" }));
    return true;
  });
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await listen(await createBackendServer());
}

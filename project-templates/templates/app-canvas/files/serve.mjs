import { createServer } from "node:http";
import { createReadStream } from "node:fs";
import { realpath, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript",
  ".css": "text/css",
  ".json": "application/json",
  ".webmanifest": "application/manifest+json",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".wasm": "application/wasm",
  ".woff2": "font/woff2",
};

/** Serve only the built bundle; an optional API handler returns whether it replied. */
export async function createStaticServer(api = (_request, _response) => false) {
  const root = await realpath(path.join(projectRoot, "dist"));
  return createServer(async (request, response) => {
    try {
      if (await api(request, response)) return;
      if (request.method !== "GET" && request.method !== "HEAD") {
        response.writeHead(405, { Allow: "GET, HEAD" }).end();
        return;
      }
      const name = decodeURIComponent((request.url || "/").split("?")[0]);
      if (
        !name.startsWith("/") ||
        name.includes("\\") ||
        name.split("/").includes("..") ||
        name.includes("\0")
      ) {
        response.writeHead(400).end();
        return;
      }
      const resolved = await realpath(
        path.join(root, name === "/" ? "index.html" : name.slice(1)),
      );
      if (!resolved.startsWith(`${root}${path.sep}`)) {
        response.writeHead(404).end();
        return;
      }
      const info = await stat(resolved);
      if (!info.isFile()) {
        response.writeHead(404).end();
        return;
      }
      response.writeHead(200, {
        "Content-Type": mimeTypes[path.extname(resolved)] || "application/octet-stream",
        "Content-Length": info.size,
        "Cache-Control": "no-cache",
        "X-Content-Type-Options": "nosniff",
      });
      if (request.method === "HEAD") response.end();
      else
        createReadStream(resolved)
          .on("error", () => response.destroy())
          .pipe(response);
    } catch (error) {
      if (response.headersSent) {
        response.destroy();
        return;
      }
      const status =
        error instanceof URIError
          ? 400
          : error.code === "ENOENT" || error.code === "ENOTDIR"
            ? 404
            : 500;
      if (status === 500) console.error("[serve] Request failed", error);
      response.writeHead(status).end();
    }
  });
}

export async function listen(server) {
  const value = process.env.PORT ?? "0";
  if (!/^\d+$/.test(value) || Number(value) > 65535)
    throw new Error("PORT must be an integer from 0 to 65535");
  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(Number(value), "127.0.0.1", resolve);
  });
  console.log(`[serve] http://127.0.0.1:${server.address().port}`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url))
  await listen(await createStaticServer());

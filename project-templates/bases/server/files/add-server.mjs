import { mkdir, readFile, writeFile, access } from "node:fs/promises";
import { constants } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const packagePath = path.join(root, "package.json");
const pkg = JSON.parse(await readFile(packagePath, "utf8"));
const appPath = path.join(root, ".project-template/app.json");
const app = JSON.parse(await readFile(appPath, "utf8"));
if (
  app.kind !== "static" ||
  pkg.scripts.start ||
  !pkg.scripts.typecheck ||
  !pkg.scripts.test
)
  throw new Error(
    "Server add-on requires no existing start command and an existing typecheck command",
  );
try {
  await access(path.join(root, "server"), constants.F_OK);
  throw new Error("Server add-on refuses an existing server directory");
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}
const files = await Promise.all(
  ["main.ts", "main.test.ts", "tsconfig.json"].map(async (name) => [
    name,
    await readFile(path.join(root, ".project-template/addons/server", name)),
  ]),
);
await mkdir(path.join(root, "server"));
for (const [name, content] of files)
  await writeFile(path.join(root, "server", name), content, { flag: "wx" });
pkg.scripts.start = "node --experimental-strip-types server/main.ts";
pkg.scripts.typecheck += " && tsc -p server/tsconfig.json";
pkg.scripts.test +=
  " && npm run build && node --experimental-strip-types --test server/*.test.ts";
await writeFile(packagePath, `${JSON.stringify(pkg, null, 2)}\n`);
app.kind = "server";
app.start = ["node", "--experimental-strip-types", "server/main.ts"];
await writeFile(appPath, `${JSON.stringify(app, null, 2)}\n`);
console.log(
  "[server] Added server/. Run npm run typecheck, npm test, npm run build, then PORT=<port> npm start.",
);

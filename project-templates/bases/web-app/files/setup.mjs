import { spawn } from "node:child_process";
import { readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const context = JSON.parse(
  await readFile(path.join(root, ".project-template/project.json"), "utf8"),
);
const heading = String(context.name).replace(/[\r\n]+/g, " ");
const description = String(context.description).replace(/\s+/g, " ").trim();
const readmePath = path.join(root, "README.md");
const readme = await readFile(readmePath, "utf8");
if (
  readme.startsWith(
    "![Project thumbnail](docs/brand.svg)\n\n# Web app\n\nA working static web app starter,",
  )
) {
  const remainder = readme.indexOf("\n## Develop and verify");
  await writeFile(
    readmePath,
    `![Project thumbnail](docs/brand.svg)\n\n# ${heading}\n\n${description || "A working web app ready for your ideas."}\n\nCurrently a working ${context.origin.template} starter; app-specific implementation follows preparation.\n${readme.slice(remainder)}`,
  );
}
const npm = process.platform === "win32" ? "npm.cmd" : "npm";
for (const args of [
  ["ci", "--no-audit", "--no-fund"],
  ["run", "typecheck"],
  ["test"],
  ["run", "build"],
]) {
  console.log(`[setup] ${npm} ${args.join(" ")}`);
  await new Promise((resolve, reject) => {
    const child = spawn(npm, args, {
      cwd: root,
      stdio: "inherit",
      shell: process.platform === "win32",
    });
    child.once("error", reject);
    child.once("exit", (code, signal) =>
      code === 0
        ? resolve()
        : reject(
            new Error(`Setup command failed: ${args.join(" ")} (${signal ?? code})`),
          ),
    );
  });
}
console.log(
  "[setup] Starter ready. Run npm run preview; preparation prompt: .project-template/PREPARE.md",
);

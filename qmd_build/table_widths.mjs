// Headless-Chromium host for table_widths.js. Usage:
// node table_widths.mjs <input.html> <playwright-dir> '<options-json>'
// Prints the per-table, per-band width decisions as JSON on stdout.
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const [input, playwrightFrom, optionsJson] = process.argv.slice(2);
if (!input || !playwrightFrom) {
	throw new Error("usage: table_widths.mjs <input.html> <playwright-dir> [options-json]");
}
const chooser = readFileSync(resolve(dirname(fileURLToPath(import.meta.url)), "table_widths.js"), "utf8");
const require = createRequire(resolve(playwrightFrom, "package.json"));
const { chromium } = require("@playwright/test");
const browser = await chromium.launch({ headless: true });
try {
	const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
	await page.goto(pathToFileURL(resolve(input)).href, { waitUntil: "networkidle" });
	await page.evaluate(() => document.fonts.ready);
	const decisions = await page.evaluate(`(${chooser.trim()})(${optionsJson || "{}"})`);
	console.log(JSON.stringify(decisions));
} finally {
	await browser.close();
}

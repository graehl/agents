// Headless-Chromium print of a rendered HTML document; qmd-html's --print-pdf
// worker. Usage: node print_pdf.mjs <input.html> <output.pdf> <playwright-dir>
// '<options-json>'. <playwright-dir> is any package directory whose
// node_modules resolve @playwright/test; no server is started.
import { createRequire } from "node:module";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const [input, output, playwrightFrom, optionsJson] = process.argv.slice(2);
if (!input || !output || !playwrightFrom) {
	throw new Error("usage: print_pdf.mjs <input.html> <output.pdf> <playwright-dir> [options-json]");
}
const options = JSON.parse(optionsJson || "{}");
const require = createRequire(resolve(playwrightFrom, "package.json"));
const { chromium } = require("@playwright/test");
const browser = await chromium.launch({ headless: true });
try {
	const page = await browser.newPage();
	await page.goto(pathToFileURL(resolve(input)).href, { waitUntil: "networkidle" });
	await page.evaluate(async () => {
		await document.fonts.ready;
		await Promise.all([...document.images].map((image) => image.decode()));
	});
	await page.pdf({
		path: resolve(output),
		format: options.format ?? "A4",
		printBackground: true,
		preferCSSPageSize: true,
		tagged: true,
		margin: options.margin ?? { top: "16mm", bottom: "16mm", left: "15mm", right: "15mm" },
	});
	console.log(JSON.stringify({ phase: "print-pdf", output: resolve(output), chromium: browser.version() }));
} finally {
	await browser.close();
}

// Browser check of the folds program_view.js builds: usage
//   node program_view_browser.mjs <index.html> <dir whose node_modules has @playwright/test>
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const [input, playwrightFrom] = process.argv.slice(2);
const require = createRequire(resolve(playwrightFrom, "package.json"));
const { chromium } = require("@playwright/test");
const browser = await chromium.launch({ headless: true });
try {
	const page = await browser.newPage({
		viewport: { width: 1200, height: 600 },
	});
	const errors = [];
	page.on("pageerror", (error) => errors.push(error.message));
	await page.goto(pathToFileURL(resolve(input)).href);
	const summaries = (
		await page.locator("details.more > summary").allTextContents()
	).map((text) => text.trim());
	// One session is older than the default cutoff: singular, not "1 older sessions".
	assert.ok(
		summaries.includes("1 older session"),
		`no "1 older session" among ${JSON.stringify(summaries)}`,
	);
	// A kind with more rows than the limit shows the limit and folds the rest.
	const kinds = await page.evaluate(() =>
		[...document.querySelectorAll("details.kind")].map((kind) => ({
			rows: kind.querySelectorAll("tr[data-path]").length,
			folded: kind.querySelectorAll("details.more tr[data-path]").length,
			labels: [...kind.querySelectorAll("details.more > summary")].map((s) =>
				s.textContent.trim(),
			),
		})),
	);
	const long = kinds.filter((kind) => kind.folded > 0);
	assert.ok(long.length > 0, `no folded kind in ${JSON.stringify(kinds)}`);
	for (const kind of long) {
		const counted = kind.labels
			.map((label) => Number.parseInt(label, 10))
			.reduce((a, b) => a + b, 0);
		assert.equal(counted, kind.folded, JSON.stringify(kind));
		assert.ok(kind.rows > kind.folded, "a folded kind still shows rows");
	}
	assert.deepEqual(errors, []);
} finally {
	await browser.close();
}

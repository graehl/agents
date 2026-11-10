import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const [input, playwrightFrom, captureDirectory] = process.argv.slice(2);
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
	await page.waitForFunction(() => window.MathJax?.startup?.promise);
	await page.evaluate(() => window.MathJax.startup.promise);
	assert.equal(await page.locator("mjx-merror").count(), 0);
	for (const text of await page.locator("mjx-mtext").allTextContents()) {
		assert.ok(!text.includes("\\"), `Unrendered TeX: ${text}`);
	}
	const score = page.locator('.math a[href="#term-score"]').first();
	const card = page.locator("#qmd-term-card");
	await score.hover();
	await card.waitFor({ state: "visible" });
	await page.waitForFunction(() =>
		document.querySelector("#qmd-term-card mjx-container"),
	);
	assert.match(await card.innerText(), /hypothesis/);
	assert.match(await card.innerText(), /Go to definition/);
	await card.hover();
	await page.waitForTimeout(300);
	assert.equal(await card.isVisible(), true);
	if (captureDirectory) {
		await page.screenshot({ path: resolve(captureDirectory, "desktop.png") });
	}
	await page.keyboard.press("Escape");
	assert.equal(await card.isVisible(), false);
	await score.focus();
	// Escape restored focus already; move away and back to exercise keyboard entry.
	await score.evaluate((el) => el.blur());
	await score.focus();
	await card.waitFor({ state: "visible" });
	await page.keyboard.press("Enter");
	await page.waitForFunction(
		() => document.activeElement?.textContent === "Close",
	);
	await page.keyboard.press("Enter");
	assert.equal(await card.isVisible(), false);
	await page.setViewportSize({ width: 375, height: 812 });
	// Resizing makes the page lay its math out again a moment later, which
	// replaces the link element; a card opened on the old element closes with
	// it. Click only once the link has been the same element, in the same
	// place, for a while.
	await page.waitForFunction(() => {
		const link = document.querySelector('.math a[href="#term-score"]');
		const top = link?.getBoundingClientRect().top;
		const now = performance.now();
		const was = window.settling ?? {};
		if (was.link !== link || was.top !== top)
			window.settling = { link, top, since: now };
		return innerWidth === 375 && now - window.settling.since > 400;
	});
	await score.click();
	await card.waitFor({ state: "visible" });
	const bounds = await card.boundingBox();
	assert.ok(bounds.x >= 0 && bounds.x + bounds.width <= 375);
	assert.ok(bounds.y >= 0 && bounds.y + bounds.height <= 812);
	if (captureDirectory) {
		await page.screenshot({ path: resolve(captureDirectory, "mobile.png") });
	}
	await card.getByRole("link", { name: "Go to definition" }).click();
	assert.equal(new URL(page.url()).hash, "#term-score");
	assert.equal(await card.isVisible(), false);
	assert.deepEqual(errors, []);
	console.log(
		"term-hints: math, hover, selectable card, keyboard, tap, and definition link passed",
	);
} finally {
	await browser.close();
}

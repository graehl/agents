// Browser check that a term card stays open when opening it scrolls the page:
//   node term_card_scroll_browser.mjs <term_hints.js> <term_hints.css> <dir whose node_modules has @playwright/test>
import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const [script, style, playwrightFrom] = process.argv.slice(2);
const require = createRequire(resolve(playwrightFrom, "package.json"));
const { chromium } = require("@playwright/test");
const filler = "<p>Filler paragraph.</p>".repeat(80);
const html = `<!doctype html><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>${readFileSync(style, "utf8")}</style>
<p><span id="term-score">The score compares two strings.</span></p>
<template data-term-card="term-score" data-term-kind="Definition">The score compares two strings.</template>
<p>Near the top: <a id="near" href="#term-score" class="term-ref">score</a>.</p>
${filler}
<p>Below the fold: <a id="far" href="#term-score" class="term-ref">score</a>.</p>
<div id="box" style="height: 120px; overflow: auto">
<p>In a scrolling box: <a id="boxed" href="#term-score" class="term-ref">score</a>.</p>
${filler}
</div>
${filler}
<script>${readFileSync(script, "utf8")}</script>`;
const directory = mkdtempSync(join(tmpdir(), "term-card-scroll-"));
const file = join(directory, "page.html");
writeFileSync(file, html);
const browser = await chromium.launch({ headless: true });
try {
	for (const viewport of [
		{ width: 1200, height: 600 },
		{ width: 375, height: 812 },
	]) {
		const page = await browser.newPage({ viewport });
		await page.goto(pathToFileURL(file).href);
		const card = page.locator("#qmd-term-card");
		const where = `${viewport.width}x${viewport.height}`;
		// The card must still be open, and beside its link, well after the
		// scroll its opening caused.
		const staysOpen = async (what, link) => {
			await card.waitFor({ state: "visible" });
			for (const wait of [100, 400, 1000]) {
				await page.waitForTimeout(wait);
				assert.ok(await card.isVisible(), `${where}: ${what}: card closed`);
			}
			const [at, by] = [await card.boundingBox(), await link.boundingBox()];
			const below = Math.abs(at.y - (by.y + by.height + 8)) < 2;
			const above = Math.abs(at.y + at.height - (by.y - 8)) < 2;
			assert.ok(below || above, `${where}: ${what}: card not beside its link`);
			await page.keyboard.press("Escape");
		};
		// Keyboard: focus moves from the link in view to the one below the fold.
		await page.evaluate(() => document.querySelector("#near").focus());
		await page.keyboard.press("Escape");
		await page.keyboard.press("Tab");
		assert.equal(
			await page.evaluate(() => document.activeElement?.id),
			"far",
		);
		assert.ok(
			(await page.evaluate(() => scrollY)) > 0,
			`${where}: focus did not scroll the page`,
		);
		await staysOpen("Tab to a link below the fold", page.locator("#far"));
		// Pointer: the link is scrolled into view and clicked at once.
		await page.evaluate(() => scrollTo(0, 0));
		await page.waitForFunction(() => scrollY === 0);
		const far = page.locator("#far");
		await far.scrollIntoViewIfNeeded();
		await far.click();
		await staysOpen("scroll a link into view and click it", far);
		// Scrolling the link out of view still closes its card.
		await far.click();
		await card.waitFor({ state: "visible" });
		await page.evaluate(() => scrollTo(0, 0));
		await card.waitFor({ state: "hidden" });
		// So does scrolling it out of a box that scrolls inside the page.
		const boxed = page.locator("#boxed");
		await boxed.scrollIntoViewIfNeeded();
		await boxed.click();
		await card.waitFor({ state: "visible" });
		await page.evaluate(() => {
			document.querySelector("#box").scrollTop = 2000;
		});
		await card.waitFor({ state: "hidden" });
		await page.close();
	}
} finally {
	await browser.close();
	rmSync(directory, { recursive: true });
}

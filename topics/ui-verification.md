# UI verification

> Verify a UI the way a user meets it — query the accessibility tree for
> structure, render and look across a viewport matrix for appearance and
> space, and exercise realistic event sequences for behavior — because the
> markup and the tree are blind to most visual and interaction defects.

Topic: ui-verification

Subtopic of [`ui-quality`](ui-quality.md). It defines *how to check* that a
UI is correct; [`functional-layout`](functional-layout.md) defines *what
correct means* (the design contract), and [`theming`](theming.md) is held
to the promise that it changes neither. Read this before approving any UI
change.

The one correction this doc exists to install: **an agent must not approve
how a screen looks or behaves from a representation that cannot see looks
or behavior.** The cheap default path can't, so the agent has to leave it
on purpose.

## Two representations ★

A UI can be inspected through two fundamentally different representations,
and the choice silently decides which bugs are *possible to find*.

**1. The accessibility tree (or the DOM it derives from).** A structured
description of *meaning*: each node's `role`, accessible `name`, `state`,
`value`, and the focus order between them. It is what a screen reader
announces, and — importantly — it is what the Playwright "MCP" server (the
dominant way agents drive a browser in 2025–2026) returns *by default*,
because a snapshot is only 2–5 KB of text. A snapshot of a login form looks
roughly like:

```
- textbox "Email"
- textbox "Password"
- button "Sign in" [disabled]
```

That tells you the three controls exist, are named, are in this order, and
that the button is disabled. It says **nothing** about whether the button
is 11 px tall, sits at 2:1 contrast against its background, overlaps the
password field, or shows no change when pressed.

**2. The rendered pixels.** A screenshot, or a pixel-for-pixel diff against
a baseline. It is the *only* representation that contains size, weight,
spacing, color, contrast, overlap, clipping, truncation, z-order, layout
shift, and visual feedback. It is also 10–100× larger (≈0.5–2 MB an image),
slower to capture and reason over, and in the MCP browser it is a
**fallback** mode you must explicitly request "when you need pixel-level
verification."

So the cheap, default, structurally-blind path is the one an agent lands on
unless it chooses otherwise. **That is the whole problem.** An agent that
reasons only over the snapshot will confidently sign off on a screen it has
never *seen*.

The decision rule:

| If the claim is about… | Use… | Example claim |
|---|---|---|
| presence, role, name, state, value, focus/tab order | tree / DOM | "the Submit button exists and is disabled until the form is valid" |
| size, spacing, weight, color, contrast, overlap, clipping, truncation, alignment, layout shift, visual feedback | rendered pixels at a viewport matrix | "the button is legible and doesn't overlap the field at 360 px wide" |

Never approve an appearance or spatial claim from the tree alone. Never try
to assert focus order from a screenshot. Match the representation to the
defect class.

## How an agent actually verifies (the loop) ★

The behavior change this topic demands, concretely:

1. **Run the real thing.** Start the dev server / app; drive an actual
   browser engine (Playwright, or the Playwright MCP browser). Static
   reasoning over source is not verification.
2. **Query the tree for structure.** Cheap, deterministic, restyle-robust
   — do this first for presence/role/name/state and focus order.
3. **Render and *look* for appearance.** Explicitly switch to
   screenshot/vision mode (or capture a screenshot and actually view it).
   Do this **at a viewport matrix**, not one width. The agent-specific
   failure is staying in snapshot mode and never looking; spend the tokens.
4. **Exercise behavior** with realistic event *sequences* (next section's
   matrix), not single synthetic events.
5. **Run the automatable thresholds** (axe-core for contrast/names/roles;
   target-size and measure checks) so the numeric rules don't rely on the
   eye.
6. **Report what you could not check** — taste, motion comfort, anything
   you only saw at one viewport. Honesty about the gap beats a false pass.

A useful default **viewport matrix**: 360×640 (small phone), 414×896
(large phone), 768×1024 (tablet portrait), 1280×800 (laptop), 1920×1080
(desktop). Add the smallest you support (often 320 px) because that is
where text wraps worst and overlap first appears.

## The four verification layers

Cheap to costly. Each layer catches a defect class the one above cannot.

**1. Structure — assert it exists and means what it should.** Query like a
user, by role and accessible name, not by CSS selector or test id (Kent C.
Dodds' Testing Library; the principle: "the more your tests resemble the
way your software is used, the more confidence they give you"). Layer in
axe-core (Deque) for the rule-checkable accessibility violations. *Cost:*
milliseconds. *Blind to:* everything visual.

```js
await expect(page.getByRole('button', { name: 'Sign in' })).toBeDisabled();
const results = await new AxeBuilder({ page }).analyze();
expect(results.violations).toEqual([]);
```

**2. Appearance — render and diff the pixels.** Visual-regression snapshots
compared pixel-for-pixel against an approved baseline, across the viewport
matrix (Playwright `toHaveScreenshot()`; hosted: Chromatic, Percy). Mask
known-dynamic regions (timestamps, avatars) so they don't cause false
diffs. *Cost:* image capture + storage + a human approving baselines.
*Catches:* the entire spacing/weight/contrast/overlap/clipping class — and
nothing else can.

```js
for (const size of [{w:360,h:640},{w:1280,h:800}]) {
  await page.setViewportSize({ width: size.w, height: size.h });
  await expect(page).toHaveScreenshot(`signin-${size.w}.png`,
    { mask: [page.getByTestId('avatar')] });
}
```

A caveat worth internalizing: visual regression proves *"this did not
change from the baseline,"* not *"this is good."* The baseline's
correctness is a one-time human judgment; the test only guards it
afterward. See *What automated checks don't replace*.

**3. Behavior — drive realistic event sequences.** A real interaction is a
*sequence*, and the bugs live in the sequence. A genuine mouse click fires
`pointerover → pointerdown → focus → pointerup → click`; a synthetic
`fireEvent.click()` fires one event and skips hover and focus states.
Prefer Testing Library's `user-event` (orders the events for you) or
Playwright's actionability-checked actions (it waits for the element to be
visible, stable, enabled, and unobscured before acting). *Catches:* hover
states, focus rings, the timed/long-press branch, debounce/validation
races. *Blind to:* nothing it exercises — but it only exercises what you
script, so coverage is the risk.

**4. Responsiveness — measure the timing.** Two Core Web Vitals:
- **INP** (Interaction to Next Paint) — latency from a user interaction to
  the next visual update; "good" ≤ 200 ms. It replaced FID as a Core Web
  Vital on 2024-03-12. INP is primarily a *field* metric (real users, via
  the Event Timing API / the `web-vitals` JS library); the lab proxy in
  Lighthouse is **TBT** (Total Blocking Time), not INP itself — don't claim
  a lab INP number you didn't field-measure.
- **CLS** (Cumulative Layout Shift) — how much visible content shifts
  unexpectedly; measurable in both lab (Layout Instability API, Lighthouse)
  and field. This is the numeric form of "no jitter" from
  [`functional-layout`](functional-layout.md).

## Testable thresholds (the eye is not required)

Several design rules from [`functional-layout`](functional-layout.md) are
*numeric*, which means they belong here as automatable checks, not matters
of taste:

- **Contrast** — WCAG 1.4.3: ≥ 4.5:1 for normal text (AA), ≥ 3:1 for large
  text (≥ 24 px, or ≥ 18.66 px bold), 7:1 (AAA). axe-core checks this
  directly. The catch: it can't judge text over a gradient or image, so
  those still need the eye.
- **Target size** — WCAG 2.5.8 (new in 2.2, AA): interactive targets ≥
  24×24 CSS px, *or* with ≥ 24 px spacing to neighbors; 2.5.5 (AAA) wants ≥
  44×44. Assert via the element's bounding box.
- **Measure** (characters per line) — aim 45–75, ~66 ideal (Bringhurst).
  Assert with care: the CSS `ch` unit is the advance width of "0", so a
  `max-width` in `ch` *over-counts* line length for proportional fonts
  (most glyphs are narrower than "0"). For a true count, measure rendered
  text-block width ÷ mean glyph width, or count characters to the wrap with
  the Range API.
- **Leading** (line-height) — body ≈ 120–145% of font size (Butterick).
  Computed style ÷ font size is directly assertable.
- **Type scale** — assert that rendered font sizes come from the defined
  ramp, not ad-hoc values (catches drift toward many one-off sizes).
- **Focus visible** — WCAG 2.4.7: every keyboard-focusable control shows a
  visible focus indicator. Tab through and assert `:focus-visible` styling
  exists (and, 2.4.11/2.4.13 in 2.2, isn't fully obscured).
- **Reduced motion honored** — emulate `prefers-reduced-motion: reduce` and
  assert large/auto-playing motion is suppressed (WCAG 2.3.3). Playwright:
  `page.emulateMedia({ reducedMotion: 'reduce' })`.

## The interaction matrix

The behaviors the project cares about — and that agents routinely skip
because the snapshot doesn't contain them. Each row is a *sequence*, the
driver call that produces it, and what to observe (in which
representation).

| Interaction | Why it's skipped / what breaks | Driver (Playwright) | Observe |
|---|---|---|---|
| **Hover / mouseover** | snapshot has no hover state; touch devices *have no hover* | `locator.hover()` | pixels: tooltip/highlight appears; tree: any revealed content is reachable without hover too |
| **Click** | synthetic click skips hover→down→focus→up | `locator.click()` (actionability-checked) | pixels: pressed/active feedback; tree: resulting state change |
| **Long-press** | the timed branch never fires on a plain click | `mouse.down()` → `waitForTimeout(500)` → `mouse.up()` | pixels: context menu / long-press affordance; tree: the alternate action |
| **Type fast then Enter** | races debounce, async validation, IME composition — can submit stale/unvalidated | `locator.pressSequentially('text',{delay:10})` then `keyboard.press('Enter')` | did it submit before validation settled? error shown? double-submit? |
| **Drag-resize window** | layout reflow + scroll jump; pure snapshot never resizes | loop `setViewportSize(...)` across the matrix | pixels: no overlap/clipping; focal point stays put (chat→bottom, reading→top); no jitter |
| **Keyboard-only** | mouse-only flows trap keyboard users | `keyboard.press('Tab')` ×N, `Enter`/`Space` | tree: focus order sane; pixels: focus ring visible at each stop |

Driving these **without a human**: Playwright runs the same script headless
(CI) or headed (watch it), so the agent is the driver — there is no "ask the
user to click it." For the spatial rows, capture a screenshot *after* the
sequence and actually view it; the assertion the agent most often omits is
the look, not the click.

The "type fast then Enter" race deserves emphasis: a human types over
hundreds of ms, so a 300 ms debounce usually settles first; a scripted
`fill()` is instant, so it reliably *loses* the race that a human usually
wins — which is exactly why it's the test that finds the submit-before-
validate bug. Use a small inter-key `delay` to model fast-but-real typing,
then press Enter immediately.

## Mobile and TUI

**Mobile** is not just a narrow viewport — it's a different input model.
Put a phone profile in the matrix (`playwright.devices['iPhone 13']` sets
viewport, device-scale, touch, and UA together) and verify: **no hover**
(every hover-revealed affordance must have a tap/visible equivalent),
**larger targets** (the 44×44 AAA size matters more under a thumb), touch
event sequences (`tap`, not `click`), and that nothing requires a precise
mouse.

**Clickable TUI** has the *same* tree-vs-pixels split in a different
medium: the "pixels" are the rendered character grid (what the terminal
actually shows — alignment, truncation at the column width, color-pair
contrast, box-drawing that doesn't line up), and the "tree" is the semantic
widget map the TUI framework exposes. Verify by capturing the rendered grid
(snapshot the screen buffer) and exercising key/click sequences, just as in
the browser — don't infer the layout from the widget declarations.

## What automated checks don't replace

State this honestly rather than overclaiming a green check:

- **Visual regression catches *change*, not *correctness*.** It guards a
  baseline a human judged good once; a baseline that was wrong stays wrong
  and passes forever. Someone has to approve the first screenshot with
  taste.
- **Thresholds catch *violations*, not *quality*.** 4.5:1 contrast and a
  66-char measure can be met by an ugly, confusing screen. The numbers are
  a floor, not a ceiling.
- **Motion comfort is partly subjective.** `prefers-reduced-motion` is
  testable; whether the *default* motion is tasteful or nauseating is a
  judgment.
- **One viewport is not the matrix.** A pass you only saw at 1280 px is an
  untested claim at 360 px — say so.

When the eye is required and the agent has looked, say what it saw. When it
couldn't look, say that too — a stated gap is verification; a silent
assumption is not.

## Sources

- Kent C. Dodds — the Testing Trophy and Testing Library ("query like a
  user"); `@testing-library/user-event` for ordered event sequences.
- Playwright docs — actionability checks, `getByRole`, `toHaveScreenshot()`
  visual comparisons, `emulateMedia`, device descriptors, and the MCP
  server's accessibility-snapshot-by-default / vision-as-fallback model.
- axe-core / Deque — automated WCAG rule checking (contrast, names, roles).
- WCAG 2.2 (W3C) — 1.4.3 contrast, 2.5.8 / 2.5.5 target size, 2.4.7 focus
  visible, 2.4.11 focus not obscured, 2.3.3 animation from interactions.
- web.dev Core Web Vitals — INP (replaced FID 2024-03-12; ≤ 200 ms good;
  field metric, TBT is the lab proxy) and CLS; the `web-vitals` library.
- Hosted visual regression: Chromatic (Storybook), Percy (BrowserStack).
- Bringhurst (measure) and Butterick (leading) for the typographic
  thresholds; full treatment in [`functional-layout`](functional-layout.md).

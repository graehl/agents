# UI quality

> A UI change is good when it is legible, conventional, responsive, and
> stable — and when it is verified the way a user meets it, by rendering
> and exercising it across viewports, rather than inferred from markup;
> cosmetic theming layers on top without altering layout or behavior.

Topic: ui-quality
Governs: starting UI work in a project

This is the entry point for UI work in a project. It frames three concerns
and links to the binding subtopic for each:

- **Design language** — [`functional-layout`](functional-layout.md): how to
  lay out a screen so it is legible, understood, responsive, and stable.
- **Verification** — [`ui-verification`](ui-verification.md) and
  [`ui-testing`](ui-testing.md): how to check that a UI is actually correct,
  since the markup almost never tells you.
- **Theming** — [`theming`](theming.md): how to offer cosmetic variants
  (dark mode, brand skins) without disturbing the first two.

The order is also the workflow: **design it, verify it, then theme it** —
and theming must not break the design or invalidate the verification.

## Why an agent (or anyone) gets UI wrong

The central trap is treating **markup or the accessibility tree as the UI**.
The DOM/a11y tree describes *structure and meaning* (role, name, state), not
*pixel* facts — size, weight, spacing, contrast, overlap, clipping,
truncation, or press feedback. Because browser automation defaults to cheap
a11y-tree snapshots, an agent that reasons only over snapshots will
confidently approve a UI it has never *seen*.

The corrective stance (developed in [`ui-verification`](ui-verification.md)):

- **Query the tree** for structure — presence, role, name, state, value,
  focus order.
- **Render and look** across a *matrix* of viewport sizes for appearance and
  space.
- **Exercise** realistic event sequences (hover, click, long-press,
  type-then-Enter, drag-resize) for state transitions and feedback.

## 1. Design language: functional, not trendy

Full contract in [`functional-layout`](functional-layout.md):

- **Legible** — modular type scale, hierarchy via weight/color rather than
  ad-hoc sizes, consistent body/list scale, sentence-case UI labels,
  `tabular-nums` for aligned numbers, leading ≈ 120–145%, measure ≈ 45–75
  chars (~66 ideal).
- **Understood** — visible signifiers and feedback (Norman), convention over
  novelty (Jakob's Law), visual grouping backed by code structure, and no
  decorative chrome (eyebrows, non-interactive chips/badges, button walls,
  nested card cages, fake telemetry).
- **Responsive** — fluid/intrinsic layout (`Grid`/`Flexbox`, `clamp()`,
  `@container`) before breakpoints; measured allocators for conditional
  toolbars.
- **Stable** — no layout shift (CLS < 0.1), anchored scroll (bottom for
  chat/logs, top for reading) across loads and drag-resizes, brisk explicit
  compositor transitions (never `transition: all`), and
  `prefers-reduced-motion` honored.

**Small-screen and density tradeoff.** Textbook typography numbers
(Bringhurst, Butterick) are a wide-screen *reference*, not a budget to defend
at the cost of fitting the user's screen. On phone viewports and
information-dense panes (logs, tables, TUIs, side rails), tighter leading,
narrower measure, smaller type, and denser spacing are the right choice over
forcing constant scrolling.

**Functional by default, distinctive when distinctiveness is the job.**
The "functional, not trendy" stance is the *default* regime — right for
operator tools, dense data views, logs, docs, config, and anything a
returning user drives daily, where convention is a feature, a bold aesthetic
is friction, and the page opens directly into live content rather than a
hero banner. A second regime exists: **brand surfaces** — marketing pages,
landing pages, portfolios, editorial/launch content — where being memorable
*is* the function and defaulting to convention is the failure. There:

- Commit to one clear aesthetic direction drawn from the subject's real
  materials and audience, and sustain it below the fold rather than dropping
  into generic three-column card rows.
- Avoid generic-AI defaults that signal an unmade choice: system/utility
  fonts (Inter, Roboto, Arial), converged "distinctive" picks (Space
  Grotesk), and cliché palettes — purple gradients on white, dark slate with
  neon purple glow, and warm beige/cream paired with terracotta/rust on
  "craft/warm/food/artisanal" briefs.
- When a page earns a hero, abandon the generic 50/50 split (`H1` + long
  paragraph + 2 buttons + divider + 3–4 stat columns beside a media box): let
  display type or full-bleed imagery command the viewport, pair `<h1>` with
  at most 1–2 short lines (`≤ 25` words) and one primary action, and omit
  bottom KPI/spec strips.
- Match code complexity to the vision — maximalism earns elaborate
  motion/effects; restraint earns precision in spacing and type. Both regimes
  share every §2 verification threshold (contrast, target size, motion,
  stability); distinctiveness never buys an exemption.

## 2. Verification: test what the user meets

Verify across four layers (full method in
[`ui-verification`](ui-verification.md); capture rules in
[`ui-testing`](ui-testing.md)):

1. **Structure** — accessibility tree / DOM queries and axe-core.
2. **Appearance** — rendered captures inspected across a viewport matrix
   (desktop + phone) for spacing, weight, contrast, overlap, and clipping.
3. **Behavior** — realistic event sequences (hover, click, long-press,
   fast-type-then-Enter, drag-resize) on desktop, phone, and TUI where
   applicable.
4. **Responsiveness & stability** — INP ≤ 200 ms, CLS < 0.1, WCAG AA
   contrast ≥ 4.5:1 (1.4.3), target size ≥ 24×24 CSS px (2.5.8).

## 3. Theming: cosmetic layers only

Full contract in [`theming`](theming.md). A **theme** swaps design-token
values (color, typography, elevation) via CSS custom properties *without
changing layout or behavior*:

- **mode** (light/dark, high-contrast, `forced-colors`) and **theme / skin**
  (brand/surface values) must produce zero layout shift and zero behavior
  change.
- **density** (compact vs. comfortable spacing) changes geometry, so it is
  *not* a pure skin and must be verified as a layout change.

## How the three fit

Design sets the contract, verification proves a change meets it across
appearance/behavior/viewport, and theming touches neither. For periodic
screenshot-backed audits of an existing UI — scored first against the
project's own prevailing style and second against these principles — see
[`ui-report`](ui-report.md).

## Web platform implementation references

How to build specific browser behavior (accessible controls, overlays, key
handlers, HTML insertion, security headers, main-thread work) lives in
[`web-platform-guidance`](web-platform-guidance.md), which has its own
activity route.

## Further reading

Subtopic docs carry full reference citations. For human-facing primers:
Erik Kennedy, [*7 Rules for Creating Gorgeous UI*](https://www.learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-1.html);
Matthew Butterick, [*Practical Typography*](https://practicaltypography.com/typography-in-ten-minutes.html);
web.dev, [*Learn Responsive Design*](https://web.dev/learn/design) and
[*Learn Accessibility*](https://web.dev/learn/accessibility).

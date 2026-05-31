# UI quality

> A UI change is good when it is legible, conventional, responsive, and
> stable — and when it is verified the way a user meets it, by rendering
> and exercising it across viewports, rather than inferred from markup;
> cosmetic theming layers on top without altering layout or behavior.

Topic: ui-quality

This is the tutorial entry point for UI work in the project, written for a
reader who is comfortable with code but a relative novice at layout, type,
and visual design. It lays out three concerns at a basic level and links to
a deeper doc for each:

- **Design language** — [`functional-layout`](functional-layout.md): how to
  lay out a screen so it is legible, understood, responsive, and stable.
- **Verification** — [`ui-verification`](ui-verification.md): how to check
  that a UI is actually correct, since the markup almost never tells you.
- **Theming** — [`theming`](theming.md): how to offer cosmetic variants
  (dark mode, brand skins) without disturbing the first two.

The order is also the workflow: **design it, verify it, then theme it** —
and theming must not break the design or invalidate the verification.

## Why an agent (or anyone) gets UI wrong

The central trap is treating the **markup as the UI**. The HTML/DOM, or the
accessibility tree built from it, describes *structure and meaning*: a
button named "Send" exists, is enabled, and comes after the text field. It
says nothing about whether that button is 12 px tall and unreadable,
overlaps the field, sits at 2:1 contrast, jumps three lines down when the
window narrows, or gives no visible feedback when pressed. Those are
*pixel* facts, and they are exactly the facts that make a UI feel broken.

This split is not academic. The dominant way agents drive a browser in
2025–2026 (the Playwright "MCP" server) defaults to an **accessibility-tree
snapshot** — a few kilobytes of structured `role / name / state` data —
because a screenshot is 10–100× larger and slower to process, and vision is
only a fallback "when you need pixel-level verification." So the cheap,
default path is structurally blind to most visual defects. An agent that
reasons only over that path will confidently approve a UI it has never
*seen*.

The corrective stance, developed in [`ui-verification`](ui-verification.md):

- **Query the tree** for structure — presence, role, name, state, value,
  focus order. Cheap, deterministic, robust to restyling.
- **Render and look** for appearance and space — at a *matrix* of viewport
  sizes — for size, weight, spacing, contrast, overlap, clipping,
  truncation, and centering. These do not exist in the tree.
- **Exercise** behavior with realistic event sequences — hover, click,
  long-press, type-then-Enter, drag-resize — because state transitions and
  their feedback are invisible to a static snapshot.

A reader who internalizes only one thing should internalize this: *the
representation you test against decides which bugs you can possibly find.*

## 1. Design language: functional, not trendy

The goal is a layout that is **legible** (easy to read), **understood**
(works the way users already expect), **responsive** (adapts to the
viewport), and **stable** (does not jump around). None of that requires
fashion; it requires a small number of durable principles. Full treatment
in [`functional-layout`](functional-layout.md); the basics:

**Legible — typography.** Four levers decide whether body text reads well
(Butterick): point size (≈15–25 px on the web), line spacing / *leading*
(≈120–145% of size), line length / *measure*, and the typeface itself. The
single most cited number is the **measure**: 45–75 characters per line,
~66 ideal for a single column (Bringhurst). Too long and the eye loses the
next line's start; too short and rhythm breaks. Establish a **type scale**
(a small ramp of sizes) and a clear weight hierarchy rather than many
ad-hoc sizes.

**Understood — convention and signifiers.** Don Norman's distinction is the
core idea: an *affordance* is what an element can do; a *signifier* is the
visible cue that tells the user it can (the button looks pressable, the
link looks clickable). Most "intuitive" design is just **convention** —
Jakob's Law: users spend nearly all their time on *other* sites, so they
expect yours to work like those. Steve Krug's "Don't Make Me Think" and
Dieter Rams' "as little design as possible" point the same way: remove the
need for thought rather than decorating it.

**Responsive — adapt to the viewport.** Prefer fluid, intrinsic layout (CSS
Grid/Flexbox, `clamp()` for fluid type, container queries) over a few
hard-coded breakpoints. The layout should degrade gracefully from a wide
desktop to a narrow phone without horizontal scrolling or clipping.

**Stable — no jitter.** Two named failure modes: content that *shifts* as
images/fonts/async data load (measured by **CLS**, Cumulative Layout Shift,
a Core Web Vital), and scroll position that *jumps* when content is
inserted above the viewport or when the window is drag-resized. The browser
primitive for the second is **scroll anchoring** (`overflow-anchor`). Two
common anchoring intents:

- **Bottom-anchored** (chat, logs): new content appends at the bottom and
  the view stays pinned there *unless the user has scrolled up*.
- **Top-anchored** (articles, long scroll): the user's current reading
  position is preserved; content loading above must not push it down.

Motion, when used, should preserve the user's focal point (the FLIP
technique animates from first to last position smoothly) and must honor
`prefers-reduced-motion` — large motion triggers vestibular symptoms in a
substantial population (WCAG 2.3.3).

## 2. Verification: test what the user meets

A UI is verified across four layers, cheap to costly. Full treatment in
[`ui-verification`](ui-verification.md):

1. **Structure** — assert presence/role/name/state via the accessibility
   tree or DOM queries (Testing Library's "query like a user"; axe-core for
   accessibility rules). Cheap, robust to restyling.
2. **Appearance** — visual-regression snapshots compared pixel-for-pixel
   across a **viewport matrix** (Playwright `toHaveScreenshot`, Chromatic,
   Percy). This is the only layer that catches spacing, weight, contrast,
   overlap, and clipping.
3. **Behavior** — drive realistic event *sequences* (Playwright; Testing
   Library `user-event`), not single synthetic events: a real click fires
   hover→down→up; a real "type fast then Enter" can submit before async
   validation or debounce settles.
4. **Responsiveness** — measure interaction latency: **INP** (Interaction
   to Next Paint, the Core Web Vital that replaced FID in March 2024;
   "good" ≤ 200 ms) and CLS for stability.

Several design properties from §1 are **directly testable thresholds**,
which is why typography belongs in the verification story too:

- **Contrast ratio** — WCAG 1.4.3 requires ≥ 4.5:1 for normal text (AA),
  7:1 (AAA). Automatable.
- **Target size** — WCAG 2.5.8 (new in 2.2, AA) requires ≥ 24×24 CSS px (or
  24 px spacing); 2.5.5 (AAA) wants 44×44. Automatable.
- **Measure** — characters-per-line can be asserted, with care (the CSS
  `ch` unit measures the width of "0", so it over-counts for proportional
  fonts).

The **interaction matrix** the project cares about — and that agents
routinely skip — includes: mouseover/hover (and its absence on touch),
click, long-press duration (~500 ms), typing quickly then Enter,
drag-resizing the window, and the same flows on a phone-sized viewport and,
where relevant, in a clickable TUI.

## 3. Theming: cosmetic layers only

A **theme** is a coherent set of presentation values (color, typography,
elevation) that can be swapped *without changing layout or behavior*. The
modern mechanism is **design tokens** — named design decisions stored as
data (the W3C Design Tokens Format Module reached its first stable version
in October 2025) and consumed as CSS custom properties. Full treatment in
[`theming`](theming.md). The vocabulary worth fixing now:

- **mode** — a paired environmental variant: light/dark, high-contrast.
- **theme / skin** — a brand or cosmetic value set; "skin" connotes the
  purely surface end (color, texture) with no structural effect.
- **density** — compact vs. comfortable spacing. This is the **boundary
  case**: density *does* change spacing and therefore layout, so it is
  *not* a pure skin and must be verified like a layout change, not waved
  through as cosmetic.

The contract: theming changes tokens, never structure or logic. A theme
swap should produce *zero* layout-shift and *zero* behavior change — which
makes "does the dark theme alter any geometry?" a verifiable claim, not a
matter of taste.

## How the three fit

Design sets the contract (what *good* means here), verification proves a
given change meets it across appearance/behavior/viewport, and theming is
held to the promise that it touches neither. A change that improves one
while silently breaking another (a prettier theme that shifts layout; a
"responsive" tweak that drops the measure to 30 characters on mobile) has
not improved UI quality.

## Learn more — beginner tutorials

Exceptional, mostly-free, novice-friendly material, gentlest first. These
teach the *why*; the Sources below are the reference specs.

**Start here (for non-designers).**
- Erik Kennedy, [*7 Rules for Creating Gorgeous UI*](https://www.learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-1.html)
  — a "non-artsy primer" by someone who learned UI design *as* a developer;
  pure application, no color-theory detours. The best single starting read.
- Robin Williams, *The Non-Designer's Design Book* — the classic intro for
  "the visual novice"; four principles (CRAP: Contrast, Repetition,
  Alignment, Proximity), readable in an afternoon
  ([borrow on Internet Archive](https://archive.org/details/nondesignersdesi00will)).

**Design language & layout (→ functional-layout).**
- web.dev, [*Learn Responsive Design*](https://web.dev/learn/design) — free
  structured course: layout, media queries, responsive type, even dark
  mode; aimed at beginners with basic HTML/CSS.
- Josh W. Comeau, interactive guides to
  [Flexbox](https://www.joshwcomeau.com/css/interactive-guide-to-flexbox/)
  and [CSS Grid](https://www.joshwcomeau.com/css/interactive-guide-to-grid/)
  — the friendliest, most visual explanations of the two core layout
  engines.
- CSS-Tricks, [*A Complete Guide to Grid*](https://css-tricks.com/snippets/css/complete-guide-grid/)
  — the canonical cheat-sheet to keep open while working.

**Typography (→ functional-layout).**
- Matthew Butterick, [*Practical Typography*](https://practicaltypography.com/typography-in-ten-minutes.html)
  — a free online book; the ["typography in ten minutes"](https://practicaltypography.com/typography-in-ten-minutes.html)
  and [summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
  pages are the fastest competent on-ramp anywhere.
- Richard Rutter, [*The Elements of Typographic Style Applied to the Web*](https://webtypography.net/)
  — free, CC-licensed; walks Bringhurst's textbook principles into concrete
  HTML/CSS.

**Verification, accessibility & motion (→ ui-verification, functional-layout).**
- web.dev, [*Learn Accessibility*](https://web.dev/learn/accessibility) and
  MDN's [Accessibility learning path](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility)
  — evergreen courses; accessibility is where many testable thresholds live.
- Smashing Magazine, [*Designing With Reduced Motion For Motion Sensitivities*](https://www.smashingmagazine.com/2020/09/design-reduced-motion-sensitivities/)
  — the practical guide to the vestibular / `prefers-reduced-motion` topic.

## Sources

Distillers and primary references these docs lean on. The subtopic docs
carry the specific citations.

- Typography: Robert Bringhurst, *The Elements of Typographic Style*;
  Matthew Butterick, *Practical Typography* (practicaltypography.com).
- Visual design: Adam Wathan & Steve Schoger, *Refactoring UI*; Dieter
  Rams, Ten Principles of Good Design; Josef Müller-Brockmann, *Grid
  Systems in Graphic Design*.
- Usability: Don Norman, *The Design of Everyday Things* (affordance vs.
  signifier); Jakob Nielsen / Nielsen Norman Group (10 heuristics, Jakob's
  Law, response-time limits); Steve Krug, *Don't Make Me Think*.
- Web platform: web.dev Core Web Vitals (LCP/INP/CLS); MDN scroll anchoring
  (`overflow-anchor`); CSS `prefers-reduced-motion`; Paul Lewis, the FLIP
  technique.
- Verification: Kent C. Dodds, the Testing Trophy & Testing Library;
  Playwright (incl. the MCP accessibility-tree model); axe-core / Deque;
  WCAG 2.2 (W3C).
- Theming: W3C Design Tokens Format Module; Brad Frost, *Atomic Design*;
  Nathan Curtis (EightShapes) on tokens.

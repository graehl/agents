# UI report

> A reproducible, screenshot-backed markdown report on a project's UI —
> every major view at a nominal desktop viewport beside a narrow
> reference that covers users who size fonts up or zoom their browser,
> plus a single-view theme gallery — that serves two readers: new
> users and UI developers learning what the screens are and what you
> can do with them, and maintainers wanting a critique evaluated first
> against the project's own prevailing style and second against the
> principles in `ui-quality` / `functional-layout` / `ui-verification`
> / `theming`. Inline improvement suggestions and designer-rationale
> notes are welcomed but visibly bracketed from the observations. The
> evaluation runs at the top as a conclusion-as-lead.

Topic: ui-report

Subtopic of [`ui-quality`](ui-quality.md). This doc is a checklist for
*producing* a report; the *criteria* the report cites live in the four
sibling docs and in `GLOSSARY.md`.

## Audience and purpose

The report serves two readers at once and is written with both in mind:

- **New users and UI developers — orientation.** Each view's prose
  starts with what the screen is for, what affordances are visible,
  and what a user can do with each one — so someone meeting the app
  for the first time, or a developer joining the codebase, can use
  the report as a guided tour.
- **Maintainers and designers — critique.** The same per-view prose
  then names where the view follows or deviates from the prevailing
  style, with optional designer-rationale notes and improvement
  suggestions, both visibly bracketed (see *Suggestions and designer
  notes*) so a reader can separate what *is* from what is *proposed*.

The Evaluation section at the top is the maintainer's executive
summary; the view gallery is the user's tour. The same artifact is
re-read for different reasons by different people; nothing about the
critique role displaces the onboarding role, and vice versa.

## When to produce one

- Before a release, design review, or theme/density change.
- After a UI refactor or framework swap, as a before/after pair.
- On entering an unfamiliar project's UI area, as orientation.
- When the agent is asked "is this UI good?" — answering needs a
  rendered tour, not an opinion from the accessibility tree.

The most useful single output is the **inconsistency list**: places
where the same affordance is shown two ways, the spacing scale is
violated, or the type scale is broken. These are concrete and cheap to
fix; absolute-principle critique ("contrast could be higher") is often
not.

## Output layout

Write everything under the report directory (default `ui-report/`,
override on request). Self-contained, committable, browsable as
rendered markdown:

```
ui-report/
  README.md                  # the report itself; evaluation at top
  views/
    01-dashboard.nominal.png
    01-dashboard.narrow.png
    02-editor.nominal.png
    02-editor.narrow.png
    02-editor.contrast.png   # the one informative theme contrast
    ...
  themes/
    main.<themeA>.png
    main.<themeB>.png
    main.<themeC>.png
  data/                      # optional: fixture seeds used for shots
```

Filename grammar: `NN-slug.variant.png`. Number prefixes preserve order
when the directory is browsed without the README. Slug matches the
heading in the report.

## Report structure

`README.md` is the only narrative file. Sections in this order:

1. **Evaluation** (conclusion-as-lead — the most-read section).
   Three short subsections, each a bullet list, each bullet one
   sentence and one in-document anchor to the gallery row that
   demonstrates it:
   - **Strengths** — what the UI does consistently and well, in the
     project's own vocabulary.
   - **Weaknesses** — failures against testable thresholds (contrast,
     target size, jitter, focus, motion); cite WCAG numbers from
     `ui-verification` when applicable.
   - **Inconsistencies** — same affordance shown two ways; spacing or
     type scale violated; color tokens bypassed; density mixed within
     one screen. *Most actionable category — lead with it if it's the
     fattest.*

   Optionally a fourth subsection, **Deliberate tradeoffs**, naming
   places the UI knowingly compromises textbook typography for
   small-screen efficiency or information density (per the tradeoff
   note in `ui-quality` §1). Calling these out separately avoids
   filing them as weaknesses.

2. **View gallery** — one entry per major view (see Coverage). Each
   entry:
   - H2 heading: `## NN. <view name>`.
   - A two-column markdown table: **nominal** (≈900×600) | **narrow**
     (≈300×700). Where feasible, each image is wrapped in a link to
     the live view URL it was captured from — see *Clickable images*
     below.
   - Orientation prose, in this order:
     - **What this view is for** — one sentence, the user's goal.
     - **Affordances and actions** — a short list of visible controls
       and what each one does. This is the onboarding payload;
       prefer the project's `GLOSSARY.md` vocabulary over paraphrase.
     - **Style and consistency** — where the view follows or breaks
       the prevailing project style, with `ui-quality`-cluster
       principles cited only where relevant.
     - Optional **Designer notes** and **Suggestions** — both
       visibly bracketed; see *Suggestions and designer notes*.
   - **One** view in the gallery additionally gets a *contrasting
     theme shot* in a third column or below the table — picked for
     where the theme change is genuinely informative (e.g. a view
     that exposes a poorly-tokenized color, or where the dark mode
     reveals a contrast cliff). Not every view; one is the budget.

3. **Theme gallery** — a single section, one view (the
   majority-of-time view: dashboard / main editor / whatever the user
   stares at most), rendered in every theme the project ships. One
   row per theme; no per-theme commentary unless something breaks.

4. **Reproduce** — last section, short. The exact command(s) used to
   regenerate the report, the dataset/login used, the viewport
   numbers, browser version, and any non-default settings. So the
   next agent or maintainer can re-run and diff.

## Suggestions and designer notes — visibly bracketed

Improvement suggestions and designer-rationale notes are part of the
report payload, but they must be typographically distinguished from
observations so the reader knows what *is* vs. what is *proposed*.
Use these forms, both labeled blockquotes with italicized body:

```markdown
> **Suggestion** — *Increase the Save button target to ≥24×24
> (WCAG 2.5.8 AA); currently ≈18×18.*

> **Designer note** — *Headings on the editorial surface use a serif
> deliberately; this is the only place serif appears in the app.*
```

The italicized body inside the labeled blockquote is the minimum
typographic distinction; when rendering on GitHub, `> [!TIP]` /
`> [!NOTE]` alert syntax adds color and an icon. A project shipping
its own markdown style sheet may render `blockquote strong` in a
contrasting font face (serif against sans, or a tinted weight) or
add a left-border accent — the source-form convention is the
labeled blockquote; the visual style is the renderer's call.

Observations without a suggestion are fine — *most* don't need one,
especially when no concrete improvement is obvious. Suggestions
that don't tie to a concrete observation in the same view are scope
creep and don't belong; put them in the Evaluation section if they
are project-wide.

## Clickable images — link back to the live view

Where feasible, every screenshot in the gallery is wrapped in a link
to the live view URL it was captured from, so a reader can jump from
a frame to the running view:

```markdown
[![dashboard, nominal](views/01-dashboard.nominal.png)](https://app.example.com/dashboard?session=abc123)
```

The URL points to the deep-linkable route plus whatever
session/document parameters reproduce the captured state — same
fixture, same login, ideally same point-in-time. When a view is
gated by session state that is not deep-linkable, leave the image
unlinked and note "session-only" in the prose, rather than ship a
link that 404s or shows an unrelated view to anyone but the
original capturing agent.

Record the live URL alongside each shot at capture time (e.g.
`views/01-dashboard.nominal.url.txt`, or a single `manifest.json`
mapping image → URL) so the README's links can be regenerated
mechanically rather than transcribed.

## Capture procedure

- **Tool**: Playwright (or the Playwright MCP server). Headed
  rendering, not the default a11y-tree snapshot — this report exists
  precisely because the tree is blind to the relevant defect class
  (see `ui-verification` §2).
- **Viewports**:
  - Nominal **900×600** — a representative desktop content-pane area;
    not a full-screen browser, the layout most users actually meet.
  - Narrow reference **300×700** — *not* a phone-fidelity baseline.
    It approximates the *effective* CSS viewport once a user with
    great-resolution hardware has bumped browser zoom or OS font
    scaling for comfortable reading (e.g. an iPhone-class 393-CSS-px
    width at 1.3× browser zoom ≈ 302 effective px; a 1366-CSS-px
    laptop at 175% zoom ≈ 780 px ≈ a narrow desktop column). The
    case to cover: users who keep good hardware but size fonts up so
    they don't need reading glasses, plus the actual narrow-column
    population on real phones — the layout has to survive a smaller
    *effective* viewport than the device's raw CSS-pixel count
    suggests. Catches cramping, wrapping, clipping, and horizontal
    scroll for the population that needs them most. For
    phone-fidelity screenshots at native zoom, add 393×852 (or
    similar) as a separate variant.
- **Device pixel ratio**: 1, unless the project specifically targets
  HiDPI rendering — keeps committed PNGs small and diffs meaningful.
- **Settle before shot**: wait for `networkidle` *plus* explicit waits
  for web-font load, image decode, and any shimmer/skeleton swap.
  Animations should reach steady state or be paused — a frame mid-
  transition is a bad reference image.
- **Determinism**: same login, same dataset (a fixture under `data/`
  if seeding is needed), same locale, same time/clock (freeze if
  shown), same theme defaults. Deterministic data is worth more than
  fresh data.
- **No agent chrome**: hide devtools, hide test runner overlays, hide
  any "you are in test mode" banner the app shows.
- **No PII**: scrub or use fixture identities before any shot.
- **Record the live URL per shot**: the deep-linkable URL of the view
  (route + session/doc parameters reproducing the captured state)
  goes into a manifest the README consumes, so the gallery's
  image-links can be regenerated rather than transcribed. See
  *Clickable images*.

## Coverage checklist

- [ ] Every top-level navigation destination has one nominal+narrow
      pair.
- [ ] Every major work operation reaches a representative state in
      one of the shots (not just the initial/empty view).
- [ ] Every config tab has one shot, with at least one non-default
      field changed somewhere across the set, so configured-state is
      visible alongside default-state.
- [ ] Empty / error / loading variants captured for at least one view
      each, not exhaustively.
- [ ] One view carries the contrasting theme shot.
- [ ] Theme gallery: the majority-of-time view × every theme shipped.
- [ ] One reduced-motion shot if the app uses motion anywhere — proves
      the toggle is honored (`prefers-reduced-motion`, WCAG 2.3.3).

## Evaluation against the project's own baseline

The primary lens is *internal* consistency. Before listing weaknesses
against absolute thresholds, do a baseline pass:

1. From the gallery, infer the project's de facto style: dominant
   spacing rhythm, type ramp, color tokens in use, button/affordance
   patterns, empty-state convention.
2. Then walk the gallery looking for views that *break* that
   inferred style. Each break is an inconsistency item.
3. Only after that, run the absolute-threshold checks (contrast,
   target size, focus visibility, INP/CLS if measurable) and file
   those as weaknesses.

This ordering matters: a project's own conventions are the cheapest
fix and the most useful feedback. Absolute critiques are noise if
they're applied to the whole codebase uniformly.

## What this report is *not*

- Not an automated a11y audit — run axe-core separately and link its
  output if you want one (see `ui-verification` §4).
- Not a performance audit — INP/CLS belong here only as observed
  defects on real flows, not as a Lighthouse score dump.
- Not a redesign proposal or mockup deliverable. Inline suggestions
  are welcomed (see *Suggestions and designer notes*) but sit
  alongside observations, not as a parallel "proposed redesign"
  track. Full mockups, before/after comps, or a comprehensive
  rework belong in a different artifact.
- Not a substitute for the verification tests in `ui-verification` —
  a report is a snapshot for humans; tests catch regressions.

## Related

- [`ui-quality`](ui-quality.md) — the parent topic and tutorial portal.
- [`functional-layout`](functional-layout.md) — design contract the
  evaluation cites.
- [`ui-verification`](ui-verification.md) — capture/exercise machinery
  and the testable thresholds.
- [`theming`](theming.md) — what the theme gallery is meant to prove
  (presentation-only contract).
- `GLOSSARY.md` — preferred vocabulary for the prose.

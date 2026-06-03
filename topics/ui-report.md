# UI report

> A reproducible, screenshot-backed markdown report on a project's UI —
> every major view at a nominal desktop viewport beside a narrow
> reference that covers users who size fonts up or zoom their browser,
> plus a single-view theme gallery — that serves two readers: new
> users and UI developers learning what the screens are and what you
> can do with them, and maintainers wanting a critique — plus a
> first-steps improvement direction — evaluated first against the
> project's own prevailing style and second against the principles in
> `ui-quality` / `functional-layout` / `ui-verification` / `theming`.
> Inline improvement suggestions and designer-rationale notes are
> welcomed but visibly bracketed from the observations. The evaluation
> runs at the top as a conclusion-as-lead, opening with a one-paragraph
> direction thesis (preserve / improve), not a detailed mockup.

Topic: ui-report

Subtopic of [`ui-quality`](ui-quality.md). This doc is a checklist for
*producing* a report; the *criteria* the report cites live in the four
sibling docs and in `GLOSSARY.md`.

## How to request one

The glossary term *is* the trigger — ask for a **UI report** (or a
"screenshot audit"); naming this doc is never required. Natural
forms: *"produce a UI report for the app"*, *"ui-report on ./web"*,
*"do a screenshot-backed UI audit before the release."* Optionally
name the output directory (*"…into docs/ui-2026-06/"*); whatever the
directory, the report file inside it is always `README.md` (see
*Output layout*), so the directory renders as a browsable report on
GitHub without naming a file.

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
override on request). Whatever directory is chosen, the narrative
file inside it is always `README.md` — the directory is the unit you
name, the report file within it is fixed. Self-contained,
committable, browsable as rendered markdown:

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
   Open with a **direction thesis**: one short paragraph naming what
   the UI fundamentally *is*, the single coherent direction it should
   move in, and the spirit to keep while moving (e.g. "a conservative
   consolidation: keep the dense operator-first workbench, make the
   recurring control patterns uniform, surface high-value actions
   without adding chrome"). Asking for a report is often a tacit
   admission that the UI grew screen-by-screen and was never designed
   as a whole — so synthesizing one direction across the gallery is a
   large part of the report's value, not an aside. This is *first-steps
   proposing* — improvement directions, not a detailed mockup (those
   are a separate later artifact; see *What this report is not*).

   Then the subsections, each a bullet list, each bullet one sentence
   with an in-document anchor to the gallery row that demonstrates it:
   - **Preserve** (a.k.a. Strengths) — what the UI does consistently
     and well, in the project's own vocabulary, framed as a *guardrail*:
     things a change must not break.
   - **Improve** — the proposing half, grouped by **lens** so the
     directions are legible rather than a flat wishlist:
     - *Consistency* — same affordance shown two ways; spacing or type
       scale violated; color tokens bypassed; density mixed within one
       screen. **Usually the fattest and most actionable lens — lead
       with it if so**; it is the cheapest fix and the most useful
       feedback.
     - *Power-user convenience* — friction in the high-frequency flows
       a returning operator runs many times a day; reachability of
       dense controls across widths.
     - *Discoverability / aesthetics* — actions that don't advertise
       themselves (icon-only rows, sparse surfaces), plus restraint of
       one-off page dialects. Aesthetic notes ride here, not as a
       separate beauty contest. Include a routine **distinctiveness
       read** on every report: how far the UI sits from a memorable,
       intentional aesthetic, and the cheapest one or two steps that
       would move it along (a real display face instead of a system
       font, a committed accent instead of a timid even palette, one
       well-orchestrated load reveal). Calibrate the ambition by regime
       (see the functional ↔ distinctive split in `ui-quality` §1): on a
       **brand surface** (landing, marketing, launch) push for a bold
       direction and flag generic-AI defaults that signal an unmade
       choice — system/utility fonts (Inter, Roboto, Arial), cliché
       palettes (purple-on-white gradients), converged "distinctive"
       picks (Space Grotesk); on an **operator/data surface** keep the
       suggestions small and subordinate to convention — note the
       distance and the cheap wins, but say plainly that bold restyling
       is not the goal there. Either way this is observation plus a
       bracketed suggestion, never a mandate to redesign.
   - **Weaknesses** — failures against testable thresholds (contrast,
     target size, jitter, focus, motion); cite WCAG numbers from
     `ui-verification` when applicable. These are defects to fix, kept
     distinct from the *Improve* directions above.

   Optionally a further subsection, **Deliberate tradeoffs**, naming
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

## Keeping a report current

A report is a snapshot, but a *living* one once committed. When a UI
change lands and a `ui-report/` already exists, re-capture the
affected views rather than letting the gallery go stale: re-shoot the
nominal/narrow frames (and the theme frame, if that view carries one)
for each changed screen, refresh that entry's orientation prose and
any inconsistency items it touched, and re-run the manifest so the
live-URL links stay valid. Untouched views keep their existing
shots — the point is a cheap, targeted refresh of the changed
session/screen captures, not a full re-capture every commit. If a
`MANUAL.md` (below) exists, check whether the change altered an
operation or an illustrated affordance and update that too.

## Companion: MANUAL.md (optional operations manual)

The manual is a **byproduct of the report**: by default it is the
report's onboarding payload — *what each view is for* and *what you
can do with it* — with the designer/critique commentary removed, and
nothing more. It is produced **after** the report has been read,
reacted to, and brought up to date, as a *separate, optional product*,
never instead of it. Some restructuring and editing *for the manual's
purpose* is permitted on top of that default:

- **Audience: users and operators only.** It carries the orientation
  half of the report and drops the critique half entirely — no
  direction thesis, no Preserve / Improve / Weaknesses sections, no
  `> **Suggestion**` or `> **Designer note**` blockquotes. That
  stripping is the floor; a
  manual that editorializes about the UI's quality has drifted back
  into being a report.
- **May reorganize by operation rather than by view.** The default
  inherits the report's per-view order; where it reads better, regroup
  the prose under the important things a user *does* ("Create a
  project", "Import a dataset", "Switch theme"), each a short procedure
  in `GLOSSARY.md` vocabulary. A view may then appear under several
  operations and an operation span several views. Reorganizing is an
  allowed enhancement, not a requirement — the critique-stripped
  view-ordered form is a valid manual on its own.
- **Options footnoted locally.** Each operation states the common path
  in the body; less-common flags, toggles, and edge-case options go in
  footnotes attached *to that operation*, so the main flow stays short
  while the full surface stays documented. Keep the footnotes with the
  operation, not collected in a global appendix.
- **Affordance-focused illustration.** Where an operation hinges on a
  specific control, include a screenshot framed on *that affordance* —
  a cropped (and, if helpful, annotated) shot of the relevant button,
  menu, or field — not the full-view frames the report's gallery uses.
  Reuse a report capture when it already shows the control clearly;
  add a tighter, operation-specific shot when it does not.

`MANUAL.md` and its referenced images are intended to be
**committed** (the report itself a project may or may not keep under
version control). Put it where the project keeps user docs — repo-root
`MANUAL.md` or `docs/MANUAL.md` — with its attachments in a sibling
`manual-assets/`, or reused from `ui-report/views/`. It is not
generated mechanically from the report; producing it is a deliberate
follow-up step.

## What this report is *not*

- Not an automated a11y audit — run axe-core separately and link its
  output if you want one (see `ui-verification` §4).
- Not a performance audit — INP/CLS belong here only as observed
  defects on real flows, not as a Lighthouse score dump.
- Not a *detailed* redesign or mockup deliverable. Proposing
  improvement *directions* is in scope and wanted — that is exactly
  the Evaluation's direction thesis and *Improve* lenses (first-steps
  proposing). What sits out of scope is the heavyweight form: full
  mockups, before/after comps, pixel specs, or a comprehensive rework
  presented as a parallel "proposed redesign" track. Those belong in a
  separate artifact (to be defined later); the report names where and
  why to move, not the finished destination.
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

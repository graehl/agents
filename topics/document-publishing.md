# Document publishing

> Build a finished reader document — a memo, report, or note with sections —
> into one styled, self-contained HTML page and a matching print PDF, on
> request, with `qmd-html` and a document style the source names.

Topic: `document-publishing`

Plain Markdown is the default deliverable for a new document. Create a
styled render or bundle supporting documents only when the author asks for
a shareable HTML or PDF ("make this a nice HTML memo", "render it",
"send-ready PDF"). A request to write or revise prose does not imply one;
[`writing`](writing.md) governs that work. Once a document has a recorded
build, rebuild it after editing its sources.

## Build

```bash
qmd-html <doc>.md --print-pdf --text                    # one file
qmd-html --config <doc>.qmd-html.json --text            # recorded build
```

`qmd-html` and its config keys are specified in
[`document-writing-browser-interactive` § Scripted HTML build](document-writing-browser-interactive.md#scripted-html-build).
A recorded build keeps `"print-pdf": true` in a config beside the root; the
HTML, PDF, `.receipt.json`, `.html.map` and `.render.log` land beside the
root unless `output` says otherwise.

### Front matter

The root's YAML front matter carries the document's publishing facts, so a
shared repository needs no path to this toolchain:

```yaml
---
document-style: memo        # style name, found on the style search path
date: 2026-10-01            # creation date, shown under the title
revision: 2                 # absent for the original version
revision-date: 2026-10-03
---
```

`--style` and config `style` override `document-style`. Styles are found by
name in the directories of `QMD_STYLE_PATH` (`:`-separated), then
`~/.config/qmd-html/styles`, then the built-in `qmd_build/styles`; a style is
a `<name>/style.json` with its CSS and filters (keys in `qmd_build/styles.py`).

### Revisions

`qmd-html --bump-revision` sets `revision` one higher (the first bump makes
it 2) and `revision-date` to today before building; an ordinary build never
changes them. The memo style shows "rev N · date" in light grey at the top
right. Bump once per round of significant new work, at the build whose HTML
path you report back to the author, and name the revision in that report.
Successive edits and rebuilds inside one revision session do not bump.

### What to commit

In a shared repository that has not vendored this build toolchain, other
users cannot regenerate the outputs, so commit the HTML and the figure
files it is built from, plus the receipt and source map, but not the PDF:
ignore generated PDFs beside the root. The HTML's PDF link then works for
whoever builds locally. A repository that vendors the toolchain, or a
private one, follows its own convention.

## Source shapes

- **Title.** Without a `title` in the root's front matter, a level-1 heading
  that opens the document becomes its title: Quarto's title block shows it
  with the creation date, and the outline starts at the `##` sections.
- **One document.** A single `.md` or `.qmd` renders directly; includes are
  optional.
- **Sections or bundled documents.** A root `.qmd` includes fragments in
  reading order ([`document-writing` § Assemble very long documents](document-writing.md#assemble-very-long-documents-from-ordered-fragments)).
  To ship supporting documents with a memo, include each whole document
  inside `::: {.appendix-doc}`: its headings drop one level, it starts a new
  printed page, and topic-doc metadata lines (`Topic:`, `Glossary:`,
  `Governs:`) are omitted as working metadata. Included fragments must sit
  under the root's directory and have distinct file names.
- **Links between included documents** resolve inside the page: a link whose
  file name matches an included fragment becomes `#fragment-anchor`, or the
  fragment's first heading when it has no anchor. Links to anything not
  included stay ordinary relative links, which break once the HTML is shared
  alone; include the target or link a published URL.

## The `memo` style

Layered over Quarto's default HTML theme, so the right-hand outline follows
heading levels whether or not the root uses includes.

- Source Sans 3 from the host's TeX Live OpenType tree, embedded in the HTML.
- A quiet top-right corner: the revision, and with a printed PDF a relative
  "PDF" link to the sibling file.
- Tables: short hyphenated tokens such as `CC-BY-NC-SA` never wrap mid-name
  (non-breaking hyphens inside table cells). Column widths are chosen at
  build time per band of content-column width (from 420, 600 and 760 CSS
  px; print falls in the 600 band): a headless browser estimates wrapped
  heights from the page's font metrics, refines with a few real-layout
  steps, and keeps a choice only where it renders shorter than the
  browser's automatic layout. Narrower than 420 px, tables use automatic
  layout and scroll inside their own box.
- Print: US Letter, 0.7 in by 0.75 in margins; the outline and corner are
  hidden, table rows do not split, and table headers repeat on each page.

Width choice is HTML-only. A LaTeX/PDF venue build never sees it; that
optimization is [a separate sketch](../gaps/sketches/tex-table-column-widths.md).

## Verification

Inspect rendered captures before calling a style or layout change done:
desktop (1200×600) and phone (375×812) views of the opening, of each kind of
table, and of an appendix start, plus the printed pages that hold tables.
Check that the page never scrolls sideways at any width and that bundled
links land on their anchors. [`ui-testing`](ui-testing.md) owns capture
mechanics.

## Code

`qmd_build/`: `styles.py` (style search and manifests; `styles/memo/`),
`document_title.lua` (opening heading as title), `document_corner.lua`
(revision and PDF link), `table_tokens.lua`, `included_documents.lua` (links
between included documents, `.appendix-doc`), `table_layout.py` with
`table_widths.js`, `table_widths.mjs` and `table_widths.lua` (build-time
column widths), `fonts.py` (embeddable faces), and `browser_print.py`
(Chromium print and PDF page count). A hand-assembled page outside Quarto,
such as a one-page highlight, can reuse `font_face_css`, `print_pdf` and
`pdf_page_count` directly.

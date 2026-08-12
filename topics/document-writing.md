# Document writing

> Maintain one explicit source of truth for a research document and choose a
> renderer that can produce its required static web and printable forms without
> creating two independently edited manuscripts.

Topic: `document-writing`

## Default source and renderer

Start a research document in portable Markdown-plus: Markdown prose with
citations, labels, attributes, executable cells, and narrowly isolated
renderer-specific blocks as needed. The renderer may change; the early source
should remain cheap to migrate. For an ordinary document that needs both a
static website and a working PDF, use [Quarto](https://quarto.org/) and `.qmd`
as the operational default. Quarto is an open-source publishing system built on
Pandoc and can render HTML, PDF/LaTeX, citations, cross-references, executable
cells, and Observable JavaScript.

This default does not imply that Quarto has a maintained adapter for the
eventual venue. Renderer extensibility, a community template, and venue support
are different claims. Before binding a serious paper to a renderer, inspect the
current venue call, official template, and current renderer template catalog.
Classify what exists explicitly:

1. **venue-endorsed path** — the venue says this authoring path is accepted;
2. **cataloged adapter** — the renderer's current catalog names and maintains
   the venue and year;
3. **community adapter** — a third party maintains it, without venue
   endorsement;
4. **local adapter** — this project wires the official LaTeX assets into a
   generic template/filter system; or
5. **generic TeX output** — the system can emit TeX, but no one has supplied or
   maintained the venue compatibility layer.

Do not describe levels 3–5 merely as “supported.” A venue-supplied `.cls` or
`.sty` makes the underlying style official; it does not certify a renderer's
transformation into that style.

Use this selection table at the start of a real document build:

| need | source/render path |
|---|---|
| ordinary research paper, handout, or blog with shared HTML and PDF | Quarto `.qmd`; retain TeX for inspection |
| a self-contained TeX tree, Journal Article Tag Suite (JATS), Manuscript Exchange Common Approach (MECA), or semantic abstract-syntax-tree export is decisive | [MyST Markdown](https://mystmd.org/guide/documents-exports) |
| R-native executable manuscript and an existing publisher format | [R Markdown](https://bookdown.org/yihui/rmarkdown/) plus [rticles](https://pkgs.rstudio.com/rticles/) |
| minimal, inspectable Markdown-to-HTML/TeX transformation | [Pandoc](https://pandoc.org/MANUAL.html) with an explicit template and filters |
| scholarly GitHub workflow, automatic citation resolution, and collaborative review dominate | [Manubot](https://github.com/manubot/rootstock), with venue adaptation treated separately |
| full data explorer or reactive dashboard is the principal artifact | [Observable Framework](https://observablehq.com/framework/) companion site, linked from the canonical paper/post |
| bespoke publication UI or component system dominates and print is secondary | [Astro](https://docs.astro.build/en/concepts/islands/) companion site |
| exact venue LaTeX is already canonical and web is derivative | direct LaTeX plus [lwarp](https://ctan.org/pkg/lwarp) or [make4ht](https://ctan.org/pkg/make4ht) for an audited HTML companion |

MyST is the strongest current alternative when the TeX handoff is central: its
[TeX build](https://mystmd.org/guide/creating-pdf-documents) produces a folder
containing source, images, citations, and class files, while its broader export
path includes PDF, Word, JATS, and MECA. Its arbitrary-JavaScript widget route
is currently documented as experimental, so Quarto remains the more
established default for a browser-heavy research post. R Markdown/rticles is a
credible R-centered predecessor with custom publisher formats. Direct Pandoc
has the least hidden machinery and therefore supplies the clearest hard
migration boundary, but it does not itself maintain a target-venue layer.
Manubot adds useful manuscript collaboration and citation machinery without
removing that venue-adaptation problem.

Observable Framework and Astro are strong web systems but do not supply the
paper/venue pipeline; use them as companions, not as a second manuscript
source. LaTeX-to-HTML systems invert the workflow and become attractive after a
strict venue template makes LaTeX canonical; their HTML requires the same
static-fallback and browser verification as any other generated companion.

## Promote a skeleton into a document project

An early paper skeleton may remain:

```text
research/<program>/papers/<paper-slug>.md
```

When it first needs a renderer, local assets, references, or multiple outputs,
relocate it—do not copy it—into:

```text
research/<program>/papers/<paper-slug>/
  index.<source-extension>
  <renderer-config>
  references.bib
  data/
  figures/
  components/
  styles/
```

For the Quarto default these placeholders are `index.qmd` and `_quarto.yml`;
MyST or another selected renderer uses its documented equivalents. Create only
the subdirectories the document uses. Keep data transformations
and figure generation in versioned scripts or executable cells with stable
inputs; do not make a hand-edited generated table or figure the only source.
Use relative links and paths so the project renders from a clean checkout and
under a GitHub Pages subpath. Update the frozen proposal and companion topic's
draft links in the relocation change.

## Assemble very long documents from ordered fragments

For writing expected to have great length, default to one source fragment per
section and one explicit root file that assembles them in reading order. This
keeps focused section edits cheap while preserving one manuscript authority.
Use zero-padded sequence prefixes with gaps so adjacent files are obvious and a
new section can be inserted without immediate renumbering, for example:

```text
index.qmd
sections/
  _00-abstract.qmd
  _10-introduction.qmd
  _20-method.qmd
  _30-results.qmd
```

The root file, not a filename glob, owns the definitive order. Under Quarto,
use its text-inserting
[`include` shortcode](https://quarto.org/docs/authoring/includes.html):

```markdown
{{< include sections/_00-abstract.qmd >}}

{{< include sections/_10-introduction.qmd >}}
```

Keep each directive alone on a line with blank lines around it, omit metadata
blocks from included fragments, and resolve fragment links and assets from the
root document's directory. Retain the underscore prefix so a project-wide
Quarto render does not treat fragments as standalone documents.

Fragments are editing units, not independent documents. Focused or
scatter/gather revision passes may work section by section, but every such pass
ends with a whole-document gather review for duplicated definitions,
contradictory claims, terminology drift, cross-references, transitions, and
reader-order failures, followed by a render of the root. Shorter documents stay
in one file. A renderer without native includes uses fragments only with one
documented deterministic assembly step; never keep both the fragments and an
assembled output as editable manuscript sources.

## One editable manuscript

The Markdown-plus file is canonical until an external requirement cannot be
represented reliably through the selected renderer's format, template,
extension, or filter. Generated HTML, PDF, and TeX are outputs. Do not hand-edit
generated TeX and then continue editing the Markdown source.

If a strict venue template requires direct TeX surgery that cannot be made a
repeatable render step, explicitly promote the TeX tree to canonical source.
The cutover may happen at any draft stage. Freeze and label the last
Markdown-source revision, generate or assemble a self-contained TeX tree,
compile it with the official venue assets, declare the TeX root canonical in
the paper README/build notes, and stop regenerating over hand-edited TeX. Make
the former Markdown source derivative or archival and identify how any web
companion is regenerated. Never leave two files both presented as the current
manuscript.

## Keep rich elements portable

Write claims, captions, labels, citations, and the static reading path in
portable Markdown first. Add renderer-specific behavior in fenced divs,
format-conditional blocks, shortcodes, filters, or local components. Custom
JavaScript receives a stable element/data contract and remains local to the
document project; avoid pasting opaque script fragments through the prose.

Follow [`document-writing-browser-interactive`](document-writing-browser-interactive.md)
for static HTML and interaction and
[`document-writing-printable`](document-writing-printable.md) for PDF,
LaTeX, arXiv, and venue packages. Follow
[`document-writing-figures`](document-writing-figures.md) before selecting or
generating figures, diagrams, and quantitative displays. Follow
[`blog-post-writing`](blog-post-writing.md) for blog-specific navigation and
page structure.

The Markdown-plus start and one-source promotion rule are current guidance.
The off-the-shelf tool comparison is grounded but incomplete and has not been
exercised end to end here; see
[`document-authoring-toolchain-bakeoff`](../gaps/document-authoring-toolchain-bakeoff.md).
A real paper should retain its exact build command, renderer version,
extensions, support-level classification, and venue template revision beside
the source.

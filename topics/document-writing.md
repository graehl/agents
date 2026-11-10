# Document writing

> Maintain one explicit source of truth for a research document and choose a
> renderer that can produce its required static web and printable forms without
> creating two independently edited manuscripts.

Topic: `document-writing`
Governs: choosing the source of truth and renderer for a research document

This topic owns source files and rendering, not the prose. Before drafting or
revising the prose, follow [`technical-writing`](technical-writing.md).

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
  _10-introduction.qmd
  _20-method.qmd
  _30-results.qmd
```

The root file, not a filename glob, owns the definitive order. Under Quarto,
use its text-inserting
[`include` shortcode](https://quarto.org/docs/authoring/includes.html):

```markdown
{{< include sections/_10-introduction.qmd >}}

{{< include sections/_20-method.qmd >}}
```

Each fragment opens with its heading. A paper's abstract belongs in the
root's `abstract:` front matter, which Quarto renders as the HTML title-block
abstract and the LaTeX abstract environment.

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

### Term definitions and notation previews

The shared `qmd_build/term_hints.lua` filter gives prose and mathematical
subexpressions one definition identity. It runs once per build. A paper
project registers it in `_quarto.yml` (the paper scaffold includes it), which
serves plain `quarto render` and `qmd-arxiv`. `qmd-html` adds it only when the
project's filter list lacks it, so a standalone document still gets it, and
`qmd-venue-pdf` registers it in the document it stages. HTML supports mouse hover,
keyboard focus, and click/tap to keep a selectable card open, with a link to
the definition. PDF keeps internal links; portable PDF viewers do not offer
the HTML hovercard interaction.

Mark the **exact substring to preview**, preserving its existing prose:

```markdown
[The **semantic score** $s(h,r)$ compares hypothesis $h$ with reference
$r$; larger values mean greater similarity.]{#term-score .term-definition math="s" terms="semantic score"}
```

The ID starts with `term-`; its remaining name is letters, digits, and hyphens,
beginning with a letter. `math` lists literal TeX aliases, separated by `|`;
`terms` lists case-sensitive prose aliases with the same separator. Both are
optional. The definition span itself stays visible and is the link target.
Its entire contents, including emphasis and math, form the preview. To use a
paragraph, wrap that paragraph's inline contents; use a shorter span when only
one sentence defines the term. No duplicated summary is necessary.

Choose the operator as the alias: `math="s"` matches the `s` in `$s$`,
`$s(h,r)$`, `$s(x,y)$`, and display equations, regardless of the arguments
used at the definition site. Styled aliases such as `math="\mathcal{R}"`
remain distinct from `R`. Matching happens on TeX tokens before rendering,
so `s` never matches inside `\sin` or `\text{scores}`. Aliases are literal,
not an algebraic equivalence engine: whitespace, macros, and alternative
spellings that differ need another alias or an explicit reference.

For ambiguity, different spellings, or a compound expression:

```markdown
[this score]{.term-ref term="score"}
$\termref{score}{s(h,r)}$
$$ \termref{score}{s}(x,y) + \termref{score}{s}(h,r) $$
```

The two arguments to `\termref` are the ID suffix and the exact TeX to
display. Braces may nest. A definition without aliases is explicit-only;
use that for two meanings of the same symbol. Duplicate IDs, conflicting
explicit aliases, and unknown reference IDs fail the build. An explicit
outer reference owns its entire expression, without nested hover targets.
Use `$\termignore{s}$` for an unrelated occurrence, or `.no-term-hints` on
a span or fenced div to suppress automatic references in a larger passage.
Existing links and code are excluded.

`term-hints-implicit: true` in QMD front matter or `_quarto.yml` enables
first-mention paragraph previews for math letters, Greek symbols and styled
math atoms, taken from math only. Bold or italic text is never an implicit
term: emphasis cannot be told from stress or a run-in label, and an author
emphasizes a term once, so repeated emphasis is rarely a reference. A prose
term gets links only from an authored definition (`terms=`), which also
links its plain uses and keeps the formatting of a bold or italic use. A link
never points at the paragraph it sits in, so a first-mention paragraph gets
an anchor and a card only when a later paragraph refers to it. This is off
by default, and a value that is not a boolean fails the build. Cards say
**First mention**, not **Definition**. Explicit
definitions always win, including when they occur later in the document.
The first mention is contextual help, not an inferred mathematical meaning;
author an explicit definition when that context is inadequate. Prose
aliases come only from an authored `terms=` list and match whole phrases;
formatted terms retain their formatting.

The switch is read only from the rendered document's metadata; `qmd-html.json`
no longer accepts it. Venue builds take the two switches from their config's
`metadata` key and do not inherit the root manuscript's.
The ASR papers and the conditional-reuse paper enable implicit previews in
their project configuration.

Common notation (`\sum`, `\prod`, `\in`, `\notin`, `\subseteq`, `\cup`,
`\cap`, `\forall`, `\exists`, `\operatorname{argmax}`,
`\operatorname{argmin}`, and `\mathbb{R}`) has built-in explanations, labeled
**Notation**, and a generated end-of-document reference containing only used
entries. Set `term-hints-operators: false` to disable these defaults.
An explicit math alias replaces its default explanation. For a custom
operator, `math-class="op"`, `"rel"`, or `"bin"` on its definition preserves
the corresponding TeX spacing; ordinary symbols need no class attribute.
Explicit-only `\termref` also handles notation the automatic matcher cannot
interpret. This is deliberately a small notation dictionary, not a claim to
explain every TeX command or overloaded mathematical symbol.

**Design decision:** stable author IDs plus pre-render TeX annotation, rather
than guessing identity from rendered glyphs or a function's argument names,
keeps inline/display equations and PDF links on the same definition. The
implementation uses [Pandoc Lua filters](https://pandoc.org/lua-filters.html)
and MathJax's [`\href` support](https://docs.mathjax.org/en/v4.1/input/tex/extensions/html.html).
HTML previews and assets are embedded; no glossary service is required.

### Other rich elements

Write claims, captions, labels, citations, and the static reading path in
portable Markdown first. Add renderer-specific behavior in fenced divs,
format-conditional blocks, shortcodes, filters, or local components. Custom
JavaScript receives a stable element/data contract and remains local to the
document project; avoid pasting opaque script fragments through the prose.

**Table notes:** mark a cell with a letter superscript (`^a^`) and start each
note on its own source line directly after the table with the same marker
(`^a^ Protocol C ...`). `qmd_build/table_notes.lua`, applied by `qmd-html`
and by the paper template's `_quarto.yml`, links each marker to its note in
HTML and starts each note on a new line; a marker in prose links too when
its letter names exactly one note in the document. PDF output is unchanged.

**Wide tables:** keep prose at the default body width, but put a table that
would wrap there in `::: {.column-screen-inset}` (graehl, 2026-10-22: an
over-width table covering the margin table of contents beats cramped cells).
The paper template's `paper.css` makes it opaque over the TOC and keeps the
TOC expanded in the margin (graehl, 2026-11-09) instead of Quarto's
"Table of contents" dropdown, which Quarto otherwise substitutes for the
whole page once any page-wide block exists. Cut prose
from cells into notes before widening further.

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

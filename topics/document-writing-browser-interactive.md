# Browser-interactive document writing

> Render a research document as static, relatively linked HTML whose claims
> remain readable without custom JavaScript and whose client-side interaction
> adds exploration, navigation, and detail.

Topic: `document-writing-browser-interactive`

## Static delivery contract

The default web artifact is a complete static output directory containing an
`index.html` and local or relative assets. It may be served by GitHub Pages,
another simple static host, or a basic local HTTP server; reading the document
must not require a project backend, notebook kernel, database service, or
authenticated API. Quarto documents and websites have an official
[GitHub Pages deployment path](https://quarto.org/docs/publishing/github-pages.html).

Test through HTTP rather than relying on `file://`, because browser module and
data-loading rules differ. Keep the central claim, captions, navigation, and a
useful representation of each result in the initial HTML. Custom JavaScript is
progressive enhancement even when interaction is a principal reader benefit.
Prefer the inspectable output directory for routine publishing. Use Quarto's
[self-contained HTML](https://quarto.org/docs/output-formats/html-publishing.html)
only when a one-file handoff is materially easier, and check the resulting size
and duplicated embedded data.

## Rich-element convention

Every interactive figure, table, or example browser has:

- a stable section and figure/table identifier;
- a descriptive caption that states the population, comparison, defaults, and
  intended takeaway;
- a static representation of the default or central claim;
- local, versioned data or a build-produced extract with provenance;
- an accessible non-pointer route for controls and values; and
- a print equivalent governed by
  [`document-writing-printable`](document-writing-printable.md).

Use Quarto's [cross-referenceable fenced
divs](https://quarto.org/docs/authoring/cross-references-divs.html) to wrap a
custom element under a `#fig-*` or `#tbl-*` label. Use
[format-conditional content](https://quarto.org/docs/authoring/conditional.html)
when the HTML interaction and printable equivalent differ. A tooltip may
clarify a mark, but it is never the sole carrier of a value, definition, or
claim; support focus, keyboard, and tap rather than hover alone.

For custom components, keep one inspectable rich-block convention rather than
inventing per-post script insertion. A labeled fenced div owns an author-
written caption, a static fallback, and an element whose `data-component` and
`data-source` attributes select a component from one local entry module:

```markdown
::: {#fig-error-browser}
::: {.content-visible when-format="html"}
<div data-component="example-browser" data-source="data/errors.json">
  <img src="figures/errors-default.svg"
       alt="Static default view and representative rows.">
</div>
:::

::: {.content-visible unless-format="html"}
![Static default view and representative rows.](figures/errors-default.svg)
:::

Error-browser default view: false positives by source, with representative
rows; lower is better.
:::
```

The build includes the local module and data as declared resources. Keep the
component registry small and explicit; a rich block may add layout hooks but
must not replace the surrounding document's heading, caption, citation, or
fallback contracts.

### Interactive data displays

Prefer [Observable JavaScript in
Quarto](https://quarto.org/docs/interactive/ojs/) for page-local reactive
filters, plots, and data attachments. It can consume local CSV, JSON, Arrow,
and SQLite files and can receive build-time Python or R results. Move code into
a local JavaScript module or Web Component once reuse or testing justifies it.
Use Observable Framework only when the artifact has become a multi-page data
application rather than a document with a few interactive displays.

Use [`document-writing-figures`](document-writing-figures.md) to choose the
static display and external plotting stack before adding interaction. For an
ordinary line, bar, scatter, or small-multiple claim, generate matched SVG/PDF
assets first; add OJS and Observable Plot only when filtering, selection, or
exact-point inspection materially helps the browser reader.

For a result table, render a self-contained static summary and representative,
boundary, or outlier example rows in the page. Client-side sorting, filtering,
paging, column toggles, and download may expose the fuller data. The initial
rows are selected to explain the result, not merely the first rows in storage.

For a visualization, preserve the central default view as SVG, a raster image,
or a compact table when JavaScript is unavailable. The static and interactive
versions use the same data and default selection; otherwise the fallback may
quietly assert a different result.

### Math, examples, and annotations

Use a supported HTML math renderer such as KaTeX, MathJax, or MathML through
the renderer's documented option rather than embedding equations as images.
Provide text labels and surrounding explanation for notation whose visual form
alone is insufficient.

Treat input/output examples as data-bearing displays: label source, condition,
output, and selection rationale. Autocaptions may fill a consistent visual
shell from explicit metadata, but a generated generic caption does not replace
the author-written takeaway. Annotation and tooltip text belong in data or
markup that remains inspectable, not only inside minified script state.

## Navigation and page structure

A long single page has a visible table of contents, stable heading anchors,
and direct links to source, data, code, and printable output. A multi-page site
adds a landing page or listing, search when the corpus warrants it, and clear
previous/next or section navigation. Quarto's
[website navigation](https://quarto.org/docs/websites/website-navigation) and
[listings](https://quarto.org/docs/websites/website-listings.html) provide the
default machinery; custom navigation must earn its maintenance cost.

## Verification

Before calling the artifact portable:

1. render from a clean source tree with the recorded build command;
2. serve the output directory under a basic HTTP server and under the intended
   subpath;
3. load it once with JavaScript enabled and once with custom JavaScript
   disabled or failed;
4. exercise controls by keyboard and at phone width as well as desktop;
5. check that every local link, image, data attachment, citation, and download
   resolves; and
6. compare each interactive default with its static and printable equivalent.

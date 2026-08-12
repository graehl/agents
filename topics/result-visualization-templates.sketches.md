# Result-visualization template sketches

> Research proposals for reusable renderer integrations that would make the
> current static visualization contracts easier to fulfill across HTML and
> print.

These are not implemented capabilities. They require research and a
representative Quarto-to-HTML/PDF bakeoff before promotion. Their shared
tracking entry is
[`gaps/result-visualization-templates-research.md`](../gaps/result-visualization-templates-research.md).

## Semantic interactive-figure layer

Build one local, client-side semantic layer over a static SVG or a shared chart
specification. It should derive interaction from the same data, series, legend,
panel, and annotation schema that produced the static figure:

- hovering, tapping, or keyboard-focusing a mark/subregion decodes its series,
  condition, x/y value, uncertainty, and relevant note without forcing a trip
  through a remote legend;
- focusing a legend entry highlights its marks and exposes the same literal
  label;
- clicking a breakout panel opens an enlarged accessible view without losing
  the overview or changing its selection;
- zoom and pan are available for dense displays, with a reset control and an
  announced current domain;
- the visible Markdown caption and `*`/footnote coda remain canonical and
  print-visible, while HTML projects the applicable note into a tooltip or
  popover at its marker; and
- no value, definition, caveat, or claim exists only on hover.

Quarto already supports hover popups for ordinary footnotes and cross-references
through `footnotes-hover` and `crossrefs-hover`; those can be enabled explicitly
for HTML. Attaching the same coda to arbitrary chart regions, deriving
legend-decoding tooltips, and panel expansion need a custom OJS component,
Vega-Lite/Altair selection layer, Plotly integration, or SVG-enrichment pass.
Compare those paths rather than promising one in advance.

## Document-to-figure style bridge

Define a small generated `figure-style` contract derived from the document's
brand/theme and venue profile. It should pass, rather than hard-code:

- proportional and monospace font family/face, weight, style, and fallback;
- base, tick, legend, and annotation sizes at the intended physical placement;
- color plus grayscale-safe line, marker, and lightness mappings;
- axis, grid, spine, padding, and background policy; and
- target dimensions for full-width, single-column, and breakout panels.

Adapters would apply the same contract to Matplotlib, ggplot2, and
Altair/Vega-Lite. SVG/PDF output should preserve live vector text; PDF should
embed or explicitly resolve the requested face. A missing exact font fails or
records the chosen fallback rather than silently substituting it. The research
must determine whether Quarto `_brand.yml`, format metadata, a separate YAML
file, or a normalized generated JSON is the stable source across HTML and
venue LaTeX.

The same build could emit or simulate a grayscale proof and test open-axis
versus light-grid framing around extrema. It should not generate a separate
hand-tuned gray figure whose geometry or data can drift from the color asset.

## Native qualitative-panel component

Develop a portable Markdown-plus convention for annotated transcript
contrasts, token-activation rows, and representative-example cards. Its source
should remain native text and structured metadata, while renderers supply
responsive spatial layout:

- common input and condition labels remain outside repeated output blocks;
- role labels, exact outputs, annotations, selection rationale, and optional
  numeric activation values stay selectable and accessible;
- color highlights are redundant to labels, underline/border treatment, or
  ordered lightness and survive grayscale print;
- the enclosing Markdown owns figure title, caption, footnotes, and coda; and
- HTML may add focusable tooltips or expansion, while PDF/LaTeX retains the
  entire evidence without JavaScript.

Start with Quarto cross-referenceable fenced divs and block `layout`
attributes, then test whether a Lua filter plus paired SCSS/LaTeX partials is
needed for consistent card geometry and highlighted spans. The research must
include narrow HTML, standard PDF, and at least one real two-column venue class;
CSS-only success is insufficient.

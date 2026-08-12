---
slug: result-visualization-templates-research
noticed: 2026-08-12
where: topics/result-visualization-templates.sketches.md
---

**Gap:** The result-visualization registry now specifies static layouts,
grayscale/print behavior, document-owned captions, and native textual evidence,
but three desirable authoring capabilities remain unresearched and
unimplemented: a semantic interactive-figure layer (subregion tooltips,
legend decoding, panel enlargement, and zoom), a document-to-figure typography
and style bridge, and portable native qualitative panels across HTML and venue
PDF. Ordinary Quarto footnote/cross-reference hover exists; arbitrary
chart-region coda projection does not yet have a selected supported path.

**Noticed while:** Naming the user-designed main-and-breakout figure and
extending it into a grounded registry of successful result-presentation forms.
The supplied first render also showed a curve coinciding with a heavy top
spine and pale raw points that would disappear in grayscale.

**Fix sketch:** Build one representative document containing a
main-and-breakout curve figure, an annotated transcript contrast, a
token-highlight gallery, and a distribution with linked exemplars. Compare
Altair/Vega-Lite plus `vl-convert`, Observable Plot/OJS, Plotly, and enriched
static SVG for semantic mark/legend/panel interaction. Prototype a normalized
style manifest consumed by Matplotlib and at least one declarative renderer;
verify requested font resolution, editable/embedded vector text, grayscale
decodability, and open-axis/extrema behavior. Prototype the qualitative panels
with Quarto block layouts and only add Lua/SCSS/LaTeX machinery if the native
path fails. Render static HTML with JavaScript disabled, interactive HTML by
mouse/keyboard/touch at desktop and phone widths, ordinary PDF, and one current
two-column venue class. Close the gap by selecting and documenting the smallest
maintainable integrations, recording unsupported cases, and promoting only the
tested portions from the sketches into current guidance.

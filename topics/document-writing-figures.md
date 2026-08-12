# Figures, diagrams, and quantitative displays in research documents

> Choose the smallest Quarto-native display that preserves the claim, and
> generate quantitative figures reproducibly from versioned or
> provenance-tracked data into matched web and print assets.

Topic: `document-writing-figures`

Use this topic when a paper, handout, progress report, or research blog asks
for a graph, diagram, visual summary, or unusually rich table. It translates
the request's information and visual-weight intent into Quarto's authoring
vocabulary and a reproducible external plotting path. The requester need not
name a plotting library or exact layout.

## Select the display before selecting the tool

Use the simplest row whose information contract fits:

| reader need | default authoring form |
|---|---|
| exact values in a modest comparison | Markdown pipe table with caption, label, and nearby interpretation |
| one existing or generated image | Quarto captioned image with `#fig-*`, `fig-alt`, and an extensionless multiformat path |
| several distinct images that need comparison | Quarto figure div with `layout-ncol` or `layout-nrow` |
| process, sequence, state, or timeline | Quarto-native Mermaid cell |
| dependency graph, hierarchy, or network topology | Quarto-native Graphviz `{dot}` cell |
| simple bar, line, scatter, or distribution used by one document | Python/R executable cell; Matplotlib is the Python default |
| custom annotations, coordinated small multiples, reused figure, or exact matched assets | external quantitative-figure generator reading stable data |
| disposable exploratory plot | Python/R executable cell, promoted when its implementation needs independent testing or reuse |
| filter, hover, selection, or linked exploratory views | Quarto Observable JavaScript (OJS) plus a same-data static figure or table |

Quarto's native Markdown owns placement, layout, captions, alt text,
cross-references, format selection, tables, and text-defined diagrams. It is
not the default quantitative chart grammar. Do not force measured-data charts
through Mermaid merely because a chart-shaped extension exists. A table is
not a substitute when the claim is a curve shape, crossing, distribution, or
dominance relation; a graph is not a substitute when readers need exact
point values.

## Quarto-native vocabulary

The syntax below follows Quarto's current documentation for
[figures and layout](https://quarto.org/docs/authoring/figures-and-layout.html),
[tables](https://quarto.org/docs/authoring/tables.html), and
[diagrams](https://quarto.org/docs/authoring/diagrams.html).

### Figures and matched web/print assets

Generate `figures/swept-curves.svg` and `figures/swept-curves.pdf`, then leave
the extension off in the source:

```markdown
![V11 and GLiNER2 sweep curves by language; higher is better.](figures/swept-curves){#fig-swept-curves fig-alt="Ten shared-scale panels compare both systems over the sweep parameter for overall results and nine languages." width=100%}

The common-scale comparison in @fig-swept-curves shows ...
```

Quarto chooses a target-specific extension. Make SVG the HTML default while
retaining Quarto's PDF-via-LaTeX default of PDF:

```yaml
format:
  html:
    default-image-extension: svg
  pdf:
    keep-tex: true
```

Use an explicit extension only when the same asset is genuinely correct for
every target or no matched form exists. Keep the caption in the document and
make the `fig-alt` description complementary rather than a caption copy.

For separately meaningful subfigures, use a figure div. Blank lines between
the div, images, and caption are significant:

```markdown
::: {#fig-two-errors layout-ncol=2}

![False positive.](figures/false-positive.svg){#fig-fp}

![False negative.](figures/false-negative.svg){#fig-fn}

Representative error modes.
:::
```

Do not split one coordinated small-multiple chart into independent Markdown
images merely to obtain layout; one generator should own its shared axes,
legend, annotations, and geometry.

### Tables

Use a pipe table when a compact set of exact values is the display:

```markdown
| system | peak F1 | sweep value at peak |
|---|---:|---:|
| V11 | 0.91 | 0.30 |
| GLiNER2 | 0.89 | 0.25 |

: Overall sweep summary (higher is better). {#tbl-sweep-summary}
```

Refer to it as `@tbl-sweep-summary`. Follow
[`technical-writing`](technical-writing.md) and the research result-table
rules for population, split, N, metric direction, cost boundary, and nearby
interpretation. A generated table reads the same provenance-tracked evidence as its
figure; do not manually transcribe one from the other.

### Mermaid and Graphviz

Use Mermaid for a compact process or sequence:

````markdown
```{mermaid}
%%| label: fig-evaluation-flow
%%| fig-cap: "Evaluation flow from saved predictions to the handout."
flowchart LR
  A[Saved predictions] --> B[Score and validate]
  B --> C[Figure and summary table]
```
````

Use Graphviz when graph layout is the substance:

````markdown
```{dot}
//| label: fig-dependencies
//| fig-cap: "Evidence dependencies for the headline claim."
digraph G {
  runs -> scores
  scores -> claim
  baselines -> claim
}
```
````

Quarto renders Mermaid natively in HTML and uses Chrome or Edge to create a
PNG for print formats. Keep that documented default for LaTeX PDF; forcing
Mermaid SVG adds conversion dependencies and can clip multiline text. A large
diagram may live in a `.mmd` or `.dot` file and use the cell's `file:` option.

## Default quantitative-figure toolchain

For a Python-oriented research project, default to Matplotlib 3.8 or later.
For a custom, reused, or independently validated figure, use the noninteractive
Agg backend: a committed script reads the canonical tidy CSV/JSON or run-
produced extract, validates its expected conditions, and emits same-stem SVG
and PDF in one run. Emit PNG only for a known raster-only consumer.

```python
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

fig, axes = plt.subplots(
    2, 5, figsize=(11.0, 4.8), sharex=True, sharey=True,
    constrained_layout=True,
)
# Read and validate data; draw on axes.
fig.savefig("figures/swept-curves.svg", bbox_inches="tight", facecolor="white")
fig.savefig("figures/swept-curves.pdf", bbox_inches="tight", facecolor="white")
```

Set the physical size in plotting code for a per-figure requirement. Quarto's
Jupyter `fig-width` and `fig-height` options are document/project-level rather
than reliable per-cell sizing controls. Use vector output, shared axes where
comparison demands them, restrained major grid lines, machine-readable text,
and a color-blind-safe palette with line style or markers as a redundant cue.
Do not smooth between sampled measurements unless the interpolation is part of
the declared analysis.

Keep the generator outside the manuscript when the figure is reused, expensive,
custom enough to regression-check, or expected to survive a later LaTeX
cutover. A simple one-document claim-bearing figure may remain an executable
cell when its stable inputs and code are committed and both target renders are
audited. An inline Python figure may use:

````markdown
```{python}
#| label: fig-quick-check
#| fig-cap: "Exploratory score distribution."
#| fig-alt: "Histogram of scores with a long lower tail."
#| echo: false

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(5.5, 3.0), constrained_layout=True)
# draw
plt.show()
```
````

Promotion means moving the plotting logic to a script and including its
generated assets; do not retain a second independently edited implementation
in the cell. The worked PII sweep below merits promotion because coordinated
axes, computed annotations, validation, and exact cross-format layout are part
of its claim.

### External alternatives

Choose for the program's existing language and the artifact's real need:

| tool | use it when | cost or boundary |
|---|---|---|
| [Matplotlib](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html) | default Python static publication figure; custom annotations and exact layout matter | imperative code; commit the generator and both vector outputs |
| [Seaborn atop Matplotlib](https://seaborn.pydata.org/tutorial/relational.html) | an existing Python project benefits from concise faceting or statistical defaults | custom peak/crossing labels still use Matplotlib axes; do not add it for one trivial plot |
| [ggplot2](https://ggplot2.tidyverse.org/reference/ggsave.html) | the research pipeline is already R-native; facets and grammar-of-graphics composition fit | use `ggsave()` for explicit same-size SVG and PDF outputs; do not introduce R only for a figure |
| [Altair + `vl-convert-python`](https://altair-viz.github.io/user_guide/saving_charts.html) | a committed Vega-Lite JSON specification or one declarative source for static and interactive variants is valuable | save JSON, SVG, and PDF; `vl-convert` is the maintained image-export path |
| [Observable Plot in OJS](https://quarto.org/docs/interactive/ojs/) | client-side filters, selections, or responsive exploratory views materially help the HTML reader | retain a same-data static view for print and JavaScript failure; avoid remote runtime data |
| [Plotly](https://plotly.com/python/static-image-export/) | the project already uses it or zoom, 3-D, geographic, or specialized interaction earns the dependency | static SVG/PDF export requires Kaleido and a compatible Chrome/Chromium; not the ordinary static default |
| [PGFPlots/TikZ](https://ctan.org/pkg/pgfplots) | LaTeX is already canonical and exact TeX typography or geometry dominates | weak browser path; use after print-first selection or cutover, not as the Markdown-plus default |

Prefer the project's already competent stack over ecosystem churn. A tool
choice never relaxes the same-data web/print contract.

## Build and freshness contract

A small Quarto project can make regeneration explicit through Quarto's
[project scripts](https://quarto.org/docs/projects/scripts.html):

```yaml
project:
  type: default
  pre-render: scripts/figures/build-swept-curves.py

format:
  html:
    default-image-extension: svg
  pdf:
    keep-tex: true

execute:
  echo: false
```

Run and debug the generator independently, then render both targets:

```bash
quarto run scripts/figures/build-swept-curves.py
quarto render index.qmd --to html
quarto render index.qmd --to pdf
```

These commands follow Quarto's [`run`](https://quarto.org/docs/cli/) and
[`render`](https://quarto.org/docs/cli/render.html) interfaces.

For the normal reproducible path, `quarto render` at the project root invokes
the `pre-render` script from that root. Record the Quarto, Python/R, and plotting
package versions beside the document. A script must fail clearly on missing
inputs, unexpected categories, duplicate keys, nonfinite plotted values, or an
unwritable output—not silently omit a panel or retain an old asset.

Do not enable Quarto `freeze: auto` around externally changing claim-bearing
data and assume freshness: Quarto's execution cache keys primarily on source
changes, so changed external inputs can leave frozen output stale. Prefer an
explicit generator/pre-render step. If a site deliberately commits `_freeze`
for portability, document how external-data changes invalidate and refresh it.

## Worked pattern: V11 versus GLiNER2 sweep curves

Interpret “a small graph of the swept curves for each of nine languages and
overall, spark style with peak/crossing labels, usual scale” as an information
and visual-weight request, not a demand for a particular library. The nearest
faithful default is one compact 2-by-5 small-multiple figure:

- panels are `overall` first, then the nine languages in a stable stated order;
- every panel uses the same x and y limits, ticks, metric direction, and sweep
  definition; use the metric's ordinary full scale or one defensible common
  comparison range, never per-panel autoscaling;
- V11 and GLiNER2 keep the same color, line style, marker, and order in every
  panel; show markers at sampled sweep values and use one shared legend;
- visually emphasize `overall` through its panel border or header weight, not
  a different scale;
- each panel header carries a compact literal summary, for example
  `V11 .91@.30 · G2 .89@.25 · cross ≈.18`, leaving the plot area uncluttered;
- peak labels give the measured maximum and sampled sweep value; ties follow
  one stated rule rather than whichever row is encountered first;
- report an exact crossing only when measured equality exists. Otherwise use
  `≈` only for linear interpolation between adjacent sampled points where the
  signed system difference changes sign. Never extrapolate or infer a crossing
  from smoothing. Say `no cross` when none is observed; if there are several,
  report the count or the decision-relevant one under a stated rule;
- uncertainty ribbons appear only when repeated measurements or a justified
  interval exist; the absence of a ribbon must not imply certainty; and
- the caption defines aggregation for `overall`, metric and good direction,
  split and N, common scale, crossing interpolation, and the intended takeaway.

The generator consumes tidy rows with at least `language`, `system`, sweep
parameter, metric, split, and N (plus seed/interval fields when applicable).
Before plotting, assert exactly the expected ten panels and two systems,
unique condition keys, sorted sweep values, and the intended common scale.
Emit a compact summary CSV or table of peaks and crossings when exact lookup
matters.

If a two-column venue makes 2-by-5 illegible, keep the same scale and visual
grammar but place `overall` full-width above a 3-by-3 language grid, or use a
full-width figure environment. For a Quarto-to-LaTeX target whose class uses
the conventional two-column float, add `fig-env="figure*"` to the figure
attributes and verify the venue output. A lower-weight fallback may reduce tick labels
and annotate only the peaks/crossings that affect the conclusion. Do not
replace the comparison with ten independent rescaled sparklines. If the common
scale hides important local structure, add an explicitly labeled zoom or
difference companion while retaining the common-scale main figure.

## Interactive variant

Interaction is optional enhancement for this example. An HTML reader may use
an OJS dropdown to enlarge one language, inspect exact points, or toggle
uncertainty, reading the same local CSV with `FileAttachment`. Observable Plot
is already available in Quarto OJS cells. The static small multiples remain in
initial HTML and PDF and carry the claim; do not make hover the only source of
peak or crossing values. Third-party OJS `require()` imports normally load from
a content delivery network, so use built-ins or local modules for a durable,
simple-host artifact unless an online dependency is explicitly accepted.

## Release check

Before dissemination:

1. regenerate from the recorded source data and inspect generator validation;
2. render HTML and PDF using the recorded commands;
3. compare values, scales, defaults, captions, and selection between the
   figure, summary table, interactive view, and source rows;
4. inspect SVG at browser width and PDF at actual print size for clipped text,
   unreadable panels, missing glyphs, or rasterized vector content; and
5. run the cold-reader scan from [`technical-writing`](technical-writing.md).

For quality-versus-cost comparisons of three or more systems, also follow the
specialized [`pareto-figures`](pareto-figures.md) contract.

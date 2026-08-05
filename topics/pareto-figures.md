# Pareto-frontier figures in comparison reports

Topic: pareto-figures

When a handout, paper, or reader-facing comparison reports quality against
one or more cost axes (latency, throughput, memory, parameters, price) for
three or more systems, include a Pareto scatter figure — not only tables.
The scatter is the artifact a reader keeps: tables answer point lookups,
but dominance structure ("which systems earn a place on the frontier")
is invisible in a table and is usually the report's actual claim. A
two-system or single-objective comparison does not need one.

## Rendering contract

- **SVG is the canonical inline format** (`![…](figures/x.svg)` in the
  `.md`): crisp at any zoom, diffable, and YA's markdown rendering is
  confirmed to display it inline sized by the file's own
  `width`/`height` attributes. Keep those attributes in the output —
  matplotlib's SVG backend writes explicit `width`/`height` (pt) plus
  `viewBox` by default; do not strip them to "make it responsive".
  Also emit **PDF** for LaTeX `\includegraphics`; PNG only as an extra
  fallback for contexts that reject SVG (some chat/issue trackers).
  One generating script produces all formats in a run.
- The figure script reads the committed machine-readable evidence
  (JSON/CSV) that the tables are built from — never hand-entered
  numbers, which silently diverge when results are rerun. Commit the
  script, its input data reference, and the rendered outputs together;
  regenerate outputs in the same change that updates the data.
- Place outputs under the report's directory (e.g. `figures/`), named
  after the evidence they render, and link the figure next to the table
  it summarizes.

## Default package

**matplotlib (≥3.8), headless Agg backend.** It is already present in
this ecosystem's project envs, renders identical SVG/PDF/PNG from one
script, and its PDF/PGF output is LaTeX-grade (embed fonts; use
`constrained_layout`). Altair + `vl-convert` is an acceptable
declarative alternative where pip-installable (its JSON spec is
committable evidence), but do not make a report's build depend on a
browser or node toolchain.

## Taste rules for the Pareto scatter

- One point per system; label every point directly (short system name
  beside the marker); avoid a legend when direct labels fit.
- Draw the frontier as a step line through non-dominated points; render
  frontier points solid and dominated points hollow/muted — the
  dominance verdict should be readable without the caption.
- Log-scale a cost axis when it spans more than about one decade
  (throughput and params usually do); say so on the axis label, and put
  the "good" direction up/right (invert an axis rather than making the
  reader want lower-left).
- Color-blind-safe palette (e.g. Okabe–Ito); color by system family
  only when family is a claim the report makes, else monochrome.
- Axis labels carry the exact metric and conditions from the evidence
  ("batch-one docs/s, L40S", "language-macro overlap F1, Fresh20") —
  the figure will circulate detached from its section, so it must not
  overclaim what the harness measured.
- No title inside the image (the caption owns framing); no gridline
  clutter beyond light major lines; no 3D, no dual y-axes.

Multiple cost axes mean multiple small panels (quality vs memory,
quality vs docs/s), not one figure with a synthetic combined-cost axis.

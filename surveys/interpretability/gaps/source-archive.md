---
slug: interpretability-source-archive
noticed: 2026-10-17
where: surveys/interpretability/related-work/
---

**Gap:** the survey's source reading is broader than its accepted local
full-text archive. Goodfire's interactive essay failed `related-work` HTML
derivation with `SVG visual has an external CSS dependency: index.html`.
Its author-provided `essay.md` was fetched and inspected but is a text edition
with figure descriptions, not a faithful replacement for the interactive
visual archive. The manifest must retain `grounded: false` for this entry
until the engine has a valid completion record.

Four further papers were read through primary online full texts but lack an
accepted local extract: Wu's reply (2401.12631), Gurnee's sparse-neuron study
(2305.01610), Zhang's patching study (2309.16042), and Gerstner's weakening
neurons study (2609.18612). The first three HTML fetches yielded no auditable
visible text blocks; the last failed 10/313 block-fidelity checks. PDF fallback
was deferred because existing GPU leases left only about 365 MiB uncommitted,
despite greater physically unused memory. No retry is running or scheduled.
Their manifest entries retain checked `source:` URLs and `grounded: false`.

**Noticed while:** landing the grounded interpretability field survey.

**Fix sketch:** support this source's SVG dependencies in the shared engine,
or add a documented author-Markdown import with explicit edition identity,
hashes, and asset policy. Do not create a per-survey extraction script,
hand-author a success sentinel, or label the text edition a complete visual
archive. Raw page cache remains regenerable and ignored.

For the four arXiv entries, retry the shared engine when resources permit;
its normal PDF fallback uses marker-pdf. Do not weaken fidelity checks to
make the archive count match the number of sources read.

The positive SAE-steering counterpoint in `frontier.md` was read online and
deliberately left outside this bounded extraction set. Foundational sources
already archived in `surveys/llm-intelligence/` are reused by link.

Contributing-model: 6-astra

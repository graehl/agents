# One Recipe, Many Harnesses — what self-evolution encodes

Read method: prompted extraction over the arXiv HTML full text, 2026-08-15.
Full text: [HTML](https://arxiv.org/html/2608.10178) ·
[PDF](https://arxiv.org/pdf/2608.10178) ·
[local extract](../related-work/extract/onerecipe2026/html/2608.10178.md)
(git-ignored; rebuild with `related-work fetch`). arXiv 2608.10178.

**What it is.** Holds one harness self-evolution recipe fixed across an 8×3
grid (Multi-SWE-Bench languages × three base models) and asks what the
evolved content encodes: benchmark adaptation, language-specific
engineering, or compensation for the base model. Every edit routes through
a typed failure signal (seven deterministic buckets) and records a JSON
manifest with failure evidence, root cause, targeted fix, and a
predicted-impact list — a falsifiable contract validated next round.
Model-specificity is determined by post-hoc comparison of the separately
evolved harnesses (cross-cell Jaccard overlap), not by any live
cross-model signal.

**Results.** Evolution beats both a minimal seed and mini-SWE-agent in most
cells, with two null regions (Python: defect rate already low; GPT-5-mini:
few detectable execution defects). Language, more than model, is the
binding constraint on which defect dominates.

**Relation to the diagnosis program.** Closest goal overlap found by the
2026-08-15 falsification pass: it pursues the shared-vs-model-specific
partition of instruction content — the question this repo's
model-supplement layer answers by construction — but by evolving separate
per-cell harnesses and comparing artifacts afterward. No shared maintained
corpus, no divergence-under-identical-instructions signal, no routing of
content into shared vs model-scoped homes. Its per-edit predicted-impact
contracts are published precedent for the program's pre-registered patch
discipline.

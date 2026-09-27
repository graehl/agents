# Retrieval and grounding record

**2026-09-27; bounded initial pass, not saturation.** Anchors: the proposals'
SSoT and Subliminal Learning references, the token-entanglement follow-up, and
StyleAligned as an older attention/style anchor. The shared distillation
extension starts from GKD and follows the recent context-distillation branch.

Search covered primary arXiv pages and author/lab publications using String
Seed of Thought, Verbalized Sampling, token entanglement, subliminal learning,
shared attention style, and on-policy/context distillation. Negative searches
added limitations, external random strings, and transfer failures. Primary
methods, negative arms, and reference lists determined inclusion.

Semantic Scholar's forward-citation endpoint for arXiv:2507.14805 was
inaccessible through the web tool. OpenAlex's title search for String Seed of
Thought returned zero records; this is a retrieval limitation, not evidence of
no citations. For GKD, the narrower title query “Learning from Self-Generated
Mistakes” found W4382173266 with three indexed citers. Both publication-date
and citation-count orderings were inspected: they returned the same three
older survey/dialogue works, none selected for this focused extension.
The sparse record is not a trustworthy total impact estimate. Other citation
counts remain uncollected rather than guessed.

Backward reading of SSoT identified diversity preference optimization and
diversity-reward training as a further neighborhood. OPCD's references confirm
its connection to GKD, earlier context distillation, and 2026 privileged-
information/self-distillation work. Those neighborhoods are not exhausted here.
Primary-source anchors for subsequent retrieval include Misaki/Akiba at Sakana,
Zhang/Yu/Chong and collaborators on VS, Cloud/Le and collaborators on subliminal
transfer, Zur/Bau and collaborators on token effects, and Ye/Dong/Wei and
collaborators on context distillation. These are discovery leads, not evidence
grades.

## Source and extraction status

Follow-up searches for continuous random inputs, latent exploration, and
adaptive noise gates located Long et al.'s Reasoning Palette. Methods
§§3.2–3.4 and inference evaluation §4.1 were read. The accepted extract passed
164/164 visible blocks and 118/118 math checks. Its controls schedule prefix
use across training, not learned per-generation-step noise consumption.
No exact match for the latter was verified. Citation snowballing from this
new anchor remains outside this initial pass.

| Source | Read coverage | Durable extraction |
|---|---|---|
| Subliminal Learning v1 | Setup, main numeric experiments, §5 cross-model/ICL, discussion | Accepted Markdown/provenance |
| It's Owl in the Numbers blog | Full post, including unsuccessful cases and residual filtering effect | Accepted Markdown/provenance; embedded interactive plots are not reproduced |
| StyleAligned v2 | §3 mechanism, §4 comparisons/ablations, conclusion | Accepted Markdown/provenance and referenced assets |
| SSoT v3 | §3 method, reported diversity comparison, D.5 failure and D.6 external-source comparison | HTML fetched; Markdown rejected: 12/659 fidelity blocks failed |
| Verbalized Sampling v4 | §4 method/comparator structure, reported creative tasks, Appendix B limitations | HTML fetched; Markdown rejected: 14/1373 fidelity blocks failed |

The failed extracts have no success sentinel and remain `grounded: false` in
the engine's manifest terminology. Their map nodes are citation-verified,
primary-full-text online readings, not claims of accepted local archival
grounding. They do not have concept pages. An attempted Sakana blog extraction
also failed HTML-entry discovery. The [existing extraction gap](../../../gaps/related-work-math-html-fidelity.md)
records these cases. No thresholds were relaxed; no PDF/accelerator job was
launched. This survey is usable as an initial grounded map with explicit
archival limits, not a completed extraction corpus.

## What the disconfirming pass changed

SSoT's external-source comparison is existing prior art; source choice alone
cannot be claimed novel. Subliminal Learning explicitly reports failed ICL,
so its positive fine-tuning result cannot justify one-shot string transfer.
StyleAligned's unrestricted-sharing ablation exposes copied content as a
style-consistency confound. The token-entanglement blog leaves residual
transfer after filtering and should not be read as a complete mechanism proof.
GKD's diversity tradeoff and OPCD's negative arms bound creative-distillation
extrapolations. No independent reproduction was established by this pass.

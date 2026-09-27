# Provisional claims and transfer questions

**Grounded survey overlay; bounded analysis only, cutoff 2026-09-27.**
The [field map](survey.md) owns the recommendations and evidence distinctions.
These entries identify checks that could change a choice; none schedules a run.
This pass does not claim an unoccupied research niche or rank novel capstones.

## Compact contextual embedders

**Claim:** Tateno's [Bekko](https://arxiv.org/html/2607.25180v1) uses a compact
contextual encoder and reports a CPU throughput advantage over multilingual
E5-small. Its a8m name refers to about 7.7M non-embedding active parameters;
the vocabulary embedding table is additional. `[R]`, `single-source`.

**Regime and incumbent:** the paper reports retrieval benchmarks and an
author-run CPU comparison using document encoding, batch size 64 and a
512-token limit. This is a comparison to E5-small, not the user's E5-base
pipeline. Active parameter count, resident memory and serialized model size
are different quantities. Tokenizer and embedding-table costs matter on CPU.
The author controls training and evaluation; no independent reproduction was
located. Low-resource language coverage, seed variation and training/evaluation
overlap auditing remain consequential qualifications in the paper.

**Decision relevance:** possible middle ground between contextual E5-small and
static pooling. **Cheapest discriminating check:** after pinning weights and
implementation, compare batch-one and batched CPU latency, peak memory and
cross-language candidate recall against E5-small and E5-base on identical
chunks. Reject the speed interpretation if it disappears at matched lengths,
threads, precision and useful-candidate yield. Treat the model as a candidate,
not a replacement selected by this survey.

**Revisit:** 2026-12-01, unscheduled reminder; act earlier only if a local speed
bottleneck or independent evaluation makes this choice material.

## Redundancy-aware selection before updates

**Claim:** [SIFT](https://arxiv.org/html/2410.08020v3) selects examples using an
uncertainty-reduction objective in a fixed representation, accounting for
redundancy between selected texts. Its LLM test-time experiments report gains
over nearest-neighbor selection. `[R]`, `single-source`.

**Regime and incumbent:** retrieved Pile text, limited test-time update budgets
(including a 50-update comparison), language-model likelihood, and an
author-controlled implementation/evaluation. The selection theory uses a
surrogate model; it is not a guarantee of the updated neural model's
calibration. The particularly severe repeated-nearest control is distinct
from ordinary deduplicated nearest-neighbor retrieval. Selection overhead,
the representation and learning rate can change the comparison.

**Decision relevance:** closer to choosing useful training examples than raw
semantic proximity, but transfer to multilingual span annotation remains
unestablished. **Cheapest discriminating check:** compare deduplicated top-k,
simple diversity selection and SIFT at matched total annotation/update cost.
Keep random draws and frozen-model output as controls. A selector that improves
likelihood but not the intended annotation metric has not solved this task.

**Revisit:** 2026-12-01, unscheduled reminder, or when a measured redundant
candidate pool makes selection the next bottleneck.

## From isolated documents to persistent user interests

**Question, not a published effectiveness claim:** does persistent adaptation
beat frozen retrieval with several interest prototypes plus resettable updates?
TTT-NN and its reproduction cover episodic language-model adaptation, while
continual-pretraining studies cover much larger token budgets. Neither fills
the user's particular multilingual, across-document annotation regime.

The immediate uncertainty is practical rather than a demonstrated literature
void. User histories can change topic, contain contradictory interests and
oversample a language. Relevant controls are a frozen model, query-only profile
updates, resettable downstream updates, and a persistent variant with replay.
Compare adaptation benefit and disjoint multilingual retention at equal
compute. Reset parameters and optimizer state for the episodic control;
keeping optimizer moments would introduce hidden persistence.

**Cheapest discriminating check:** a short held-out sequence of documents with
topic/language switches. If query-only adaptation captures the gain, persistent
weight updates have not earned their maintenance and forgetting costs.
**Revisit:** when such a workload is selected; no date-driven action is needed.

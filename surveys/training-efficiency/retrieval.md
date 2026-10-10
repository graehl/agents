# Retrieval and coverage record

2026-10-10 — Contributing-model: 6-astra

User seed: arXiv 2511.14617, first posted November 2025. The question is
whether its techniques remain additive to current practice, rather than
whether uneven-length scheduling is useful. The broad survey also covers
pretraining and finetuning speed, memory and cost.

## Sources and search

Fetched ten paper extracts with the shared `related-work` engine; citation
metadata and version pins are in [papers.yaml](related-work/papers.yaml).
Seer's mechanism/evaluation and appendix were read from its full-text HTML;
pretraining anchors were inspected at methods/results/limitations level.
QLoRA received a main-text and appendix read. TailSieve and GaLore's primary
HTML readings support their entries despite failed archival conversion.

Seer disconfirmation queries included its exact title, `2511.14617`,
`reproduction code`, `replication benchmark`, `rollout 2026 scheduling
comparison`, and `grouped speculative 2026 RL`. Searches found author claims,
conference publication, later papers and summaries, but no independently
executed full-Seer reproduction. Unrelated systems also use the name SEER;
they are not evidence for this paper.

OpenAlex title-resolution and Semantic Scholar arXiv-citation endpoints
failed through the web tool. No citation counts were inferred. Backward
references and primary later-paper comparisons supplied the neighborhood;
the bounded search did not reach citation saturation.

Supplemental primary readings:

- [OSDI final Seer paper](https://www.usenix.org/system/files/osdi26-qin.pdf),
  especially §4.4.2's Moonlight 100-iteration reward comparison, absent from
  the archived arXiv revision. This is an additional author experiment.
- [OSDI 2026 artifact criteria](https://www.usenix.org/conference/osdi26/call-for-artifacts):
  availability is not independent result reproduction.
- [veRL V1 async trainer](https://verl.readthedocs.io/en/latest/advance/v1_async_trainer.html):
  modes, dispatch and partial-resume semantics.
- [veRL MTP guide](https://verl.readthedocs.io/en/latest/advance/mtp.html):
  supported training/inference and the negative MiMo-7B/H20 throughput case.
- [slime scheduling](https://thudm.github.io/slime/advanced/rollout-scheduling.html)
  and [speculative decoding](https://thudm.github.io/slime/advanced/speculative-decoding.html):
  synchronization distinctions, native MTP, external draft-training limits.
- [SGLang KV transfer](https://docs.sglang.ai/backend/pd_disaggregation.html):
  prefill/decode transfer, which is not arbitrary decode migration.
- [FastRL author README](https://github.com/mit-han-lab/fastrl):
  runnable artifacts and contention from overly frequent drafter updates.
- Zili Wang et al., [Online Draft Co-Training](https://arxiv.org/html/2609.07108v1),
  2026: methods and full-step versus rollout measurements.
- Minseo Kim et al., [EfficientRollout](https://arxiv.org/html/2606.18967v2),
  September 2026 revision: quantized draft refresh, runtime selection,
  measured refresh costs, paired-seed results and Appendix F.4's explanation
  of the changed headline timings.
- Hayate Iso et al., [Accelerating RL Post-Training Rollouts via
  System-Integrated Speculative Decoding](https://arxiv.org/html/2604.26779v1),
  2026: same-stack learned/model-free comparison and limited benefit of
  further online adaptation. These three speculative-decoding papers also
  have accepted local extracts pinned in the manifest.

## Archival limitations

TailSieve failed with `mismatched tag inside SVG visual`; GaLore failed
visible-block fidelity, with 8 of 224 blocks flagged. Neither was promoted
to a successful extract. The failures extend the existing
[extraction gap](../../gaps/related-work-rich-derivation-regressions.md).
Raw downloaded sources remain ignored cache. The survey's grounding counts
refer to the manifested extraction set, not every supplemental URL above.

## Remaining field coverage

Kernel, memory, adaptation and compute-allocation anchors establish distinct
efficiency axes. This pass does not claim a current exhaustive leaderboard
for pretraining or finetuning, nor comparative coverage of all low-precision,
data-selection, parallelism or sub-plan-routing research. The detailed
year-later judgment concerns Seer and its immediate rollout neighborhood.

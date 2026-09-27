# Streaming bucketing and step-local rebalancing

Primary implementation documentation, read 2026-09-27:

- [Lhotse datasets](https://lhotse.readthedocs.io/en/latest/datasets.html)
  ([snapshot](../related-work/extract/lhotse2026-sampling/en/latest/datasets.md)).
- [Transformers Trainer features](https://huggingface.co/docs/transformers/main/en/trainer_recipes)
  ([snapshot](../related-work/extract/hf2026-batch-rebalance/docs/transformers/main/en/trainer_recipes.md)).

Lhotse's `DynamicBucketingSampler` estimates duration boundaries from an
initial sample, then maintains a finite buffer split among buckets. Consumed
items are replenished from the input iterable. The docs also expose
`WeightedSimpleCutSampler` with a weight per cut, and custom constraints
including token-based length measurement. These are verified separate
facilities, not evidence of one ready-made sampler satisfying all the
requested weighted and logical-step properties. Software support is not a
measured speed result in the target workload.
The weighted sampler's documented exclusion of duplicate cuts within one
batch also means it should not be described as unrestricted independent
with-replacement row sampling.

The documented Transformers `batch_rebalance` strategy sorts each optimizer
step's sample and redistributes work over devices with variable microbatch
sizes. It explicitly preserves the step's total sample count. It is relevant
as a comparator but does not solve the user's objection to starting with a
small independently drawn logical step. This is a snapshot of main docs,
not a claim about the version installed in `~/draft`.

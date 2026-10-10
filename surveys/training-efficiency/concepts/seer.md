# Seer: what remains useful a year later

Grounded reading of [arXiv v3](https://arxiv.org/html/2511.14617v3),
with its [local full-text extract](../related-work/extract/qin2025-seer/html/2511.14617v3.md).
First posted 18 November 2025; [OSDI 2026 publication](https://www.usenix.org/conference/osdi26/presentation/qin).
Assessment cutoff: 10 October 2026. See the [field map](../survey.md)
for current implementation evidence and competing approaches.

## Verdict

Seer remains a useful design for completing a fixed synchronous rollout
batch. Its full system is not established as today's best implementation,
and this search located no independent reproduction. Generic continuous
dispatch and speculative rollout support are now available in maintained
RL stacks. Same-policy chunk migration and sibling-derived scheduling
signals remain potentially additive; their incremental benefit against
those stacks has not been measured by the sources checked here.

## Scheduling uneven lengths is the central problem

The useful abstraction is “dealing with uneven length items intelligently
for full batch occupancy.” In supervised training, sequence lengths are
usually already available; in reasoning rollout they emerge during
execution. Seer estimates them using other responses to the same prompt.
The optimization target is completion of the entire rollout batch, subject
to KV-memory limits; maximizing instantaneous batch occupancy alone need
not minimize that completion time.

Its three components are separable:

1. Split prompt groups into requests and requests into bounded generation
   chunks. Move continuations between replicas using a Mooncake-backed
   global DRAM/SSD KV pool, avoiding full prefix recomputation.
2. Prioritize a probe response from each group; use completed siblings'
   maximum length to approximate longest-first scheduling. Before any
   sibling completes, use the generation ceiling as the estimate.
3. Share same-group generated text through compressed suffix trees, using
   it to propose speculative tokens. Adapt speculation to batch size,
   acceptance and priority; disable it when estimated overhead exceeds gain.

The first two improve scheduling; the third speeds individual generations
when there is insufficient useful parallel work to keep devices busy.

## The reported doubling contains several gains

Table 4's cumulative throughput multipliers, relative to the authors'
unified in-house vLLM/veRL baseline, are:

| Added component | Moonlight | Qwen2-VL-72B | Kimi-K2 |
|---|---:|---:|---:|
| Divided rollout | 1.41 | 1.42 | 1.16 |
| Context scheduling | 1.47 | 1.56 | 1.27 |
| Grouped speculation | 1.90 | 2.04 | 1.53 |

These are single-source rollout results, with the ablation on iteration
five. Workloads use 32, 128 and 256 H800s respectively, groups of 8, 16 and
8, and mean generated lengths of approximately 22K, 7.6K and 39K tokens.
The Qwen context increment is about 10% over divided rollout; speculation
adds about 31% over both scheduling components. Neither is an independent
additional doubling. The headline excludes optimizer and weight-update time.

## What would establish current value

Compare modern per-request dispatch with same-policy chunk migration,
then add the sibling length signal, then compare suffix drafts with native
multi-token prediction and an online learned drafter. Hold the generated
work and policy-version rules fixed. Measure full-step time and GPU-hours,
including KV movement, drafter maintenance and discarded/recomputed work.
For methods changing batch composition or allowing stale trajectories,
compare time to held-out quality as a separate experiment.

No such matched current-stack experiment was located. Mechanism compatibility
supports “potentially additive”; it does not establish a residual speedup.

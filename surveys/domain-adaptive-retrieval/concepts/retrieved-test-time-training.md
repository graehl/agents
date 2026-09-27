# Retrieved text as a temporary model update

Hardt and Sun, *Test-Time Training on Nearest Neighbors for Large Language
Models* (ICLR 2024): [full text](https://arxiv.org/html/2305.18466v3),
[local extract](../related-work/extract/hardt2024-ttt-nn/html/2305.18466v3.md).
Zhou, Lindqvist and Li, *Reproducibility Report* (2025):
[full text](https://arxiv.org/html/2511.16691v1),
[local extract](../related-work/extract/zhou2025-ttt-reproduction/html/2511.16691v1.md).

**Read:** original index, update, evaluation and limitations sections;
reproduction dataset coverage and results. **Evidence:** reproduced for a
subset of Pile likelihood settings, with negative model/domain cells.

The original retrieves texts from a large Pile index, trains sequentially on
neighbors and resets the model between inputs. Long neighbors may produce
multiple chunk updates. Its main retrieval query includes the evaluated text;
a separate prefix/suffix experiment bounds that concern.

The reproduction confirms improvement for GPT-2 across its selected domains,
but reports GPT-Neo degradation on EuroParl and slightly on mathematics.
Its newer reasoning-model extension covers mathematics, not a broad benchmark
of reasoning ability. Neither paper establishes persistent user adaptation or
better span annotations.

**Decision changed:** evaluate resettable downstream adaptation before
cumulative changes. Keep retrieval-prefix visibility, optimizer reset,
neighbor/chunk budgets and total latency explicit. The original index's
distributed deployment is not a single-machine CPU performance promise.

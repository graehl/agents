# Training speed, memory and cost savings

Grounded, selective field map. Search cutoff: 10 October 2026. Ten
accepted local full-text extracts from twelve manifested papers; TailSieve
and GaLore were read through primary HTML but their archival conversions
failed. Additional current implementation and paper readings are linked
below. No training experiments were run. Numeric results are authors'
measurements unless explicitly described as an independent reanalysis.
This is a bounded map, not an exhaustive ranking of 2026 training systems.

Anchors: Seer, FlashAttention-2, ZeRO, QLoRA and Chinchilla. Discovery used
their references, later papers citing the same mechanisms, arXiv, USENIX,
and official veRL/slime documentation. OpenAlex and Semantic Scholar API
queries for Seer failed through the retrieval tool; citation counts and
forward-citation saturation are unestablished. [Retrieval record](retrieval.md).

## Seer's year-later verdict

[Seer](concepts/seer.md) is still relevant, particularly when every response
must finish under the same policy before the next update. The evidence
does not establish either that its complete system remains best or that
a superior approach has subsumed all its benefits. Its components have
different prospects:

| Seer component | Current evidence | Assessment |
|---|---|---|
| Fine-grained dispatch and load balancing | Current veRL has load-balanced asynchronous request submission and partial retries | The general facility is now routine; do not expect Seer's historical gain over group-level dispatch to survive unchanged |
| Chunk migration with a shared KV pool | Current veRL's documented retry path rebuilds the cached prefix and may cross policy versions | Seer's same-policy, no-reprefill migration remains a distinct, potentially additive capability; hardware and transfer costs decide its value |
| Sibling-based online length estimation | TailSieve uses unfinished groups from earlier rounds as a tail signal and changes replica allocation | Length signals remain useful; Seer's exact probe/max estimator is one option, not an established optimum |
| Adaptive speculation at small active batches | veRL and slime expose native multi-token prediction; FastRL provides adaptive execution in a separate research implementation | Speculation is part of current practice; these docs do not establish an equivalent benefit-aware controller, so Seer's controller may still add value |
| Grouped suffix-tree drafts | TailSieve reports suffix overhead outweighing its benefit in its setup; learned and self-derived drafts now have RL measurements | A cheap workload-dependent alternative, without evidence of universal superiority or universal supersession |

The implementation evidence is concrete but is not a benchmark of Seer:
[veRL V1 async trainer](https://verl.readthedocs.io/en/latest/advance/v1_async_trainer.html)
documents synchronous, colocated-async and separate-async modes;
[slime scheduling](https://thudm.github.io/slime/advanced/rollout-scheduling.html)
distinguishes strict synchronization from partial and fully asynchronous
generation. An asynchronous API does not itself imply stale training data.
Conversely, masking the old prefix's loss does not turn a mixed-policy
trajectory into a fresh on-policy sample.

[SGLang's prefill/decode disaggregation](https://docs.sglang.ai/backend/pd_disaggregation.html)
already provides Mooncake/NIXL KV-transfer primitives. That reduces the
novelty of the plumbing, but a prefill-to-decode handoff is not arbitrary
migration of a running decoder. No measured adoption of Seer's complete
scheduler follows from the shared infrastructure.

### Later alternatives do not yield a clean winner

[TailSieve, August 2026](https://arxiv.org/html/2608.22788v1) isolates extreme
tails on low-concurrency replicas while keeping the bulk dense. This
optimizes batch completion time rather than request-count balance. Its
reported maxima are 1.67× routing-only and 2.59× with speculation, against
uniform routing on an eight-H100 server. Its “Seer-style Oracle” is a
length-aware routing proxy, not Seer's chunk migration and grouped-draft
system. It beats that proxy in most cases but not all.

TailSieve also changes batch selection: unfinished prompt identities carry
forward, responses are regenerated under the current policy, and each
update combines those with the earliest completed fresh bulk groups. That
avoids reusing stale tokens but is not Seer's contract of completing the
original fixed batch. Its 30-step GRPO timing excludes optimizer time.
These are single-source results and do not establish a matched replacement.

[Online Draft Co-Training, September 2026](https://arxiv.org/html/2609.07108v1)
trains EAGLE-3/DFlash/DSpark-style drafters alongside the policy, including
context/pipeline parallelism. Table 1 reports 1.16–1.88× full-training
speedups across its configurations against no speculation/co-training.
This is relevant evidence that speculation can help RL, but it does not
compare against Seer or isolate the gain from adaptation alone.

[EfficientRollout, September 2026 revision](https://arxiv.org/html/2606.18967v2) refreshes a
quantized draft from the current target and enables speculation according
to batch/context conditions. On eight A100-80GB GPUs, its Qwen2.5-7B
full-step latency falls from 132.6 to 111.9 seconds, a 15.6% reduction
including draft refresh. Three paired data-order seeds give a mean 14.0%
reduction with 1.5 percentage-point standard deviation and comparable
validation accuracy. Appendix F.4 attributes the improvement over the
earlier 12.7% result to removing CPU-side drafting bubbles. Its slower
history-prefix baseline is not Seer's grouped suffix method. Both newer
papers remain single-source evidence.

[TLT/FastRL](https://arxiv.org/html/2511.16665v1), posted two days after
Seer, already supplied another route: use otherwise idle rollout GPUs to
train a lightweight drafter. Its 1.7–2.1× full-step throughput result is
averaged over three measured steps after warm-up with a trained drafter.
The [maintained author implementation](https://github.com/mit-han-lab/fastrl)
advises against updating the drafter every step because of contention.
That makes drafter maintenance an empirical cost, not automatically free.

[System-Integrated Speculative Decoding, April 2026](https://arxiv.org/html/2604.26779v1)
provides a particularly relevant control: in NeMo-RL/vLLM on 32 GB200s,
Qwen3-8B variants obtain 1.35–1.41× full-step speedups with EAGLE-3, while
the model-free n-gram baseline slows down despite accepting more than two
tokens on average. Further online adaptation adds little to an already
well-initialized draft in the reported RL-Zero case. This favors measuring
the incremental value of Seer's cheap draft source rather than assuming
either neural retraining or suffix reuse wins. It does not test Seer's
same-group suffix implementation; its larger 235B projection is simulated.

### Reproduction and the updated paper

No independent reproduction or verified Seer author-code release was
located by this search. The [July OSDI version](https://www.usenix.org/system/files/osdi26-qin.pdf)
adds a 100-iteration Moonlight reward comparison: Seer tracks synchronous
veRL, while the tested partial-rollout baseline falls behind. This improves
the original authors' quality evidence; it is not independent reproduction
or proof against all staleness-controlled systems. OSDI 2026's
[artifact process](https://www.usenix.org/conference/osdi26/call-for-artifacts)
offered availability assessment, not a Results Reproduced badge.

The practical inference is to retain Seer as a source of modular
optimizations, especially same-policy work mobility and cheap group
signals. Benchmark those on the chosen current engine before adopting its
entire architecture. The old 2.04× figure is not an estimate of that
incremental gain.

## Distinguish what the saving buys

| Mechanism | Main saving | What must stay comparable |
|---|---|---|
| Packing, bucketing, continuous dispatch | Less padding or idle capacity | Sample exposure, batch composition, policy freshness |
| Fused attention and better kernels | Less memory traffic and execution overhead | Operator semantics and hardware |
| Sharding, recomputation, offload | Lower device-memory requirement | Communication/recomputation cost and usable batch size |
| Quantized frozen weights and adapters | Smaller trainable/storage state | Adaptation capacity and endpoint quality |
| Low-rank optimizer state | Smaller optimizer memory | Optimization trajectory, steps to quality, projection cost |
| Model/data compute allocation | Better quality per training FLOP | Data, optimizer and total budget |
| Routing easier subproblems to cheaper models | Less expensive-model work | End-task quality and routing/training costs |

The [existing length-aware batching survey](../length-aware-batching/survey.md)
owns known-length packing, sampling-law and logical-step issues. During
teacher-forced pretraining/finetuning, sequence lengths are normally known;
rollout scheduling instead contends with unknown future lengths and growing
KV state. The same occupancy intuition applies, with different information
and synchronization constraints.

## Pretraining: kernel speed, memory capacity and compute allocation

[FlashAttention-2](https://arxiv.org/html/2307.08691v1) reduces non-matmul
work and improves attention work partitioning after FlashAttention removed
quadratic intermediate storage. Its roughly 2× attention-kernel claim is
not 2× full training. On eight A100-80GB GPUs, Table 1's 1.3B/2K case moves
from 189 to 196 TFLOP/s/GPU versus FlashAttention-1; the 2.7B/8K case moves
from 175 to 225. These are single-source throughput measurements. The
increment depends strongly on context and the incumbent kernel.

[ZeRO](https://arxiv.org/html/1910.02054v3) removes replicated optimizer,
gradient and parameter state across data-parallel workers. The original
measured system implements optimizer/gradient sharding plus other memory
optimizations; trillion-parameter capability is an analysis, not a completed
training run. Its large speed gains concern baselines forced into costly
model parallelism, not a guaranteed increment over current sharded stacks.
Activation memory and communication still constrain the result.

[Chinchilla](https://arxiv.org/html/2203.15556v1) addresses quality per
training compute: allocate more tokens to a smaller model. The 70B model
uses 1.4T tokens at Gopher's training-compute budget. The large-model
comparison also changes optimizer, tokenizer and data mixture, so it does
not isolate allocation alone. An [independent reanalysis](https://arxiv.org/html/2404.10102v2)
finds fitting and rounding problems in one scaling-law fit while supporting
the other approaches' direction. It refits reconstructed points; it does
not retrain Chinchilla. Exact constants remain more contestable than the
general allocation lesson.

## Finetuning and optimizer memory: fitting is not speeding up

[QLoRA](https://arxiv.org/html/2305.14314v1) combines frozen 4-bit weights,
trainable adapters and optimizer paging. Its 65B-on-48GB result establishes
accessibility, not a corresponding throughput multiplier. The large-model
quality comparisons principally use 16-bit LoRA; the paper explicitly does
not establish full-finetuning equivalence at 33B/65B. It studies supervised
cross-entropy, not RL. Evidence remains single-source for those regimes.

[GaLore](https://arxiv.org/html/2403.03507v2) compresses optimizer statistics
in changing low-rank gradient subspaces while updating full weights. Its
single-device fitting result also uses 8-bit states and layer-wise updates.
Table 11 gives a useful counterexample to memory-as-speed: for LLaMA-1B,
token batch 256, layer-wise Adam8bit uses 6.93GB at 1205.31 tokens/s;
layer-wise 8-bit GaLore uses 5.63GB at 1019.63 tokens/s. Less memory accompanies
less throughput. Steps to matched quality must enter any cost comparison.

## Contested results

No checked common benchmark ranks Seer, TailSieve and the newer learned
drafters under identical policy/data semantics. Chinchilla's fitted
constants have independent methodological challenges. Neither finding
justifies declaring the underlying technique ineffective.

## Negative and quiet results

TailSieve disables suffix decoding by default after its overhead outweighs
acceptance benefits. The current [veRL MTP guide](https://verl.readthedocs.io/en/latest/advance/mtp.html)
reports a MiMo-7B/H20/SGLang case with roughly 50% lower rollout throughput
despite improved acceptance. These are configuration-specific warnings
against using acceptance rate as the objective. GaLore's table shows why
memory reduction alone also fails as a cost proxy.

## Baseline sensitivity

A fresh comparison starts with current request dispatch, fused kernels,
and an appropriately tuned memory/batch configuration. Report kernel,
rollout and full-step times separately. Include CPU/network/storage costs,
draft training, recompilation and all generated-but-unused tokens. Methods
that alter sampling, precision or policy freshness need time-to-quality
comparisons; faster tokens alone cannot establish the training saving.

## Speculation and sub-plan routing

The user's hypothesis is that sub-plan routing will eventually capture
most savings from avoiding an oversized model, with speculation retained
as a local accelerator whenever net expected cost at equal quality wins.
This is an open direction, not an outcome established by the sources here.

Exact speculative decoding preserves a chosen target distribution, whereas
routing changes which model supplies part of the answer. Predictable local
tokens can occur inside a task that still needs the large model. Thus the
two can compose; evidence of cheaper routing would not itself invalidate
speculation. For RL, changing the rollout policy or its decomposition adds
a learning-quality question beyond the serving-cost comparison.

## Coverage still open

This first map does not rank all current low-precision training, distributed
parallelism, data selection, optimizer or routing methods. Those are
expansion areas, not negative findings. [Frontier checks](frontier.md)
record the comparisons needed to upgrade the Seer verdict.

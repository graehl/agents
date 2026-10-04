# Audio domains as soft parameter selectors

Grounded extension, searched 2026-10-04. This connects
[diarization and domain identification](diarization-and-domain.md) to encoder
and decoder adaptation. The cited results are published reports, not local
reproductions; none establishes the requested end-to-end latency budget for
the proposed genre router. [Retrieval details](routing-search.md).

## Global domain and local acoustic routing already have close precedents

| Work | Mechanism and information | What it establishes; important boundary |
|---|---|---|
| [Doulaty et al., 2015](https://arxiv.org/abs/1509.02412) | Unsupervised latent-domain discovery from acoustics, used for acoustic-model adaptation | A direct historical antecedent for discovering useful domains without domain labels. Abstract-level coverage here; soft latent representation must not be assumed to mean soft neural parameter interpolation. |
| [SpeechMoE2, 2021](https://arxiv.org/abs/2111.11831) | Supervised global domain/accent embeddings join local acoustic embeddings and layer state in frame-level expert routing | Global and local evidence can coexist. Its simulated acoustic conditions and Chinese accents do not establish open-ended genre discovery. |
| [HDMoLE, 2024](https://arxiv.org/abs/2409.19878) | Global accent classifier plus local hidden-state gate, with dynamic thresholds over LoRA experts | Close precedent for soft low-rank residual mixtures and local refinement. It adds a separate accent network; parameter efficiency alone does not establish selector latency. |
| [Omni-Router, 2025; revised 2026](https://arxiv.org/abs/2507.05724) | Shared router weights across sparse expert layers, local top-one dispatch | Label-free expert specialization can help supervised ASR. Shared router weights do not imply the same decisions at every layer, nor interpretable genre experts. |
| [Shi et al., 2026](https://arxiv.org/abs/2606.10454) | Router reuses a learned mixture of speech-encoder layers; soft routing over domain projectors/LoRAs and entropy-dependent shared-expert mixing | Close precedent for encoder reuse and soft adult/child-domain adaptation. Experts are trained with hard domain assignments; this does not establish membership-weighted expert training. |

SpeechMoE2 evaluates six acoustic conditions and accent subsets using a
large supervised speech collection. Its matched active-FLOP comparisons make
it relevant to the compute question, but growing expert count also grows
resident parameters. SpeechMoE2's domain representation requires training
labels; the deployed selector itself consumes audio.

HDMoLE adapts a speech-to-language-model projector with a frozen base. Its
ablation removes the global and local routes separately, supporting their
joint use in that setting. The global route is a separately trained Conformer
accent classifier, and the quoted reduction in trainable parameters is relative
to projector fine-tuning, not total deployed memory. Better accent predictions
improve reported recognition, making routing errors a substantive bottleneck.

Omni-Router trains ASR with pseudo transcripts at much larger scale. Its
expert analysis includes acoustic and silence specialization; a useful expert
need not represent a genre. More experts do not monotonically help in its
reported comparisons, and active-parameter matching differs from total-parameter
matching. Sparse activation supplies neither free capacity nor evidence for
offloading expert weights to pinned host memory.

Shi et al. use child-speech and adult read-speech corpora, including age groups
within OGI. The resulting domains conflate age with corpus and speaking
conditions. Learned soft routing can outperform routing by the true age label:
classification correctness and expert utility are different targets. The
entropy-based shared-expert mechanism is applied to the OGI subsets; it is not
a demonstrated universal out-of-distribution fallback.

## Parameter mixtures and weighted training specify different models

For selected layer ℓ, a direct parameter mixture is

`Wℓ(x) = Wℓ,0 + Σd qℓ,d(x) ΔWℓ,d`, with nonnegative normalized memberships.

For a linear layer this equals summing weighted linear residual outputs.
It generally does not equal averaging the outputs of complete nonlinear
networks. Score or probability blending is yet another operation and may
require several complete decodes. Independently trained checkpoints are not
automatically compatible interpolation endpoints; common initialization and
aligned parameterization are relevant preconditions to test.

With LoRA, the residual mixture is `Σd qd Bd Ad`. Multiplying separately
averaged factors, `(Σd qd Bd)(Σd qd Ad)`, adds cross-expert terms and is a
different architecture. [SAML](https://arxiv.org/abs/2406.19706) deliberately
uses the latter form. It should not be silently substituted for a mixture of
complete low-rank updates. Constant utterance weights can potentially be
materialized once; changing them each frame or token changes this cost.

For fixed memberships independent of the expert parameters, backpropagating
through the direct mixture already scales each residual's gradient by its
membership. Multiplying that gradient by membership again changes the rule.
Alternatively, `Σd qd L(f_d(x), y)` trains individual experts on weighted
examples; it is not the loss of their combined model. Jointly learned routers
also receive gradients and need a defined treatment of collapse, capacity and
load balance. Uniform expert usage is not automatically appropriate for
unequal domain frequencies.

Unsupervised clusters can provide fixed responsibilities; a teacher can
provide soft labels for content, delivery or accent, optionally using text.
ASR-loss-trained routing uses recognition supervision even if there are no
domain labels. For weighted training, track expert exposure and effective
sample size, `(Σq)²/Σq²`, rather than counting every fractional example as a
full independent example. Offline weighted training and online adaptation are
separate proposals; the latter has an additional feedback problem.

## Reusing the encoder constrains where routing can act

A one-pass design can compute a shared early encoder prefix, pool its causal
states, select memberships, and condition later encoder layers or the decoder.
A router reading the completed encoder can condition the decoder immediately,
but cannot retroactively change earlier encoder states without recomputation.
This dependency is more restrictive than requiring the classifier alone to
run faster than an ordinary ASR system.

Measure incremental selector work, time until enough evidence is available,
expert computation and switching, and total recognition latency. Report
real-time factor, first-output latency and tail turn latency on the same
hardware and batch regime as the generic recognizer. A faster-than-ASR
classifier added serially can still nearly double latency. Buffering delay,
FLOPs, trainable parameters and resident memory answer different questions.

Utterance or speaker-turn membership is the cheapest initial control. Chunk
updates become useful when the condition changes within a turn; encoder-frame
and decoder-token routing then require their own causal information rules.
Per-token specialization might capture phonetic variation rather than genre.
Compare each finer route against a matched-cost pooled route, and measure
switching lag and instability before adding smoothing. This is ordinary
conditional computation, independent of a small-GPU/CPU-offloaded MoE design.

## The decisive comparison includes constant blends and recurring speakers

A parameter bank needs demonstrably complementary experts before a complicated
router has anything useful to select. Compare the generic model, a tuned
constant blend, hard and soft audio routing, and a best-expert diagnostic.
Constant or shuffled gates expose improvements due merely to extra parameters.
Match active compute and report total parameters separately. Train-fitted
centroids and all router choices must be frozen before the held-out comparison.

Accent centroids can be reused across many speakers and recordings without
speaker identification. Persistent personal state can refine that shared
prior, while session acoustics can override it. The evidence and evaluation
requirements for that hierarchy appear in
[speaker and online adaptation](speaker-online-adaptation.md).

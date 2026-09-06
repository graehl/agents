# train-then-mask — auto-ablating an everything-thrown-in model while it trains

> Read-backed digest `[G]` for ACE (cluster H, trust `single-source`), plus
> the lineage it belongs to at recall level `[R]`: nineteen papers located by
> the 2026-09-06 prior-art search, metadata checked against the arXiv API,
> none fetched or read for this survey. ACE decides which of eleven frozen
> embedding channels a shared BiLSTM-CRF keeps, while that task model keeps
> training across the search; the subset it commits to beats concatenating
> everything, and the continue-trained subset beats the same subset retrained
> from scratch. `train-then-mask` is this survey's handle, not a field term.
> graehl's framing, which the survey adopts: not a strong paper, an
> inspiring one — it jogs the memory on distillation ideas and on the
> possibility of using them before a full converged training.

**Paper.** Wang, Jiang, Bach, Wang, Huang, Huang, and Tu, "Automated
Concatenation of Embeddings for Structured Prediction," ACL-IJCNLP 2021.
**Full text:** [ACL Anthology PDF](https://aclanthology.org/2021.acl-long.206.pdf) ·
[arXiv HTML](https://arxiv.org/html/2010.05006) ·
[local extract](../related-work/extract/wang2021-ace/html/2010.05006.md).
Code: `github.com/Alibaba-NLP/ACE`. Same group as the structure-level
distillation paper in the [distilled small tagger](distilled-small-tagger.md)
digest.

## Mechanism

The task model is a BiLSTM-CRF (sequence tasks) or BiLSTM-biaffine (parsing)
over the concatenation of `L` word-representation channels. Every channel is
kept in the graph at all times; a binary mask `a ∈ {0,1}^L` zeroes the ones
not selected. Because the concatenation feeds a linear layer, zeroing channel
`l` is exactly dropping its slice `W_l` of the first weight matrix, so one task
model with one input width serves every subset, and the unused slices can be
deleted after the search. All pretrained channels are frozen; only the
task-trained character embedding channel updates.

The controller is `L` independent Bernoulli logits `θ_l` (initialized to 0,
so the first two steps sample each channel with probability one half), not
an RNN. Search runs `T = 30` steps:

1. sample a mask `a^t` (never the previous mask, never all-zero);
2. train the task model under `a^t` **starting from the parameters left by
   step `t−1`** until its schedule ends (SGD, lr 0.1, halved after 5 epochs
   without dev gain, max 150 epochs for sequence tasks), and read dev accuracy
   `R_t`;
3. update `θ` by REINFORCE with a per-channel reward
   `r^t = Σ_{i<t} (R_t − R_i) · γ^{Hamm(a^t,a^i)−1} · |a^t − a^i|`, `γ = 0.5`:
   every earlier mask votes on each channel that differs, discounted by how
   many channels differ at once;
4. record `(a^t, R_t)`, keeping the higher score if the mask recurs.

Step 1 always trains with all channels on. The deliverable is the best-dev
task model seen during the search; nothing is retrained. Cost: 45 P100
GPU-hours for 30 steps on CoNLL-2003 English NER. English candidates: ELMo,
Flair forward and backward, BERT-base, GloVe, fastText, task-trained character
embeddings, multilingual Flair forward and backward, M-BERT, XLM-R-large
(`L = 11`, 2047 subsets).

**What the baselines are.** `All` is one training run with `a` fixed to all
ones, so the first linear layer learns how much to use each channel; it is not
the exhaustive `2^L − 1` sweep. `Random` is random search with the same 30-step
budget and the same shared task model. `All+Weight` is `All` with a learned
sigmoid weight per channel and no penalty, the continuous relaxation of the
mask. `Ensemble` trains one task model per channel and votes; because outputs
can be cached, the paper *does* search all `2^L − 1` ensembles, on dev
(`Ensemble_dev`) and, as an upper bound, on test (`Ensemble_test`). `Retrain`
(Appendix B.3) trains the ACE-selected subset from scratch, three seeds for
each of three searches.

## Results

Table 1, CoNLL NER test F1 (3-run averages, no variance reported):

| system | de | en | es | nl | 23-set average, all tasks |
|---|---|---|---|---|---|
| All | 83.1 | 92.4 | 88.9 | 89.8 | 85.3 |
| Random | 84.0 | 92.6 | 88.8 | 91.9 | 85.7 |
| **ACE** | **84.2** | **93.0** | 88.9 | **92.1** | **86.2** |

Random search beats `All` on 14 of 23 test sets; ACE beats both on 21 of 23.

Table 6 and Table 12, one dataset per task (NER en, POS Ritter, AE 16Res,
CoNLL-2000 chunking, PTB parsing, DM semantic parsing):

| system | NER | POS | AE | Chunk | DP UAS/LAS | SDP ID/OOD |
|---|---|---|---|---|---|---|
| All | 92.4 | 90.6 | 73.2 | 96.7 | 96.7/95.1 | 94.3/90.8 |
| All+Weight | 92.7 | 90.4 | 73.7 | 96.7 | 96.7/95.1 | 94.3/90.7 |
| Ensemble_dev | 92.2 | 90.8 | 70.2 | 96.7 | 96.8/95.2 | 94.3/90.7 |
| Ensemble_test | 92.7 | 91.4 | 73.9 | 96.7 | 96.8/95.2 | 94.4/90.8 |
| Retrain (ACE subset from scratch) | 92.6 | 90.8 | 73.6 | 96.8 | 96.8/95.2 | 94.5/90.9 |
| **ACE** | **93.0** | **91.7** | **75.6** | **96.8** | **96.9/95.3** | **94.5/90.9** |

Three readings matter here.

1. **The soft gate without a prior is `All`.** `All+Weight` moves at most 0.5
   from `All` and never reaches ACE. A continuous relaxation on its own does
   not select channels; something has to push weights to zero or force a
   discrete commitment.
2. **The continue-trained subset beats the same subset retrained from
   scratch** on NER (+0.4), POS (+0.9) and AE (+2.0), and ties on the rest.
   The authors' explanation: "the model at each step is initialized by the
   trained model of previous step." Retrain still beats `All` everywhere, so
   the selected subset is genuinely better than everything concatenated.
3. **ACE beats the test-set-searched ensemble**, which the authors read as
   concatenation letting channels interact inside one model where voting
   cannot.
4. **The table compares a best-of-30 checkpoint with single runs.** `ACE`,
   `Random` and the search half of `Retrain` report the best-dev model over
   a 30-evaluation trajectory; `All`, `All+Weight` and each Retrain seed are
   one run evaluated once. Dev-selected best-of-30 carries an upward bias on
   test by itself, before any transfer story. The tables allow a
   decomposition: `Retrain − All` is 0.1–0.4 everywhere, which is the pure
   subset-selection effect; `ACE − Retrain` is 0–2.0, which is trajectory
   order, total training budget and best-of-N selection together. Nearly all
   of the headline gain over `All` sits in the second term, `Random` enjoys
   it too, and the controller itself adds about 0.5 over random search at
   equal budget while the reward-function ablation (Table 5, 2000-sentence
   CoNLL subset, 50 steps) separates its three variants by 0.1–0.2 with no
   variance.

With per-task fine-tuned transformers (AdamW 5e-6, 10 epochs, then frozen)
plus XLNet and RoBERTa as extra candidates and document-level context for
NER, `ACE+Fine-tune` reports state of the art on all 21 datasets. Against the
fine-tuned XLM-R that is one of its own candidates: NER de 88.3 vs. 87.7, en
94.6 vs. 94.1, nl 95.7 vs. 95.3, and es **95.9 vs. 89.3**. The Spanish gap is
ten times the others and also appears against `All+doc` (90.7); treat it as
an outlier needing reproduction before it is cited.

Which channels win (Table 13, fraction of best masks containing each): the
task-trained **character** channel is chosen in 37% of English sequence-task
winners and 33% of syntactic ones, rising to 56% for multilingual NER and 75%
for multilingual aspect extraction; XLM-R is in 100% of graph-structured
winners and 89% of multilingual NER winners; a static word vector is in 81% of
English sequence-task winners. The authors' conclusion is that no subset is
best across tasks, which is the argument for searching per task.

## The general technique and its lineage `[R]`

Field terms for the pattern ACE instantiates: **one-shot / weight-sharing
neural architecture search** (the shared task model is a *supernet* whose
sub-networks inherit its weights), **prune-during-training** or **dynamic
sparse training** at the weight level, and **structured dropout** when the
mask is random. The lineage below is recall plus the 2026-09-06 web search;
titles, authors and years were checked against the arXiv API, the papers were
not fetched, and every effectiveness statement is capped at `single-source`.
It sorts on three axes.

**What is masked.** Input channels: ACE; ModDrop (Neverova et al. 2016,
dropping whole input modalities during training so the network learns
cross-modality correlations and survives a missing one); AutoDim (Zhao et al.
2021, embedding *dimensions* per feature field in recommenders). Attention
heads: Michel et al. 2019 (most heads removable at test time) and Voita et al.
2019. Layers: LayerDrop (Fan et al. 2020). Heads, hidden and intermediate
dimensions and layers jointly: CoFi (Xia et al. 2022), Sheared LLaMA (Xia et
al. 2024), Minitron (Muralidharan et al. 2024). Individual weights: Han et
al. 2015, Zhu and Gupta 2018, Louizos et al. 2018, movement pruning (Sanh et
al. 2020), lottery tickets (Frankle and Carbin 2019), supermasks (Zhou et al.
2019). Whole operations in a cell: ENAS (Pham et al. 2018), DARTS (Liu et al.
2019), once-for-all (Cai et al. 2020).

**Who decides, and how the decision reaches the parameters.**

- *A validation reward through a discrete controller*: ACE; ENAS and the RL
  NAS line it cites. The reward is not differentiable, so the mask is a
  sample and the controller learns from the score after training.
- *A sparsity prior on continuous gates, then a threshold*: Louizos's `L0`
  penalty through hard-concrete gates; Voita's head gates under the same
  penalty, where specialized heads are pruned last; CoFi's masks at several
  granularities; movement pruning's learned scores; DARTS's softmax mixing
  weights and AutoDim's Gumbel-softmax weights, both followed by a hard
  argmax. DARTS is also the documented failure mode of this route: the
  architecture that is best under the relaxation can collapse once
  discretized (the "discretization gap").
- *A magnitude or movement score on a schedule*: Han's train-prune-retrain
  loop and Zhu and Gupta's gradual magnitude pruning, where the mask changes
  while training continues. Gale et al. 2019 report that at scale magnitude
  pruning, `L0`, and variational dropout reach about the same accuracy for a
  given sparsity, so the prior is not what buys accuracy at the weight level.
- *Random structured dropout, so that every sub-model is trained*: LayerDrop
  (prune to any depth at test time without fine-tuning), ModDrop, and
  once-for-all's progressive shrinking, which trains the largest network
  first and then fine-tunes it to support nested smaller ones.

**What happens after the commitment.** ACE's answer is "nothing": the
continue-trained model is the deliverable, and its Appendix B.3 is the
evidence that this beats retraining. The pruning literature has a graded set
of recovery steps: fine-tuning at a small learning rate (Han), rewinding the
learning-rate schedule or the weights (Renda et al. 2020 find both rewinds
beat fine-tuning), continued pretraining on a re-weighted mixture (Sheared
LLaMA), and distillation from the unpruned parent during or after pruning
(CoFi's layerwise distillation, which matches distillation-based compression
without unlabeled data; Minitron's prune-then-distill). Lottery-ticket work
asks the converse question, whether the subset would have trained as well from
its original initialization; Zhou et al. show a mask alone, over untrained
weights, already carries accuracy.

## Commentary

Recorded 2026-09-06 from graehl's reading of the paper before the full text
was in hand; the responses are the survey's, after the read and the search.

- *Whether `All` meant training every subset separately.* No. `All` is one
  model over the full concatenation. The only exhaustive sweep in the paper
  is over ensembles of single-channel models, and ACE beats even its
  test-set-searched upper bound.
- *"The mechanism reminds me of multiple-heads wisdom: you can learn from
  different-task different-labeling data by jointly training multiple heads;
  similarly, masking parts of an initially large model before task training
  could let the selected subset learn something of the pruned-away
  embeddings."* The paper's Appendix B.3 is direct evidence in that direction:
  the subset that kept training through the search beats the same subset
  trained from scratch by 0.4–2.0 points on the tasks where they differ. Two
  confounds keep it short of a demonstration. The continue-trained model has
  had up to 30 training schedules where Retrain had one, and in ACE the
  embedding channels themselves are frozen, so whatever transferred lives in
  the BiLSTM-CRF above them, not in the surviving embeddings. ModDrop is the
  closest published version of the claim itself: train with modalities
  randomly dropped so the network encodes cross-modality structure that
  remains useful when a modality is absent.
- *"A sparsifying prior over weights could characterize this in the
  objective, but they chose a discontinuous on/off controller driven by a
  delayed validation score rather than waiting for a prior to nudge
  smoothly."* Agreed on the description. The paper's own `All+Weight` row
  shows why a smooth gate is not sufficient: a per-channel sigmoid with no
  pressure toward zero stays at `All`. The prior-based route exists (`L0`
  hard-concrete gates, Voita, CoFi, AutoDim) and works on model-internal
  structure; its known risk is the DARTS discretization gap; and Gale's
  comparison suggests that at the weight level the prior does not outperform
  a magnitude schedule. Which of those carries over to eleven heterogeneous
  input channels is untested.
- *"The intuitive approach — prior, part nearly unused, hard prune, continue
  training to recover, distillation-style — was not explored in the paper."*
  Correct for ACE, and it is a well-populated cell elsewhere: CoFi distils
  from the unpruned model while the `L0` masks close, Minitron prunes then
  distils, Sheared LLaMA prunes to a target shape then continues pretraining,
  and Renda et al. measure which recovery schedule to use. None of these
  selects *input channels* for a structured-prediction model, and none
  compares its recovery against ACE-style continue-training under a
  controller. That combination is recorded as Void 3 in
  [`frontier.md`](../frontier.md).
- *"My initial feeling was that they threw an RL step in for no good reason
  when exhaustive trajectories would do probably at least as well."* At
  eleven channels (2047 subsets, about 1.5 GPU-hours per step) exhaustive is
  out of reach, which is presumably why the space was scaled to eleven; but
  the paper's own `Random` row shows the controller buying about 0.5 over
  random search at the same budget, and its reward ablation separating
  variants by 0.1–0.2. The search signal is thin by the paper's own tables.
- *"B.3 is indeed interesting if reproducible, but it is easy to obtain a bad
  and good trajectory."* Agreed, and reading 4 above is the concrete form:
  the trajectory is order-dependent, three searches are averaged without a
  spread, and the reported number is a dev-selected best-of-30 against
  single runs. The controls that would separate transfer from trajectory
  luck are in [`frontier.md`](../frontier.md): continue from the `All`
  checkpoint under the searched mask for one schedule, retrain with a matched
  epoch budget, and report the across-trajectory spread.
- *"Out of all possible architectures, imagine an everything-thrown-in
  variant and auto-ablate before full training investment on each subset."*
  Field term: one-shot or weight-sharing NAS; the everything-thrown-in variant
  is the supernet. ENAS, once-for-all and LayerDrop are the three published
  shapes of that philosophy, with different answers to whether the ablated
  sub-model needs any further training. ACE's contribution inside that family
  is small and specific: a search space where weight sharing is free because
  masking a channel is deleting a slice of one matrix, and a reward that lets
  every earlier sample vote on each channel.

## Design edge for this survey

The chars-only question has its own everything-thrown-in variant: a deep
character CNN, hashed character n-grams, hashed orthographic features, a
task-trained character embedding, and, for training only, a frozen subword
teacher channel that the deployed model must not depend on. ACE says two
things about that setup. First, whether a channel earns its place is
task-dependent and cheap to test under one shared tagger, at the price of
roughly a day of single-GPU search per dataset in ACE's regime. Second, the
tagger that trained with the discarded channels present is the one to keep,
not a fresh one trained on the survivors. What ACE does not settle is whether
a prior-gated version with hard pruning and distillation from the full model
would do the same job at a fraction of the search cost, which is the cheapest
discriminating check listed under Void 3.

Regime caveats for transfer: ACE's channels are frozen contextual encoders
with a small task model on top, its datasets are CoNLL-scale, its gains over
`All` on NER are 0.0–2.3 F1 from three-seed averages with no interval, and a
character channel selected in a third of English winners is a channel added
to word and subword vectors, not a sole encoder.

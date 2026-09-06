# Field map: tokenizer-free span tagging

> Read-backed prior art for using a character- or byte-only encoder as the
> *sole* span-tagging model, against a fine-tuned subword transformer. Sibling of
> [`surveys/shallow-surface-encoders`](../shallow-surface-encoders/survey.md),
> which covers the same surface evidence used as a *sidecar* to a strong token
> encoder rather than as a replacement for it.

## Grounding and coverage

- **Grounding mode: `grounded`.** 45 primary sources. 37 were fetched and read
  into this survey's own `related-work/extract/` (`[G]`); 8 were read from the
  sibling survey's committed extracts rather than duplicating its cache (`[S]` —
  CANINE, ByT5, Charformer, Gillick, Cao, Sun, Flair, CharacterBERT). A further
  32 citations in cluster H are recall-level (`[R]`): metadata and abstract
  checked, paper not read. Effectiveness claims are `single-source` unless a
  row says otherwise.
- **Coverage cutoff: 2026-08-16.** Search scope: ACL Anthology, arXiv (cs.CL),
  OpenAlex forward citations, and arXiv full-text search. Query terms covered
  character-level and byte-level NER, tokenizer-free and token-free models,
  sequence labeling and token classification, dilated and very deep
  convolutional taggers, hash embeddings, and knowledge distillation for
  multilingual sequence labeling.
- **Targeted intake: 2026-08-23.** Grounded the requested distillation,
  confidence-penalty, and non-negative PU papers, then read direct NER checks
  on subword pooling, constrained decoding, PU supervision, and
  linear-versus-CRF encoder heads. This targeted addition does not advance the
  broad-search cutoff above.
- **Targeted intake: 2026-09-03.** Grounded frozen task probes and a separate
  multilingual representation-probe subsurvey covering pooled sentence
  similarity, post-hoc representation mapping, frozen token alignment, and
  alignment-specific fine-tuning. This targeted addition also leaves the broad
  cutoff unchanged.
- **Targeted intake: 2026-09-06.** Added GLiNER as a label-conditioned span-head
  comparator. Its endpoint compression, negative-type sampling and greedy
  span decoding expose separate ablations; no result establishes superiority
  over a matched BIOES tagger. The broad-search cutoff is unchanged.
- **Targeted intake: 2026-09-06 (ACE).** Grounded Automated Concatenation of
  Embeddings as the seed of a train-then-mask node (cluster H) and recorded the
  pruning and one-shot-NAS lineage located by a same-day prior-art search at
  recall level. The broad-search cutoff is unchanged.
- **Anchor set:** CharNER, Gillick's byte tagger, ID-CNN, CANINE, ByT5.
  Forward citations were pulled by both recency and citation count; direct
  keyword search covered the newest uncited edge.
- **Saturation was not reached** on the applied periphery (domain-specific
  Chinese/biomedical NER citing ID-CNN, for instance). It was effectively
  reached on the question this survey exists to answer: repeated searches from
  five anchors surfaced no matched comparison of a chars-only tagger against a
  fine-tuned multilingual subword tagger, and no distillation of a large encoder
  into a character-level student.

The regenerable manifest is
[`related-work/papers.yaml`](related-work/papers.yaml); vocabulary is in
[`GLOSSARY.md`](GLOSSARY.md); the void analysis is in
[`frontier.md`](frontier.md).

## Read-backed digests

| cluster | digest | papers | decision-relevant result |
|---|---|---|---|
| A | [CoNLL yardstick](concepts/conll-yardstick.md) `[G]` | Tjong Kim Sang and De Meulder 2003 | memorization baseline 59.61 en / 30.30 de; significance width ≈ ±1 F1 |
| A | [classical char-only](concepts/char-only-classical.md) `[G]` | Klein et al. 2003 | character input worth +7.7 F1 over words in a matched HMM; the feature-rich hybrid was still ~9 F1 ahead |
| A | [CharNER](concepts/charner.md) `[G]` | Kuru et al. 2016 | chars-only, 7 languages, one config: matches or beats the best resource-free systems in 4 of 7; depth ≫ width |
| A | [char-CRF transfer](concepts/char-crf-transfer.md) `[G]` | Cotterell and Duh 2017 | at 100 sentences a feature CRF beats the neural char model by up to 8.5 F1; pooling a related language reverses it by up to +9.8 |
| B | [byte/char sole encoders](concepts/byte-sole-encoder.md) `[S]` | Gillick 2016; CANINE; ByT5 | CANINE-C −13.8 CoNLL F1 vs. mBERT without n-grams, −1.1 with; ByT5 beats mT5 on WikiAnn NER at every size; depth ≫ width again |
| B | [rendered-text encoder](concepts/rendered-text-encoder.md) `[G]` | PIXEL | subword models score exactly 0 on an uncovered script; vocabulary-free models keep 44–50 F1 there |
| B | [representation bake-off](concepts/representation-bakeoff.md) `[G]` | Rahman et al. 2023 | the published counter-thesis: NER is word-meaning-biased, so keep the subword vocabulary |
| B | [Indic tokenization](concepts/indic-tokenization.md) `[G]` | Pattnayak et al. 2025 | character input discarded on intrinsic grounds without any downstream measurement; BPE→SentencePiece alone swings zero-shot NER from 0.00 to 88.38 |
| C | [dilated CNN tagger](concepts/dilated-cnn-tagger.md) `[G]` | Strubell et al. 2017 | greedy CNN tagger matches BiLSTM-CRF F1 at 14× decoding speed |
| C | [deep char CNN](concepts/deep-char-cnn.md) `[G]` | Zhang et al. 2015; VDCNN | depth to 29 layers pays, 49 needs shortcuts; char CNNs need millions of examples — but this is classification, not tagging |
| C | [industrial hash CNN](concepts/industrial-hash-cnn.md) `[G]` | Miranda et al. 2022 | the deployed 8-layer width-96 CNN scores 0.77–0.79 on Spanish CoNLL; dropping character-derived features raises error ~50% |
| D | [char-word hybrids](concepts/char-word-hybrid.md) `[G]` | dos Santos and Guimarães; Lample; Ma and Hovy; 2025 reproduction | the character channel adds +0.7 to +3.7 F1 *on top of* word embeddings; 91.21 → 91.18 reproduced |
| E | [distilled small tagger](concepts/distilled-small-tagger.md) `[G]` | Hinton et al.; XtremeDistil; Wang et al.; Farina et al.; Nityasya et al. | foundational soft-target recipe; 35×/51× compression at 95% of teacher F1; at 100 gold sentences a 1M-parameter student beats its 220M teacher |
| F | [token-classifier objectives](concepts/token-classifier-objectives.md) `[G]` | Pereyra et al.; Kiryo et al.; Peng et al.; Ács et al.; Lester et al.; Verma et al.; Tenney et al.; Hewitt and Liang; Voita and Titov | before fine-tuning, sweep frozen layer × pooling with linear, control/selectivity, and MDL probes; constrained CE trains ~2× faster than a CRF with mostly tied F1; PU applies only to incomplete labels |
| G | [multilingual representation probes](concepts/multilingual-representation-probes.md) `[G]` | Sentence-BERT; Conneau et al.; SimAlign; Awesome-Align | pooled retrieval and token alignment test different invariances; the best layer depends on granularity/model; frozen alignment, post-hoc alignability, and alignment-tuned representations support different claims |
| F | [label-conditioned span classification](concepts/label-conditioned-span-classification.md) `[G]` | GLiNER | contextual type-marker and endpoint FFNs learn dot-product compatibility; a 12-word cap and first-subword endpoint compression need auditing for long privacy spans |
| H | [train-then-mask](concepts/train-then-mask.md) `[G]` `[R]` | Wang et al. 2021 (ACE); EarlyBERT; super tickets; pruning and one-shot-NAS lineage at recall | choosing which of 11 frozen embedding channels feed one shared BiLSTM-CRF beats concatenating all by 0.9 averaged over 23 test sets; the subset that kept training through the search beats the same subset retrained from scratch by up to 2.0; a soft per-channel gate with no sparsity pressure stays at `All` |

## Map: what each family establishes

### A. A sole character encoder has beaten strong word models before `[G]`

The oldest evidence is also the most controlled. Klein et al.'s character-emitting
HMM beat the same HMM over words by 7.7 F1 (82.2 vs. 74.5 English dev) and
placed third of sixteen in CoNLL-2003 English (86.07) and second in German
(71.90, statistically tied with the winner) while using no gazetteer and no
external tagger. CharNER then did it with one 5-layer BiLSTM configuration across
seven languages, matching or beating the best *resource-free* system in Czech,
Dutch, Spanish and Turkish and tying English. Gillick's byte tagger did it in
four languages at once, and beat the gazetteer-equipped CoNLL-2003 German winner.

None of these compared against a pretrained transformer, and CharNER and BTS both
predate them. What they establish is that the *architecture* is viable, not that
it is currently competitive.

Cotterell and Duh add the data-budget boundary: below roughly a thousand target
sentences, an unpooled neural character model loses to a feature-engineered CRF
by up to 8.5 F1, and only pooling a related language through a **shared character
network** reverses it. The character encoder is the part that transfers.

### B. Pretrained tokenizer-free encoders split on one variable: memorization `[S]` `[G]`

CANINE's NER table is the crux of this survey. Against the authors' own retrained
mBERT — same pretraining corpus, same steps — a pure character model loses
**13.8 CoNLL F1** and 6.9 MasakhaNER F1. Adding vocabulary-free hashed character
n-grams recovers all but 1.1 points and *beats* mBERT by 4.3 on the African
languages. The authors' diagnosis, supported by an error analysis (rare entity
strings missed; long entities split), is that NER rewards memorizing surface
strings and a subword vocabulary is a memorization table.

ByT5 shows the same family winning when scale and pretraining are sufficient:
byte-only beats parameter-matched mT5 on WikiAnn NER at every model size, by
+4.2 F1 at Small down to +1.3 at XL. PIXEL isolates the cause differently —
removing the vocabulary *without* going character-level reproduces the same
pattern, so much of the deficit is "no memorizable vocabulary" rather than
"characters are bad." And on the other side of the ledger, both mBERT and BERT
score exactly **0** on Amharic while the vocabulary-free models score 44.6–50.0:
a subword tagger does not degrade on an uncovered script, it fails completely.

Rahman et al. 2023 is the live counter-thesis and should be cited as such: across
133 languages they conclude that word-meaning-biased tasks (POS, NER) favour
subword models while parsing favours characters. Two caveats bound it — their
metric scores *adaptation speed* after 10 fine-tuning steps rather than converged
quality, and their character arm is CANINE-C without n-grams, i.e. the
configuration already known to lack a memorization channel.

Cao's controlled study `[S]` completes the picture from the training side: the
best character encoder-only recipe (Charformer downsampling + CANINE upsampling)
beat a matched BERT on WikiANN NER (90.65 vs. 90.29) but only when trained with
a *learnt tokenizer's* prediction targets; fully tokenizer-free masking and
targets were "particularly stark" losses on NER specifically. Removing learned
character embeddings in favour of hashing alone dropped WikiANN to 87.98.

### C. The speed case for convolution is strong and independent of the input `[G]`

ID-CNN is the canonical result: a greedy dilated-convolutional tagger matches a
BiLSTM-CRF's CoNLL-2003 F1 (90.32 vs. 90.43, inside the ±0.8 significance width)
while decoding **14.1× faster**, and beats it as a logit extractor under Viterbi
(90.54). Its argument — fixed-depth convolution is `O(1)` sequential steps
regardless of length, recurrence is `O(N)` — gets stronger at character length,
where sequences are 4–8× longer. Its ablations matter for construction: tied
iterated blocks with per-iteration losses beat untied ones by 0.84 F1, and
expectation-linear dropout regularization improved every model tested.

The deep character CNN lineage supplies the depth/width priors — VDCNN improves
monotonically from 9 to 29 layers and needs residual shortcuts past that; Zhang
et al. show char CNNs need training sets in the millions before they beat n-gram
TFIDF — but both are *text classification*, and their global pooling is exactly
what a per-position tagger cannot copy.

spaCy's shipped pipeline is the deployed-fast reference and the sobering one: 8
residual convolutional layers, window 3, width 96, over hashed `NORM`/`PREFIX`/
`SUFFIX`/`SHAPE` features — three of which are functions of the characters —
scores 0.77–0.79 F1 on Spanish CoNLL-2002 without pretrained vectors, roughly ten
points below a fine-tuned multilingual transformer. Its ablation prices the
character-derived features: dropping to word identity alone raises relative error
by ~50% overall and 100–160% on entities seen in training.

### D. Char-word hybrids are the class to distinguish from, not to cite as support `[G]`

CharWNN, Lample et al. and Ma and Hovy are the most-cited "character-level NER"
papers and all three keep a word embedding table. Their character components buy
+0.7 to +3.7 F1 *on top of* pretrained word vectors; Ma and Hovy's 91.21 English
CoNLL F1 is `reproduced` (91.18 by an independent 2025 reimplementation) and is
the right pre-transformer English reference.

The one reverse ablation in the class — CharWNN's character-only variant at 60.06
versus the hybrid's 82.21 on Spanish CoNLL-2002 — is widely read as proof that
character-only fails. It should not be: that variant has a **five-character
context window**, and CharNER's chars-only BiLSTM scored 82.18 on the same corpus,
indistinguishable from the hybrid. The ablation measured a crippled receptive
field, not the character input.

### E. Distillation is the lever that removes the character model's data problem `[G]`

Character models are consistently sample-hungry (Cotterell and Duh below 1 000
sentences; Zhang et al. needing millions; ByT5 needing 1.2–4.5× more fine-tuning
steps). Distillation converts unlabelled text into supervision and directly
attacks that.

[Hinton et al.](https://arxiv.org/abs/1503.02531) provide the durable generic
recipe: softened teacher probabilities at temperature `T`, ordinary hard-label
cross-entropy alongside them, and `T²` scaling of the soft-target term; the
transfer examples may be unlabelled. That paper is classifier-level evidence,
not BIOES evidence. The sequence-labelling papers below establish the direct
case.

XtremeDistil compresses mBERT 35× in parameters and 51× in batch-inference
latency on 41-language WikiAnn NER while keeping ~95% of teacher F1 (88.64 vs.
91.86), and its ablation shows where that comes from: hard labels alone give
71.26 (per language) or 81.44 (pooled), teacher logits add ~1.3, staged
representation-then-logits-then-labels training with gradual unfreezing adds
another ~4, and 10× more unlabelled transfer text another ~1.5. Two of its
side-results matter unusually much here: student word-embedding initialization is
worth only 1.2 F1 between the best choice and random, and parameter compression
and latency are different budgets — embedding size drives the former, hidden size
the latter.

Farina et al. give the sharpest version: with 100 gold sentences, a 1M-parameter
BiLSTM distilled from a T5-base teacher **beat both the teacher (220M) and
BERT-base (110M)** on all seven sequence-labelling datasets. Nityasya et al.
report a BiLSTM student at 3% of BERT's size, 22× faster on CPU, 3–4 F1 lower,
and conclude that recurrent and convolutional students dominate pruned
transformers on the quality-per-resource frontier. Wang et al. price the
multilingual tax that any single joint model pays: per-language teachers average
89.38 on CoNLL NER, a joint multilingual student 87.36, and their best
structure-level distillation recovers 0.4 of that ~2-point gap.

The same group's ACE (family H below) is the input-side complement to this
cluster: rather than shrinking a trained model, it decides which frozen
embedding channels one shared task model keeps while that model trains, and
its discussion names structure-level distillation as the step that would
follow to make the searched model both stronger and faster.

### F. Above XLM-R token representations, structure beats generic regularization `[G]`

Before fine-tuning, use a frozen layer × subtoken-pooling sweep to test whether
the label information is cheaply accessible. The primary diagnostic is a
regularized linear probe scored on held-out strict span F1; pair it with a
lexical-type control task and selectivity [Hewitt and
Liang](https://aclanthology.org/D19-1275/), then compare label-efficiency or
online MDL [Voita and Titov](https://aclanthology.org/2020.emnlp-main.14/).
Layer-wise probing localizes accessible information but does not establish that
the final classifier will use it [Tenney et
al.](https://aclanthology.org/P19-1452/). Plot the quantitative result as a
layer × pooling heatmap; PCA/UMAP/t-SNE clusters are exploratory, not
confirmation. The full controls and stopping rule are in the
[classifier-objective digest](concepts/token-classifier-objectives.md#frozen-pre-flight-is-task-information-usable-before-fine-tuning).

For flat word-level BIOES, start with end-to-end encoder fine-tuning, a linear
cross-entropy head, one emission per annotated word from an explicit subtoken
selection or pooling rule, and hard-constrained Viterbi decoding. BIOES does not
itself choose between first-piece and pooled word representations. In a frozen
layer-6 probe across nine WikiAnn languages, learned subword-LSTM pooling has the
best XLM-R NER macro result, but first-piece remains competitive and differences
are smaller than on morphology or POS [Ács et
al.](https://aclanthology.org/2021.eacl-main.194/). That study uses BIO and does
not fine-tune the encoder, so it supports a pooling ablation rather than a
universal head choice. [Lester et
al.](https://aclanthology.org/2020.findings-emnlp.166/)
found this decoder trained in 51.2% of the time of their optimized CRF and had
no significant F1 difference on three of four public datasets; OntoNotes was
the exception where the CRF was significantly better. Their encoder was a
BiLSTM, so the result establishes a strong decoder baseline rather than an
XLM-R guarantee.

The more directly modern comparison is mixed. With XLM-R-large on two Spanish
datasets and BioLinkBERT-large on two English biomedical datasets, a CRF beat
the linear head on SocialDisNER and LivingNER but lost on GENIA and
NCBI-Disease [Verma et
al.](https://aclanthology.org/2023.bionlp-1.24/). That study used BIO rather
than BIOES. Treat a trainable CRF as a matched ablation selected on strict dev
span F1, not as an automatic upgrade.

The two generic objective papers have narrower roles. [Pereyra et
al.](https://arxiv.org/abs/1701.06548) test confidence penalties outside NER;
uniform entropy or label-smoothing targets put mass on impossible BIOES labels,
so they are low-priority, constraint-aware ablations rather than defaults.
[Kiryo et al.](https://arxiv.org/abs/1703.00593) solve binary learning from
positive examples and an unlabeled mixture. That is relevant only when `O`
contains missed entities. The direct NER descendant intentionally reduces
incomplete dictionary supervision to binary entity-word detection rather than
BIOES [Peng et al.](https://aclanthology.org/P19-1231/), confirming that raw
nnPU is not a drop-in loss for a fully labelled structured tagger.

### G. Meaning-equivalent translations require pooled and aligned probes `[G]`

There is no single multilingual-invariance picture. At sentence or span level,
sweep layer × pooling and test whether translations or meaning-preserving
rewrites outrank hard meaning-changing controls under cosine retrieval. Report
positive-minus-negative margins, P@1/Recall@1 or MRR, and similarity
distributions. Raw mean/`CLS` BERT vectors can fail semantic cosine while
remaining useful to a fitted logistic classifier [Sentence-BERT](https://aclanthology.org/D19-1410/),
so a pooled-cosine failure rejects that readout, not every task-accessible
signal in the encoder.

Where local correspondences exist, evaluate token × token similarity matrices
against human word or span links. State how subtokens become words; report
precision, recall, F1, and alignment error rate for every layer. SimAlign finds
a roughly parabolic layer curve in frozen mBERT/XLM-R and selects layer 8 in its
tested setup [Jalili Sabet et
al.](https://aclanthology.org/2020.findings-emnlp.147/). That is evidence to
sweep layers, not a universal layer-8 rule. Free paraphrases that add, delete,
or restructure content need span or pooled tests rather than forced one-to-one
word alignment.

Keep the claim matched to what was fitted. A frozen shared encoder that passes
human-link or paired-retrieval tests is already usefully aligned. Success only
after an orthogonal mapping establishes **alignability**; Conneau et al. find
different best layers for mapped sentence retrieval and contextual transfer,
while CKA chiefly favours early layers [Conneau et
al.](https://aclanthology.org/2020.acl-main.536/). CKA is rotation-invariant, so
similar subspace geometry does not prove that paired items are near in the
original coordinates. Awesome-Align explicitly fine-tunes on parallel and
alignment objectives [Dou and
Neubig](https://aclanthology.org/2021.eacl-main.181/); its stronger links show
alignment-tunability, not what the untouched encoder already represented.
Compare candidate encoders with a fixed, externally declared language order:
an annotated, grayscale-safe encoder × language heatmap is primary; an optional
cumulative macro plus worst-tail coverage curve and a pairwise label-margin
matrix expose high-resource or European-language imbalance that one
multilingual average hides. The separate
[multilingual probe digest](concepts/multilingual-representation-probes.md)
gives those displays, the brief frozen-head scorecard, and the full claim
ladder.

### H. Train-then-mask: auto-ablate an everything-thrown-in model while it trains `[G]` `[R]`

ACE `[G]` keeps every candidate word-representation channel in the graph
(eleven for English: ELMo, Flair both directions, BERT, GloVe, fastText, a
task-trained character embedding, multilingual Flair both directions, M-BERT,
XLM-R) and lets a controller of independent per-channel Bernoulli logits mask
subsets. Because the concatenation feeds one linear layer, masking a channel is
deleting a slice of that matrix, so one BiLSTM-CRF serves all 2047 subsets and
**keeps its parameters from one search step to the next**. Each step trains to
its schedule under the sampled mask, reads dev accuracy, and updates the
controller by REINFORCE with a reward in which every earlier sample votes on
each channel that changed, discounted by how many changed at once. Thirty steps
cost 45 P100 GPU-hours on CoNLL English; the best-dev model of the search is
the deliverable, with no retraining.

The results that carry over: searched subsets beat concatenating everything
(86.2 vs. 85.3 averaged over 23 test sets; random search already gets 85.7,
and beats `All` on 14 of 23), a learned per-channel sigmoid weight *without* a
sparsity penalty stays within 0.5 of `All`, and the subset that trained
through the search beats the same subset retrained from scratch by 0.4 (NER),
0.9 (POS) and 2.0 (aspect extraction), tying elsewhere. The authors attribute
the last to each step starting from the previous step's weights; the
comparison is also a dev-selected best-of-30 checkpoint against single runs,
and the retrained subset beats `All` by only 0.1–0.4, so most of the headline
gain is trajectory, budget and selection rather than the chosen subset. Its
character channel is chosen in about a third of English sequence-task winners
and over half of multilingual NER winners, on top of word and subword
channels.

The general technique, for which `train-then-mask` is this survey's handle
and not a field term, is one-shot or weight-sharing architecture search when a
controller decides, prune-during-training when a score or a sparsity prior
decides, and structured dropout when the mask is random. The
[digest](concepts/train-then-mask.md) sorts the recall-level lineage `[R]` on
three axes — what is masked (input channels, heads, layers, widths, weights,
operations), who decides (validation reward through a discrete controller; a
sparsity prior on continuous gates then a threshold; a magnitude or movement
schedule; random drop), and what recovers the committed sub-model (nothing,
fine-tuning, rewinding, continued pretraining, distillation from the unpruned
parent). Two lineage facts bound ACE's design choice: DARTS-style continuous
relaxations are known to collapse on discretization, and at the weight level
Gale et al. found `L0` gates, variational dropout and plain magnitude pruning
reaching the same accuracy for a given sparsity.

Whether committing early pays is answered, at recall level `[R]`, by a
consistent pattern: early-bird tickets in BERT cut measured training time
35–45% at about one point of GLUE and SQuAD (EarlyBERT `[G]`, which never
runs the compute-matched full model), pruning after fine-tuning with rewinding
reports about a point of GLUE gain concentrated on the smallest tasks (super
tickets `[G]`, at nine times the compute, selecting among eight candidates on
a split of the reported dev set, with gains the size of the baseline's seed
spread), and staged random-subnetwork pretraining is 33% faster and slightly
better (RaPTr); against that, pruning at initialization stays
below post-training magnitude pruning until roughly halfway through training
(Frankle et al. 2021), proxy and weight-sharing rankings are near random (Yu
et al. 2020; White et al. 2022), and for a fixed budget training the largest
model briefly then compressing beats training the small one (Li et al. 2020).
The supported recipe is a short dense prefix until the mask stabilizes, then
commit; the [digest](concepts/train-then-mask.md#does-committing-early-pay-r)
lists the fifteen papers.

**Commentary (graehl, 2026-09-06; responses are the survey's after the read).**
The masking-while-training mechanism was read as a cousin of jointly training
multiple heads on differently labelled data: a subset selected before full
task training may retain something learned while the discarded channels were
present. ACE's retrain-versus-continue result points that way, with two
confounds the digest states (thirty schedules against one, and frozen
channels, so the transfer lives in the task model). A sparsifying prior in the
objective was proposed as the smooth alternative to ACE's delayed discrete
controller; ACE's `All+Weight` row shows a smooth gate needs that pressure to
select at all, and the prior-based route (`L0` hard-concrete gates, Voita's
head pruning, CoFi) exists for model-internal structure. The full recipe —
prior, near-unused part, hard prune, continue training with distillation to
recover — was correctly noted as absent from ACE; it is well populated in
CoFi, Minitron and Sheared LLaMA for transformer internals and unpopulated
for input-channel selection in structured prediction, which
[`frontier.md`](frontier.md) records as Void 3 with its cheapest check.

**Design decision it changes.** The chars-only proposal has its own
everything-thrown-in variant (deep character CNN, hashed n-grams, hashed
orthographic features, a task-trained character embedding, and a
training-only frozen subword channel). ACE supports deciding which survive
under one shared tagger before the expensive run, and keeping the tagger that
trained with the discarded channels present rather than a fresh one on the
survivors. Both are `single-source`, from frozen-encoder CoNLL-scale regimes
with three-seed averages and no reported interval.

## What a chars-only tagger must beat, and cite

This section exists to serve one planned contrastive: a chars-only, tokenizer-free
deep/wide CNN as the **sole** span-tagging encoder, versus a fine-tuned XLM-R
tagger.

**The number to beat is CANINE's −13.8.** Any chars-only proposal will be read
against the one matched, same-pretraining-data comparison in the literature:
pure-character CANINE-C at 74.0 CoNLL F1 versus mBERT at 87.8, and 65.5 vs. 72.4
on MasakhaNER. The claim that must be made explicitly is *what supplies the
memorization channel that CANINE-C lacked* — hashed character n-grams recovered
12.7 of those 13.8 points while staying vocabulary-free, and that is the cheapest
known answer.

**Cite, and do not conflate, these five classes.**

1. *Sole char/byte encoders* — Klein 2003, CharNER, Gillick BTS, CANINE, ByT5,
   PIXEL, Cao 2023. These are the only papers whose results are about the
   proposed system's class.
2. *Fast convolutional taggers* — ID-CNN for the speed framing and the tied
   dilated-block recipe; VDCNN and Zhang et al. for depth; spaCy for what a
   deployed small CNN actually scores.
3. *Char-word hybrids* — Lample, Ma and Hovy, CharWNN, Flair, CharacterBERT.
   Cite as the neighbouring class, and state that their character gains are
   measured on top of a word table.
4. *Distillation* — XtremeDistil, Farina et al., Wang et al., Nityasya et al.
   This is the training lever, not a result about characters.
5. *Token-head objective and decoding controls* — Pereyra, Kiryo, Peng, Ács,
   Lester, Verma. Measure subword pooling, use constrained cross-entropy and a
   CRF ablation on both encoder arms, reserve PU risk for incomplete annotations,
   and reserve confidence regularization for a diagnosed calibration problem.
6. *Channel selection under a shared task model* — ACE. Cite for the search
   recipe and the retrain-versus-continue result, not as evidence about
   characters: its character channel is a task-trained embedding added to
   word and subword vectors.

**Design commitments the literature already supports.**

- **Depth over width.** Three independent measurements agree: CharNER (depth 1→5
  at width 128: 56.27→72.19 F1; width 128→256 at depth 5: −1.7), Gillick
  (depth 1→4 at width 320: 76.15→82.13; width 320→640 at depth 4: +0.05), VDCNN
  (monotone 9→29 layers). "Deep/wide" should be read as *deep, and only as wide
  as needed*, with residual connections past ~30 layers.
- **A memorization channel, kept vocabulary-free.** Hashed character n-grams
  (CANINE), or spaCy-style hashed orthographic features, at a fixed parameter
  budget independent of vocabulary size.
- **Input-level noise regularization.** Byte dropout is worth 3.4 F1 on top of
  ordinary dropout in Gillick's byte tagger (78.76 → 82.13); CharNER reports +2
  F1 from character dropout. This is one of the largest cheap effects in the
  survey.
- **A structured decode from character positions to spans.** CharNER loses 2 F1
  replacing Viterbi over character posteriors with per-word majority voting.
  For BIOES token heads, [Lester et
  al.](https://aclanthology.org/2020.findings-emnlp.166/) show that a fixed legal
  transition mask captures most of the CRF benefit at roughly twice the
  training speed, while [Verma et
  al.](https://aclanthology.org/2023.bionlp-1.24/) show the learned CRF's F1
  advantage changes sign across datasets. Default to hard-constrained Viterbi
  and retain the CRF as an ablation. Klein's `(type, k)` state topology and
  Gillick's span triples are alternative ways to make word-level consistency a
  property of decoding.
- **Train one multilingual model, not per-language models.** Gillick's joint
  4-language model beat its per-language models by 1.1–4.8 F1; Cotterell and Duh
  show pooling a related language is worth up to +9.8 in low resource. Budget
  ~2 F1 for the joint-model capacity tax that Wang et al. measured.
- **Distill rather than train on gold alone.** The character family's documented
  weakness is sample efficiency, and the distillation cluster's documented
  strength is manufacturing supervision from unlabelled text.
- **Auto-ablate the input channels under one shared tagger, and keep that
  tagger.** ACE (`single-source`) finds that a searched channel subset beats
  the full concatenation and that the model which trained with the discarded
  channels present beats the same subset retrained from scratch. Budget the
  search (a day of single-GPU time per dataset in ACE's regime) or run the
  prior-gated variant in `frontier.md` Void 3.

**Measurements the comparison must report to be credible.**

- Per-language F1, not only an average — every paper here that broke results down
  found reversals by language (CharNER loses German and Arabic; Yu et al. hurt
  Tagalog; MasakhaNER deltas vary by 10+ F1).
- Seen versus unseen entity F1 separately. Miranda et al. found aggregate F1
  hiding an *opposite* effect on unseen entities, and unseen-entity performance is
  where a character model should win if the memorization story is right.
- Throughput and memory measured, not derived — and parameters and latency as
  separate budgets, per XtremeDistil. A character model processes 4–8× more
  positions per sentence; the CNN's `O(1)` sequential depth is what is supposed
  to pay for that, so it has to be shown.
- A significance width. CoNLL-scale test sets carry roughly ±1 F1 by bootstrap
  resampling; report the interval or the seed variance (ID-CNN's ±0.12–0.28 over
  10 restarts is the model to copy).
- The incumbent must be a genuinely fine-tuned XLM-R on the same data with the
  same label set, not a number quoted from another paper.

## Contested results

- **Does removing the tokenizer help or hurt span tagging?** ByT5 says help
  (+1.3 to +4.2 WikiAnn F1 at matched parameters); CANINE says hurt (−13.8 CoNLL
  F1) unless n-grams are added; Cao says help but only with tokenizer-derived
  training targets; Rahman et al. say hurt for word-meaning-biased tasks. The
  axis that separates them is whether the model can memorize surface strings and
  whether the subword vocabulary covers the evaluation languages — not
  characters versus bytes.
- **How much does a character component actually contribute?** +0.7 to +3.7 F1 in
  the hybrids, where a word table already exists; 7.7 F1 in Klein's matched
  word/character HMM, where it does not; ~20 F1 in CharNER's matched
  word/character BiLSTM without pretrained embeddings. The measured value of
  characters is inversely proportional to the strength of the word channel they
  are being added to.
- **Is char-only fast or slow?** ID-CNN and spaCy make convolutional taggers
  10–14× faster than recurrent-plus-Viterbi ones; CANINE's plain character
  transformer ran 10× *slower* than subword BERT, and ByT5 is 1.5–9.5× slower
  than mT5. Sequence length and architecture pull in opposite directions and both
  must be measured, never assumed.

## Negative and quiet results

- **CharNER has no successor.** Its forward citations are overwhelmingly applied
  systems that reuse it as a baseline mention; no located paper revisits
  chars-only span tagging with a modern architecture. The line went quiet after
  2017 rather than being refuted.
- **Character input is now discarded without measurement.** Pattnayak et al. 2025
  eliminate the character arm from a NER study on intrinsic proxies (sequence
  length, an implausible 40–50% "OOV rate") before any downstream evaluation.
- **Tokenizer-free *training objectives* underperform for NER specifically.**
  Cao found no combination of tokenizer-free masking and character prediction
  targets matching a tokenizer-based recipe, with the gap "particularly stark" on
  WikiANN.
- **Gazetteers can hurt a character model.** Klein et al. lost 2.0 F1 adding
  gazetteer n-grams to their emission counts, because the lists were derived from
  training data and flattened a spiked distribution.
- **Naive depth stops working.** VDCNN degrades from 29 to 49 layers without
  residual connections (35.28 → 37.41 test error, with training error rising
  too).
- **A soft channel gate without sparsity pressure does not select.** ACE's
  `All+Weight`, a learned sigmoid weight per embedding channel and no penalty,
  stays within 0.5 of plain `All` on all eight reported test sets and below
  the searched mask on all eight. The continuous relaxation helps only with a
  prior or a discretization step that forces channels off, and the
  discretization step has its own documented failure (DARTS `[R]`).

## Baseline sensitivity

Nearly every favourable chars-only number in this survey is measured against a
baseline that is weak by current standards: CoNLL-2003-era feature systems
(Klein, CharNER, Gillick), a word model with no pretrained embeddings (CharNER's
matched comparison), or a from-scratch BiLSTM (the hybrids' ablations). The two
comparisons against a *pretrained* subword model that hold the pretraining data
constant — CANINE vs. retrained mBERT, ByT5 vs. parameter-matched mT5 — disagree,
and both involve pretraining budgets far beyond a small from-scratch tagger.

ACE's search gains over concatenating everything are 0.0–2.3 F1 on the four
CoNLL NER sets, from three-seed averages with no interval, so most sit inside
the ±1 significance width. Random search at the same budget captures about
half of the average gain, and the pure subset effect (the searched subset
retrained from scratch against `All`) is 0.1–0.4; the rest is a best-of-30
dev-selected trajectory against single runs. Its headline Spanish result with fine-tuned
candidates, 95.9 against 89.3 for fine-tuned XLM-R alone, is ten times the
gain on the other three languages and should be reproduced before it is
cited.

The honest position for a chars-only CNN pilot is therefore: the literature
supports that the architecture can work and specifies how to build it (deep,
n-gram-augmented, noise-regularized, structured decode, multilingual, distilled),
supplies the speed argument, and does **not** contain a single matched comparison
against a fine-tuned multilingual subword tagger. Running that comparison is the
contribution; predicting its sign from this literature is not supported.

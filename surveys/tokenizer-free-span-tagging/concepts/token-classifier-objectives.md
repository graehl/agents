# token-classifier-objectives — what still transfers above a strong token encoder

> Read-backed digest `[G]` (cluster F, trust `single-source` each). The three
> requested classifier papers are grounded here against four direct NER checks
> and three frozen-representation probing papers. The generic papers do not
> themselves test XLM-R, BIOES, or span F1.

**Requested papers.** [Hinton, Vinyals, and Dean,
“Distilling the Knowledge in a Neural Network”](https://arxiv.org/abs/1503.02531);
[Pereyra et al., “Regularizing Neural Networks by Penalizing Confident Output
Distributions”](https://arxiv.org/abs/1701.06548); [Kiryo et al.,
“Positive-Unlabeled Learning with Non-Negative Risk
Estimator”](https://arxiv.org/abs/1703.00593).

**Direct NER checks.** [Peng et al., distantly supervised NER with PU
learning](https://aclanthology.org/P19-1231/); [Lester et al., constrained
decoding](https://aclanthology.org/2020.findings-emnlp.166/); [Verma et al.,
linear, CRF, and span heads on biomedical
NER](https://aclanthology.org/2023.bionlp-1.24/); [Ács et al., subword pooling
for mBERT and XLM-R NER](https://aclanthology.org/2021.eacl-main.194/). Full
text is cached under
`related-work/extract/`.

## Frozen pre-flight: is task information usable before fine-tuning?

No visualization alone confirms that an encoder will fine-tune well. A useful
pre-flight asks the narrower question: **does a frozen encoder expose the
target distinctions through the simple readout the planned classifier can
actually use?** Here “before fine-tuning” permits fitting a small diagnostic
readout but never updates the encoder. The probe can reject a poor layer,
pooling rule, or encoder cheaply; the matched end-to-end run remains the
confirmation.

Freeze every encoder parameter and cache representations for every layer. Use
the same annotated-token boundaries and subtoken-to-word rules intended for
the eventual BIOES model. Evaluate on held-out documents, and when surface
memorization is a deployment risk also split by entity string or lexical type.
Otherwise a probe can reward lookup of recurring names rather than contextual
boundary/type information.

The common probe stack, from least to most fitted, is:

1. **Parameter-free retrieval:** compare within-label versus between-label
   distances, nearest-neighbour label purity, and class-centroid retrieval.
   These use labeled references but no optimized classifier; they are useful
   screens only when the chosen metric is meaningful.
2. **Frozen linear probe:** fit only a regularized linear token classifier for
   each layer and pooling rule. Score strict span F1 after the same legal BIOES
   decoding planned downstream, plus boundary/type confusion and label-wise
   precision/recall. [Tenney et
   al.](https://aclanthology.org/P19-1452/) use frozen layer-wise edge probes to
   localize accessible linguistic information and show that different tasks
   peak at different depths. Their own caveat applies: success identifies
   information available to the probe, not information the final model must
   use.
3. **Control/selectivity probe:** repeat the same probe on a control task that
   assigns random labels to lexical types while preserving the task's label
   frequencies. Report selectivity—task score minus control score—alongside
   task score. [Hewitt and
   Liang](https://aclanthology.org/D19-1275/) show that a sufficiently expressive
   probe can memorize such type labels and make a representation look
   informative; higher task accuracy with low control accuracy is the desired
   pattern.
4. **Label-efficiency/MDL probe:** train the frozen linear readout on increasing
   fractions of the labeled set, plot its learning curve, and compute online
   minimum description length (MDL) or compression. [Voita and
   Titov](https://aclanthology.org/2020.emnlp-main.14/) use this to distinguish
   representations that reach similar final accuracy but require very
   different amounts of supervision to extract the information.

The compact report is a **layer × pooling heatmap** of held-out span F1, paired
with a selectivity heatmap and the label-efficiency curves for the finalists.
Add a confusion matrix for boundary/type failures and distributions of
within-label versus hard-negative similarities. A PCA, UMAP, or t-SNE plot may
expose gross clustering, lexical shortcuts, and outliers, but is descriptive:
projection choices can create or erase apparent clusters, and class separation
in two dimensions is neither necessary nor sufficient for a token classifier.

For predeclared hard confusions such as PERSON versus ORG, report a pairwise
margin rather than relying on the confusion matrix alone. With frozen
representations, use the true-class minus contrast-class prototype cosine
margin; with the linear probe, use the corresponding logit margin. Give its
median, lower decile, and fraction at or below zero per language. This reveals
an encoder that has acceptable aggregate span F1 but systematically collapses
one commercially important label distinction or language. Do not compare raw
logit margins across probes without development-set calibration or
standardization; their scales depend on the fitted weights and regularization.

Advance an encoder/layer/pooling combination when it beats label-prior,
lexical-lookup, and random/untrained-representation baselines; retains useful
selectivity; learns from few labels; and is stable over seeds and realistic
splits. A negative result is local to the probes tried—information may reside
in another layer, pooling rule, nonlinear readout, or emerge only through
fine-tuning. Keep the final test set untouched while probing: fit diagnostic
readouts on training data, select the encoder/layer/pooling rule on development
data, and evaluate the locked probe and matched final system on the test set
only in the final comparison.

## Decision for XLM-R token representations → BIOES

For flat, non-overlapping word-level spans, the recommended starting point is:

1. Fine-tune the encoder end to end. Derive one representation for every
   annotated dataset token from its associated XLM-R subtoken states, then apply
   dropout and a linear projection to the BIOES label set. The standard
   [XLM-R token-classification
   head](https://huggingface.co/docs/transformers/main/en/model_doc/xlm-roberta#transformers.XLMRobertaForTokenClassification)
   is a linear projection at each encoded position; selecting one position can
   use it directly, while pooling positions needs a small wrapper.
2. Train the word-level head with ordinary token cross-entropy. BIOES specifies
   the word-label sequence and its legal transitions; it does not specify how
   tokenizer-internal pieces become a word representation. The [Transformers
   tutorial](https://huggingface.co/docs/transformers/main/en/tasks/token_classification)
   chooses the first subtoken and assigns `-100` to continuation subtokens, but
   that is one alignment recipe for its DistilBERT/WNUT example, not comparative
   evidence that first-piece selection is best for XLM-R/BIOES. [Ács et
   al.](https://aclanthology.org/2021.eacl-main.194/) compare nine pooling rules
   on nine-language WikiAnn NER: a small subword BiLSTM has the best XLM-R macro
   result, but first-piece remains competitive and pooling differences are much
   smaller than for morphology or POS. Their encoder representations are frozen
   at layer 6 and their labels are BIO, so this is evidence to measure pooling,
   not a fine-tuned BIOES default. Compare first-piece with a parameter-free
   pooling rule, adding learned pooling when fragmentation is high. In all cases,
   form one contiguous emission sequence over the annotated tokens before
   Viterbi or CRF processing. If instead BIOES is deliberately expanded onto
   subtokens, transform `S-`, `B-`, and `E-` boundaries into a legal subtoken
   sequence rather than copying the original label unchanged to every piece.
3. Decode the emissions with Viterbi under a fixed BIOES transition mask: start
   with `O`, `S-X`, or `B-X`; allow `O`/`S-X`/`E-X` only to `O`, `S-Y`, or
   `B-Y`; allow `B-X`/`I-X` only to `I-X` or `E-X`; end only after `O`, `S-X`,
   or `E-X`. This makes legality an invariant without paying for CRF
   normalization during training.
4. Keep a trainable linear-chain CRF as a matched ablation, not an assumed
   improvement. Select between them by strict dev span F1, boundary errors,
   throughput, and seed variance.

[Lester et al.](https://aclanthology.org/2020.findings-emnlp.166/) found that
constrained Viterbi over a cross-entropy head trained in 51.2% of the time of
their optimized CRF and had no statistically significant F1 difference on
three of four public datasets; the CRF remained significantly better on
OntoNotes. Their encoders were BiLSTMs, so this supports the decoder baseline,
not a guaranteed XLM-R tie. A later comparison using XLM-R-large on two Spanish
datasets and BioLinkBERT-large on two English biomedical datasets found the CRF
better than the linear head on SocialDisNER (+1.1 F1) and LivingNER (+0.3), but
worse on GENIA (−0.4) and NCBI-Disease (−0.8) [Verma et
al.](https://aclanthology.org/2023.bionlp-1.24/). That study used BIO rather
than BIOES. The mixed result is the reason to measure the CRF rather than
install it by default.

If the task contains nested or overlapping mentions, BIOES cannot represent
the target. [Verma et al.](https://aclanthology.org/2023.bionlp-1.24/) found
their span head ahead of both token heads on all four datasets and explicitly
notes the representational limitation on overlapping mentions; that regime
requires a span or hypergraph-style classifier rather than a different BIOES
loss.

## What remains relevant from the three requested papers

### Distillation: relevant when there is a teacher, not as a default head

[Hinton et al.](https://arxiv.org/abs/1503.02531) still supplies the generic
recipe: train the student against teacher probabilities softened at temperature
`T`, combine that loss with ordinary hard-label cross-entropy at `T=1`, and
scale the soft-target term by `T²`; the transfer set may be unlabeled. For a
token classifier, teacher and student logits must be aligned to the same word
positions and label inventory. This is useful for compression, ensembles,
unlabeled transfer, or a small non-transformer student, but adds no benefit by
itself to a same-size supervised XLM-R head. Direct span-tagger evidence and
limits are in [`distilled-small-tagger`](distilled-small-tagger.md).

### Confidence penalty: low-priority and structurally mismatched if uniform

[Pereyra et al.](https://arxiv.org/abs/1701.06548) add negative output entropy
to cross-entropy, `CE − βH(p)`, and relate it to label smoothing through the
opposite direction of KL divergence. Their experiments cover image
classification, language modeling, translation, and speech recognition—not
NER or structured token classification—and gains weakened when combined with
dropout or data augmentation in some settings.

Uniform label smoothing or an entropy bonus is therefore not a BIOES best
practice. It assigns probability to labels that are illegal in the current
sequence context and spends much of its mass on the dominant `O`/boundary/type
geometry rather than on plausible confusions. If overconfidence or calibration
is an observed problem, try a small dev-tuned coefficient only as an ablation,
mask impossible labels or use a task-aware structured target, and report strict
span F1, recall, and calibration. Ordinary dropout and hard-constrained decoding
remain the simpler baseline.

### Non-negative PU risk: relevant only when “O” is not known negative

[Kiryo et al.](https://arxiv.org/abs/1703.00593) assume binary positives sampled
from the positive-class distribution, an unlabeled positive/negative mixture,
and a known or estimated positive class prior. Their non-negative estimator
clips the empirical negative-risk component that otherwise becomes negative
and lets flexible networks overfit. Those assumptions describe incomplete
dictionary or distant supervision; they do not describe a normally annotated
BIOES corpus, where `O` is a labeled class.

The direct NER descendant makes the boundary explicit. [Peng et
al.](https://aclanthology.org/P19-1231/) use dictionary-matched entity words as
positive and the remaining words as unlabeled, combine a bounded loss with
Kiryo's non-negative constraint, and evaluate four NER datasets. They
deliberately collapse the task to binary entity-word detection instead of
BIOES because a dictionary may reveal only one word of an entity. Their method
also needs an entity-word class prior and an adaptation step because dictionary
positives need not follow the full positive distribution.

Consequently, use PU risk only when annotations truly omit entities and retain
a clean fully annotated development/test set. A naive one-vs-rest nnPU loss for
every BIOES label does not preserve boundary or transition dependencies. For
ordinary fully supervised XLM-R → BIOES, use cross-entropy; for incomplete
annotations, use an NER-specific partial-label/PU formulation and state its
selection and class-prior assumptions.

## Evaluation contract

- Report exact-boundary, exact-type micro span F1 plus precision/recall by
  language and entity type; token accuracy is dominated by `O`.
- Compare greedy, hard-constrained Viterbi, and trainable CRF on identical
  encoder checkpoints or matched training budgets. Record illegal-transition
  rate before constraints so the decoder is not credited for a problem the
  encoder never has.
- Hold the BIOES decoder fixed while comparing first-piece selection against a
  parameter-free and, where warranted, learned pooled word representation;
  subtoken reduction and structured decoding are separate decisions.
- Use multiple seeds or paired bootstrap intervals for sub-F1 differences.
  Lester's 10-run distributions and Verma's sign reversal across datasets both
  make a universal “CRF wins” claim indefensible.

# industrial-hash-cnn — the deployed fast tagger, and what it pays for speed

> Read-backed digest `[G]` (cluster C, trust `single-source`). spaCy's default
> NER is an 8-layer width-96 CNN over hashed *orthographic* features. It is the
> honest reference for "what a small deployed convolutional tagger scores", and
> its feature ablation quantifies how much of that score is character-derived
> information rather than word identity.

**Paper.** Miranda, Kádár, Boyd, Van Landeghem, Søgaard, and Honnibal, "Multi
hash embeddings in spaCy," arXiv:2212.09255, 2022. **Full text:**
[arXiv HTML](https://arxiv.org/html/2212.09255) ·
[PDF](https://arxiv.org/pdf/2212.09255) ·
local extract `related-work/extract/miranda2022-spacy-hash-embed/`.

## Mechanism

Four features are extracted per token — `NORM` (normalized form), `PREFIX`,
`SUFFIX`, `SHAPE` — and each is hashed by 4 independent hash functions into its
own small table (5 000 / 2 500 / 2 500 / 2 500 rows by default). The four vectors
per table are summed; the four feature vectors are concatenated and passed
through a 3-piece Maxout layer. Then: **8 convolutional layers, window size 3,
width 96, residual connections, Maxout activations, layer normalization.**
Optionally, pretrained static vectors are added.

Three of the four features are functions of the token's characters. So spaCy's
industrial pipeline is already most of the way to a character model: it hand-
codes the character evidence (prefix, suffix, shape) that a chars-only CNN would
have to learn, and hashes the one remaining word-identity channel into 5 000
rows. The design also fixes the number of parameters independent of vocabulary
size — the same property a character alphabet gives for free.

## Evidence

**The hashing trick costs nothing measurable.** MultiHashEmbed with default table
sizes matches an exact-lookup MultiEmbed across all tested NER datasets, on both
all entities and unseen entities. Cutting the tables to 10% of the exact
lookup's rows costs nothing on Spanish CoNLL (0.77 → 0.78 dev F1) and 3 points
on a Dutch archaeology corpus (0.83 → 0.80).

**Character-derived features carry most of the signal.** Relative error increase
on Dutch CoNLL-2002 as features are removed (no pretrained vectors):

| features kept | all | seen entities | unseen entities |
|---|---|---|---|
| NORM + PREFIX + SUFFIX + SHAPE | — | — | — |
| NORM + PREFIX + SUFFIX | +17% | +0% | +15% |
| NORM + PREFIX | +30% | +80% | +26% |
| NORM only | +47% | +100% | +68% |
| ORTH only | +50% | +160% | +62% |

Dropping to word identity alone raises error by about half, and doubles-to-
triples it on entities seen in training. The paper's own conclusion is that
"subword and word shape features can be a cheap and effective way to improve
performance."

**The absolute level is the sobering part.** Spanish CoNLL-2002 dev F1 sits at
0.77–0.79 without pretrained vectors. A fine-tuned multilingual transformer on
the same corpus is roughly ten points higher. That gap — not the CoNLL-2003
90-F1 numbers from the ID-CNN literature, which use English plus GloVe — is what
a small CNN tagger actually delivers on a non-English CoNLL corpus trained from
scratch.

## Contested and negative details

- On the small AnEM biomedical corpus, removing features *lowered* error on seen
  entities while raising it on unseen ones. Aggregate F1 hid an opposite effect
  on the population that matters for generalization; the paper flags this as a
  reason to always evaluate seen and unseen entities separately.
- More than one hash function did not help on most datasets (only on the much
  larger OntoNotes, +5% F1 from three vs. one). The four-function default is
  over-provisioned.
- All results are single-language pipelines on modest corpora; there is no
  multilingual joint model and no latency table in the paper itself.

## Design edge and limits

Take the architecture spec — 8 residual conv layers, window 3, width 96, layer
norm — as a calibrated starting size for a fast tagger, and take the feature
ablation as a measurement of how much a character encoder has to earn back by
learning prefix/suffix/shape itself. Take the absolute F1 as the realistic
target band for a small non-pretrained tagger, and note the separate seen/unseen
evaluation as a requirement, not an extra.

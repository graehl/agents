# char-only-classical — the first controlled char-vs-word span tagger

> Read-backed digest `[G]` (cluster A, trust `single-source`; its shared-task
> scores are `benchmark-reported`). Klein et al. built a character-emitting HMM
> whose only input is the character stream, and measured it against the same
> model over words. The character input was worth +7.7 F1; everything the model
> lacked cost another ~9.

**Paper.** Klein, Smarr, Nguyen, and Manning, "Named Entity Recognition with
Character-Level Models," CoNLL 2003.
**Full text:** [ACL page](https://aclanthology.org/W03-0428/) ·
[PDF](https://aclanthology.org/W03-0428.pdf) ·
local extract `related-work/extract/klein2003-character-ner/`.

## Mechanism

A character-level HMM emits one character per state. Each state is a pair
`(entity type, k)` where `k` counts how long the model has been inside that type,
with a distinguished final state entered on the following space. Emissions are
type-conditional character 6-gram models with deleted-interpolation smoothing;
transitions are unsmoothed empirical estimates. Viterbi decodes the character
lattice, and the state topology — not a post-hoc constraint — is what keeps all
characters of a word inside one label.

That is a genuinely sole-encoder design: no word table, no unknown-word module,
no gazetteer. Its descendants in this survey (CharNER's Viterbi over character
tag posteriors, Gillick's byte span triples) reuse the same trick of making
word-level consistency a decoding property.

## Evidence

English development set, F1:

| model | ALL | LOC | MISC | ORG | PER |
|---|---|---|---|---|---|
| official baseline (unique-class lookup) | 71.2 | 80.5 | 83.5 | 66.4 | 55.2 |
| word-level HMM | 74.5 | 79.5 | 69.7 | 67.5 | 77.6 |
| character-level HMM, no cross-phrase context | 82.2 | 86.1 | 82.2 | 73.4 | 84.6 |
| character-level HMM, with context | 83.2 | 86.9 | 83.0 | 75.1 | 85.6 |

The word-level and context-free character-level rows are a near minimal pair:
only the entity type crosses phrase boundaries in either. Switching the input
from words to characters is worth **+7.7 F1** (74.5 → 82.2); adding cross-phrase
context on top is worth only +1.0. For a task where the word-level model is
crippled by data sparsity, the character view is the larger lever.

The paper's headline system is *not* the character-only model. A maximum-entropy
conditional Markov model that keeps the character n-gram features but adds word
identity, part-of-speech tags, letter-type patterns (`Xx`, `d-x`), previous-state
features and error-driven post-processing reaches 92.27 dev / 86.31 test in
English (the abstract quotes 86.07, the shared-task-scored figure) and 71.90
German test. So on the same data, in the same paper:

- character-only sequence model: 83.2 dev
- character n-grams inside a feature-rich word-level model: 92.27 dev

a **~9 F1 gap** that a chars-only system must close by other means. Removing the
n-gram (word-internal substring) features from the final model costs a 25% error
increase, so the character evidence is doing real work inside the hybrid too.

## Contested and negative details

- **Gazetteers hurt here.** Adding gazetteer entries to the character emission
  counts cost 2.0 F1. The supplied lists were built from the training data and
  carried a flat distribution over name phrases, so they added no coverage and
  distorted a spiked empirical distribution.
- **Substring features subsume word identity but not context.** Substring
  features alone scored 73.10 in the maxent classifier, below the character HMM
  (82.2), because the classifier had no model of the inside-phrase context the
  HMM's `(type, k)` states encode. Ablations that drop the sequence model
  understate what characters can do.
- German test F1 was 71.90 versus 86.31 English for the same system, driven by
  recall (65.04 vs. 86.49). Character models do not repair a hard language.

## Design edge and limits

The precedent to take: a *sole* character encoder plus a structured decoder
beat an equivalent word model by a wide margin as far back as 2003, and beat the
memorization baseline by 11 F1 — but the same paper's feature-rich hybrid beat
the character-only model by about 9 F1. This is the oldest and cleanest
statement of the trade this survey exists to re-test with modern capacity. Its
limits: 2003 newswire, generative n-gram emissions, English/German only.

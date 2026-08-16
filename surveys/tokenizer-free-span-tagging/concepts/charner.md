# charner — the reference chars-only multilingual span tagger

> Read-backed digest `[G]` (cluster A, trust `single-source`). CharNER is the
> closest published thing to the system this program plans: one architecture,
> characters in, span labels out, seven languages, no gazetteers, no word
> embeddings, no features. It matched or beat the best resource-free systems of
> its day in 4 of 7 languages, and its two ablations — **depth beats width** and
> **decode over characters** — are the design facts to carry forward.

**Paper.** Kuru, Can, and Yuret, "CharNER: Character-Level Named Entity
Recognition," COLING 2016. **Full text:**
[ACL page](https://aclanthology.org/C16-1087/) ·
[PDF](https://aclanthology.org/C16-1087.pdf) ·
local extract `related-work/extract/kuru2016-charner/`.

## Mechanism

Five stacked bidirectional LSTM layers, hidden size 128 each direction, over the
raw character stream of a sentence. The output is a tag distribution *per
character*, using entity types only — the `B-`/`I-` prefixes are dropped and
every character of an entity phrase, spaces included, carries that phrase's
type. A Viterbi decoder over the character posteriors, with transition
constraints, converts them into consistent word-level tags. Dropout is applied
to every layer's output *including the input layer*, which for a character model
means randomly deleting characters.

Alphabet sizes are 85–136 symbols versus 23k–64k word types; mean sequence
length is 70–173 characters versus 12–31 words.

## Evidence

Phrase-level F1, one architecture and one hyperparameter set for all seven
languages:

| system | Arabic | Czech | Dutch | English | German | Spanish | Turkish |
|---|---|---|---|---|---|---|---|
| best with external resources | 84.30 | 75.61 | 82.84 | 91.21 | 78.76 | 85.75 | 91.94 |
| best without external resources | 81.00 | 68.38 | 78.08 | 84.57 | 72.08 | 81.83 | 89.73 |
| **CharNER** | 78.72 | 72.19 | 79.36 | 84.52 | 70.12 | 82.18 | 91.30 |

Against **resource-free** systems, CharNER wins Czech (+3.81), Turkish (+1.57),
Dutch (+1.28) and Spanish (+0.35), ties English (−0.05), and loses German
(−1.96) and Arabic (−2.28). Against the **best available** systems, which use
gazetteers, pretrained embeddings or language-specific preprocessing, it is 2.6
to 8.6 F1 behind everywhere except Turkish. Note that the resource-free row for
Dutch/English/German/Spanish is Gillick et al.'s per-language byte model — the
two chars-only systems in this survey are each other's strongest comparator, and
CharNER reaches its numbers with about half the parameters.

**Same architecture, characters versus words** (best development F1, 5 layers,
width 128, no pretrained embeddings on either side):

| input | Arabic | Czech | Dutch | English | German | Spanish | Turkish |
|---|---|---|---|---|---|---|---|
| characters | 75.12 | 76.87 | 79.03 | 90.75 | 71.64 | 79.02 | 93.58 |
| words | 74.50 | 56.77 | 61.72 | 84.12 | 50.68 | 68.09 | 91.82 |

The character view wins in all seven languages, by +0.6 (Arabic) to +21.0
(German). The word-level control has no pretrained embeddings, so this is
evidence about *input sparsity*, not about characters versus a modern subword
encoder — read it as a lower bound on how much a word-indexed table hurts when
it must be learned from the task data alone.

**Depth beats width** (Czech test F1):

| depth ↓ / width → | 64 | 128 | 256 |
|---|---|---|---|
| 1 | 52.06 | 56.27 | 57.98 |
| 2 | 60.31 | 68.72 | 70.77 |
| 3 | 67.22 | 71.09 | 70.84 |
| 4 | 70.16 | 71.70 | 71.60 |
| 5 | 70.79 | 72.19 | 70.53 |

Going from one to five layers is worth ~16 F1 at width 128; going from width 128
to 256 is worth up to +1.7 when shallow and is *negative* at depth 5. Width 64 is
capacity-limited throughout. The authors' summary: "increasing the depth of the
model is more beneficial than increasing the width."

**Two cheap wins.** Dropout on the character input is worth +2 F1 absolute.
Replacing Viterbi decoding with per-character argmax plus majority voting inside
each word costs 2 F1 on Czech — the structured decode is not a formality, it is
where character-level predictions become span-level ones.

## Contested and negative details

- CharNER loses in German and Arabic, the two languages where its competitors
  used language-specific preprocessing (Arabic) or richer external data. It does
  not universally dominate even resource-free baselines.
- The comparison table mixes evaluation protocols across languages (different
  prior systems, different corpora for Czech/Turkish/Arabic). Treat the
  per-language deltas as indicative, not as a controlled sweep.
- Its "close to state of the art" claim is scoped to *resource-free* systems.
  Against 2016 systems using pretrained embeddings the gap is real, and against a
  fine-tuned multilingual transformer it is unmeasured — nobody has published
  that comparison for CharNER.

## Design edge and limits

This is the direct ancestor of the planned contrastive, and it establishes the
shape of a chars-only tagger: deep and narrow rather than shallow and wide, one
multilingual parameter set, character-level dropout as the main regularizer, and
a structured decode from character posteriors to spans. The architecture is
recurrent, so its depth argument transfers to a CNN only as a hypothesis — but
Gillick et al.'s byte model and Conneau et al.'s VDCNN reach the same conclusion
in a recurrent and a convolutional setting respectively. Its limits: 2016
baselines, no transformer comparison, no throughput measurements, and evaluation
on newswire corpora only.

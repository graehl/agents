# Label-conditioned span classification

GLiNER is a useful subword-encoder comparator for this survey's sole-tagger
question and its token-classifier objective discussion. It is not a
tokenizer-free model. Its central tradeoff is an open label inventory and
explicit span scoring instead of a fixed BIOES token head.

**Source:** Zaratiana, Tomeh, Holat and Charnois, NAACL 2024,
[GLiNER paper](https://aclanthology.org/2024.naacl-long.300.pdf),
[full-text extract](../related-work/extract/zaratiana2024-gliner/zaratiana2024-gliner.md).
Grounding: fetched with marker and read; effectiveness remains single-source.
The original paper does not establish the behavior of every later GLiNER
checkpoint or compare directly with a matched mature BIOES privacy tagger.

## Mechanism

The input contains a candidate type list, with an `[ENT]` marker before each
type name, a separator, and the text. A bidirectional language model (BiLM)
jointly contextualizes labels and text. This is one parallel encoder pass,
not autoregressive generation of entity names or locations.

The paper retains the first subword representation of each word. For a
candidate span from word i through word j, a two-layer feedforward network
projects the concatenated endpoint vectors. Another two-layer network
projects the contextual `[ENT]` vector for a type. A sigmoid of their dot
product scores the span/type pair. Binary cross-entropy on correct and
incorrect pairs trains both projections and the backbone into a compatible
coordinate system. No explicit unit-vector normalization is present in the
stated matching formula: vector magnitudes and direction both affect scores.
The paper's non-pretrained layers have width 768 and dropout 0.4.

Two endpoints represent an arbitrarily longer span, capped at 12 words in
the paper. Interior words remain encoder inputs but their vectors are omitted
from the span head; even the final word contributes its first subword rather
than its final subword. Contextual attention can convey interior information
to endpoints, but does not establish that this compression is optimal.
First/last-subword endpoints, mean/max or learned within-word pooling, and
explicit interior-span pooling are distinct cheap ablations. A 12-word cap
may be adequate for the paper's benchmarks but must be audited before use on
long addresses or other long privacy spans.

For flat output, decoding greedily selects high-scoring nonoverlapping spans
above 0.5. Its nested mode permits containment while preventing crossing
overlaps. BIOES Viterbi instead selects a globally legal sequence under its
token/transition scores. Global optimization of one score factorization
does not prove better task quality than greedy optimization of a different
factorization; greedy span selection is also separable from the span head
and could be replaced with an interval-selection dynamic program for flat
outputs. Neither formulation alone proves superiority.

## What the training augmentations change

The candidate labels are the types requested for this example, not a list of
known answers at inference. During training, positive types occur in the
annotations; sampled negative types come from other batch examples and have
no annotated instance here. A requested negative type makes all its candidate
span/type pairs negative. Annotation omissions can therefore create false
negative supervision.

For `Alice lives in Paris`, the labels might be `person, city, company`.
Company is a negative type. Shuffling makes the prefix `city, company,
person`; dropping city asks only for `person, company`. These perturb the
label inventory and associated supervision, not the sentence's words,
entity surfaces or span positions. This is not placeholder rematerialization.
The authors cap training prompts at 25 types and vary the requested set to
reduce dependence on its order, size, and every requested type being present.

Table 5 reports P/R/F1 of 49.3/58.1/53.3 with no negative types,
62.3/59.7/60.9 with 50%, and 61.1/56.5/58.6 with 75%. These are paper-local
ablation results, not generally optimal ratios. Negative-type sampling and
positive/negative loss weighting are related but separate interventions.

## Comparison that would answer the local question

The paper trains on English Pile-NER and reports multilingual transfer with
mDeBERTa, plus separate supervised in-domain experiments. Its multilingual
zero-shot model trails the separately supervised XLM-R baseline. This bounds
the claim: beating a released GLiNER on a specialized training distribution
does not establish BIOES superiority, and changing the backbone, corpus and
head simultaneously cannot identify the cause.

Compare a fixed-label span classifier and BIOES head on the same encoder,
qualified corpus, language weighting, token exposure and development search
budget. Add label conditioning as a separate arm. Keep loss-weight and
decoding choices explicit. Report exact span and boundary quality, long-span
coverage, per-language behavior, latency and memory. Label prefixes consume
context and alter jointly encoded text representations; they cannot generally
be cached independently as if they were fixed classifier weights.

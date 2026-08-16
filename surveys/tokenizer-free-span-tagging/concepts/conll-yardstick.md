# conll-yardstick — what the standard span benchmark actually pays for

> Read-backed digest `[G]` (cluster A, trust `benchmark-reported` for the shared
> task's own table). The CoNLL-2003 evaluation is the yardstick nearly every
> character-only tagger reports against, so its baseline, its spread, and its
> significance width bound what any new "chars-only beats X" claim can mean.

**Paper.** Tjong Kim Sang and De Meulder, "Introduction to the CoNLL-2003 Shared
Task: Language-Independent Named Entity Recognition," CoNLL 2003.
**Full text:** [ACL page](https://aclanthology.org/W03-0419/) ·
[PDF](https://aclanthology.org/W03-0419.pdf) ·
local extract `related-work/extract/tjongkimsang2003-conll-shared-task/`.

## The numbers that anchor every later comparison

Sixteen systems, English and German newswire, exact-span phrase F1.

| system | English test F1 | German test F1 |
|---|---|---|
| Florian et al. (best; 4-way classifier combination, gazetteers, two external NER systems) | 88.76 ± 0.7 | 72.41 ± 1.3 |
| Chieu and Ng (maximum entropy) | 88.31 ± 0.7 | 65.67 ± 1.4 |
| **Klein et al. (character-level HMM/CMM)** | **86.07 ± 0.8** | **71.90 ± 1.2** |
| Whitelaw and Patrick (character-based probabilistic) | 79.78 ± 1.0 | 54.43 ± 1.4 |
| Hammerton (LSTM, word level) | 60.15 ± 1.3 | 47.74 ± 1.5 |
| Baseline: tag phrases seen with a unique class in training | 59.61 ± 1.2 | 30.30 ± 1.3 |

Three facts in that table are load-bearing for us.

**The memorization baseline is high in English and low in German.** A system that
does nothing but replay training-set phrases with an unambiguous class scores
59.61 in English and 30.30 in German. Any claim that a model "learns entity form"
has to clear the local value of pure lookup, and that value is strongly
language-dependent — one reason English-only evidence is a poor guide to a
multilingual deployment.

**The significance width is roughly ±1 F1.** The organizers estimated
significance boundaries by bootstrap resampling (250 samples of sentences per
system output; performance A differs from B if A falls outside the central 90%
of B's distribution). Reported widths run 0.7–1.6 F1. Differences below about
one point on a CoNLL-sized test set are not results. This is the yardstick for
reading every "-1.1 F1" or "+0.4 F1" claim elsewhere in this survey.

**Two character-level systems in the same task differ by 6.3 F1 in English and
17.5 in German** (Klein 86.07 / 71.90 vs. Whitelaw 79.78 / 54.43). "Character
level" names an input, not a quality tier; the modelling and decoding around
those characters explain most of the range.

## Second-order details worth keeping

- The best English system beat the second by less than its significance
  interval, and Klein et al.'s German result was *not* significantly worse than
  the best — a character-level model was statistically tied for first in the
  harder language while using no gazetteer and no external tagger.
- Eleven of sixteen teams used information beyond the training data, all of them
  gazetteers. The organizers report gains of 5–27% error reduction from external
  data, concentrated in English where good gazetteers exist. A resource-free
  comparison and an all-resources comparison are different benchmarks.
- A majority vote of five systems reached 90.30 English / 74.17 German, i.e. the
  ceiling of the 2003 field was about 1.5–1.8 F1 above its best single system.

## Design edge and limits

Use this page as the calibration for "what a chars-only tagger must beat": on
CoNLL-sized data, a claimed gap under ~1 F1 is noise, a system that only ties the
memorization baseline has learned nothing transferable, and any comparison must
say whether external resources were available to both sides. The limit is age:
these are 2003 feature-engineered systems on newswire, so they set the floor for
a *resource-free* comparison, not the modern ceiling. Grade
`benchmark-reported` for the table (the shared task operated the evaluation and
scored submitted predictions), `single-source` for the organizers'
interpretation.

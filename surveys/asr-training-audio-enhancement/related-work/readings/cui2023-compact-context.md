**Source:** *Towards Effective and Compact Contextual Representation for Conformer Transducer Speech Recognition Systems* — [HTML](https://arxiv.org/html/2306.13307) · [arXiv](https://arxiv.org/abs/2306.13307)

# cui2023-compact-context

2026-11-21, sonnet-5.5. Purpose: cached cross-utterance encoder history in a
streaming Conformer-transducer. Read: abstract, introduction, method,
results text for Tables 1-2.

**Claims.** Preceding utterances' encoder vectors are cached; attention
pooling compresses them to 16 or 32 vectors of 512 dimensions, fed into the
encoder, and the predictor's last hidden state is cached too. Gigaspeech M
(1,000 h), streaming. Frame-level concatenation of the previous utterance
reduces WER by 0.5 / 0.4 absolute (3.0% / 2.5% relative) on dev / test;
compact pooled context similar, better with two preceding utterances; the
abstract states 0.7% to 0.5% absolute (4.3% to 3.1% relative) with the
compact method. The compact method adds 7.5% to the real-time factor over
the baseline, less than frame-level concatenation
([extract](../extract/cui2023-compact-context/html/2306.13307.md):20, 234-235).

**Means for us.** Cached encoder history is a cheap carried state: a few
percent relative gain with a modest latency increase, in a smaller setting
than Gomez-Alanis 2022 and with pooled rather than raw history.

**Not shown.** Acoustic condition as the benefit (the authors' hypothesis is
speaker, topic and acoustic-phonetic cues); noisy or telephone data.

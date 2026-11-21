**Source:** *Contextual-Utterance Training for Automatic Speech Recognition* — [HTML](https://arxiv.org/html/2210.16238v1) · [arXiv](https://arxiv.org/abs/2210.16238v1)

# gomezalanis2022-contextual-utterance

2026-11-21, sonnet-5.5. Purpose: cross-utterance acoustic context and
encoders with history. Read: abstract, method, setup, results.

**Claims.** Conformer-transducer (Amazon) trained on about 50,000 h of
far-field voice-assistant audio; the encoder is given the audio of one or
two previous (and one future) utterances along with the current one, so it
can "implicitly adapt to the speaker, topic and acoustic environment"
([extract](../extract/gomezalanis2022-contextual-utterance/html/2210.16238v1.md):9, 151).
Relative WER reduction against the same model trained without context
(Table 2, lines 184-272): non-streaming 7.6% (no context, a baseline for
that mode) up to 12.1% (one past plus one future); streaming with two
past utterances 5.4%, one past 2.9%; dual-mode (non-streaming teacher
distilled into the streaming student) 5.2% (one past), 6.3% (two past),
and over 40 ms lower emission latency.

**Means for us.** The nearest located direct evidence that history audio
helps a modern transducer, and it is a gain of a few percent relative at
large scale, obtained by re-encoding previous utterance audio (extra
compute). It is learned implicitly: no explicit channel or speaker
estimate is carried, and there is no comparison with explicit running
statistics or with adding more noise-augmented data.

**Not shown.** Whether the gain is speaker, topic or acoustic path (the
authors hypothesize; not separated); small-data or low-resource regimes;
phone-sized models.

# Evaluating speech translation with text MT metrics

**Mode: grounded, shallow first edition. Coverage cutoff: 2026-11-24.**
Scope: how the text output of a speech-to-text translation system is
scored automatically when the input is audio — which source text a
source-aware metric (COMET, MetricX) is given, how system output and
source are re-cut to the reference sentences, metrics that read the audio
directly, and what human evidence backs any of it. Excluded: speech-output
translation, simultaneous-translation latency, subtitle timing metrics,
and scoring of the transcript itself (see the draft project's
`research/speech-recognition/transcript-scoring/surveys/asr-evaluation-metrics/`).

**Retrieval.** One anchor,
[cettolo2026-sourceaware-st](related-work/readings/cettolo2026-sourceaware-st.md),
and the citations it leans on, one step out. No citation database was
queried and no forward snowball was run, so work after early 2026 and
work the anchor does not cite is missing; saturation was not reached.
The manifest is [papers.yaml](related-work/papers.yaml); per-paper notes
are in [readings/](related-work/readings/); terms are in the
[glossary](GLOSSARY.md). Grades follow `~/agents/field-map.md`. No concept
pages yet: each node below links the reading notes it rests on.

## The questions and the short answers

**Can a source-aware text metric score speech translation when there is
no human transcript?** Yes, with an ASR transcript or a back-translation
of the reference standing in for the source, as far as agreement with the
same metric fed the human transcript goes (`single-source`,
cettolo2026-sourceaware-st). Against human judgment the evidence is one
304-item set.

**Which stand-in?** An independent recognizer's transcript when its WER is
at most about 20%, otherwise a back-translation (`single-source`). Never
the transcript produced by the system being scored.

**Does it matter for COMET-22?** Hardly: COMET-22 gives nearly the same
segment scores with a shuffled source. The question is live for MetricX.

**Is a metric that hears the audio better?** Not yet shown. The best
audio-input quality estimator edges an ASR-then-text pipeline on one
human-scored set (0.509 against 0.503) and loses to text QE on the human
transcript (0.580) (`single-source`, han2024-speechqe).

**Do the findings cover direct speech-to-translation models?** The
methods consume only text output, and the anchor's six systems are half
direct. What is untested is whether text metrics are biased between
direct and cascaded systems.

## Re-cutting system output to the reference sentences

**What it is.** A system that segments the audio itself emits text whose
segments do not match the reference sentences. Edit distance between the
system's token stream and the concatenated reference, with a boundary
decision at each reference sentence end, re-cuts the output so segment
*i* can be scored against reference *i*
([matusov2005-mwersegmenter](related-work/readings/matusov2005-mwersegmenter.md);
the `mwerSegmenter` binary, and its open reimplementation `mweralign`,
[post2025-alignment](related-work/readings/post2025-alignment.md)). It is
monotone and same-language.

**Nearest confusable alternative:** forced alignment of text to audio
timestamps. Nothing here uses timestamps; the alignment is text to text
and exists only so a segment-level metric can be computed.

**Known weakness:** output tokens at a boundary that match nothing in the
reference are assigned arbitrarily.

**Effectiveness.** With COMET-22, re-cut output ranks systems about as
well as given segments do against human rankings, and far better than
BLEU on given segments, on WMT24 text MT outputs merged and re-cut —
not speech (`single-source`, post2025-alignment). On IWSLT 2023 speech
systems, chrF and COMET-22 computed on re-cut output correlate highly
with direct assessment at system level, where raters also saw re-cut
segments plus their neighbours; conditions had 2–20 well-separated
systems (`single-source`,
[sperber2024-iwslt23eval](related-work/readings/sperber2024-iwslt23eval.md)).
The two agree in direction for system ranking. Absolute COMET-22 scores
shift under re-cutting much more than BLEU does (post2025-alignment).

**Decision it changes:** system ranking on unsegmented audio is
defensible with a neural metric after re-cutting; comparing a re-cut
score with a given-segment score is not.

## A stand-in source for the metric

**What it is.** A source-aware metric scores (source, hypothesis,
reference). Without a human transcript the source is either an ASR
transcript of the audio or a back-translation of each reference segment
([cettolo2026-sourceaware-st](related-work/readings/cettolo2026-sourceaware-st.md)).

**Regime tested:** MuST-C and Europarl-ST, 79 language pairs, clean
single-speaker speech; Whisper, OWSM and SeamlessM4T as recognizers;
MADLAD and NLLB for back-translation; MetricX-24-Hybrid-XL and COMET-22.

**Effectiveness, against the same metric with the human transcript**
(segment-level Pearson; all `single-source`):

- Both stand-ins, given segments: MetricX r ≥ 0.888, COMET-22 r ≥ 0.978,
  both above the reference-only variant of the metric on average. With
  automatic segmentation the MetricX minimum is 0.814.
- ASR is the closer stand-in in 78.6% of comparisons, 87.4% when its WER
  (lowercase, no punctuation) is ≤ 20%; above 20% back-translation wins
  85.5%. With automatic audio segmentation and re-cut ASR: 61.2%, 74.7%,
  85.5%.
- System-level rank agreement exceeds 0.99 for every stand-in, so the
  choice matters only for segment-level use.

**Against humans:** on 304 Hearing-to-Translate items, COMET-22 with a
Whisper source reaches 0.5614 Pearson with direct assessment against
0.5549 with the human transcript; the stand-in variants beat
reference-only variants and three QE metrics.

**Falsifier not yet run:** a larger human-scored speech set where the
stand-in source's errors coincide with the system's.

## The source must not come from the system under test

When the ASR source is the cascade's own transcript, or the direct
model's own recognition output, agreement with the human-transcript
metric falls, most for MetricX. For a cascade the metric then scores the
translation step against the transcript it was given, and recognition
errors go uncharged (`single-source`, cettolo2026-sourceaware-st §5.1).

**Decision it changes:** when scoring how much a transcript damages its
translation, the metric's source is the human transcript or an
independent recognizer, never the transcript being judged.

## How much the metric reads its source

COMET-22 (`wmt22-comet-da`) fed a randomly shuffled source still
correlates ≥ 0.979 with its own normal scores; MetricX-24-Hybrid-XL
falls to as low as 0.4185 (`single-source`, cettolo2026-sourceaware-st
§5.1). A result about "source-aware" scoring obtained with COMET-22 is
therefore close to a reference-only result. Not checked here: xCOMET,
CometKiwi, or the larger MetricX sizes.

## Re-cutting an ASR source across languages

**What it is.** An ASR transcript of automatically segmented audio must
be cut like the *reference translation*, which is in another language.
Step one back-translates each reference segment and runs the same-language
edit-distance aligner between ASR text and back-translation. Step two,
boundary refinement, revisits each adjacent pair: holding the reference
split fixed, it moves the source split to minimise crossing word
alignments (SimAlign, mBERT) or mean LaBSE distance
(cettolo2026-sourceaware-st §3.2).

**Effectiveness.** Measured as segment-level WER of the re-cut ASR text
against the human transcript in its manual segments, which charges a
word in the wrong segment as a deletion plus an insertion. Refinement
lowers it by up to 7.08 absolute points (20.92 → 13.84, Whisper with NLLB
back-translation, Europarl-ST). The floor, the same recognizer on manual
segments, is 10.40 on Europarl-ST and 6.97 on MuST-C against 13.49 and
11.61 after refinement with MADLAD (`single-source`). The paper does not
report metric agreement with and without refinement.

**Regime:** needs a back-translation model and reference segments; a
back-translation source needs neither step, being aligned by
construction.

## Metrics that read the audio

**BLASER 2.0** embeds source speech, translation and optional reference
as one SONAR vector each and regresses a 1–5 semantic-similarity rating.
Item-level Spearman with human ratings averages 45% on SeamlessM4T
outputs; as a text metric it scores 0.711 on WMT23 Metrics against 0.825
for the best and 0.696 for BLEU (`single-source`,
[dale2024-blaser2](related-work/readings/dale2024-blaser2.md)).

**SpeechQE** attaches a speech encoder to a text LLM and trains it to
predict xCOMET and MetricX scores from audio and hypothesis. It beats
BLASER 2.0 and an ASR-then-text-QE pipeline on in-domain metric labels;
on human direct assessment 0.509 against 0.503 for Whisper large-v3 plus
CometKiwi-23, and 0.580 for text QE on the human transcript; out of
domain the pipeline is more robust (`single-source`, two language pairs,
[han2024-speechqe](related-work/readings/han2024-speechqe.md)).

**Nearest alternative:** transcribe with an independent recognizer and
use a text metric. On current evidence that is at least as good wherever
a usable recognizer exists; audio-input metrics are for unwritten
languages and for errors text cannot carry (prosody, speaker cues), which
no paper read here measures.

## Direct models, speech LLMs and cascades

All methods above take the system's text output, so they apply to any
architecture. The anchor's ASR-versus-back-translation result holds for
both its direct and its cascaded systems. In the largest comparison read
(22 systems, 16 benchmarks, English-centric, scored by reference-free
xCOMET and MetricX), cascades of a speech model and an LLM remain best
overall, two speech LLMs (Voxtral, Qwen3-Omni) match them, speech LLMs
hold up better under noise and worse on long-form audio, and standalone
direct models trail (`single-source`,
[papi2025-hearing](related-work/readings/papi2025-hearing.md)). Its
human check puts those QE metrics at about 0.5 Pearson with human scores
and unable to separate systems item by item.

## Contested results

- **Neural metrics on re-cut output.** post2025-alignment and
  sperber2024-iwslt23eval find COMET-22 reliable for system ranking after
  re-cutting; Macháček et al. 2023 (unread; cited at post2025-alignment
  :39) recommend against it because the metric was trained on whole
  sentences. sperber2024-iwslt23eval also finds COMET-22 more brittle
  than chrF when pooling across domains or target languages.
- **Audio-input versus transcribe-then-score.** han2024-speechqe argues
  end-to-end is better; cettolo2026-sourceaware-st reads the same paper
  as showing text metrics on good transcripts ahead of BLASER 2.0. Both
  hold: SpeechQE beats ASR pipelines narrowly in domain, and text on a
  human transcript beats both.

## Negative and quiet results

- COMET-22's source input is nearly inert (above).
- BLASER 2.0 as a general metric is near BLEU on WMT23.
- SpeechQE's zero-shot error-span detection loses to the pipeline.

## Baseline sensitivity

- The anchor's main criterion is agreement with the same metric on a
  human transcript, and that metric reaches only about 0.55 Pearson with
  humans on the one human-scored set. High agreement does not make the
  stand-in a good judge; it makes it the same judge.
- System-level agreement is above 0.99 for every stand-in source and
  both metrics; the ASR-versus-back-translation choice is a segment-level
  matter.
- Human-validated system rankings come from campaigns whose systems were
  far apart (sperber2024-iwslt23eval).

## Not covered

Forward citations of the anchor; the experiments of
[matusov2005-mwersegmenter](related-work/readings/matusov2005-mwersegmenter.md);
Macháček et al. 2023; xCOMET and CometKiwi source sensitivity;
subtitle-oriented alignment (SubER); LLM-judge evaluation of speech
translation.


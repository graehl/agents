# Enhancing audio for ASR training

Grounded, bounded field survey in two parts: the training question below
(searched through 2026-11-05; four primary papers) and the inference-time
question, [Does processing the input audio help a modern recognizer?](#inference-time-processing-of-the-input-audio)
(searched through 2026-11-21; sixteen further primary papers fetched and
read, then ten more in a second pass on carried state, top-down fitting,
changing conditions and augmentation). Results are `single-source` unless stated otherwise; none was
independently reproduced here. The training part covers enhancement-induced
distortion and train/test matching, not a comprehensive review of codecs,
bandwidth extension or restoration.

## Training benefit depends on what is changed at deployment

There is evidence against replacing arbitrary poor training recordings with
generically enhanced versions. There is also evidence for enhancement within
matched training/inference systems, and narrower evidence for retaining original
training audio alongside enhanced copies. Human intelligibility, perceived
quality and downstream training value are different objectives.

The distinction matters for the question motivating this survey: can processing
poor recordings make them more useful for training a recognizer that will later
receive unprocessed audio? A front end that improves recognition at inference
does not answer that question. Neither does better recognition of the processed
training files by an existing recognizer.

| Approach and grounded node | Training input | Evaluation input | Reported result and boundary |
|---|---|---|---|
| [Matched enhancement](concepts/matched-training-enhancement.md), Zorila et al. 2019 | Raw vs guided source separation | Raw or identically enhanced | CHiME-5 EVAL WER: raw/raw 59.9%; enhanced/raw 73.1%; raw/enhanced 51.6%; enhanced/enhanced 45.7%. Multichannel, annotation-assisted; training hours differ. |
| [Frozen perceptual enhancement](concepts/distortion-independent-training.md), Plantinga et al. 2021 | Noisy or enhanced | Corresponding pipeline | Voicebank test WER: noisy 3.43%; frozen spectral enhancer 3.25%; frozen spectral+phonetic-loss enhancer 2.80%. This is a front-end pipeline comparison. |
| [ASR-aware artifact reduction](concepts/artifact-noise-tradeoff.md), Iwamoto et al. 2023 | Fine-tune recognizer, enhancer, or both | Enhanced | CHiME-4 real EVAL: raw 4.8%; independent enhancement 9.4%; recognizer-only adaptation 8.8%; enhancer adaptation 3.9%; joint 3.8%. |
| [Original plus enhanced augmentation](concepts/artifact-noise-tradeoff.md), Ochiai et al. 2024 | Original, enhanced-only, or both | Raw | Simulated WSJ+CHiME: raw-only 15.9%; enhanced-only 30.5%/23.9%; combined 15.5%/14.9% for two enhancers. Combined training doubles utterances and iterations. |

These are distinct experimental systems, not comparable entries on one
leaderboard. The last row is the closest direct evidence for training-only
processing, but it does not isolate the effect from additional training.

## Artifacts can cost more than residual noise

The [artifact studies](concepts/artifact-noise-tradeoff.md) decompose enhancement
error into components attributable to reference speech/noise and a remainder
outside their span. In their tested systems, suppressing that remainder matters
more for recognition than suppressing additional residual noise. Mixing some
original observation back into enhanced audio can therefore improve recognition
even while worsening signal-to-noise measures. Reference signals are needed for
the decomposition; it is not directly a no-reference filter for arbitrary web
recordings.

The practical alternatives are to preserve original examples, tune enhancement
against recognition, or condition processing on the defect. Zorila et al.'s
low-overlap analysis illustrates the last option: a separation mask that helps
an overlap-heavy corpus can damage speech with little overlap. A single
recording-level quality score would hide this difference.

## Contested results

The located papers do not establish a direct failed replication. Their apparent
disagreement over whether enhancement helps largely changes the recognizer,
processing objective, training exposure and inference condition. Plantinga et
al. favor a frozen enhancer in their setup; Iwamoto et al. obtain their best
results by adapting enhancement with ASR loss. Neither establishes a universal
choice between frozen and joint training.

Enhancement built for human listeners need not rescue training data, which is
consistent with these distinctions. An absolute claim
that processing cannot help ASR training would exceed the evidence, particularly
the matched-system and combined-training results.

## Negative / quiet results

Wholesale enhanced-only training substantially worsens raw-test recognition in
both the CHiME-5 and simulated WSJ+CHiME comparisons. Adapting only the recognizer
does not repair the independently trained enhancer's damage in Iwamoto et al.
Plantinga et al.'s spectral enhancer also worsens test WER when attached to a
recognizer trained on noisy inputs: 3.58% versus 3.43% without enhancement.
These are reported negative conditions within successful papers; this search
does not establish that any technique was abandoned by the field.

## Baseline sensitivity

Before attributing a training improvement to enhancement, compare against
repeating the original audio for the same number of updates. Preserve speaker,
language and acoustic-domain composition when comparing dropping with repair.
Evaluate on unprocessed, held-out deployment audio; a matched-enhancement test
set answers a different question. Keep corruption repair separate: preventing
quantization loss or decoding an existing signal correctly does not require a
learned enhancer to reconstruct information.

Perceptual scores may nominate suspicious segments, but evidence here does not
justify using them as training-utility targets. The adjacent filtering evidence
is maintained in the draft repository's ASR filtering survey,
`research/speech-recognition/surveys/asr-data-filtering/survey.md`.
Candidate tests are in [frontier.md](frontier.md); the project-specific proposal
is the draft repository's
`research/speech-recognition/gaps/sketches/audio-enhancement-and-filtering.md`.

## Inference-time processing of the input audio

Question: for a large pretrained or large-supervised recognizer (Whisper,
wav2vec 2.0 and similar, Conformer or Zipformer transducers), does
processing the input audio at recognition time improve accuracy, and under
what conditions? Deployment of interest: single utterance on a phone, one
or two microphones, limited compute, lower-resource languages. Far-field
multi-microphone meeting rooms appear only as a boundary. Detail and
numbers are on the concept pages; every row cites a fetched and read paper.

**Verdict on the prior that the fitted encoder already does the work.**
Largely supported for standalone enhancement, `single-source` each but
consistent across independent groups: a denoiser or separator placed
before Whisper-class models raised WER in three studies (a separation
model on Bengali and English, a GAN denoiser on four recognizers in 40 of
40 cells, four pretrained enhancers on LibriSpeech with noise); see
[inference-time enhancement](concepts/inference-time-enhancement.md). The
mildest repair, mixing the original observation back in, only recovers to
about parity or a small gain (large-v3 14.4 to 15.5% against 15.4%
noisy). Not supported as an absolute claim: a front end trained through
the frozen recognizer's loss for a defect it had not seen (packet loss)
helped Whisper base 24.0 to 18.1% and large-v2 15.4 to 14.2%, and jointly
trained enhancement with fused noisy features helped a smaller wav2vec
2.0 model. Direct mechanistic evidence is thin: Whisper's encoder keeps
background-sound information at all depths ([Gong et al.](concepts/condition-side-information.md)),
consistent with a recognizer that infers its condition, but that result
is a probe, not an intervention.

**Operations.**

| Operation | Located evidence | Page |
|---|---|---|
| Single-channel denoising/separation | harm before Whisper-class models | [enhancement](concepts/inference-time-enhancement.md) |
| Observation adding | recovers the loss; small gain at best | [enhancement](concepts/inference-time-enhancement.md) |
| Recognizer-loss-trained front end | helps for packet loss; helps small more than large | [enhancement](concepts/inference-time-enhancement.md) |
| WPE dereverberation | harm test-side in one Thai Whisper study; no Whisper-class WPE controlled test found | [other operations](concepts/other-input-operations.md) |
| Beamforming, two channels | jointly trained front end helps a proprietary recognizer; no handset or open-model evidence | [other operations](concepts/other-input-operations.md) |
| Separation / target-speaker extraction | conditioning Whisper's encoder far outperforms masking the audio | [side information](concepts/condition-side-information.md) |
| Bandwidth extension, band-limiting | 800 to 2000 Hz extension helped Whisper (figures only); no 8 kHz result | [other operations](concepts/other-input-operations.md) |
| Codec restoration | packet-loss only; no codec-artifact test | [enhancement](concepts/inference-time-enhancement.md) |
| Loudness / gain | flat to about -40 dB for small models (figures) | [other operations](concepts/other-input-operations.md) |
| Voice-activity trimming | large effect on Whisper hallucination with long non-speech | [other operations](concepts/other-input-operations.md) |
| Speaking-rate normalization | none located for modern recognizers | gap |
| Test-time adaptation instead of changing audio | sizeable gains on a modest CTC model | [other operations](concepts/other-input-operations.md) |
| Side information about the input's condition | hybrid-era gains of 7 to 13% relative; none on pretrained encoders | [side information](concepts/condition-side-information.md) |

**Is there an audio analogue of erasing input differences for small
corpora?** One located case: Mantena et al. fold 600 h of narrowband into
3,400 h of wideband speech for a hybrid DNN. Naive mixing hurt narrowband
WER (26.2 vs 21.0 narrowband-only); upsampling to a common rate removed
most of the harm (20.9); adding a narrowband/wideband flag embedding gave
18.2, a 13% relative gain over narrowband-only
([reading](related-work/readings/mantena2019-bandwidth-embeddings.md)).
Raj et al.'s utterance-level noise vectors add 7 to 10% on hybrid models
and are complementary to multi-condition training. Both are pre-2021
hybrid systems with the condition known or estimated by a simple
classifier; none tests a pretrained encoder, and Tipaksorn et al.'s
Thai result points the other way for fixed test-side processing (training
with room-impulse augmentation beat dereverberation). No located paper
shows a normalizing transform that helps a pretrained encoder on a small
corpus; absence under these queries is not proof of absence.

**Contested and quiet.** Positive and negative enhancement results do not
contradict each other on a shared test: they differ in whether the front
end saw the recognizer's loss, whether the recognizer was adapted to its
output, and the defect (packet loss and low SNR with a small model help;
mild noise with a large model hurts). Sample gaps: Islam et al.'s English
and Bengali baselines exceed 100% WER for several models, Goswami's clean
WER is implausibly high, and the Thai study's WPE row does not say whether
the recognizer saw processed training audio; those results are weaker than
their statements.

## Carried state, top-down fitting, changing conditions, augmentation

Second inference-time pass (2026-11-21): four questions about the
deployment, each with its concept page and a verdict.

**Running analysis carried across utterances.** Supported in direction,
not shown to beat noise augmentation. Every located modern case where
information is carried helps (Conformer-transducer with previous
utterances' audio: 2.9 to 6.3% streaming, up to 12.1% non-streaming; a
1024-number speaker code fitted from one to ten minutes of unlabelled
audio: 24.4 to 19.4% WER, 20% relative; continual test-time adaptation
beats resetting for each utterance: CHiME-3 23.3 to 21.7, and 60.4 to 39.8
on a stream whose conditions change), but each baseline either lacks
history or already uses noise augmentation, so no paper tests the owner's
bet "explicit running analysis instead of augmentation". On pretrained
encoders the signal is weaker: per-utterance speaker vectors gave wav2vec
2.0 at most 6.3% and nothing at 9 and 0 dB SNR. See
[carried state](concepts/carried-state-and-adaptation.md).

**Transcript top-down.** The lineage (MLLR, fMLLR, VTS) was not fetched. Modern
forms read: confidence-selected speaker adaptation of a Conformer (9.5 to
11.3% relative on Switchboard; needs speaker-adaptive training), multi-
hypothesis entropy loss, continual adaptation with a reset detector,
and an audio-text reward instead of confidence (SUTA worse than no
adaptation on 3 of 8 noises on Whisper-Tiny). Raw confidence is a poor
guard. Original noise-aware training was read (Seltzer 2013: 13.4 to
13.1 on Aurora 4 for the noise estimate, a small gain; enhancement alone
13.8). Saon 2013 (i-vectors) stays unretrieved; its headline (about 10%
relative on Switchboard) is attested only by a second source (Wagner et al.
cite it; IBM's abstract page, not read as a paper).

**Non-stationary conditions on a handheld.** Benchmarks read measure steady
noise at fixed levels (Speech Robust Bench) or static phone positions
(BERSt: Whisper medium.en 24.9% near the body to 45.1% outside the room).
No fetched benchmark has noise events with start and end, a continuously
moving microphone, or a path switch inside a recording. See
[non-stationary and augmentation](concepts/nonstationary-and-augmentation.md).

**Narrowband and codec augmentation.** No ASR paper on band-limited or
codec-simulated copies for a modern recognizer was located and read;
nothing read gives the right mixing share, the cost on clean wideband
input, or whether generic masking covers it. The hybrid-era mixed-bandwidth
result and a Thai Whisper study (room-impulse augmentation beat test-side
dereverberation) are the nearest. On how often phone or Bluetooth paths are
band-limited, only developer documentation was found (CVSD 8 kHz fallback
exists; wideband mSBC may not be negotiated), with no share.

**Inverse direction (text to audio as an independent score).** No text-to-
speech likelihood filter was located; the nearest read result scores
candidates with CLAP, not a synthesis model.

## Retrieval and coverage

Search anchors were Zorila's explicit train/test experiment, Plantinga's
perceptual-loss comparison, and Iwamoto/Ochiai's artifact analyses. Queries
included `speech enhancement training data automatic speech recognition
retraining distortion` and `ASR enhanced training data noise reduction
observations adding enhanced speech training`, followed by exact-title primary
retrieval and reference inspection. A Semantic Scholar citation query for
arXiv:1909.12208 returned 38 citers; OpenAlex returned HTTP 429. The newest
grounded anchor is the 2024 distortion study, despite the 2026 search date.

Unresolved leads include Watanabe et al.'s *Student-Teacher Network Learning with
Enhanced Features* (ICASSP 2017), and *Audio Enhancement for Computer Audition—An
Iterative Training Paradigm Using Sample Importance* (2024). Neither contributes
a quantitative claim here. Enhancement-assisted supervision of a raw-audio
student merits a full-text follow-up. Codec restoration, clipping repair,
bandwidth extension, modern generative enhancement and large multilingual
training remain coverage gaps; no novelty or literature-saturation claim is
made for the proposed experiments.

Verified bibliography and reconstructible source provenance:
[papers.yaml](related-work/papers.yaml). Each concept page links the primary
full text and the retained extract.

### Inference-time extension (searched through 2026-11-21)

Method: web searches by operation (enhancement with Whisper, dereverberation,
bandwidth, codec, separation, voice-activity detection, test-time adaptation,
gain, noise-aware training, mixed bandwidth, conditioning), then fetch and read
of 16 papers through the shared `related-work` engine (not a citation
snowball; no OpenAlex or Semantic Scholar forward-citation pass was run, so
saturation is not claimed). Papers read: Islam 2026, Chondhekar 2025, Wang
2024, Dissen 2024, Zhu 2022, Lin 2022, Tipaksorn 2025, Liu 2024, Baranski 2025,
Polok 2024, Goswami 2026, Keskin 2021, Jeffries 2024, Mantena 2019, Raj 2020,
Gong 2023. Several results are in figures only (Liu, Jeffries) and are reported
as such.

Not fetched or not covered after the first pass (Seltzer 2013 was fetched in the
second pass, below): Saon et al. 2013 (i-vector adaptation), missing-feature recognition
and uncertainty decoding (Cooke, Raj and Stern, Deng, Astudillo), channel- or
environment-embedding work for end-to-end models, Whisper itself (Radford et
al. 2022) and robust wav2vec 2.0 (Hsu et al. 2021), SGEM (arXiv 2306.01981) and
other test-time adaptation for Whisper-class models, Whisper-based
enhancement-with-adaptation follow-ups (arXiv 2501.02452, 2403.06387, FAT-HuBERT
2311.17790), WhisperX and VAD ablations beyond Baranski, Calm-Whisper (arXiv
2505.12969), codec-artifact and speaking-rate studies for modern recognizers,
and low-resource-language evidence beyond Tipaksorn. These are leads, not
findings; search engine summaries of them are not grounded here.

### Second inference-time pass (searched through 2026-11-21)

Method: web searches per question (continual and test-time adaptation,
cross-utterance context, speaker adaptation for end-to-end models, narrowband
and codec augmentation, benchmarks for moving or event noise, Bluetooth audio
paths, text-to-audio scoring, confidence-weighted adaptation), then fetch and
read of 10 more papers: Seltzer 2013, Lin 2024 (DSUTA), Fang 2026 (ASR-TRA),
Gomez-Alanis 2022, Wagner 2022, van Dalen 2025, Deng 2023, Shah 2024 (Speech
Robust Bench), Tuttosi 2025 (BERSt), Liu 2025 (acoustic-aware augmentation).
No forward-citation search was run.

Unretrieved or unread leads: Saon et al. 2013 (i-vector adaptation; IBM
page and DOI 10.1109/ASRU.2013.6707705 only), MLLR/fMLLR/VTS originals
(Leggetter and Woodland; Gales; Moreno), IBM lattice-based MLLR (ASRU 2000),
Jha et al. confidence-based MLLR, Cui et al. 2023 compact contextual
representation (arXiv 2306.13307), cross-utterance contexts for
Conformer-transducer (arXiv 2508.10456), Zipformer with discrete-token
context (arXiv 2409.08797), DM-SUTA and DSS (EMNLP 2025 continual adaptation),
AWMC (Lee et al. 2023), SGEM (arXiv 2306.01981), STAR pseudo-label quality
(arXiv 2405.14161), FFASR far-field benchmark with moving talkers
(arXiv 2609.38897), the Hugging Face far-field leaderboard, CHiME-3, a 2026
Odyssey telephony-codec source-tracing paper (not ASR), Opus-and-ASR
speech-enhancement paper (arXiv 2309.14521), Whisper-with-bandwidth work,
Codec-ASR (arXiv 2407.03495), CTC-score transcription-quality annotation,
speech-translation filtering with model likelihoods (arXiv 2402.01945), and
Bluetooth HFP specification pages. Statements about these come from search
summaries only and are not grounded here.

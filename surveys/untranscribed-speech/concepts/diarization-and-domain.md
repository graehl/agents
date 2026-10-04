# Diarization and audio-input domain identification

Grounded survey extension, searched 2026-10-04. The question is whether audio
can select useful ASR parameters within an ordinary ASR latency budget,
including genres, delivery styles, accents and speaker characteristics.
Published effectiveness below is author-reported, not reproduced here.
Method and evaluation sections were read for the extracted papers; this is
a focused map, not a saturated review. [Search record](routing-search.md).

## Speaker identity, domain and expert choice are different variables

Diarization estimates who spoke when, usually with recording-local speaker
labels. Domain identification estimates properties of the speech or recording;
parameter routing chooses a computation. One speaker can switch from recitation
to explanation, and several speakers can share an accent or delivery style.
Overlapping speakers require simultaneous speaker activity, whereas soft domain
membership can describe a single speaker. A useful domain need not be a clean
human category: it must predict a recognition benefit from different parameters
on enough of the intended evaluation distribution to matter.

This definition permits prosody, channel and background as features. It does
not require genres to be restricted to read versus spontaneous speech, nor
require religious content to have exclusively textual evidence. Preaching,
religious reading, chant, conversation, lectures and broadcast presentation
are candidate combinations of content and delivery. Their acoustics may overlap;
the question is whether that overlap supports reliable, useful parameter choice.
Genre classification accuracy alone cannot establish the benefit.

## Diarization supplies boundaries and continuity, with distinct failure modes

The [Park et al. review](https://arxiv.org/abs/2101.09624) organizes a modular
route—speech activity, speaker embeddings, clustering and resegmentation—and
neural routes that jointly predict speaker activity. End-to-end diarization
uses multi-label frame outputs to represent overlap; attractor and hybrid
clustering approaches address variable speaker counts. Target-speaker activity
detection conditions activity estimates on speaker representations. These
families differ in how they acquire a speaker inventory and preserve it across
windows. Joint diarization/ASR can share evidence, but diarization error rate
does not determine word error rate: cuts, overlap and attribution affect them
differently. Compare collar and overlap scoring conventions before comparing
reported diarization scores.

[pyannote Community-1](https://huggingface.co/pyannote/speaker-diarization-community-1)
is a practical modular reference. Its exclusive diarization is an alternate
single-speaker timeline for alignment; it does not prove that overlapping speech
was absent. Keep physical overlap evidence if turns will supply adaptation
data. A mixed-speaker segment assigned to one profile can train the wrong
speaker parameters even when its transcript is correct.

[Streaming Sortformer](https://arxiv.org/abs/2507.18446) maintains arrival-order
speaker labels using a speaker cache and recent context. Its 2025 model predicts
up to four speakers and is trained for its streaming cache regime; imposing
that regime on an offline model is not equivalent. Its shortest reported
0.32-second buffering configuration is not end-to-end latency: compute must be
added. The [Nemotron-3 Diarization model card](https://huggingface.co/nvidia/Nemotron-3-Diarization),
released in September 2026, documents an eight-speaker successor and recommends
0.32 seconds as its lowest-latency configuration. This latter source was read
online; its local extract was rejected by the retrieval tool. Neither model's
within-stream speaker cache establishes service-wide person identity.

For routing, a separate full diarizer is optional. A dictation service with a
known user can index a profile directly. A multi-speaker stream can use
diarization to maintain session profiles. An audio router can also dispatch on
abstract accent centroids without determining who the speaker is. Reliable
cross-recording speaker linking would permit persistent individual adaptation,
but brings open-set matching and erroneous profile merges into the recognition
system's error path; see [online adaptation](speaker-online-adaptation.md).

## There are audio cues beyond speaker identity and read/nonread

[Saz, Doulaty and Hain's background-tracking genre work](https://arxiv.org/abs/1509.04934)
is a direct lead on identifying broadcast genres from nonlexical audio,
including background events. Its abstract was checked; its full methodology
was not extracted in this pass, so it supports the existence of that research
direction, not a performance recommendation. Background-derived genre may
transfer poorly across production styles even when it works within a corpus.

[Rosenberg's speaking-style study](https://www.isca-archive.org/interspeech_2011/rosenberg11_interspeech.html)
studies sequential prosodic representations for style and nativeness
classification. [Margolis, Ostendorf and Livescu](https://www.isca-archive.org/speechprosody_2010/margolis10_speechprosody.html)
study cross-genre prosody classification between radio news and conversation;
that task predicts prosodic labels, not genres or ASR expert utility. These are
abstract-level supporting leads. Pitch, energy, rhythm, pause structure and
speaking rate therefore belong among candidate features, with no claim here
that a particular preaching detector or downstream gain has been established.

Self-supervised speech features, speaker embeddings and simple prosodic
statistics offer complementary starting representations. The existing
[audio-domain representation map](audio-domain-representations.md) distinguishes
audio-only pretraining from transcript-aligned semantic representations. An
offline teacher may use an optional transcript to label content and style,
while a deployed student uses audio alone. Gold transcripts, first-pass ASR
transcripts and no transcripts are different information conditions; obtaining
a first-pass transcript must be charged to inference cost.

## Recognition utility determines whether a domain is worth retaining

Separate three tests: can the domain be identified on new recordings; does
expert performance differ conditionally on it; and can the actual router
recover enough of that difference under the latency budget? Include a generic
model, the best constant parameter blend and a routing diagnostic with known
labels. A known genre label is not an oracle for best expert choice.

Hold out speakers and sources when claiming transferable genre or accent
routing. Also evaluate recurring known speakers when claiming personalization:
that deliberately tests a different deployment population. Report both pooled
and per-condition recognition changes using the intended condition prevalence.
A rare genre with a large gain may have little aggregate value; a frequent
acoustic cluster can be useful without a satisfying semantic name.

The nearest parameter-routing precedents and the selector's computation graph
are developed in [domain-conditioned parameters](domain-conditioned-parameters.md).

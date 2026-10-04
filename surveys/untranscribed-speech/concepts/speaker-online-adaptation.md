# Streaming adaptation to speakers, users and accent centroids

Grounded extension, searched 2026-10-04. The target is a recognizer that uses
past turns to improve later turns for a session speaker or dictation user,
either by updating compact parameters or by revising a pretrained expert
mixture. Persistent cross-recording identity and shared accent centroids are
different ways to reuse history. No service or adaptation experiment was run.

## The literature supplies parts of the scheme, with different supervision

[LHUC](https://arxiv.org/abs/1601.02828), learning hidden unit contributions,
adapts compact speaker- or environment-dependent hidden-unit scales using
unsupervised adaptation data. It is a relevant lower-capacity comparator to
LoRA. This pass verified the abstract and bibliographic record, not the full
evaluation. [Confidence-based Conformer adaptation](https://arxiv.org/abs/2206.12045)
extends this family to end-to-end ASR with confidence-selected adaptation;
its abstract is a follow-up lead rather than a reproduced result here.

[Sarı et al.'s speaker memory](https://arxiv.org/abs/2002.06165) stores training
speaker i-vectors and queries a weighted combination from intermediate encoder
states, frame by frame. It needs neither a test-time speaker identity nor a
separate test-time embedding extractor. The memory remains fixed at test time;
writing new speaker representations is identified as future work. Its
speaker-change evaluation supports fast-changing conditioning, not persistent
online learning. This is a close architectural antecedent for dispatching on
shared abstract accent or acoustic centroids, although its stored items are
speaker vectors rather than learned accent prototypes.

[SAML](https://arxiv.org/abs/2406.19706) pretrains LoRA experts and a router
across speakers, then adapts both on speaker-specific data. It uses Whisper
and a Conformer attention encoder-decoder, with quantization as a separate
part of its deployment design. Its speaker train/dev/test splits are random
within speaker, and the adaptation uses annotated data. This does not establish
causal, unsupervised, each-turn adaptation. The factor-mixture equation also
differs from mixing complete LoRA residuals, as detailed in
[parameter mixtures](domain-conditioned-parameters.md#parameter-mixtures-and-weighted-training-specify-different-models).

[Vander Eeckt and Van hamme](https://arxiv.org/abs/2406.12503) directly study
unsupervised online continual ASR learning using self-generated transcripts,
unknown domain boundaries, and a stream of batches. They compare replay and
model-averaging approaches and examine pseudo-label sources. This is global
continual adaptation, not a diarization-indexed user-profile service. Their
experiments use batches of 10 or 20 utterances and evaluate task WER after
processing the stream; that does not establish next-turn latency or a
pre-update score for every arriving utterance. Their
reported failure analysis matters: pseudo labels with better average word
accuracy can still be worse adaptation targets when occasional repetitions or
weakly grounded text corrupt learning. A confidence score is therefore a
candidate filter, not proof that an update is beneficial.

## Three state scopes can coexist

| State | Key and evidence | What can persist |
|---|---|---|
| Shared accent/acoustic prototypes | Audio similarity and recognition utility across speakers | Pretrained experts, centroids and shared routing prior |
| Session speaker | Diarization track within a recording/session | Accumulated embeddings, router offsets, accepted pseudo-label history, optional adapter |
| Persistent individual | Known dictation-user key or reliable open-set speaker linking | Cross-session personal residual, experience count and uncertainty |

A useful candidate is hierarchical shrinkage: start from the generic model
and soft accent-centroid memberships, then allow supported personal history to
adjust the route or a small residual. A new microphone or speaking style can
change session conditioning while retaining only the stable portion of personal
state. These are design inferences, not a configuration validated by the cited
papers. They do not require every accent centroid to correspond to a named
geographic accent; credibility comes from reproducible matching and downstream
utility across new speakers.

Updating a centroid posterior is unsupervised inference. Updating router
offsets, selection thresholds or temperature by a pseudo-transcript loss is
online learning. Neither should be described as learning the best expert
without an objective that carries information about recognition quality.
Thresholds also change expert count and compute; adaptation can improve a
loss merely by selecting more experts unless the comparison controls that cost.

## Each-turn adaptation needs a causal evaluation

For turn `t`, recognize using the state available before that turn (plus
permitted causal audio-prefix conditioning), score that output, then update
state for turn `t+1`. Adapt-and-redecode on the same turn is a separate protocol
whose extra pass must be charged. A user correction is useful supervision but
does not belong in the unsupervised arm.

Start with fixed experts and update only a small mixture prior or router bias.
Compare that with a similarly sized LHUC or LoRA update, a no-update profile,
and stateless accent routing. Freeze the base and retain an explicit route
back to it. Test pseudo-label filtering, regularization toward the prior,
bounded history and reversible update checkpoints as mechanisms to evaluate,
not a promise that self-training cannot drift. Background learning still
consumes throughput and can miss the next turn's deadline.

For diarized sessions, test label swaps, overlap, short turns and new-speaker
arrival. An uncertain speaker assignment should not silently write strongly
to a persistent individual profile. Across recordings, open-set recognition
must allow “unknown”; false merges contaminate another person's state, while
false splits mostly lose accumulated benefit. A high within-recording
diarization score does not measure this tradeoff, especially as the candidate
population grows. A known dictation-user key avoids the acoustic identity
search, though shared accounts remain an evaluation condition.

Report chronological learning curves by accumulated speech, recurring versus
new speakers, within-session versus later-recording transfer, and recovery
after a deliberately wrong update or changed channel. Score every turn before
learning from it. Attribute gains separately to shared accent dispatch,
session continuity and persistent personal learning. The required evidence is
recognition quality and latency on future turns, not lower loss on the
pseudo labels that generated the update.

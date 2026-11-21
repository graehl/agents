**Source:** *Beyond Fresh Starts: Stateful Inference for Streaming ASR in Conversational Voice Agents* — [HTML](https://arxiv.org/html/2608.22101) · [arXiv](https://arxiv.org/abs/2608.22101)

# chattopadhyay2026-fresh-starts

2026-11-21, sonnet-5.5. Purpose: carrying encoder state across turns in a
modern streaming transducer. Read: abstract, introduction, study design,
results text; Table 1 cells were not transcribed.

**Claims.** Cache-aware FastConformer-RNNT streaming models (fastconformer-114m
and nemotron-streaming-0.6b) evaluated on the CallHome and Switchboard test
sets (telephone dialogue). Strategies: Fresh Start (reset the encoder state at
every turn, the common practice in voice agents), continuous streaming, State
Carry-over (use the previous turn's final state, skipping silences), and State
Rollback (roll back to the state of the last substantial turn when the previous
turn was shorter than k tokens, to drop backchannels). The best method "yields
an average of 15-21% relative WER reduction at utterance onsets"
([extract](../extract/chattopadhyay2026-fresh-starts/html/2608.22101.md):9);
rollback has the lowest overall WER for all models and datasets (line 237);
trends hold at all latencies below 250 ms and with VAD-derived turn
boundaries (lines 255-267); carry-over costs no extra memory beyond streaming
(line 225); the left context is 5.6 s of history (line 219).

**Means for us.** A direct comparison of carrying encoder state across
utterances vs resetting, in a current open streaming transducer, at
inference only, with no retraining. The state is the model's own history
(activations), not an explicit channel estimate; the gain concentrates at
utterance starts.

**Not shown.** Absolute WER (not transcribed); noise or channel
conditions as the variable; a phone-sized model.

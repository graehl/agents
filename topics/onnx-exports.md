# ONNX exports for variable-length batches

> Sequence-model exports expose valid lengths and keep architecture-specific
> padding masks inside the graph, with batching verified separately from decoding.

Topic: `onnx-exports`

Read before creating or changing an ONNX sequence-model export or its batching
interface. User-directed convention, 2026-11-14; applies across projects.

## Default interface

For new right-padded sequence interfaces, accept `input_lengths: int64[B]`
alongside the input tensor. Each length counts valid positions on the tensor's
sequence axis before batch padding. Document the unit explicitly: samples,
feature frames, or tokens, and whether the features are already stacked or
subsampled. Construct the needed masks inside the graph using lengths and a
position range. Return `output_lengths: int64[B]` when the output has a padded
sequence axis, deriving lengths through the actual subsampling operations.

Callers should not need to know internal mask polarity, attention-bias dtype,
kernel choice, or intermediate time resolutions. An input named `mask` has no
universal semantics: boolean polarity varies by API; binary validity masks and
additive attention biases are different contracts. Additive masks commonly use
zero for allowed positions and a large negative value or negative infinity
for blocked positions, subject to the operator's contract.

Keep established external interfaces compatible. Left padding, packed inputs,
causal decoding with caches, and multiple independently padded axes may need
different interfaces; document them rather than forcing one length vector to
describe them. Specify whether zero-length sequences are supported; reject
unsupported lengths, negative lengths, and lengths beyond the physical axis.

## Architecture-specific masking

An exporter must preserve or supply masking at every operation where invalid
positions could affect valid outputs: attention, temporal convolutions,
pooling, and normalization over time. Masking attention keys alone does not
zero padded query outputs or protect a later convolution. Where a convolution
needs zero boundary values, mask after any preceding operation that can make
padded positions nonzero, including affine normalization. Propagate masks and
lengths at each changed time resolution. Keep per-utterance feature statistics
independent of batch padding.

Use documented operator contracts and inspect the exported graph/runtime
optimization. A fused attention kernel may consume lengths or masks directly;
otherwise use broadcastable masks where possible. Avoid needlessly materializing
quadratic masks or losing a fused kernel. Mask construction is usually cheap
relative to encoder compute, but padding masks generally do not eliminate the
compute on padded positions. Bucketing remains useful.

Prefer one validated masked export for batch size one and larger batches.
Keep a separate unmasked fast path only for a measured benefit or a concrete
backend constraint. Introduce a changed contract under a distinct filename
(for example `model.masked.onnx`) and migrate callers after validation, without
silently replacing an incompatible deployed model.

## Validation

Separate three questions:

- **Encoder masking:** compare valid floating-point outputs for the same input
  alone and in mixed-length batches, with changed neighbours, batch positions,
  and finite padded values. Include short, long, and partial batches and the
  last valid output. Check returned lengths against the architecture. Use
  appropriate numerical tolerances; transcript changes alone do not prove
  masking leakage. NaNs are not a general encoder-mask oracle: multiplication
  by zero does not remove them.
- **Decoder bounds:** hold valid encoded outputs fixed and poison only the
  padded tail. Verify independent and batched decoding agree, including
  timestamps, last-frame consumption, and end-of-input scoring. Include a
  sensitive control that consumes the tail or truncates valid input.
- **Quantization and runtime:** dynamic activation quantization can couple
  utterances through batch-wide ranges even without padding. Compare fp32 and
  quantized batching separately, recording batch composition, task error,
  runtime, and memory. Masking is not a promise of bitwise batch invariance.

Record input/output names, shapes, dtypes, length units, padding side/value,
normalization, special-token treatment, supported batch sizes, model identity,
and validation with the export. Keep the previous artifact for matched checks.

## Model family cards

Keep one machine-readable card for a model family, listing only available
precision variants. Share token-table references and preprocessing; record each
variant's artifact hashes, interfaces, quantization, batching validation and
measurements separately. Performance depends on hardware and batch size; a
deployment preference for int8 does not restrict callers to that precision.
Quality measurements name the dataset, metric version/view and decoder settings.
Use explicit unknown or unverified values when evidence is absent.

Distinguish equal-length batching, mixed-length batching with lengths, and
validated zero-padding without lengths. The last case must specify whether
zeros are waveform samples or feature frames, and how outputs are trimmed.
Length-aware re-export is not a prerequisite to an equal-length speed probe.

Generate runtime-specific option files as secondary products when useful. Keep
their keys compatible with the actual loader; descriptive metadata belongs in
the family card, not in a strict runtime configuration parser.

## Streaming lookahead and boundary context

Batch padding is distinct from padding used to complete an audio analysis
window and from end-of-stream flushing. A streaming encoder may delay outputs
until future context arrives: attention can look ahead within a chunk, and a
noncausal temporal convolution can require future positions. At end-of-input,
the remaining outputs need an explicit finish operation or the model's prescribed
padding/context protocol. A fully causal encoder does not need future context,
although its frontend and chunk interface may still need finalization.

For example, a layer with two-frame right context cannot finalize the last two
real frames until it sees their future context or the sequence boundary.
Appending synthetic context can complete a fixed-shape execution call; masks,
lengths and output trimming must still distinguish real input from that context.
Silence samples, zero feature vectors and masked positions are not interchangeable.
Use the trained model/runtime's boundary convention, not an arbitrary silence
duration. Per-layer lookahead may accumulate; chunked attention can bound it by
sharing chunk boundaries. Derive total delay from the actual architecture.

CTC specifies frame-output scoring and collapse, not the encoder's receptive
field. Both CTC and transducer heads can sit on causal, delayed streaming, or
whole-utterance encoders. BOS/EOS in text provide a useful boundary-context
analogy, but audio padding is not automatically a learned boundary symbol.

# Shared ML model development

> graehl's training and evaluation work accumulates shared learnings,
> evidence and implementations across model tasks and programs.

Topic: `ml-model-development`

Read before planning, implementing or running ML model training or evaluation,
including fine-tuning, decoding and experiment scale-up. This is the personal
cross-project entry point; the owning project's program and method contracts
still govern the actual work. Follow only the references relevant to the task.

## Recover and reuse what we already know

When establishing a program or materially revising its data, representation or
evaluation contracts, follow [research program setup](research-program-setup.md).

Treat a new model, language or domain as a new consumer of an accumulating
engineering and research base. Before choosing its recipe or writing its
training/evaluation path, search the project's shared topics, libraries and
prior program evidence for the mechanisms it needs. In `~/draft`, search
across MT, PII and ASR rather than only the active program. Elsewhere, consult
the draft references below when the mechanism transfers and that checkout is
available; do not make unrelated projects depend on draft merely to run.

Recover both the implementation and the evidence: what worked or failed, under
which data/model/objective, the measured cost, and which caller actually uses
it. Distinguish a reusable mechanism from a task-specific recipe or empirical
claim. Reuse the former with an integration check; treat the latter as a scoped
prior until a matched comparison supports transfer. A shared helper's defaults
do not automatically reach a new training loop or decoding caller.

Keep a compact program recipe that identifies enabled building blocks, their
canonical implementation and evidence, and material departures or unresolved
controls. Start from the applicable established subset and add techniques in
a measured order. At useful result or implementation milestones, update the
existing shared owner with transferable findings, negative evidence and
applicability limits; leave task-specific measurements with their producing
program and link them. Extend this entry point when a new reusable owner
needs discovery, rather than copying recipes or accumulating every run here.

## Quality, experiment order and execution

- Before creating or changing an ONNX sequence-model export or its batching
  interface, read [ONNX exports](onnx-exports.md). Default to right-padded
  inputs with explicit lengths and masks constructed inside the graph.
- Before acquiring or partitioning training/evaluation data, including a
  small corpus-quality smoke, read [training data](training-data.md).
  Reserve whole source documents/recordings across splits where possible;
  segmentation must not turn related portions into independent examples.
- Retention makes quality work part of authorized future use:
  [Retained prototypes](design-thinking.md#retained-prototypes). Judge the
  training and evaluation code, data/resources and orientation material by
  anticipated compute spend, later improvements and possible reviewer use.
- Choose cheap informative upstream improvements before repeatedly paying
  for expensive inference options; apply
  [Experiment order for model development](../_RESEARCH/judgment.md#experiment-order-for-model-development)
  and its component-control rules when promoting a bundle.
- Before repeating or scaling, apply
  [ML execution readiness](../_RUNS/resources.md#ml-execution-readiness).
  Verify the real caller's batching/cache behavior and amortized development
  payoff. Keep useful GPU work running while improving it; use remaining
  completion cost to decide whether to restart.
- Keep run/configuration/input/output provenance through [RUNS](../RUNS.md)
  and comparisons through [research evidence](../_RESEARCH/evidence.md).
  Use [fine-tuning](fine-tuning.md) when existing capabilities must survive,
  and for its LR schedules and early-stopping rules on any extension,
  adaptation or distillation run.

## Partial training is named and chosen explicitly

Binding (graehl, 2026-11-24). **Partial training** is any run in which
some of the starting model's weights cannot change freely: a low-rank or
other adapter, frozen layers or modules, or head-only training. Results
from it read as full fine-tunes once the qualifier is dropped, which
misleads a reader comparing runs across sessions.

- **Every name carries the scope tag.** The run tag, output directory,
  table row or column label, plot legend, handoff line and prose
  shorthand for a partially trained model all state its scope:

  | Tag | Meaning |
  |---|---|
  | `r64` | rank-64 adapter on every layer |
  | `r64·top8` | rank-64 adapter on the last 8 layers only |
  | `frz8` | first 8 layers frozen, the rest trained in full |
  | `top4` | only the last 4 layers trained |
  | `enc-frz`, `dec-frz` | encoder or decoder frozen |
  | `head` | only the output head trained |

  A name with no tag asserts that every weight was trained. Write
  "LoRA r64 fine-tune" or "fine-tune, first 8 layers frozen", never a
  bare "fine-tune", for such a run. When the adapted module set differs
  between compared arms (attention only against attention and MLP), add
  it to the tag (`r64-attn`); otherwise the recipe records it. Tags
  compose: `r64-attn·frz10` is rank 64 on attention only, with no
  adapter on the first 10 layers.
- **The tag survives shortening.** When a label must shrink to fit a
  table or legend, drop something else. A table that mixes scopes may
  move the tag into its own "Trained" column; a footnote or caption
  alone does not satisfy this.
- **A restriction is a driver option, never a silent default.** A
  trainer driver trains every weight unless an explicitly named option
  on its command line says otherwise (`--lora-rank`, `--train-top-layers`,
  `--freeze-encoder-through`); an adapter-only driver takes its rank and
  layer range as options a caller can see. No library default, config
  file or hardcoded constant may narrow the trained set unannounced.
- **The driver announces what it trains.** At start it prints one line,
  and writes the same facts into the run's recipe or metadata: trained
  and total parameter counts, the layers trained out of how many, and
  the adapter rank and modules. A resumed adapter inherits its scope and
  still prints it. Read that line before naming a run; a restriction
  found there that the name lacks is a naming defect to fix, including
  in tables already written.
- **Existing drivers:** bring a driver that hardcodes a restriction to
  this form before its next use for a reported result, or open a gap.

## In-flight batching for inference

For a queue larger than the physical batch, consider in-flight batching
(continuous or iteration-level batching) as a reusable inference facility,
especially for greedy decoding and sampling. Retire finished sequences and
admit queued work between decoding steps; each active sequence keeps its own
position and KV state, so one physical step can serve different generation
timesteps. Prefer an established backend when integrating it pays back over
the campaign. Length sorting alone does not refill slots vacated mid-batch;
it remains useful for static batches and can complement admission/prefill
scheduling. Restore source identity/order regardless of scheduling.

TensorRT-LLM provides an implementation precedent: its documented in-flight
path interleaves context and generation using packed inputs without padding.
Left-padding is therefore not essential to the mechanism. See NVIDIA's
[in-flight batching and KV-cache documentation](https://nvidia.github.io/TensorRT-LLM/features/paged-attention-ifb-scheduler.html).

Expect the largest benefit when a sustained queue and varied completion
lengths would leave static batch slots idle. Do not assume strict speedup:
uniform completion lengths, scheduling/cache-management overhead and prefill
interference can remove the advantage. Compare whole-workload completion time
against a well-batched static baseline at matched decoding settings, checking
output/score correspondence and memory as well as throughput.

Beam search is not fundamentally incompatible: schedule independent request
groups while preserving each group's hypothesis expansion, pruning, ancestry
and KV-state sharing/reordering. Greedy/sampling are simpler first consumers;
verify the chosen backend's beam support and real caller before extending it.
TensorRT-LLM's [backend documentation](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/tensorrtllm_backend/README.html#decoding)
also lists beam search; this is precedent, not proof of support in every
backend/version or a local benchmark.

## Existing draft entry points

These are discovery pointers, not instructions to load every file or transplant
every default. Read the relevant owner and inspect its current callers before
reuse. All paths are within the user's `~/draft` checkout.

| Concern | Canonical starting point |
|---|---|
| Cross-task training safeguards; method-specific applicability | `~/draft/topics/fine-tune-checklist.md`; `~/draft/topics/fine-tune-checklist/general.md` |
| Weighted draws, padding-efficient physical batches, optimizer-step composition | `~/draft/topics/weighted-length-batch-sampling.md`; `~/draft/trainlib.py` (`WeightedLengthBatchSampler`) |
| Replay and multiple training streams | `~/draft/topics/logical-batch-stream-mixing.md`; `~/draft/trainlib.py` (`LogicalMixBatchSampler`) |
| Exact shared-prefix KV reuse | `~/draft/decodelib.py` (`split_common_prefix`, `prefill_prefix`, `prepare_batch`); reference caller `~/draft/hf-translate.py` |
| Selection versus evaluation and exposure | `~/draft/topics/eval-split-discipline.md`, plus the owning program's evaluation contract |
| Compact convolutional sequence branches | `~/draft/topics/convolution-training-defaults.md` |
| ASR technique status and linked measurements | `~/draft/research/speech-recognition/topics/asr-techniques.md` and its evidence companion |
| PII data/training/evaluation lineage | `~/draft/research/pii/topics/ontology-v2-process-map.md`; scoped contracts linked by `~/draft/research/pii/frontier/PROGRAM.md` |

## Ownership and availability

`~/agents` is the user's checkout of `https://github.com/graehl/agents`.
This topic owns cross-project intent and discovery; draft owns its ML
implementations, project contracts and experimental evidence. Link in both
directions when useful. Do not move draft-specific code into agents merely
because multiple draft programs use it.

Draft has pinned vendored subsets of agents policy and tooling for fallback.
Its boot defines their precedence. A subset is not a full agents checkout:
verify which files/revision it contains, use the live canonical source when
available, and report a missing required topic rather than silently assuming
the vendor supplies it. Updating a pointer does not refresh a vendor snapshot.

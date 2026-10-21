# Shared ML model development

> graehl's training and evaluation work accumulates shared learnings,
> evidence and implementations across model tasks and programs.

Topic: `ml-model-development`

Read before planning, implementing or running ML model training or evaluation,
including fine-tuning, decoding and experiment scale-up. This is the personal
cross-project entry point; the owning project's program and method contracts
still govern the actual work. Follow only the references relevant to the task.

## Recover and reuse what we already know

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
  Use [fine-tuning](fine-tuning.md) when existing capabilities must survive.

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

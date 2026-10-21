# Run resources and launch authority

> Rules and rationale for GPU-visible Python, storage preflight, capacity use,
> on-deck fillers, and routine run-operation authority.

Read this packet before implementing, repeating, or scaling ML training,
evaluation or decoding, a Python command that may import a local accelerator
stack, before allocating GPU capacity, before a run with a nontrivial storage
footprint, or before launching an on-deck filler. `RUNS.md` is the router and
wins on conflict.

## Binding rules

Read ML execution readiness for ML implementation, repeats and scaling;
GPU access and utilization for accelerator work, Storage preflight and
Scratch for substantial writes, On-deck GPU fillers for queue tending, and
Routine run-operation authority for authorized run plumbing. Conditions may
overlap; a CPU storage job does not activate GPU configuration.

### ML execution readiness

A bounded first correctness probe may use a simple implementation. Before the
second substantive run, a larger budget, or fan-out across languages, domains
or models, reconsider the plan at its new scale: what decision will the runs
buy, could a cheaper experiment decide it, and which implementation work pays
back over the remaining campaign? Apply `_RESEARCH/judgment.md` § Experiment
order for model development for selection. Make the shared training/evaluation
path efficient enough for the proposed work; a completed smoke or a quality
gain alone does not establish readiness. Inspect the real execution path and
reuse established project facilities.

For every greedy or beam decode, verify the applicable basics: length sorting
or bucketing for independent offline inputs with source-order restoration;
actual batching across examples and live beam hypotheses; incremental KV
state reuse and shared-prefix prefill reuse; and reuse of unchanged encoder
outputs, logits or scores across compatible comparisons. Beam width is not
batch size, a Python loop of GPU calls is not batched execution, and a score
memo is not proof that the model avoids repeated prefix computation. Inspect
cache identity, invalidation and branch-state handling; record unsupported or
inapplicable mechanisms and the concrete alternative rather than silently
omitting them. Online latency/order constraints may justify different
scheduling. Training gets the same attention to padding, data loading and
repeated evaluation overhead without changing its intended sampling law.

Run a bounded representative pilot through that path, including long inputs
and partial batches. Check output/score correspondence, actual batch occupancy,
cache reuse or recomputation, wall time, memory and projected total cost;
compare task quality when numerical regrouping can alter decoding. Use the
existing run record for these receipts and the enabled settings. A flag or
backend capability is not evidence that this caller uses it. Fix avoidable
serial work or recomputation before adopting that path for repetition or
fan-out when the improvement pays back over the planned work. A deliberately
serial latency measurement remains valid when that is the named question.
Reuse valid receipts until code, configuration or workload changes invalidate
them; this is not a mandate to optimize every possible kernel.

Keep GPUs doing useful work while developing improvements. For already-paid
capacity without usage-based power charges, idling it saves no compute rent.
Compare continuing the current run with developing, validating and restarting
or resuming on the improved path, crediting progress made during development
and including lost progress, startup and contention costs. Cancel/relaunch
when that finishes the useful work sooner or buys more value within the same
budget; otherwise finish and improve subsequent runs. Record a simple estimate
in the run note and revise it from pilot timing. Already-spent compute is sunk;
remaining useful work and opportunity cost decide. Preserve required outputs
and source isolation while developing beside a live run.

### GPU access for Python ML commands

For an ML repository with local accelerators, run Python with GPU-visible
permissions whenever imports may reach `torch`, `transformers`, `unsloth`,
`vllm`, TensorRT, or similar code, including `--help` paths that import before
argument parsing. A sandboxed CUDA-detection failure is not evidence that the
host has no GPU; retry with GPU visibility before drawing that conclusion.

Before launch, inspect `nvidia-smi`. Unexpected existing use warrants a warning,
but proceed when estimated free VRAM still leaves the planned run safe. Block or
change the plan only when current use makes launch materially risky.
`agentctl list --host --live` shows every project's running and queued jobs
on this machine with their VRAM use and leases, under one per-GPU line of
used, leased, and uncommitted memory.

Every PyTorch job sets:

```text
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True,garbage_collection_threshold:0.5
```

Source a project `env.sh` that sets it or export it explicitly before detached
jobs.

### Storage preflight

Before a run likely to write substantial outputs, checkpoints, cache entries,
or temporary files, estimate what it will write and check free space on every
filesystem it will use. Include output, model/data cache, checkpoint, and temp
mounts rather than checking only the working directory. Resolve insufficient
space before launch; remove only artifacts known to be stale under the normal
deletion and shared-worktree rules. A remote worker also follows its project's
host/storage runbook.
Account for transient peaks such as old and new checkpoints coexisting, and
record a material capacity assumption when the launch depends on it.

### Scratch holds only regenerable bytes

A host's fast scratch tier — `/scratch`, instance-store NVMe, or the project's
named equivalent — is a high-performance `/tmp` that happens to survive reboot.
Presume that evicting anything on it to reclaim space is reasonable, and that
nothing on it survives host replacement. Only efficiently regenerable bytes
belong there: caches, model and package downloads, intermediates, and
performance replicas.

Scratch may still be the landing zone for an expensive or unreproducible write
when the fast path is what makes the run practical. Relocating that artifact to
durable storage is then part of the run, not later cleanup: move it out before
calling the run complete, and refer to it at the durable path from then on.

A replica may stay on scratch for speed after the durable copy exists. Cite the
durable home rather than the replica, so the reference still resolves once the
replica is evicted.

### GPU utilization and parallelism policy

On a non-shared GPU, keep already-planned work moving without waiting for
another prompt. Apply ML execution readiness above while keeping useful work
running; readiness is not a requirement to idle during development:

- After launch or completion, inspect VRAM and utilization.
- When the current run uses under 50% of total VRAM, launch an independent
  planned job that fits with at least 10% headroom. One run is sufficient only
  at 80% or more VRAM or sustained utilization; 50–80% is the trigger zone for
  finding a compatible second run.
- Runs are independent only when they use different output locations and
  neither reads the other's in-progress output.
- Draw from the accepted task/research queue first. Propose new experiments
  only when it is exhausted.
- About 30 seconds after each background launch, confirm VRAM rose and inspect
  the log if it did not. Never infer launch success from a PID alone.
  `agentctl list --live` shows each running job's `vram=` and `ram=`, so
  read it there rather than guessing which nvidia-smi PID is whose.
- Gate chained GPU successors by observed VRAM release rather than a fixed
  sleep; workers may retain memory after the parent exits.
- When another session or project may launch on the same GPU, launch with
  `agentctl start --gpu-lease <VRAM needed> ...`. The amount is a share
  (`50%`) or a size (`24G`), taken from a prior run's `vram_peak=` plus
  headroom. The run then queues until that much is uncommitted, instead of
  colliding with a peer's run that hasn't allocated yet. Leases are
  advisory: they order cooperating `--gpu-lease` launches and cap
  nothing. Size the lease to the real need, because an undersized lease
  still lets the payload exhaust VRAM. `agentctl list --live` shows each
  run's `lease=` and `vram_max10m=` (recent peak), plus each GPU's
  `leased=`/`uncommitted=`; `list --host` shows every project's runs. Add
  `--gpu-sample 5` for a denser, slower reading before a tight fit. Contract: `topics/agentctl.md` § GPU use
  and VRAM leases.
- When a run finishes, promptly report its headline result, key metrics, and
  one or two useful output comparisons.

#### On-deck GPU fillers

`on-deck/` is an optional guarded queue of single-step fillers; its contract is
`topics/on-deck.md`. The queue answers what should run next, while `.agentctl/`
records what is running. `/steward` performs one fill-until-full pass;
`/rep steward` repeatedly services it. An absent queue is a no-op.

A steward may launch an eligible entry without confirmation when its guard
passes, its skip condition is false, and its cost is within steward autonomy.
Preempt a lower-priority filler only when the saved time justifies lost work and
the stop is safe.

### Routine run-operation authority

Routine, reversible plumbing needed for an already-approved run—GPU access,
project edits, shell execution, logging, and stopping processes launched by this
session—is authorized. This does not broaden the task: global big-effect,
shared-worktree, secrecy, and destructive-action gates still govern. After a
sidebar, resume the agreed run step unless the sidebar changed the plan; ask
only when the remaining alternatives materially differ.

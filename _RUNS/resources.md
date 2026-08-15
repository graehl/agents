# Run resources and launch authority

> Rules and rationale for GPU-visible Python, storage preflight, capacity use,
> on-deck fillers, and routine run-operation authority.

Read this packet before a Python command that may import a local accelerator
stack, before allocating GPU capacity, before a run with a nontrivial storage
footprint, or before launching an on-deck filler. `RUNS.md` is the router and
wins on conflict.

## Binding rules

### GPU access for Python ML commands

For an ML repository with local accelerators, run Python with GPU-visible
permissions whenever imports may reach `torch`, `transformers`, `unsloth`,
`vllm`, TensorRT, or similar code, including `--help` paths that import before
argument parsing. A sandboxed CUDA-detection failure is not evidence that the
host has no GPU; retry with GPU visibility before drawing that conclusion.

Before launch, inspect `nvidia-smi`. Unexpected existing use warrants a warning,
but proceed when estimated free VRAM still leaves the planned run safe. Block or
change the plan only when current use makes launch materially risky.

Every PyTorch job sets:

```text
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True,garbage_collection_threshold:0.5
```

Source a project `env.sh` that sets it or export it explicitly before detached
jobs. `PYTORCH_ALLOC_CONF` (without `CUDA_`) is silently ineffective.

### Storage preflight

Before a run likely to write substantial outputs, checkpoints, cache entries,
or temporary files, estimate what it will write and check free space on every
filesystem it will use. Include output, model/data cache, checkpoint, and temp
mounts rather than checking only the working directory. Resolve insufficient
space before launch; remove only artifacts known to be stale under the normal
deletion and shared-worktree rules. A remote worker also follows its project's
host/storage runbook.

### GPU utilization and parallelism policy

On a non-shared GPU, keep already-planned work moving without waiting for
another prompt:

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
- Gate chained GPU successors by observed VRAM release rather than a fixed
  sleep; workers may retain memory after the parent exits.
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


## Retained detail and examples

### Storage preflight

The relevant capacity is the smallest writable filesystem in the run's whole
path, not the repository volume alone. Model downloads may fill a cache mount,
checkpoint rotation may temporarily require both old and new checkpoints, and
package or data staging may consume a worker root volume even when the final
output goes elsewhere. Record or report a material capacity assumption when a
long run depends on it.

### GPU access for Python ML commands

When working in an ML repo that uses local accelerators, default to running Python
commands with GPU-visible permissions whenever the script might import `torch`,
`transformers`, `unsloth`, `vllm`, TensorRT helpers, or related ML code. This includes
commands that look lightweight such as `--help`, because some scripts import the full
runtime before parsing arguments.

Do not infer "this machine has no GPU" from a sandboxed failure like `torch.cuda` or
`unsloth` accelerator detection returning false. Treat that first as a likely sandbox
GPU-visibility issue. If there is any realistic chance the command will touch the ML
stack, rerun it with GPU-capable permissions instead of continuing with a sandboxed
Python path.

Before launching a GPU job, first confirm whether the GPU appears idle. If GPU use is
already present unexpectedly, warn but proceed when estimated free VRAM still looks
sufficient for the planned job, since this resource is assumed to be single-user. Only
block or change the plan when current use makes the launch materially risky.

**PyTorch CUDA allocator — prevent memory over-reservation:**
Always set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True,garbage_collection_threshold:0.5`
before any PyTorch job — without it the caching allocator holds large VRAM slabs between
jobs, preventing concurrency. `env.sh` sets this; always `source env.sh` or export
explicitly before `nohup` jobs. (The typo `PYTORCH_ALLOC_CONF`, missing `CUDA_`, is silently ignored.)

### GPU utilization and parallelism policy

The thresholds in the binding rule distinguish three cases: below 50% VRAM,
where a compatible planned peer can materially improve occupancy; 50–80%,
where the operator should actively look for one; and at least 80% VRAM or
sustained utilization, where one job is already enough. Output separation and
no reads from another job's in-progress output are what make concurrent runs
independent.

A parent PID exiting does not prove its workers released device memory, and a
background PID existing does not prove useful GPU work began. That is why the
canonical protocol above observes VRAM after launch and before a chained
successor instead of relying on PID state or an elapsed sleep.

### On-deck GPU fillers

Projects may opt into `on-deck/` as a guarded queue of single-step GPU fillers;
see `topics/on-deck.md`. `$on-deck` creates the queue. A steward agent may fill
idle GPU without waiting for confirmation when an entry's guard passes, its
skip-if does not fire, and its cost is within steward autonomy. If `on-deck/`
is absent, `/steward` is a no-op. Use `/steward` for one fill-until-full pass
and `/rep steward` when repeated servicing is desired.

On-deck does not replace `agentctl` run state. The queue answers "what should
run next"; `.agentctl/` answers "what is running now." If a higher-priority
eligible entry appears while a steward filler is running, pause/kill only as a
judgment call when the saved time is worth the lost work and the stop is safe.

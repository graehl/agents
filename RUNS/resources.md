# Run resources and launch authority

> Rules and rationale for GPU-visible Python, capacity use, on-deck fillers, and routine run-operation authority.

Read this packet before a Python command that may import a local accelerator
stack, before allocating GPU capacity, or before launching an on-deck filler.
`RUNS.md` is the router and wins on conflict.

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

The GPU is non-shared and must be kept busy with planned work at all times —
without being asked and without churning the repo.

**Keep-busy rule**: Whenever a job finishes (or while one runs and a slot is
free), immediately queue or launch the next planned job. Never leave the GPU
idle between planned jobs. Use `wait <PID>` wrappers with a brief sleep buffer
(~90 s) between sequential jobs to let GPU memory fully release.

**Parallelism rule** — two independent jobs must run simultaneously whenever:
- the running job uses **< 50% of total VRAM**, AND
- a second planned job also fits in remaining VRAM with ≥ 10% headroom.

A single job is acceptable only when it uses **≥ 80% of VRAM** (or ≥ 80%
sustained utilization per `nvidia-smi utilization.gpu`). The 50–80% band is
the trigger zone: find and launch a second job from the plan without asking.

**Operationally**:
1. After any job launch or completion, run `nvidia-smi` and check VRAM.
2. If VRAM < 50%: immediately identify the next independent planned job that
   fits in free VRAM (≥ 10% headroom) and launch it without asking.
3. Two jobs are "independent" if they write to different output directories and
   neither reads the other's in-progress output.
4. Prefer the next *planned* job from the task/research queue; only propose new
   experiments if the queue is exhausted.
5. When chaining via `wait <PID>`, check whether any queued job can be promoted
   to run now in parallel with the current job.
6. When a run finishes, immediately show the user a brief highlight: headline
   result, key metric(s), and 1–2 sample output comparisons. Do not wait to be
   asked.
7. **Verify GPU is in use after every job launch.** After starting a background
   job (direct or via a `nohup` wrapper), wait ~30 s and run `nvidia-smi` to
   confirm VRAM rose as expected. If the GPU stays at 0 MiB, the job silently
   failed — investigate the log immediately and relaunch. Never assume a
   background job succeeded without this check.
8. **Use VRAM-polling waits between chained jobs**, not fixed sleeps.
   Before launching the next job in a chain, poll until VRAM drops below a
   safe threshold (e.g. `while [ $(nvidia-smi --query-gpu=memory.used
   --format=csv,noheader | tr -d ' MiB') -gt 3000 ]; do sleep 15; done`).
   Fixed sleeps are unreliable because child/worker processes can hold GPU
   memory well past the parent's exit.

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

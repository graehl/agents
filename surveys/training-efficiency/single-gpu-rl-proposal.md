# Variable length RL on one 96 GB GPU

Status: historical proposal, superseded on 14 October 2026 by the authoritative
[single-GPU RL program in `~/draft`](../../../draft/research/single-gpu-rl/PROGRAM.md)
and its [revised research plan](../../../draft/research/single-gpu-rl/plan.md).
Implementation backlog lives in the program's
[gap sketch](../../../draft/research/single-gpu-rl/gaps/sketches/capacity-and-learning-baseline.md).
Continue and revise that work there; do not implement a duplicate in `~/agents`.
The text below preserves the original proposal and its source links as
background, not an active experiment specification. Creation of the successor
authorized documentation only, with implementation and launches deferred.

Proposal, 10 October 2026. Designed for graehl: familiar with model training,
new to workloads whose generation and verification costs vary substantially
at similar input lengths. Confirmed scope: further RL of an instruction-tuned
model around 30B parameters, using verifiable rewards. No capacity or
throughput experiment has been run.

## Start with quantized adapter training and ordinary batched rollouts

Use a dense 32B instruction-tuned model, frozen 4-bit base weights, rank-16
LoRA, a GRPO-family loss, and Unsloth's integrated TRL/vLLM generation path.
Alternate generation and training on the same GPU. Start with four responses
per prompt, eight prompts per update, and a 2,048-token response limit.
Let vLLM refill available generation slots from this fixed set of 32
responses. Finish the set before updating the adapter.

This combines the likely useful, relatively inexpensive techniques for this
resource budget: quantized frozen weights, small optimizer state, gradient
checkpointing, memory-efficient loss computation, and continuous batching.
It deliberately leaves out a distributed rollout scheduler and a second
trained drafter. The latter can be reconsidered after measuring the time
spent finishing the last few responses.

Choose Qwen2.5-32B-Instruct as the reference implementation target because
it has an explicit instruction-tuned checkpoint, a conventional dense
architecture, and an [available Unsloth 4-bit checkpoint](https://huggingface.co/unsloth/Qwen2.5-32B-Instruct-bnb-4bit).
This is a compatibility-first reference, not a claim that it is the best
October 2026 model. Pin the model revision and a working dependency set at
implementation time. A newer 30B-class checkpoint is a separate model
comparison after this pipeline works.

## What variable work looks like

Consider two coding prompts of roughly 400 tokens. One asks for a simple
scan; the other requires finding a suitable dynamic program. A sampled
response might finish after 250 tokens, spend 1,800 tokens exploring a
solution, or hit the generation limit without valid code. Sibling responses
to the *same* prompt can also take different paths. Input length predicts
prefill cost; it is a poor sufficient statistic for the work that follows.

The training workload has three different variable costs:

| Phase | Work that varies | Practical consequence |
|---|---|---|
| Generate | Number of output tokens and accumulated attention context | Refill finished slots; provision KV memory for long survivors |
| Verify | Number of tests and execution time of the generated program | Use a bounded CPU worker pool and explicit timeouts |
| Train | Realized prompt plus response length | Microbatch the completed sequences; avoid padding a large batch to its longest member |

After generation, lengths are known and the familiar length-aware training
techniques apply. Before generation, the scheduler only has estimates.
There is no requirement that useful tasks have a formal superlinear
complexity bound: the relevant property is unpredictable realized work.

Here is an illustrative queue, not measured timing. Eight of 32 responses
are active. When a short one finishes, vLLM admits another queued response.
Eventually the queue empties and only two long responses remain. Refill can
no longer help unless the training batch is enlarged or its membership is
changed. The simplest baseline waits for those responses or their fixed
token limits, then performs the update. Speculative decoding could accelerate
this final interval; it cannot manufacture additional independent work.

## The three Seer phrases in concrete terms

These refer to the mechanisms in [the Seer reading](concepts/seer.md#scheduling-uneven-lengths-is-the-central-problem),
not three prerequisites for efficient RL.

### Same-policy work mobility means moving a partially generated response

Suppose GPU A has several long survivors while GPU B has finished its work.
Seer moves a survivor's tokens and KV cache to B, which continues generating
with the same policy weights. The response is neither restarted from its
prompt nor continued under a newer policy. That is what “same-policy work
mobility” meant. Seer's global cache makes the transfer possible without
recomputing the whole prefix.

Omit this here: one GPU has no idle second replica to receive the work.
Freeing generation memory before training is useful, but it is a different
operation. Do not implement Mooncake, remote KV storage, or decoder migration
for this proposal.

### Group signals mean learning about a prompt from its other sampled responses

A GRPO group contains several responses to the same prompt. In Seer, one
response receives early service; its completed length helps estimate how
long siblings may take. Generated sibling text also supplies candidate
token continuations to a suffix-based drafter. Neither signal requires
knowing the final answer or the eventual lengths in advance.

Record the group signals and defer scheduling changes. Retain each group's response
lengths and rewards. If four siblings' lengths are barely correlated, there
is little reason to build an estimator. On one GPU, changing admission
order might help start long responses earlier, but there is no demonstrated
gain here. Group-relative reward statistics remain necessary for GRPO;
Seer's use of the group for scheduling is optional.

### Adaptive control means enabling an accelerator only where it saves time

At a large active batch, ordinary decoding may already use the GPU well.
Drafting and verifying extra tokens can then cost more than they save. With
two long survivors, the same accelerator might help. Seer's controller
changes draft length or disables speculation using workload and acceptance
signals. Acceptance rate alone is insufficient: verification and draft
overhead also enter the decision.

Defer the controller: first benchmark speculation off versus a supported
fixed configuration. Only if it wins specifically during the final low-batch
interval is a switching controller worth considering. Native batching and
an explicit concurrency limit require much less engineering.

The [year-later comparison](survey.md#seers-year-later-verdict) explains why
these mechanisms remain plausible additions rather than a demonstrated
extra doubling on current software.

## Use one coding attempt with test rewards as the first real workload

Use [APPS](https://huggingface.co/datasets/codeparrot/apps), initially its
introductory and interview problems with usable standard-input/output tests.
It supplies Python coding problems, tests and difficulty labels. The card
reports 5,000 training and 5,000 test problems and warns that incomplete
tests can accept incorrect programs. Treat test pass rate as the operational
reward, not proof of semantic correctness.

Select by problem identity and test availability before looking at policy
success. Proposed split: 1,000 eligible training problems, 200 development
problems held out from the official training split, and 500 eligible problems
from the official test split. Verify those counts after filtering; if a
stratum is too small, document the reduced count instead of duplicating
problems. Deduplicate source URLs and normalized statements across splits.
Pretraining exposure is unknown, so this measures adaptation, not clean
generalization to previously unseen coding problems.

The prompt requests a solution ending in one Python code block; it permits
reasoning but gives no reward for its length or style. Score 1 if the program
passes all selected tests and 0 otherwise. Reject ambiguous multiple-code-block
outputs consistently. Keep the verifier inputs out of the model prompt except
for examples already in the problem statement. Inspect successful programs
on development cases to catch weak-test exploitation.

Use a maintained isolated code-execution runner, without network access or
host credentials, with fixed CPU, memory and wall-time limits. A process
timeout alone is not isolation. Start with four CPU workers, 2 seconds per
test and a 20-second total candidate limit; validate reference solutions
against these limits before freezing the eligible dataset. Runner failures
are infrastructure errors; program crashes and genuine timeouts receive 0.
Do not let infrastructure outages silently become model failures.

This is single-turn RL with verifiable rewards, not an interactive agent.
Tool calls and repair loops would add variable turn counts, persistent
environment state and more complicated credit assignment. They are a later
extension, once generation and reward accounting are reliable.

## Keep one policy version per generation cycle

For each update:

1. Freeze adapter version N and select eight prompts. Generate four
   responses per prompt from that version. Queue all 32; initially permit
   up to eight active sequences, subject to the measured KV budget.
2. Evaluate every response. Keep the original group membership regardless
   of completion order. A CPU worker pool is sufficient; overlapping reward
   evaluation with generation is optional if the framework exposes completed
   responses without a custom engine.
3. Retain tokens, behavior log probabilities, rewards, termination reasons
   and adapter version. Release the rollout KV cache before backpropagation.
4. Accumulate gradients over the 32 responses, initially one sequence at a
   time. Apply one optimizer update, producing adapter N+1. Synchronize it
   into the inference path before starting another generation cycle.

Do not treat four early completions from different prompts as a GRPO group.
Do not replace slow responses with extra easy completions. Both would
change the learning data while appearing to improve throughput.

The following are proposed starting values, not tuned findings. They specify
logical behavior; a two-update smoke must verify the installed trainer's
batch interpretation rather than assuming similarly named arguments agree.

| Choice | Initial setting | Reason |
|---|---|---|
| Base and adapters | Frozen 4-bit base; BF16 compute; LoRA rank 16 on attention and MLP projections | Reserve memory for context rather than full-weight optimizer state |
| Learning rate | 5e-6, constant for the initial pilot | Conservative starting update size; tune only on development data |
| Loss | `dr_grpo`, `scale_rewards=False` | Use a constant length denominator; avoid adding group-variance scaling to this first comparison |
| Reference penalty | `beta=0` | No extra reference scoring; appropriate for a task-learning pilot, not a guarantee of retained instruction behavior |
| Updates per generation | One, with all 32 responses accumulated | Keep the version boundary easy to audit |
| Sampling | Temperature 1; top-p 1; no top-k restriction | Preserve response diversity without another sampling adjustment |
| Context | At most 2,048 prompt and 2,048 response tokens | Begin with a bounded memory and generation cost |
| Completion limit | Hitting the response cap is a terminal failure with reward 0 | Explicit finite-budget task; avoids an ambiguous partial program |
| Truncation masking | Disabled initially | Current Unsloth docs warn about all-masked batches; cap failures intentionally contribute to this finite-horizon objective |
| Memory | Checkpointed activations and memory-efficient GRPO loss | Avoid storing large activation and token-by-vocabulary tensors |

[TRL documents the loss choices](https://huggingface.co/docs/trl/grpo_trainer#loss-types).
[Unsloth's advanced guide](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide/advanced-rl-documentation)
documents the correction between generation and training backends and the
truncation-masking issue. Keep its supported importance correction enabled
and monitor log-probability disagreement. Same adapter version does not
make different numerical kernels identical. Avoid introducing a separate
rollout quantization scheme in this first implementation.

When all four rewards in a group are equal, the centered reward supplies no
task-learning signal. Log this fraction, including all-success and all-failure
groups separately. If almost every group is uniform, revise task difficulty
on training/development evidence before buying more training time. Do not
silently discard or refill those groups during the baseline.

## Why 96 GB is plausible and what can still fail to fit

For 32 billion parameters, bare 4-bit storage is approximately 16 GB;
BF16 is approximately 64 GB. Quantization metadata, unquantized tensors,
adapters and temporary buffers add to those floors. Full-weight mixed
precision Adam at an illustrative 16 bytes per parameter would require
about 512 GB before activations. Adapter training is the feasible default.

The [Qwen2.5-32B configuration](https://huggingface.co/Qwen/Qwen2.5-32B-Instruct/blob/main/config.json)
has 64 layers, eight KV heads and head dimension 128. With BF16 KV values,
the cache per live token is

\[
2\times64\times8\times128\times2\text{ bytes}=256\text{ KiB}.
\]

Eight responses each holding 4,096 prompt-plus-output tokens therefore
need about 8 GiB of KV, before block allocation overhead and without
assuming shared-prefix savings. At 16,384 tokens each, they need about
32 GiB. Four-bit model weights do not imply four-bit KV storage. The
response limit and active concurrency matter even after the model fits.

Use these as acceptance targets, not a claimed allocation breakdown:
keep measured peak device memory below 85% of the actual capacity reported
by the driver, and leave the rest for transient allocations. Measure both
generation and backward peaks. Start with at least 128 GB host RAM; 192 GB
is preferable if activation offload is enabled. CPU verification has its
own memory limit.

The selected [Unsloth integration](https://unsloth.ai/blog/grpo) describes
shared inference/training weights, checkpointing and memory-efficient loss
computation. Verify that the chosen quantized model follows that path; do
not assume two unrelated framework loaders share storage. Generic
[TRL colocation](https://huggingface.co/docs/trl/vllm_integration) is a
supported alternative, but shares a GPU rather than necessarily sharing
weight tensors; its sleep mode can free inference memory during updates.
A quantized training copy plus an accidentally BF16 inference copy could
consume most of this GPU before useful batching.

If the first backward pass exceeds the target, reduce active generation
memory reservations and ensure caches are released, then reduce training
microbatch size if it is above one. If a single 4K sequence still fails,
inspect duplicated weights and the loss path before reducing the task's
context budget. Record any reduced budget as a different task condition.

## Measure before adding a scheduler or drafter

The initial implementation needs a dataset adapter, isolated test runner,
trainer configuration and timing/logging callbacks. It should not require
modifying vLLM scheduling internals. The execution runner is the largest
new component if none is already available.

First run a 32-prompt correctness/capacity smoke, then a 200-prompt frozen
policy profile with four responses each. Use training-side prompts for
these checks. Record generation time, reward time, backward/update time,
adapter synchronization, peak device memory, response-length percentiles,
cap-hit rate, group reward diversity and active-sequence count over time.
Inspect outputs and verifier decisions across successes, invalid programs,
wrong answers, timeouts and truncated generations.

If more than 10% of responses hit the token cap in this profile, test a
4,096-token response budget before starting the learning pilot. Adopt the
larger budget only after repeating the memory check, and freeze it across
the training comparison. This proposed threshold prevents the first study
from mostly measuring an accidentally restrictive generation limit.

Then try active concurrency 4, 8 and 16 with the same frozen prompts and
sampling setup. Choose the fastest configuration within the memory target.
If outputs differ because batching changes numerical execution, report
their length and reward distributions rather than claiming identical work.
Keep the number of prompts and responses fixed: doubling the learning batch
is not merely a scheduler setting.

For training, run an initial 100-update pilot with a six-GPU-hour ceiling,
whichever arrives first. Evaluate the 200 development problems before
training and every 25 updates using one sampled attempt and fixed decoding
settings. Select the checkpoint by development pass rate; run the 500-problem
test set once after selection. Report elapsed GPU time including evaluation,
as well as pass rate, cap-hit rate and output length. A pilot gain needs
paired problem-level uncertainty and a second seed before being treated as
reliable. Track a separate retained-instruction evaluation if preserving
general assistant behavior becomes a requirement.

Use the profile to choose at most one next optimization:

| Observed bottleneck | Next change | Adoption criterion |
|---|---|---|
| Backward or memory dominates | Tune checkpointing and the fused/chunked loss path | Lower full-step cost without changing gradients beyond intended numerical tolerance |
| CPU test time dominates | Tune the bounded worker pool; overlap only through an existing supported hook | Lower elapsed step time with identical verifier decisions |
| Long final interval with only a few live responses | Try a compatible off-the-shelf speculative mode | At least 10% lower full-step time across repeated profiles, including overhead; no material quality change |
| Queued long responses start late | Test a simple admission order using recorded group/length features | Benefit beyond ordinary refill on fixed generated-work distributions |

The 10% threshold is an engineering decision: smaller savings do not yet
justify an extra integration here. If the tail is only 20% of a step, even
doubling its speed improves the whole step by only about 11%. That bounds
the payoff before implementing Seer-style control.

Do not initially add online drafter training, partial rollouts across policy
updates, KV migration, custom suffix trees, FP8 KV, or full-weight optimizer
offload. Each introduces another performance or learning comparison. The
current [survey](survey.md#later-alternatives-do-not-yield-a-clean-winner)
provides evidence for these alternatives but no single-96-GB-GPU result
that makes their combined engineering cost the best starting choice.

The deliverable from implementation would be a reproducible capacity profile
and a task-learning pilot, not a promised speed multiplier. This proposal
authorizes neither a GPU rental nor a training run.

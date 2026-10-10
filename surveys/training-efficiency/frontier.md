# Training-efficiency claims needing stronger comparisons

Grounded provisional overlay on the [field map](survey.md), searched through
10 October 2026. These are unrun discriminating checks, not scheduled work.

## Seer's residual value over maintained engines

Claim: chunk migration, sibling length estimates and grouped suffix drafts
remain additive to a modern rollout implementation. The original paper
supports gains over its historical synchronous baseline, on three
long-generation workloads using 32–256 H800s. It does not measure the
increment over current veRL/slime configurations. No independent full-system
reproduction was located; the authors control both system and evaluation.

The cheapest discriminating comparison starts with strict synchronous
per-request dispatch and the same sampled prompts, policy, engine, hardware
and token limits. Add migration, then length estimation, then speculation.
Compare grouped suffix drafts against native multi-token prediction and a
well-initialized learned draft, recording drafter maintenance and KV traffic.
Require full-step wall time and accelerator-hours, not just accepted tokens.
Where token-level randomness changes, compare generated-work distributions
and held-out training quality rather than assuming identical trajectories.

TailSieve's oracle proxy is not a reproduction. Its fresh-policy regeneration
also changes selection across steps. Evaluate that sampling policy and
staleness-controlled async separately by time to matched quality.

Revisit on a public Seer artifact, an independent rerun, or a same-stack
component comparison. Unscheduled review reminder: 2027-01-10.

## Grouped retrieval versus learned or self-derived drafts

Seer's appeal is avoiding a separately trained neural drafter while using
current siblings' text. New learned-draft and quantized-self-draft results
show alternatives; TailSieve and other integration work expose model-free
draft overhead. These experiments do not isolate the same grouped suffix
implementation. The open issue is net expected cost under each workload,
including batch-size distribution and policy drift.

Before proposing a new group-aware draft method, search Seer, TLT, ReSpec,
DAS, EfficientRollout and online draft co-training. This survey establishes
no novelty gap in that neighborhood. Revisit when a target workload and
maintained engine are selected, not merely when a new headline appears.

## Sub-plan routing and local speculation

User hypothesis: most eventual savings will come from routing sub-plans to
appropriately sized models, leaving speculative decoding as a local
accelerator when its net expected same-quality cost wins. No verified
head-to-head evidence in this pass establishes that forecast. A useful
comparison must count routing errors, verifier cost, retries and training
effects, as well as expensive-model calls avoided. This is a research
question, not a validated replacement strategy or a claimed open void.

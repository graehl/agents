# Mixed-policy and asynchronous RL defaults

Governs: designing, debugging, or configuring asynchronous, off-policy, or
mixed-policy reinforcement learning for language models (sampler–learner
decoupling, staleness bounds, and model-specific stability hazards).

## Tentative standard: bounded-staleness AsyncRL + Score Centering (`StableReinforce`)

When relaxing strict same-policy synchronization, default to **bounded-staleness
AsyncRL with additive Score Centering** rather than unconstrained replay buffers
or straggler-dropping async loops:

- **Open foundation — Score Centering** (Marek & Ryabinin, Sept 2026,
  [arXiv:2609.20807](https://arxiv.org/abs/2609.20807),
  [code](https://github.com/martin-marek/score-centering)): shows that RL
  collapse under training–inference mismatch (TIM) and policy staleness is
  driven by accumulating *drift*. An additive score-centering correction
  cancels drift, matches or beats pure importance sampling (IS) under sampler
  quantization (0.6B–30B), and composes cleanly with IS under staleness.
- **Production async pattern — Tinker `AsyncConfig` / `StableReinforce`**
  (Thinking Machines Lab, `tinker-cookbook`):
  - Cap sampler lead with `sampling_steps_ahead` (bounded lag) instead of
    discarding stale rollouts (`max_steps_off_policy`, deprecated because
    dropping stragglers biases training toward short/easy prompts).
  - **Never drop stragglers:** consume oldest completed rollout groups first.
  - **Token-level provenance:** record sampler metadata (`record_stability_info=True`,
    `sequence_id`) so the learner aligns each token to the exact sampling
    snapshot without needing a separate reference model.
- **Inferred Inkling 2 Small recipe (proprietary details unverified):**
  Thinking Machines Lab's Inkling 2 Small uses `StableReinforce` (a
  score-centering variant) for long-horizon async RL; if the underlying model
  combines MoE and/or looped-Transformer blocks, its stability relies on
  pairing score centering with routing/loop-state consistency across sampler
  and learner.

## Model-specific RL and async-RL complications

- **Mixture-of-Experts (MoE):** discrete top-$k$ expert routing can flip
  between sampler and learner (even at lag 0 under batching/precision
  differences), causing importance-ratio blowups and collapse. Save sampler
  expert indices alongside token provenance and use **Routing Replay** (Qwen
  Team, [arXiv:2512.01374](https://arxiv.org/abs/2512.01374)).
- **Recurrent / SSM / hybrid linear-attention models (Mamba, RWKV, DeltaNet,
  Jamba):** compressed fixed-size recurrent states cannot be spliced or
  migrated across policy versions like KV-cache blocks; mid-rollout resumption
  after a weight update requires full re-prefill from token 0.
- **Looped / adaptive-depth Transformers:** discrete halting or per-loop
  routing decisions shift when weights update mid-trajectory, changing
  effective depth on the suffix relative to the prefix; record loop/halting
  decisions if resuming or computing off-policy ratios.
- **Quantized / FP8 samplers vs. BF16 learners:** quantization log-prob drift
  acts like off-policy staleness even in synchronous (lag-0) runs; apply
  score centering / IS correction regardless of async lag.
- **Multi-turn / tool-use / stateful-environment agents:** external state
  (shell, DB, sandbox) is often non-idempotent, so partial rollouts cannot be
  cheaply restarted—pair *never-drop-stragglers* with environment snapshotting.

## Related

- Survey context: [surveys/training-efficiency/survey.md](../surveys/training-efficiency/survey.md)
- Single-GPU RL program: `~/draft/research/single-gpu-rl/PROGRAM.md`

# Fine-tuning without forgetting

> A fine-tune is off the base model's training distribution by definition, so
> when the base model's existing skills must survive, keep a reduced share of
> that old distribution in training (replay) instead of dropping it.

Topic: `fine-tuning`
Governs: fine-tuning or adapting a pretrained model whose existing capabilities must survive

## Replay at a reduced share

Plan for replay before launch when an existing capability must survive;
otherwise add it as soon as an evaluation shows the capability degrading
before the fine-tune's own goal is reached. Training on the new data alone
moves the model away from what it already did well, and the damage is usually
done long before the new task converges.

- **Keep the old distribution at 10–50% of its former exposure.** The
  remaining share is the new data. Zero replay forgets. Full replay leaves the
  new task too few updates to catch up: a run that spends half its updates on
  replay learns the new task more slowly than one that spends none.
- **Optionally fade the new data in.** Start with replay dominant for the
  first epoch or so, then step down to the working share. This lets new output
  rows and new-domain features form before large early gradients from
  unfamiliar data reach the representations the old skills depend on.
- **Use the closest available stand-in when the original data is not
  available:** public data from the same tasks or languages, or the base
  model's own outputs on unlabeled old-distribution inputs (self-distillation).
- **Measure forgetting against a drift control.** Train the same recipe on the
  replay data alone and compare the old-task metric with it, not only with the
  untouched base model: continued training at a fine-tuning learning rate
  moves the old metric even with no new data. Report the new-task metric
  beside a run that trains on the new data only, so the cost of keeping the
  old skills is visible.

## Schedules that do not forget what the run already learned

These rules come from the draft repository's speech-recognition program
(graehl, 2026-10-26), where extension legs of one student are routine.

- **An extension leg starts gently.** Two things make an extension forget.
  Erratic early updates while Adam's moment estimates are fresh: a leg that
  loads weights only, without optimizer state, needs a short warm-up of at
  least about \(2/(1-\beta_2)\) updates (100 at \(\beta_2 = 0.98\); Ma and
  Yarats, AAAI 2021), or carries the optimizer state over; an exact resume
  needs no new warm-up. And sustained steps at a high peak LR: the final
  anneal settles near where the weights travelled, not back in the starting
  basin, so keep the leg's peak LR at or below the leg it extends.
- **Long warm-up costs progress on an extension.** Continuing a Vietnamese
  recognizer, a 1% warm-up led a 10% one on validation loss at every check
  and on test WER, with dev WER tied (one seed each).
- **Re-raising the LR is a deliberate exception.** When the selection metric
  stopped improving across the previous leg, raising the LR to leave the
  basin is acceptable; accept the forgetting risk and compare against the
  conservative leg.
- **Fresh or fragile parameters keep a longer warm-up:** a new head, a new
  language, or an unconverged student takes large early gradients.
- **Prefer Schedule-Free AdamW or WSD over multi-segment cosine legs.**
  Repeated cosine legs regress at each restart and underperform a single
  horizon. When training with **fp32 master weights** (standard mixed
  precision: fp32 parameters + bf16 autocast, as in HF `Trainer(bf16=True)`),
  default to `AdamWScheduleFree` (Defazio et al., 2024;
  `optim="schedule_free_adamw"` in HF Transformers) for anytime evaluation and
  seamless multi-segment continuation with carried optimizer state, or
  Warmup-Stable-Decay (WSD) when an explicit cooldown branch is preferred.
  - **fp32 master weights are mandatory for `AdamWScheduleFree`.** Under pure
    `bfloat16` parameter storage, in-place `lerp_` and the `1 - 1/beta1`
    eval/train inversion suffer severe 7-bit mantissa rounding drift and stall
    or diverge; fall back to `AdamW` + WSD when weights are stored in pure
    `bfloat16`.
  - **Call `optimizer.eval()` before both evaluation and checkpoint saving**,
    and `optimizer.train()` before stepping (HF `Trainer` does this
    automatically; custom PyTorch loops must do it explicitly).
  - **BatchNorm caveat:** models with BatchNorm layers (e.g. CNN/Conformer
    conv modules) need a short forward pass in `model.train(); optimizer.eval()`
    to refresh BN running stats at $x$ before eval, or should use WSD instead.
    LayerNorm/RMSNorm Transformers need nothing extra.
  - **Partial optimizer-state retention across leg boundaries
    (`--resume-state-retain` in `[0, 1]`):** default `1.0` carries full state
    (appropriate for continuations and adding same-task data). Use `0.0` to
    start fresh, or `(0, 1)` on structural shifts (new objective, new
    head/unfrozen modules, or large batch/LR jumps) to keep curvature
    conditioning (`exp_avg_sq`) while damping first-moment/momentum buffers
    and Schedule-Free's `k` / `weight_sum` / `z` offset.

### Early stopping during adaptation

- **No performance-based early stopping in the warm phase.** When training on
  a new corpus, adapting a student or distilling, declare a warm phase that
  covers adaptation and LR settling, not merely LR warm-up, and disable
  performance-based stopping during it. Start patience counting only after the
  model beats its starting baseline on the fixed development task metric;
  validation-loss patience alone cannot establish that improvement. Declare the
  phase length and comparison before launch.
- **A diagnosed degenerate trajectory may stop earlier:** non-finite updates,
  or sustained collapse to empty or wrong output confirmed in decoded examples
  after checking the data and execution path. A temporary metric regression or
  a large departure from the pretrained weights is not enough. Preserve the
  diagnostic evidence and report the stop as a failure, not convergence.
  Fixed compute ceilings and explicit user stops still apply; exhausting a
  budget without improvement is not convergence and does not authorize
  extending the run.

## Evidence

Adding a language to a trained speech recognizer, one seed each (draft
repository, `research/speech-recognition/multilingual/add-language.md`):

- Parakeet 0.6B (25 languages) plus Vietnamese, 40k updates: with no replay
  the 25 old languages collapse (FLEURS macro WER about 120%). With 50% replay
  they stay within about 0.5 macro WER of the replay-only control (12.65 vs
  12.17). Vietnamese reaches 22.3 WER, against 16.9 for a run that spends
  every update on it.
- A 115M Arabic model plus Spanish showed the same pattern at 10k updates:
  replay held Arabic at its control level, and Spanish-only training erased
  Arabic.

The 10–50% range and the fade-in come from graehl (2026-10-15); the
20%-replay and faded-in runs that test them are pending.

Schedule-Free AdamW vs. multi-segment cosine legs (`Qwen/Qwen2.5-0.5B` full
fine-tune on Albanian `cust-voanews`, 600 steps, matched data stream and
seed, 2026-11-26):

- **fp32 master weights + bf16 autocast** (13.57 GB peak VRAM all arms):
  single-leg oracle cosine (`5e-5`) reached `1.2979` dev NLL; 3×200-step
  cosine legs (`cos-3legs-fresh`) regressed at restarts and finished at
  `1.3533` (+0.0554); WSD (`5e-5`, 10% cooldown) reached `1.3142`;
  `AdamWScheduleFree` (`5e-5`) beat oracle cosine at early/mid checkpoints
  (`1.4888` vs `1.5358` at step 200) and tied it at step 600 (`1.2983`,
  −0.0550 vs 3-leg cosine).
- **Pure `bfloat16` weights** (no fp32 master weights, 9.48 GB VRAM):
  `AdamWScheduleFree` stalled at `2.1028` (`5e-5`) and drifted upward after
  step 400 at `1.5e-4` (`1.5398 → 1.6473`), while `AdamW` + WSD reached
  `1.3353`.

Tiny-state, Muon, and Blackwell FP8 evaluation (`Qwen/Qwen2.5-0.5B`, 300
steps, fp32 master + bf16 autocast, same Albanian `cust-voanews` stream,
2026-11-26):

- **Native `torch.optim.Muon` (`1e-3`, 2D hidden matrices) + `AdamW` (`5e-5`,
  1D/embed/head)** beat `AdamW` at every checkpoint (`1.4118` vs `1.4258` at
  step 300) while cutting optimizer state by 36% (`2.40 GB` vs `3.77 GB`,
  peak VRAM `12.24 GB` vs `13.57 GB`).
- **Tiny-state (VRAM-limited) winner: `Adafactor`** (`scale_parameter=False,
  relative_step=False`): `3.0 MB` optimizer state (99.9% smaller than AdamW),
  `9.89 GB` peak VRAM, fastest wall time (`57.4s` vs `75.2s` AdamW and
  `165.4s` `AdamW8bit`), and `1.4475` NLL (matching `AdamW8bit`'s `1.4492`).
- **Not promoted for fine-tuning:** `ScheduleFree+`
  (`AdamCScheduleFreePlusPaper`: `9.42 GB` opt state, `2.2795` NLL — Polyak
  step size tuned for long from-scratch pretraining), `AMUSE` (`1.4779`,
  `5.13 GB` opt state), and `SF-NorMuon` (`1.5126`, `5.13 GB` opt state).
- **Blackwell SM 12.0 FP8 (`torch._scaled_mm`):** raw FP8 kernels are
  `1.94×–2.37×` faster than BF16 for 0.5B–12B MLP shapes (`1.07×` for 115M
  FastConformer FFN), but eager PyTorch quantization overhead makes it
  `0.39×–0.88×` slower end-to-end; requires fused kernels (`torchao` +
  `torch.compile` or `transformer_engine` / `DeepGEMM`).

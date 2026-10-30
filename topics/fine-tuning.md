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

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

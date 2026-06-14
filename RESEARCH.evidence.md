# RESEARCH — evidence ledger

Append-only, agent-owned notes behind `RESEARCH.md`: rationale that does
not sharpen an actionable rule, named-technique pointers, and observations
worth keeping out of the token-paying main doc. Not loaded routinely;
consult when extending or auditing `RESEARCH.md`. Convention:
`topics/evidence-ledger.md`.

## 2026-06-14 — named techniques behind "Attributing a surprising change"

Pointers for the many-factor case. Non-actionable: the section itself says
to just run the one-at-a-time ablation/progression when cheap, and
accidental drift is rarely interaction-rich, so these are background, not
a workflow step.

- Screening designs — **fractional factorial**, **Plackett–Burman**:
  estimate main effects of many factors in far fewer than `2^N` runs by
  aliasing higher-order interactions, valid under effect sparsity +
  heredity (an interaction is active only if its parents are).
- **Combinatorial group testing** (Dorfman pooling): the "chopped subsets"
  generalization of binary search from one culprit to several; needs a
  monotone same-sign signal — a culprit must make any pool containing it
  read positive.
- Binary search / group testing fail under **sign cancellation even with
  independent (additive) effects**: a help pooled with a larger hurt reads
  ~null (false negative). So subset search needs same-sign + sparsity, not
  just independence — the same villain that makes the net understate
  per-cause effects.
- Cheap interaction *detector* (not identifier): run both progression and
  ablation. The per-factor gap (add-to-baseline vs remove-from-full) sums
  the interactions involving that factor, and `f(full) - [f(baseline) +
  sum of marginals]` is the total-interaction residual.

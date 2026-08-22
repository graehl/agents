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

## 2026-08-22 — score readouts without reading the failure (Sol incident)

Motivating incident for “Read the failure before reporting it”
(`_RESEARCH/evidence.md`). A Sol session on draft's pii-eval ontology-v2 v12
confirmation-annotation-calibration direct pass reported “failed its
zero-error stop rule” from the saved score alone. User pushback (“at least
look at one line of output”, “search logs for sus”) forced the autopsy the
readout should have led with: four dead invocations around the one valid run
(`direct-full-g31b-v3/20260822T034859Z`), a span-copy repair at row 10
(`2006‑XII` emitted as `2006“XII`, spans out of source order), and row 35
truncated mid-string at exactly the 3,072-token ceiling by a 6,000-character
Russian clinical chunk eliciting 101 findings. The retraction: the stop rule
fired mechanically, but the score was diagnostic-only (role 1 of 4) and
proved nothing about 31B annotation quality.

Design notes that do not sharpen the rule text:

- Trigger keyed to decision-bearing/surprising readouts, not all scores:
  mandatory row-reads on every hillclimb intermediate would be pure tax; the
  failure only matters when the number changes what happens next.
- Every prior inspection mandate had the wrong key for this incident: the
  result-sanity preview fires on *newly wired* paths (its “unless the path is
  unchanged” exemption licensed the skip), closure tests fire on *parking a
  line*, and the judgment.md option audit presupposes logs were already read.
- The “does not by itself license respending” clause guards the symmetric
  abuse: reclassifying a stop as a protocol defect must not become a free
  re-roll past a frozen stop rule; amending the protocol stays with its own
  rules and the user.
- The `PROGRAM.md`-reread bullet is user-directed (2026-08-22): program
  charters may state intake requirements (for example, sentence segmentation)
  whose omission explains the failure, and a negative result is exactly when
  those requirements have fallen out of context.

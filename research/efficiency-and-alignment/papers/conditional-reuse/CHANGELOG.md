# Conditional reuse and the limits of efficiency as an alignment signal: changelog

Each release is a git commit; this file records what each release changed and
is never rendered into the paper. Newest first.

## 2026-10-17 — Sparse optimizer interventions and audit conditions

Contributing-model: 6-astra

Add sharp scalar momentum reset bounds, finite-time bias-corrected Adam
segment optimization, adaptive-denominator suppression examples, and a
one-corruption SGD counterexample with honest later gradients. Prove a
sufficient stability condition linking cheap residual bounds to sampling
coverage. Distinguish step rejection, clipping, forged gradients, and direct
state edits. Add reproducible finite checks, all-step optimizer consistency
checks, and a scoped discussion of hardware attestation and verification.
The program now owns a theorem-development pilot and evidence record;
neural realizability and proof-assistant verification remain unestablished.

## 2026-10-17 — Behavioral and training-trajectory audit bounds

Contributing-model: 6-astra

Distinguish attacker-supplied triggers from ordinary-use boosting and
topic-specific lying, with output-only, weights-access, and training-trajectory
reviewers. Add elementary bounds for adaptive query coverage, audit/deployment
overlap, paired comparison scores, and random transition replay. Training draws
are seeded and reproducible; audit randomness is private even when the
attacker knows published audit methods. Ground the training proposal in
Proof-of-Learning and Proof-of-Training-Data, and update interpretability,
hidden-objective auditing, and cryptographic-backdoor references. Efficient
data-intake representation and neural concealment overhead remain unproved.

## 2026-10-17 — Conditional-reuse bound and sponsored-choice example

Contributing-model: 6-astra

Initial theoretical draft: exact Boolean gate accounting, passive-test miss
probability, a separate program-description bound, and the fictional Lucky
Charms example. Distinguishes an efficiency warning signal from a certificate,
without proposing an experimental companion.

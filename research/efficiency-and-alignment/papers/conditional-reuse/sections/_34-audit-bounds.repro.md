# Behavioral audit proof checks

The claims are elementary arguments in the manuscript, not model experiments.
Checked algebraically on 2026-10-17 by the contributing model 6-astra.

## Proposition 2

Fix the auditor, its query budget and reference function before selecting the
alternative. Under the honest transcript, the sum over input points of their
query-inclusion probabilities is the expected number of distinct queried
points, at most n. Choose a point with probability at most n/N. Coupling on
identical auditor coins makes the entire two transcripts identical until that
point is reached, so the total variation of transcript distributions is at
most n/N. Rejection probability is therefore at most alpha+n/N (and trivially
at most one). Adaptivity and randomized auditors are covered; weight access
and economically meaningful deployment mass are not.

## Proposition 3

The layer-cake representation of a [0,1]-valued measurable function proves the
expectation bound from the stated total-variation definition. Independent
situations and policy randomness give the product probability. In an adaptive
sequence, replacing independence requires a lower bound on every conditional
hazard along histories with no detections; equal one-trial marginals do not
suffice. All input-side observations and persistent state belong to the
situation. No production-versus-audit distance has been measured.

## Paired scores

For Y in [-1,1], Var(Y) <= 1. Independence gives Var(mean) <= 1/n.
Markov applied to the squared centered sample mean gives the two-sided bound.
Under either separated hypothesis, a wrong decision at Delta/2 entails a
deviation of at least Delta/2. A union bound over K fixed null categories
gives the displayed family-wise bound without requiring independence between
categories. Scores must be fixed before confirmation. A systematic nonzero
null difference or shared reference-model bias is outside the stated test.

Numerical example: (1 - 0.10 + 0.02)^36 < 0.05. The exact expression owns the
claim; the source contains no empirical success rate.

Executed against the dirty manuscript based on HEAD
`1a3bfe831d20ebb6873af205a14e4db01a2dc613`:

```bash
python3 -c 'print((1-0.10+0.02)**36, __import__("math").comb(990,100)/__import__("math").comb(1000,100), __import__("math").comb(999,100)/__import__("math").comb(1000,100))'
```

Output: `0.04970061748029956 0.34692771479200596 0.9`.
The latter two values check the transition-sampling expression for 10 and one
invalid updates among 1,000, with 100 sampled. Provenance level: manually
authored derivation plus this recorded arithmetic check, not a tracked run.

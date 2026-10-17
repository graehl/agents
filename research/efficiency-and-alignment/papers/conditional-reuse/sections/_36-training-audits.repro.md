# Training trajectory audit proof checks

The counting argument concerns a fixed transcript with an exact validity
predicate and a uniformly sampled subset. It is not a cryptographic soundness
proof for the practical systems cited in the paper.

Every selected record must open against the same binding commitment. Treat
hash collisions or other commitment failures separately from the elementary
sampling probability; the displayed expression is conditional on binding and
correct local verification. Missing evidence is rejection, not an omitted
sample. Dataset membership and all replay dependencies must be checked.

Of all choose(T,q) samples, choose(T-m,q) contain no invalid transition.
For q <= T-m, the ratio is the product of (T-m-j)/(T-j) for j from 0 through
q-1. Each factor is bounded by 1-m/T. For q>T-m the miss probability is zero.
For m=1, cancellation gives miss probability (T-q)/T exactly. At q=T every
nonzero m is detected. At m=0 every sample passes, even when the correctly
trained policy is malicious. These boundary cases distinguish transition
integrity from alignment.

Full exact verification establishes the declared endpoint by induction only
when the initial full state, update rule, ordered consumed data, randomness
and numerical semantics are fixed. It proves consistency with that training
history, not that no other computation occurred. Pretrained ancestry must be
verified or explicitly trusted. Final serving identity is a separate binding.

The nonuniform coverage argument sums inclusion probabilities to expected
sample count. It is a coverage statement, not a construction of a feasible
harmful transcript at the least-sampled update; record-dependent extra tests
can carry additional information. No final-harm-versus-invalid-step bound is
assumed. Under tolerance, even every accepted local update does not imply
exact endpoint equality or a bounded accumulated behavioral error.

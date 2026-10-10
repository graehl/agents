# Are mutants a valid stand-in for real faults?

> Read-backed digest (cluster B, trust `single-source`. One controlled
> study. Its headline coupling rate agrees with the Google high-priority-bug
> analysis in [targeted-mutation](targeted-mutation.md), which shares an
> author and uses a different method, so that is not an independent
> replication).

**Paper.** Just, Jalali, Inozemtseva, Ernst, Holmes, Fraser, "Are Mutants a
Valid Substitute for Real Faults in Software Testing?," FSE 2014
([PDF](https://homes.cs.washington.edu/~mernst/pubs/mutation-effectiveness-fse2014.pdf),
[local extract](../related-work/extract/just2014-mutants-real-faults/just2014-mutants-real-faults.md)).

## Method

The study uses 357 real faults from five Java programs (JFreeChart, Closure,
Commons Math, Joda-Time, Commons Lang; 321 KLOC). These were left from 1,179
candidate fix commits after requiring that the fault be reproducible and
that the fix could be separated from unrelated changes. Two authors checked
each fix independently (lines 115-158). This set became the core of
Defects4J.

From the developers' tests the authors built 480 suite pairs.
\(T_{pass}\) passes on the buggy version, and \(T_{fail}\) differs from it by
exactly one test, the one that triggers the fault. In 258 of these pairs the
triggering test adds no statement coverage (lines 162-187). They also
generated 35,141 suites with EvoSuite, Randoop and JCrasher (line 221).

Major mutated only the classes the fix modified, with four operator groups:
replace constants, replace operators, modify branch conditions, delete
statements. That gave about 230,000 mutants (lines 55, 233-235). Equivalent
mutants were not removed. Each comparison was run twice: once ignoring
coverage, and once counting only mutants in code that both suites cover
(lines 259-265).

A real fault is *coupled* to the mutants when \(T_{fail}\) kills at least one
mutant that \(T_{pass}\) does not.

## Evidence

- **Coupling rate.** 73% of real faults are coupled to mutants from these
  standard operators. For 95 of 357 faults (27%), no triggering test killed
  any additional mutant (lines 73-74, 315, 332).
- **Coverage control.** Across the 480 pairs, the mutation score went up in
  362 (75%), while statement coverage went up in only 222 (46%). Where the
  triggering test added no coverage, the mutation score still went up in
  153 of 258 pairs (59%). Where it did add coverage, the score went up in
  209 of 222 pairs (94%) (lines 297-299).
- **How many mutants per fault.** With coverage held fixed, a triggering
  test kills on average 2 extra mutants, against 28 when it also adds
  coverage. 40% of the coverage-neutral triggering tests killed no extra
  mutant at all (lines 305-311). The mutants coupled to faults came mostly
  from conditional-operator replacement, relational-operator replacement and
  statement deletion (line 313).
- **The uncoupled 27%.** Of the 95 uncoupled faults, 25 needed a stronger
  version of an existing operator: statement deletion that also removes
  return or break, argument swapping, argument omission. 7 needed a new
  operator. 63 (17% of all faults) have no plausible operator at all. These
  are mostly algorithm rewrites (37), plus code deletion, wrong-but-similar
  method calls, context-sensitive faults and numerical faults (Table 4,
  lines 317-398).
- **Correlation with real-fault detection.** On generated suites (194
  faults), mutation score correlates with real-fault detection more strongly
  than statement coverage does, significantly so for every program except
  Joda-Time (lines 468-470). With coverage controlled, \(\tilde T_{fail}\)
  has a significantly higher mutation score than \(\tilde T_{pass}\) for
  21/22, 27/32, 76/80, 18/18 and 40/42 faults across the five programs. The
  average \(\hat A_{12}\) is between 0.66 and 0.81 (Table 5, lines 476-483).

## Decision edge and limits

This is the validity premise behind every mutation budget. Its useful
result is about what mutation adds *beyond coverage*. Once coverage is
saturated, a fault-revealing test still raises the mutation score in about
6 of 10 cases, but only by about 2 mutants. That signal is real but narrow.
Mutation compute therefore pays off on code that is already covered and
only if mutants are placed near the fault. Diluting them across the whole
program washes the signal out, which is why Major mutated only the fixed
classes (line 235).

This study generated mutants only on the classes each fix modified, which
is the same kind of fault-scoped placement as diff-based mutation at review
time (framing a). It says nothing about running mutants in parallel or with
schemata (framing b). Its mutation analysis is the full kind (framing c),
run over every generated mutant, and it is used here as ground truth, not
as a cost-efficient practice.

Operator choice matters more than operator count: conditional, relational
and statement-deletion operators carry most of the coupling. 10% of faults
would be caught by operators that are only somewhat more expensive. The
17% that are algorithmic stand outside syntactic mutation no matter how
much compute is spent.

Limits. Five Java programs, all well tested. Faults were mined from linked
bug-fix commits, which may bias the sample (line 499). The definition of
coupling (at least one extra mutant killed) is a weak bar. Equivalent
mutants were left in, which is harmless for paired comparisons but
understates absolute scores.

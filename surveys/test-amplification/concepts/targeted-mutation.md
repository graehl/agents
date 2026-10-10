# Targeted mutation at code review (Google)

> Read-backed digest (cluster B, trust `single-source`; one deployment
> reported in two papers by the same four authors. The fault-coupling rate
> agrees with Just et al. 2014, which shares an author, so it is not an
> independent replication).

**Paper.** Petrović, Ivanković, Fraser, Just, "Practical Mutation Testing at
Scale: A view from Google," IEEE TSE 2021
([arXiv](https://arxiv.org/abs/2102.11378),
[PDF](https://arxiv.org/pdf/2102.11378),
[local extract](../related-work/extract/petrovic2021-practical-scale/html/2102.11378.md)).

**Paper.** Petrović, Ivanković, Fraser, Just, "Does Mutation Testing Improve
Testing Practices?," ICSE 2021
([arXiv](https://arxiv.org/abs/2103.07189),
[PDF](https://arxiv.org/pdf/2103.07189),
[local extract](../related-work/extract/petrovic2021-improve-practices/html/2103.07189.md)).

## Method

### The production system (TSE)

Mutation runs only when a changelist goes to code review, and only on the
lines it adds or modifies. A mutant is generated only on lines that existing
tests cover, because a mutant on an uncovered line is certain to survive.
Line coverage maps each line to the test targets that cover it, and that
mapping picks the smallest set of tests to run against each mutant
(TSE:69-73). Each line gets at most one mutant from five operators (AOR,
LCR, ROR, UOI, SBR). If the first operator tried cannot apply, the next one
is tried (TSE:79, 352).

Before mutating, an `expert` function marks *arid* AST nodes, which are
never mutated. A compound node is arid only when all of its children are.
More than a hundred hand-written rules, grown from "Not useful" clicks in
review, cover logging, time and deadline calls, flags, monitoring,
memory-capacity hints, caches and similar code (TSE:176-186, 285). Targeted
selection orders the operators by their past survival and productivity in
similar AST contexts, found with pivot multisets plus MinHash nearest
neighbours, instead of a random shuffle (TSE:388-398). Each mutant gets its
own temporary repository state, and all of them build and test in parallel
in a single round. The authors rejected iterative rounds as an inefficient
use of build and test capacity (TSE:132, 304). At most 7 surviving mutants
per file are shown as review findings (TSE:132).

### The longitudinal and coupling study (ICSE)

The dataset is 14,730,562 mutants on 662,584 changes over six years. The
comparison group is 8,788,791 changes from projects that had coverage
reporting but no mutation testing (ICSE:94-96). Exposure counts how often a
file had findings reported before. For fault coupling, the authors took
1,502 fixes of high-priority bugs and changed the system to generate *all*
mutants on the lines each fix touched, in both the buggy and the fixed
version. The arid filter stayed on. A mutant counts as fault-coupled when
it survives on the buggy version and the fix's test kills it on the fixed
version (ICSE:345-356).

## Evidence

### Cost reduction (TSE)

| Generation strategy, per changelist (5,000-CL sample) | Median mutants | 25th–75th percentile |
|---|---|---|
| All mutants | 820 | 460–1,734 |
| One per line | 77 | 31–138 |
| One per line, arid nodes skipped | 7 | 3–19 |

Source: TSE:680-694. The differences are significant by Mann-Whitney U.

Across 776,740 changelists the system generated 16,935,148 mutants and
surfaced 2,110,489 of them; 66,798 got explicit feedback (TSE:642). The
existing tests killed 87.5% of generated mutants (TSE:716). That part of the
compute produces no finding, which is why the operator ordering aims to
maximize survival. Context-based operator selection, compared with random
selection, raised the survival probability of a generated mutant by more
than 40% and its probability of a "Please fix" by almost 50% (TSE:754).

### Usefulness to developers (TSE)

Developers first marked 85% of sampled mutants as unproductive (TSE:43).
Over six years the arid rules raised the productive share from 15% to 89%.
The first three rule families (logging, time, flags) alone took it to about
80% (TSE:48, 285). Of all surfaced mutants that got feedback, 82% were
marked productive, and that share rose from 80% to 89% after the service
launched (TSE:668). The abstract reports over 24,000 developers on over
1,000 projects (TSE:15).

### Effect on tests and coupling to real faults (ICSE)

- **More tests.** The number of changed test hunks per file rises with
  mutant exposure (Spearman \(r_s = 0.9\)). In the coverage-only comparison
  group the correlation is \(r_s = -0.24\). The median number of test hunks
  added during review is 1 with mutation and 0 without (ICSE:136-138). The
  authors rule out larger changelists and coverage-driven testing as
  confounders (ICSE:144-167). This is an observational design, not a
  randomized trial.
- **Stronger tests.** Mutant survival on later changes falls as exposure
  rises (\(r_s = -0.50\)), and reviewer fix requests also fall
  (\(r_s = -0.34\)) (ICSE:189-191).
- **Fault coupling.** For 1,043 of 1,502 high-priority bugs (70%), a
  fault-coupled mutant existed on the change that introduced the bug, and
  every bug-introducing change was already covered by tests (ICSE:370). The
  analysis took about 400k mutants and more than 33M test-target executions.
  222 bugs needing more than 500 test targets were excluded as too costly
  (ICSE:242-246). Mutation testing was actually enabled for only 10.8% of
  the bug-fixing changes (ICSE:227). The 70% figure is therefore
  counterfactual: it says what the system *would* have flagged. Of 50
  sampled uncoupled bugs, 14 needed a stronger operator, 13 needed a missing
  operator, and 23 had no applicable operator (ICSE:386-392).
- **One mutant per line suffices.** On lines with several mutants, more than
  90% of lines had all mutants killed or none (ICSE:406, 414). This is how
  the authors carry the all-mutants coupling result over to the production
  setting, which generates only one mutant per line.

## Decision edge and limits

This work answers the "mutate only where you know what could be affected"
option (framing a) directly. Mutation is scoped to the diff, only covered
lines get mutants, and only the tests that cover a line run against its
mutants. Together these keep a changelist to a median of 7 mutants. The
evidence says mutation compute pays off at review time on changed, covered,
non-trivial lines, after coverage has nothing more to report. The binding
constraint is how many findings developers will act on, not compute. Most
of the remaining compute goes to killed mutants, so better operator
selection buys more findings per build.

On framing (b), mutating many sites at once: Google parallelizes across
mutants, giving each its own build, and reports neither mutant schemata
(one compiled program carrying many switchable mutants) nor split-stream
execution (forking a test run at the mutated point). The ICSE redundancy
result argues against spending compute on many operators at one site.

On framing (c), mutating one site and rerunning everything: the coupling
rig, which ran every affected test target for every mutant on a line, is
the paper's own evidence that this does not scale.

Limits. All of this is from one company, one code style and one review
culture. The arid rules are tuned to Google, and the paper says other
environments need their own (TSE:846). "Productive" means a developer
clicked "Please fix", not that a fault was prevented. Mutant suppression
was in place throughout, so the reported coupling and productivity are
conditional on it.

# Fuzzing payoff curves and stopping rules

> Read-backed digest (cluster C, trust `single-source` throughout; six papers.
> Five share Böhme as an author, so agreement among them is not independent
> confirmation; Nikolic & Jain is an independent preprint). Covers how fast
> fuzzing returns diminish, how to estimate the remaining payoff of a running
> campaign, when to stop, and how to split a fixed budget across many
> programs.

## Exponential cost of discovery (Böhme & Falk)

**Paper.** Marcel Böhme and Brandon Falk, "Fuzzing: On the Exponential Cost of
Vulnerability Discovery," ESEC/FSE 2020
([PDF](https://mboehme.github.io/paper/FSE20.EmpiricalLaw.pdf),
[local extract](../related-work/extract/bohme2020-exponential-cost/bohme2020-exponential-cost.md)).

### Method

The study runs libFuzzer on 263 OSS-Fuzz programs (6 h, 4 repetitions) and on
25 Fuzzer Test Suite (FTS) programs (6 h, 20 repetitions), plus AFL on six
open-source programs (96 h; libxml2 for 90 days). It does not run more
machines. It simulates "2^x machines" by dividing campaign timestamps by
2^x, which assumes zero synchronization overhead and a perfectly shared seed
corpus. The authors call this a lower bound on cost. A blackbox urn model
(species discovery) and simulations explain the observed curves.

### Evidence

- Linearly more new species (crashes, features, edges, known vulnerabilities)
  need exponentially more machines; a linear fit of species gained on
  log(machines) gives R² > 98% on OSS-Fuzz and > 97% on FTS (except vorbis).
  Their example is that each extra bug found in 24 hours "might" need twice the
  machines. That factor is illustrative, not a fitted constant.
- Rediscovery is cheap: 512 machines reach in under a minute what one machine
  reaches in about 6 h (time to the same crash count, vulnerabilities and
  coverage).
- The law holds only if species probabilities follow a power law. With a
  single species, or with equiprobable species, it fails.
- A preliminary experiment on real parallel greybox instances found that
  without a shared queue, 32 greybox fuzzers scale barely better than 32
  blackbox fuzzers. Measured scaling is therefore worse than the simulated
  curve.

## Residual risk and adaptive bias

**Paper.** Marcel Böhme, Danushka Liyanage, Valentin Wüstholz, "Estimating
Residual Risk in Greybox Fuzzing," ESEC/FSE 2021
([PDF](https://mboehme.github.io/paper/FSE21.pdf),
[local extract](../related-work/extract/bohme2021-residual-risk/bohme2021-residual-risk.md)).

### Method

Residual risk is the probability that the next input reveals the first bug.
It cannot be estimated directly, so the paper estimates discovery probability
(the chance that the next input adds coverage) as an upper bound. Greybox
fuzzing has *adaptive bias*: new seeds raise the chance of rare behaviour as
the campaign runs, so blackbox estimators are invalid. The paper proposes
reset estimators, mean-local estimators (weighted per-seed estimates) and
log-log extrapolation. Ground truth comes from blackbox side campaigns as
long as the greybox run. Setup: libFuzzer on six FuzzBench subjects, 20
campaigns each, up to about 10^9 inputs (2–7 days per campaign).

### Evidence

- Good-Turing and Laplace underestimate true discovery probability by up to
  four orders of magnitude on greybox campaigns. The gap usually narrows later
  in the campaign, except on freetype.
- Mean-local Laplace stays within one order of magnitude for nearly the whole
  campaign and becomes conservative late. Mean-local Good-Turing almost never
  underestimates. Reset estimators overestimate by up to three orders.
- Discovery probability is roughly a power law in the number of inputs, with
  R² near 97% on four of six subjects. Cutting risk by a factor x then costs
  about c·x more inputs.
- AFL was excluded because its circular queue makes estimates swing.

## Coverage-rate extrapolation (Liyanage et al.)

**Paper.** Danushka Liyanage, Seongmin Lee, Chakkrit Tantithamthavorn, Marcel
Böhme, "Extrapolating Coverage Rate in Greybox Fuzzing," ICSE 2024
([PDF](https://mboehme.github.io/paper/ICSE24-predict.pdf),
[local extract](../related-work/extract/liyanage2024-coverage-rate/liyanage2024-coverage-rate.md)).

### Method

The method shuffles local windows of the greybox incidence matrix to build
blackbox approximations without adaptive bias. It estimates the coverage rate
on each window and fits a log-log line to extrapolate. The baseline is Chao and
Jost's biostatistical extrapolator. Data: AFL++ on five Fuzztastic programs,
30 one-week campaigns each, with coverage sampled in 15-minute units. Both
methods get add-one smoothing because singleton counts are often zero.

### Evidence

- For short-horizon predictions (half the current campaign length), mean
  absolute log error is 0.07–0.9 against 0.2–2.9 for the baseline. That is at
  least an order of magnitude better on 4 of 5 subjects, mainly for campaigns
  over 50 h. On readelf the difference is mostly not significant.
- The baseline is consistently negatively biased and worsens with horizon. The
  new method's median error stays flat up to three times the campaign length.
- When predicting the time a target rate is reached, the result is
  significantly closer on only 3 of 5 subjects (35–77% closer).

## Green fuzzing: saturation on predicted-vulnerable code

**Paper.** Stephan Lipp, Daniel Elsner, Severin Kacianka, Alexander Pretschner,
Marcel Böhme, Sebastian Banescu, "Green Fuzzing: A Saturation-Based Stopping
Criterion using Vulnerability Prediction," ISSTA 2023
([PDF](https://mboehme.github.io/paper/ISSTA23-green.pdf),
[local extract](../related-work/extract/lipp2023-green-fuzzing/lipp2023-green-fuzzing.md)).

### Method

The criterion stops a campaign when coverage of *potentially vulnerable*
functions stalls for a window of 2–8 h. A function-level classifier built on
static-analyzer findings and code metrics flags those functions. Training
data: 22 programs and 121 vulnerable functions from CVEs. The trade-off study
replays 24-h runs of 8 greybox fuzzers × 8 programs × 20 repetitions (1,280
campaigns) from the FuzzTastic dataset. Its 119 bugs are deduplicated by top-3
stack frames.

### Evidence

- Classifier ROC-AUC is about 0.84 under cross-validation and 0.75 on held-out
  programs.
- Against crash saturation it stops 6–12 h earlier (25–50%) on four subjects
  while missing about 0.5 bugs on average. Averaged over all settings it saves
  4.1 h. Bugs are missed in 11.5% of bug-finding campaigns, and the criterion
  finds extra bugs in 4.3%. On objdump it runs 6–12 h *longer*.
- Against function-coverage saturation it saves 4.8–9.6 h while missing 0.2
  bugs. It saves nothing on JasPer, where many functions are flagged.

## Entropic: allocation inside one campaign

**Paper.** Marcel Böhme, Valentin J. M. Manès, Sang Kil Cha, "Boosting Fuzzer
Efficiency: An Information Theoretic Perspective," ESEC/FSE 2020. The fetched
text is the CACM 2023 Research Highlight
([PDF](https://mboehme.github.io/paper/CACM23-entropic.pdf),
[local extract](../related-work/extract/bohme2020-entropic/bohme2020-entropic.md)).

### Method

Entropic gives more fuzzing energy to seeds whose mutants show higher Shannon
entropy over globally rare coverage features. It uses add-one estimates so
that unfuzzed seeds are tried. The change is 363 lines in libFuzzer and is
compared with stock libFuzzer: FTS (12 programs, 1 h, 40 repetitions) and
OSS-Fuzz (263 programs, 6 h, 4 repetitions).

### Evidence

- On FTS, Entropic beats libFuzzer on 9 of 12 programs and is usually more than
  twice as fast to the same coverage.
- On OSS-Fuzz, Entropic has more coverage at 6 h on about 77% of programs and at
  least 10% more on about 25%. It is at least 2× faster to libFuzzer's 6-h
  coverage on about 50%. The two break even at about 10 minutes. Entropic
  loses on the larger programs, because its overhead grows with branch count;
  the median overhead is 2% of total time.
- The text reports that Google evaluated it independently and made it
  libFuzzer's default schedule. It gives 25,000 machines in one place and
  100k in another. The located text does not include Google's evaluation, so
  the grade stays `single-source`. The text also says "all experiments …
  repeated at least 40 times," which conflicts with the 4-repetition OSS-Fuzz
  setup.

## Fixed budget across many programs (Nikolic & Jain)

**Paper.** Ivica Nikolić and Racchit Jain, "Fuzzing at Scale: The Untold Story
of the Scheduler," arXiv 2024 ([arXiv](https://arxiv.org/abs/2406.18058),
[PDF](https://arxiv.org/pdf/2406.18058),
[local extract](../related-work/extract/nikolic2024-fuzzing-at-scale/html/2406.18058.md)).
The paper is an unreviewed preprint.

### Method

This is "wide" fuzzing: far more programs than cores, here p ≫ c, with 30
cores. An unmodified fuzzer runs on every program, and a scheduler pauses
and resumes the fuzzer processes (SIGSTOP/SIGCONT) in 0.1-s slices. The
objective is total edge coverage across all programs. The baseline is
round-robin, equal time per program. Three dynamic schedulers treat each
program as a multi-armed bandit arm whose reward is coverage per unit time:
simple ε-greedy, discounted (γ = 0.9), and Boian, which cycles γ and raises ε
from 0.01 to 0.75 so allocation flattens as past coverage stops predicting
future coverage. Benchmarks: UbuntuBench, 5,467 automatically built binaries
from 75,799 Ubuntu packages, and 345 OSS-Fuzz binaries. Comparisons use 1,000
UbuntuBench programs at an average of 15 min each, or all 345 OSS-Fuzz
programs at 1 h each. Each configuration runs once. Results are reported both
as total coverage and as "voting", the net share of programs covered better.

### Evidence

- **Total coverage.** Boian beats round-robin by 29% on UbuntuBench and 10% on
  OSS-Fuzz. Simple and discounted bandits gain 15–19% and 9–11%. Boian gave
  programs between 119 s and 8,878 s, against round-robin's 900 s each.
- **Voting.** Under the per-program measure, simple and discounted bandits are
  *worse* than equal allocation (−47% and −19% on UbuntuBench), because they
  starve most programs. Only Boian beats round-robin on both measures (+8%
  and +9% voting).
- **Scheduler against fuzzer.** Switching AFL to AFL++ under round-robin gains
  14% and 11% total coverage. Keeping AFL with Boian gains 41% and 10%. AFL
  with Boian against AFL++ with round-robin: +23% total but +1% voting on
  UbuntuBench; 0% total and −11% voting on OSS-Fuzz. "As important as the
  fuzzer" holds for total coverage on the large, unfuzzed benchmark, not for
  per-program coverage on OSS-Fuzz.
- **Bugs.** Boian with AFL++ and with Honggfuzz, 3 days × 30 cores each, found
  4,908 bugs in 675 UbuntuBench programs, counted as unique Valgrind crash
  traces. Bugs were not triaged or reported, and the count includes SIGHUP,
  SIGINT and abort traces. No bug comparison against round-robin was run;
  every scheduler comparison is on coverage.
- **Residual-risk methods.** None are used. The reward is raw discounted
  coverage per unit time, with no missing-mass estimate, no Good-Turing, and
  no correction for adaptive bias, and the estimator papers above are not
  cited. The paper states without citation that OSS-Fuzz allocates fuzzing
  time equally.

## Decision edge and limits

- **Per-target returns fall off fast.** On one target, more machines buy
  rediscovery at linear cost but new findings at exponential cost. Budget
  beyond saturation goes further on new harnesses, other targets or better
  mutators than on more cores. Böhme & Falk's practitioner discussion
  ("fuzzing everything a little") points the same way, but is a discussion
  remark, not a measured result.
- **Across many targets,** shifting time toward programs still gaining coverage
  beats equal allocation on total coverage (10–29%, single runs). A greedy
  shift starves most programs, so the scheduler has to raise exploration
  over time. A natural improvement, not yet tested, would replace the raw
  coverage-rate reward with the bias-aware discovery-probability estimators
  above, which give the marginal value of the next slice directly.
- **Stopping.** A stall in raw coverage or crash counts is a weak signal.
  Classical missing-mass estimators make greybox campaigns look safer than
  they are, by up to four orders of magnitude. If a risk threshold drives
  stopping, use bias-aware estimators (mean-local) or log-log extrapolation.
  Lipp's criterion trades a small number of missed bugs for 4–10 h saved per
  24-h run, and it relies on a vulnerability predictor of moderate accuracy.
- **Within one campaign,** a better power schedule (Entropic) roughly halves
  time to coverage on most subjects. It does not change the exponential shape.
- **Limits.** Machine scaling is simulated, not measured. Subjects are C/C++
  parsers and libraries. Coverage features stand in for bugs. Evaluations use
  4–30 repetitions; the scheduler study uses one. No independent replication
  of these estimators or schedulers was located.

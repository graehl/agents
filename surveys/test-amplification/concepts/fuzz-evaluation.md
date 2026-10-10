# Discounting "technique saves fuzzing compute" claims

> Read-backed digest (cluster C). The two literature surveys are
> `single-source`. Their findings about the field point the same way six years
> apart, but the SoK builds on Klees, so it is not independent confirmation.
> The re-runs are `failed-replication` only for the specific claims they
> tested: AFLFast's generality in Klees, eight papers' claims in the SoK.
> None of those papers is covered elsewhere in this survey.

## Evaluating Fuzz Testing (Klees et al.)

**Paper.** George Klees, Andrew Ruef, Benji Cooper, Shiyi Wei, Michael Hicks,
"Evaluating Fuzz Testing," ACM CCS 2018
([arXiv](https://arxiv.org/abs/1808.09700),
[PDF](https://arxiv.org/pdf/1808.09700),
[local extract](../related-work/extract/klees2018-evaluating/klees2018-evaluating.md)).

### Method

The authors reviewed 32 fuzzing papers from 2012–2018, found by citation
chasing from 10 high-impact papers. They then ran more than 50,000 CPU-hours
of AFLFast against AFL 2.43b on nm, objdump, cxxfilt, gif2png and FFmpeg:
24-h trials, at least 30 per configuration, under several seed choices. For
cxxfilt they built ground truth by replaying all 57,142 crashing inputs
against 812 later versions built with ASan/UBSan. A bug is the commit that
stops the crash, with one batch commit split by hand.

### Evidence

- **Survey.** No paper carried out every step of their recipe; every
  evaluation lacked something. 17 of 32 do not say how many trials they ran,
  apparently one. 12 of the 15 with multiple trials report no variance and no
  statistical test. 11 use timeouts under 5–6 h. About a quarter count bugs
  directly; most count deduplicated crashes. The median paper tests 7 real
  programs.
- **Run-to-run variance.** On nm, a single run could make AFL look better
  (about 1,200 against 800 crashes), but medians over 30 runs reverse it (400
  against about 1,250). On gif2png (51 against 39) and FFmpeg (369.5 against
  382.5), the median gaps are not significant over thirty 24-h trials.
- **Time and seeds.** With three sampled seeds on nm, AFLFast leads
  significantly at 6 h and AFL leads significantly at 24 h. With an empty seed
  AFLFast finds 1,239 crashes on nm; with one valid seed it finds 24, no
  different from AFL's 23.
- **Deduplication.** The 57,142 coverage-unique cxxfilt crashes map to 9 bugs.
  That overcounts by about 6,339× for coverage profiles and 66× for top-3 stack
  hashes (595 hashes), and about 16% of hashes are shared across bugs, so
  stack hashing would drop some bugs. AFLFast's crash advantage is significant
  (p about 10^-10), but its bug advantage is not (p = 0.066). No single run
  found all 9 bugs.
- **Generality.** AFLFast's advantage reproduces on the binutils programs it
  was originally tested on, but is not significant on FFmpeg or gif2png.
- **Recommendations.** Multiple trials with statistical tests (they follow
  Arcuri and Briand: Mann-Whitney U and Vargha-Delaney A12); known-bug
  targets, with coverage only as a secondary measure; several documented seed
  sets, including the empty seed; timeouts of at least 24 h, or a stated
  reason for less, with performance plotted over time; and a shared benchmark
  of about 25 programs or more.

## SoK: Prudent Evaluation Practices for Fuzzing

**Paper.** Moritz Schloegel, Nils Bars, Nico Schiller, Lukas Bernhard, Tobias
Scharnowski, Addison Crump, Arash Ale-Ebrahim, Nicolai Bissantz, Marius
Muench, Thorsten Holz, "SoK: Prudent Evaluation Practices for Fuzzing," IEEE
S&P 2024 ([arXiv](https://arxiv.org/abs/2405.10220),
[PDF](https://arxiv.org/pdf/2405.10220),
[local extract](../related-work/extract/schloegel2024-sok-prudent/html/2405.10220.md)).

### Method

The authors found 289 fuzzing papers from 2018–2023 at four security and three
software-engineering top venues. They randomly sampled 150 (52%) and reviewed
each for targets, baselines, runtime, cores, seeds, metrics, statistics and
claimed CVEs. They checked 339 CVEs from 35 papers against public records and
maintainer responses. They then tried to reproduce parts of eight papers
(MemLock, SoFi, DARWIN, FuzzJIT, EcoFuzz, PolyFuzz, Firm-AFL, FishFuzz),
using 10 trials of 24 h on one core each unless the paper specified otherwise.
The question was whether Klees et al.'s guidelines had been adopted.

### Evidence

- **Statistics.** 63% of papers run no statistical test. 55% use fewer than 10
  trials in at least one experiment. 15% apply Mann-Whitney U with 5 or fewer
  trials; with 3 trials that test can never reject. 88% report no effect size
  and 73% report no uncertainty.
- **Resources and seeds.** 5% allocate compute unfairly. That includes four
  papers that gave the new tool untimed preprocessing, such as static analysis,
  before an equal fuzzing budget. 25% do not report core counts. 50% do not
  disclose seeds, and 5% give fuzzers different seed sets.
- **Metrics.** 45% do not define how coverage was measured. Bitmap collisions
  can under-report coverage by up to 9%. Of 339 claimed CVEs, only 43% are
  valid and fixed or acknowledged. 20% were ignored by maintainers, 11% were
  invalid or disputed, and 26% are still reserved.
- **Baselines.** 20% omit a relevant state-of-the-art fuzzer and 3% omit their
  own base fuzzer. AFL, unmaintained for years, remains the most common base
  (30%) and comparison target (35%).
- **Case studies.** None of the eight papers' claims was fully reproduced. On
  FuzzBench, DARWIN was best on 4 of 18 targets against the 15 of 19 the paper
  claimed, and did no better than a random-reweighting control. FuzzJIT
  reported up to +33% coverage over Fuzzilli; the reproduction measured −2% to
  −12%. EcoFuzz leads on a nonstandard metric but has lower branch coverage.
  FishFuzz's coverage gain falls from 8.44% to 1.69% when measured on a
  neutral binary. MemLock's crashes appear only under an undocumented
  stack-size limit. SoFi's artifact was incomplete and could not be run. Its
  seven browser-engine "vulnerabilities" were all rejected by developers.
- **Recommendations.** At least 10 trials, or a power analysis; bootstrap or
  permutation tests with multiple-comparison control; effect sizes and
  intervals; 24 h or more, extended if a fuzzer has not flatlined; equal
  seeds; coverage measured on a common, collision-free binary; known-bug
  benchmarks; ablation baselines that isolate the new component.

## Decision edge and limits

A published claim that technique X saves compute or finds bugs faster should
be discounted before it drives allocation:

- **Baseline age.** Gains over AFL or AFLGo-era code may vanish against AFL++
  or LibAFL. LibAFLGo (see `change-directed-fuzzing.md`) shows this for
  directed fuzzing, and DARWIN shows it for mutation scheduling. AFLChurn and
  AFLGo were measured against AFL.
- **Hidden compute.** Build-time analysis, preprocessing, GPUs (Fuzz4All) or
  extra cores outside the timed budget all make the comparison unequal. Count
  wall-clock from target selection, as LibAFLGo does.
- **Statistics on few trials.** Effects measured with 4–5 repetitions (Entropic
  on OSS-Fuzz, Zhang's driver comparison, Fuzz4All) give direction but not
  ratchet-grade evidence. Single runs (Nikolic & Jain's scheduler comparison)
  give less. Means over censored time-to-exposure data with imputed caps
  (AFLGo) are biased. A ranking at one cutoff can flip at another, as Klees
  showed with nm at 6 h and 24 h.
- **Metric drift.** Unique crashes, AFL "paths" and CVE counts overstate, by
  three orders of magnitude for coverage-unique crashes on cxxfilt. Prefer
  deduplicated known bugs (MAGMA, FuzzBench bug benchmarks) or survival
  analysis.
- **Limits.** Both surveys cover academic papers, not industrial deployments.
  The SoK's case studies were chosen partly because something looked off on
  first reading, so the eight failures are not a base rate. Klees's ground
  truth covers one program (cxxfilt), and its other experiments count
  coverage-unique crashes, a metric the paper itself shows to be unreliable.

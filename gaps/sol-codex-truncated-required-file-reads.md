---
slug: sol-codex-truncated-required-file-reads
noticed: 2026-08-11
where: AGENTS.global.md project-entry reads / Codex tool-output truncation
---

**Gap:** the failure surface for Sol under Codex reading required files is
unmeasured. In session `019ff32e-d080-7753-b021-1bfc10996d96` at `xhigh`, Sol
put project instructions, user/harness supplements, vocabulary, and a large
handoff in one command. The shell produced about 141k tokens; nested and outer
tool budgets reduced the model-visible result to about 10k tokens, with
explicit truncation warnings and a middle-elision marker. `AGENTS.local.md`
was emitted in the elided middle. Sol followed up on several other files but
not that one, then initially represented the boot read as complete. It read
the local amendment only after the user prompted a symlink/instruction-layout
audit.

One occurrence does not establish the probability or boundary of the failure.
Unknown factors include individual and combined file length, required-file
position within truncated output, number and kind of co-read artifacts,
reasoning effort, and request prefixes that make the main task appear urgent
enough to favor progress over completing boot reads. Whether and where other
harnesses impose comparable output ceilings is also unmeasured.

At the 2026-08-11 measurement, optional `AGENTS.supplemental.md` is 19,699
tokens and `RESEARCH.supplemental.md` is 11,375, both beyond Codex's default
10,000-token complete-result ceiling. `RUNS.supplemental.md` is 7,935 and fits.
Harness-injected files are outside this tool-read comparison.

On 2026-08-12 those monoliths were reorganized into condition-routed packet
directories. The largest independent reads after cleanup are
`AGENTS/change-delivery.md` at 7,446 tokens, `_RESEARCH/artifacts.md` at 6,074,
and `_RUNS/monitoring.md` at 4,968; the RESEARCH and RUNS routers are 486 and 385
tokens. This lowers the known truncation exposure without adding a per-read
verification ritual. It does not measure how often an agent misses a route or
otherwise mistakes partial output for a complete required read.

**Noticed while:** investigating Sol's phrase “the large tool output truncated
before it” after a PII-research takeover boot. The trace showed middle elision,
not silent tail loss, and showed that command completion was mistaken for
complete incorporation of required contents.

**Fix sketch:** `AGENTS.codex.md` records the observed default outer ceiling
and its independence from the nested command budget. Long global packets are
now condition-routed files below that ceiling. No per-read confirmation ritual
is presently justified. This is in the category of basic steps that must
already be reliable: a typical task depends on roughly 1000 other little steps
of similar difficulty, and we can't guard each one with 4 additional simple
steps. Teaching this instance may merely move the failure.

The measurement is current as of 2026-08-11 and should be reevaluated monthly.
Characterize probability across output sizes and target positions, with and
without urgency/prioritization prefixes; remeasure Codex's active ceilings and
compare other harnesses when directly observable. Use the result to decide
whether any additional mitigation has material leverage; do not infer that it
does from this trace alone.

# Investigation and delegation details

> Slow-path rationale for verification, retrieval, delegation, and standalone bug-report intake.

Consult the matching named section for a standalone defect intake, an
unfamiliar-code investigation, or delegation whose boundaries need more than
the compact rule. `AGENTS.global.md` retains the binding rules and wins on
conflict.

## Verification and retrieval

Verify claims about a project against the repo before relying on them;
treat user and agent assumptions as hypotheses until checked. `rg` is
available.

**Verify before voicing, not only before relying.** When about to
state a specific fact about the user's system, a tool, or a config —
a path, default, flag, schema key — and a definitive check is cheap
(read the source, list the dir, run one query), do the check instead
of asserting from priors or narrating a guess as settled. Speculation
and thinking-aloud are welcome, but label them; an unverified specific
must not arrive dressed as fact. This binds equally when agreeing with
the user's own guess — the second-epistemic-step duty in *Agreement
and disagreement quality* applies to confirmations too. Worked
instance: stating a tool's default config dir from memory instead of
reading its `getAgentDir()`, and nearly conceding a real settings key
was a "hallucination" to agree with the user — one grep showed it
existed.

### Delegation

Whether and when to delegate is your judgment call — these defaults
inform it rather than gate it. Do not overdelegate, for two concrete
reasons: implementation never goes to a lesser model than the
session's, and plans are built visibly in the parent so the user can
engage with them as they form — hence no dedicated planning subagents,
and the core trace, a single continuous investigation, and final
synthesis stay in the parent. A higher-priority instruction that
explicitly requires a named agent still governs.

Delegation is flat: subagent depth is capped at 1 — generally enforced
mechanically; plan for it regardless. A subagent is a *leaf*, with no
inter-agent facilities beyond reporting to its creator and messaging
siblings. Orchestration lives in the parent; never write a delegated
prompt whose plan assumes the agent can spawn helpers, and tell each
leaf to use its tools directly. A leaf is not one-shot: where the
harness can continue a spawned agent, re-engaging the same leaf across
turns is fine.

Shapes worth considering:

- **Data-parallel fan-out** — independent items, one leaf each, when
  parallelism materially cuts wall-clock time.
- **Sequential fold** — one leaf re-engaged item by item over a bulky
  homogeneous sweep, keeping per-item detail out of the parent's
  context; the accumulator is the message stream back to the parent or
  a handoff/journal file read in full before each append. Neutral, not
  preferred: direct work appending digests to such a journal has the
  same property. Do not fold away the core investigation — the parent
  keeps the trace it must reason over.
- **Standing advisor/oracle** — one leaf kept for the task and
  consulted repeatedly for independent judgment, e.g. a goal oracle
  asked "is the original request actually finished?" before claiming
  completion.

A journal for a task starts untracked in `tasks/journals/`, and no
journal is ever committed automatically — not every journal has
lasting value. Most feed the eventual commit message rather than the
repo: condense there and discard. For one worth keeping as a file,
redact/condense it for value and ask for review before git
publication, into `topics/journals/` or a `journals/` subfolder
beside the plan file being implemented. Name a journal file after the
topic(s) or task(s) it touches. Beyond the fold accumulator, a
journal is the place to log mid-task spec or requirement changes —
dated, each marked user-directed or agent-derived — so drift from
the original request stays reconstructible.

### Standalone bug-report intake

When a session- or topic-opening user message resembles a report of a
new or unrelated defect, read `topics/handling-bug-reports.md` before
deciding whether the current tree needs a change. The user's direct
observation is credible evidence that the behavior occurred, but the
topic governs checking whether the same defect exists here now,
distinguishing the exact report from a related defect, and reporting
an evidence-backed no-change outcome when appropriate.

A complaint about the result of an implementation effort already in
progress does not trigger this intake protocol. It is evidence and
refinement inside the active feedback loop. Tests, investigation,
classification, or a focused subtask remain available when naturally
useful; this exclusion only prevents the instructions from mandating
that process for every correction. If the message instead introduces
a genuinely unrelated defect, apply the protocol when taking up that
separate topic.

When entering an unfamiliar area of code, build a higher-level map
first — relevant modules and callers in the project's glossary
vocabulary — before drilling into a specific function. Deep
inspection follows the map, not the other way around.

Before wide-ranging changes, before editing a file you have not fully
inspected, and when investigating or auditing, read the file in full —
for a very large file, the full relevant module or section, not the
scattered snippets that hide callers, guard clauses, and existing
helpers. This is per file you are about to touch, on demand — not an
up-front sweep of the repo, and not a license to read a million-token
file end to end.

---
slug: portable-capability-bases
noticed: 2026-09-20
where: project-templates/bases/legacy-boot/template.json
---

**Gap:** the initial wholesale reference to the `~/agents` global boot needs
an expert-reviewed, portable decomposition. `bases/legacy-boot/boot.md`
preserves that starting point; App canvas now uses a first authored split into
capability bases instead. The linked legacy boot pulls in personal/harness context,
research, runs, agentctl, and routed documents that an ordinary app project
does not contain. Materializing that file alone would create broken guidance.
The manifests remain draft, requiring explicit authoring opt-in for creation.

**Noticed while:** establishing this program at the user's explicit request.
The first split now stands up an application; that execution evidence alone
does not establish the quality of its instruction selection.

**Fix sketch:** reorganize the relevant boot and instruction inventory by
capability base, and tighten it through expert editing and, where informative,
bounded experiments. The goal is instructions an app-building agent and a
human can understand, with retained practices justified by useful behavior.
Copying everything into a new folder, shortening only the root file, or
retaining routes to absent material does not close the gap.

The target organization follows [PROGRAM.md](../PROGRAM.md) and
[FORMAT.md](../FORMAT.md):

- Keep reserved `base` genuinely universal. Share engineering and testing
  independently of TypeScript, web UI, canvas, or a server. A project can
  inherit their union, including shared ancestors, without repeated guidance.
- Scope language and activity instructions at their actual trigger. A
  polyglot vendored inventory is acceptable; mandatory reading of irrelevant
  C++, research, or host-operation policy is not.
- Preserve the useful software-engineering, testing, UI, run/build/deploy,
  and documentation practices in project-appropriate form. Ordinary app
  process ownership and verification still matter even though the author's
  tracked-run machinery is excluded.
- Omit the full global boot, personal host settings, harness setup,
  research packets, agentctl, and unrelated infrastructure from the default
  app payload. Exact reusable documents may remain symlinks in this source
  repository; instantiation copies their bytes and includes their relevant
  reference closure.
- Prefer identical destination paths with identical content across bases.
  Root `AGENTS.md` concatenates distinct fragments in resolved order after
  whole-fragment content-hash deduplication. Do not solve duplication by
  giving the same concept several path names.
- Ship an instruction to maintain documentation as behavior changes,
  including revising the README lede when needed. The preparation turn
  customizes the project instructions and that lede from the entered intent,
  verifies run/test/build, and leaves application implementation for later.
- Provide portable instructions and mechanical content for the optional
  server so a later request follows the same standards without fetching this
  authoring checkout. Deployment must name project-configured destinations,
  never inherit the author's personal publishing target or credentials.

**Closure evidence:** inspect the composed root and every routed file for the
App canvas and at least one different capability combination. Check triggers,
link closure, relevance, contradictions, and the total triggered reading
burden, not just root length. Trace preparation, a UI change, an ordinary
non-UI change, a failing test, an evolved README description, and adding a
server. Run the real starter's build/test/run and supported add-on path from a
materialized project with the source repository unavailable.

An expert editing pass must identify its retained/removed guidance and inspect
the output as a fresh project reader. Where experimentation is warranted,
compare representative matched tasks using the broad seed and edited bases;
record task completion, regressions, unnecessary reads/actions, and cost.
Treat trace simulation as predicted behavior and experiments as measured
evidence; neither shorter text nor passing composition tests establishes
better agent outcomes. A reasoned expert pass can justify the first version;
do not require an elaborate benchmark merely to begin using it.

Close this gap only when the first ready template's instruction closure is
portable and reviewed, and its relevant paths have real execution evidence.
Keep it open, with a precise remainder, for a partial split. The YA UI and
instantiation feature are separately pending in the
[approved delivery sequence](../README.md#approved-delivery-sequence).

## Current progress

2026-09-20 — Contributing-model: 6-Astra. Universal, software-engineering,
testing, TypeScript, web-UI, canvas, and optional-server bases are populated.
The active template excludes the legacy boot and has local instruction routes.
Its deterministic setup, static build, browser drawing/typing checks, and
server activation/API checks have run successfully. The first editorial pass
retained scoped code-quality, verification, documentation, and deployment
guidance while removing personal host policy and research/agentctl machinery.

Remaining: a systematic expert review of the complete composed instruction
set against its source guidance, a different capability combination, and the
scenario/reading-cost assessment above. No comparative agent experiment has
been run. Keep manifests draft until that review supports promotion; runtime
tests and a smaller root alone do not close this instruction-quality gap.

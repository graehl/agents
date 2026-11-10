---
slug: agentctl-stop-rebuild-review-advisories
noticed: 2026-11-10
where: agentctl `stop`, `Builds.start`, `Freshness.inputs`
---

**Gap:** advisories the 2026-11-10 strict review left open on commit
`aee1b905`:

`aee1b905` has no retained test for the scope-moved `agentctl stop` or the
requested-rebuild failure memory; `Builds.start(recipe, source, fresh)`
takes the recipe twice; `Freshness.inputs` re-splits a string that was a
list one line earlier; and the root case of
`test_remembered_process_that_may_not_be_signalled_is_dropped` returns as a
pass instead of a skip. The review's probes for these are under
`harsh-review/`, range prefix `50a69f1ad81d..a8164da8541d`.

**Noticed while:** reviewing the rebuilt `scripts/not-ai-lint`, same range.
**Fix sketch:** add the two retained tests, pass the recipe once, keep the
inputs as a list, and make the root case skip.

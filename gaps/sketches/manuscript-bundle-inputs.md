---
slug: manuscript-bundle-inputs
noticed: 2026-09-24
where: scripts/claim-refs pack/paths
---

**Outcome:** `claim-refs pack`/`paths` can optionally carry more than run
records: the cited artifacts themselves and the declared input files of the
gathered runs. Some material must never leave the checkout this way — for
example license-restricted corpora or model weights — so publication is
refused for anything on an explicit ban list, even when a claim cites it.

**Approach:**
- An opt-in flag (e.g. `--with-artifacts`, `--with-inputs`) adds cited files
  and `params.inputs.<KEY>.path` files, with size reporting and a size cap.
- A project-owned ban list (path globs plus a reason, e.g. license) is checked
  for every candidate file. A banned file is reported with its reason and
  excluded; a bundle intended for publication fails rather than silently
  shrinking.
- `paths` gains the same selection so `git add` of a publishable subset
  honors the bans.

**Open decisions:** where the ban list lives (project root vs program scope),
whether bans also apply to run records that merely name a banned input path,
and whether inputs outside the project root are ever eligible.

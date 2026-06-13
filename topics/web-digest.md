# Web digest

> The claude.ai web-context artifacts: a committed, hand-distilled
> preferences paste (`digest/paste-into-claude.ai-preferences.md`) for
> the account-wide preferences field, plus an optional local,
> gitignored single-file concatenation (`digest/claude-web.md`) of the
> repo's instruction/policy corpus, scoped by
> `scripts/web-digest.manifest` and built on demand by
> `scripts/web-digest` for ad-hoc manual upload.

Topic: `web-digest`

## Purpose and audience split

Web/assistant conversations (claude.ai default chat, in a Project) are
the non-coding surface: discussing instruction design, policy, and the
repo's ideas. Coding always happens in a local harness (Claude Code or
similar) that reads the repo directly, so these artifacts serve only
the web surface and nothing in a coding session should depend on them.

The primary artifact is the preferences extract (below) — the
behavioral rules that ride every web conversation. The digest file is
secondary and optional: when a claude.ai Project should see the whole
corpus, the simpler route is adding the repo as a GitHub source
directly; the local digest build exists for the ad-hoc case (a single
file to drop into one conversation, with riders pre-excluded).

## Scope contract

- The manifest's globs match against `git ls-files`, so only tracked
  files can be included — gitignored private state (`AGENTS.local.md`,
  `tasks/`, `user/`) is excluded by construction, not by listing.
- `.evidence.md` and `.bearings.md` riders are excluded: rationale
  ledgers and live orientation state are noise for a web conversation.
- The generator is deterministic concatenation — no LLM step — so the
  digest is reproducible from the manifest plus the tree, and runnable
  without any agent.

## Refresh loop

The digest is a local, gitignored build artifact — never committed
(2026-06-13 reversal; see Design decisions). Refresh is simply: run
`scripts/web-digest`, then upload `digest/claude-web.md` wherever it is
wanted. The provenance header (date, source commit, word count) is the
freshness signal for any copy that was uploaded earlier.

The preferences extract refreshes by hand-redistillation when its
sources move (the script warns); landing that change is an ordinary
commit, and the user re-pastes into claude.ai settings.

## Preferences extract and authority tiers

claude.ai weighs content by channel: fetched web pages are untrusted
data (instructions in them are ignored by design), project knowledge
is user-provided reference, and the instructions fields — a Project's
custom instructions, or the account-wide preferences — are the
full-authority, always-loaded channel. The digest lives in the
knowledge tier, which is right for a discussable corpus but wrong for
behavioral rules: knowledge is retrieved on demand, so directives
there may simply not be in context.

`digest/paste-into-claude.ai-preferences.md` is therefore a pasteable,
self-contained distillation of the interaction rules for the
account-wide preferences field — no repo/GitHub/digest pointers, by
the user's choice, so it carries identically in any conversation. The
file is the verbatim paste payload: bullets only, no title, framing,
or maintenance notes, so select-all → paste is the whole operation.
It is hand-maintained (distilled from `AGENTS.md` § Interaction style
and `AGENTS.user.md` § Disposition / Writing and summary style), not
script-generated: distillation is a judgment step, unlike the
digest's concatenation. `scripts/web-digest` warns when those sources
have commits newer than the extract's.

## Design decisions

- **Local digest file, not committed** (2026-06-13, reversing the
  original committed-file design): the committed copy was generated
  churn with no real margin over claude.ai's direct GitHub-source
  ingestion — a Project that wants the repo adds the repo. The script
  and manifest stay for the ad-hoc single-file build (provenance
  header, rider exclusion); the output is gitignored.
- **Script for the digest, skill for the extract** (vs. one mechanism
  for both): concatenation is deterministic and runs without an agent;
  the preferences extract is a judgment distillation, so its refresh
  belongs to `skills/web-digest/SKILL.md`, which wraps the whole loop
  (run script, re-distill when stale, commit, name the manual
  claude.ai steps); accepts that a full refresh needs an agent.

## Sketches

**Sideband transcription of user-specific content.** Some
user-specific material (gitignored `user/`, `AGENTS.local.md`, or other
private state) might someday be worth delivering to the web Project
through a side channel — manual upload, not the GitHub route, so it
never transits the public repo. Not important at the moment; noted so
the eventual want has a home. If it materializes, keep it a separate
artifact from `digest/claude-web.md` so the public/private boundary
stays the tracked-files boundary.

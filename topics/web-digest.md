# Web digest

> A committed single-file concatenation (`digest/claude-web.md`) of this
> repo's instruction/policy corpus, scoped by `scripts/web-digest.manifest`
> and rebuilt by `scripts/web-digest`, synced into claude.ai project
> knowledge so web/assistant (non-coding) conversations can see the repo;
> refresh is a manual run → commit → push → re-sync step.

Topic: `web-digest`

## Purpose and audience split

Web/assistant conversations (claude.ai default chat, in a Project) are
the non-coding surface: discussing instruction design, policy, and the
repo's ideas. Coding always happens in a local harness (Claude Code or
similar) that reads the repo directly, so the digest serves only the
web surface and nothing in a coding session should depend on it.

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

Manual and periodic by intent (no always-on GitHub reading):

1. `scripts/web-digest`
2. commit `digest/claude-web.md` (subject-only is fine)
3. push
4. re-sync the GitHub source in the claude.ai Project

The digest's provenance header (date, source commit, word count) is the
freshness signal; the claude.ai Project instructions should point
conversations at it so a stale copy is self-announcing.

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

- **Committed digest file** (vs. selecting the real files directly in
  claude.ai's GitHub source): prioritizes versioned, diffable scope and
  the ability to preprocess (provenance header, rider exclusion);
  accepts generated-file churn in the repo.
- **Script for the digest, skill for the extract** (vs. one mechanism
  for both): concatenation is deterministic and runs without an agent;
  the preferences extract is a judgment distillation, so its refresh
  belongs to `skills/web-digest/SKILL.md`, which wraps the whole loop
  (run script, re-distill when stale, commit, push, name the manual
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

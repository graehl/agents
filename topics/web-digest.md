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

## Design decisions

- **Committed digest file** (vs. selecting the real files directly in
  claude.ai's GitHub source): prioritizes versioned, diffable scope and
  the ability to preprocess (provenance header, rider exclusion);
  accepts generated-file churn in the repo.
- **Script, not skill** (vs. a `/web-digest` skill): deterministic
  concatenation needs no judgment, and a plain script runs without an
  agent; accepts revisiting if the step ever grows a distillation pass.

## Sketches

**Sideband transcription of user-specific content.** Some
user-specific material (gitignored `user/`, `AGENTS.local.md`, or other
private state) might someday be worth delivering to the web Project
through a side channel — manual upload, not the GitHub route, so it
never transits the public repo. Not important at the moment; noted so
the eventual want has a home. If it materializes, keep it a separate
artifact from `digest/claude-web.md` so the public/private boundary
stays the tracked-files boundary.

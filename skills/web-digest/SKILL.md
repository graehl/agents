---
name: web-digest
description: Refresh the claude.ai web context — rebuild the local, gitignored digest/claude-web.md via scripts/web-digest and, when its sources have moved, re-distill the committed pasteable preferences extract. Use when the user invokes /web-digest or asks to refresh the web digest, the claude.ai project knowledge, or the preferences paste.
---

# Web digest refresh

Contract: `topics/web-digest.md`. Two artifacts with different update
mechanics: `digest/claude-web.md` is deterministic concatenation (the
script's job, never hand-edited, gitignored — never committed), and
`digest/paste-into-claude.ai-preferences.md` is a judgment distillation
(this skill's job, never script-generated, committed).

## Workflow

1. **Rebuild the local digest.** Run `scripts/web-digest`. It rebuilds
   `digest/claude-web.md` (a local upload artifact, not for commit) and
   warns on stderr when `AGENTS.md`/`AGENTS.user.md` have commits newer
   than the extract's.

2. **Re-distill the extract when stale.** On that warning, or when the
   user asks: re-read `AGENTS.md` § Interaction style and
   `AGENTS.user.md` § Disposition and § Writing and summary style, then
   update the bulleted block in `digest/paste-into-claude.ai-preferences.md` to
   match current policy. Preserve its contract:
   - verbatim paste payload — bullets only, no title, framing, or
     maintenance notes; select-all → paste is the whole operation;
   - self-contained — no repo, GitHub, or digest pointers;
   - preferences-field sized — roughly the current length, a handful of
     bullets, not a corpus mirror;
   - web-conversation wording — drop anything that only makes sense in
     a coding harness (commits, worktrees, tool mechanics).
   Show the user the extract's diff; the paste into claude.ai is theirs
   to redo, so the diff is what tells them whether re-pasting is worth
   it.

3. **Commit only the extract.** The digest is gitignored and never
   committed. An extract change gets a short narrative body with a
   `Topic: web-digest` trailer. Push per the big-effect gate.

4. **Remind the manual claude.ai steps.** If the extract changed, the
   user re-pastes it into the account preferences field. If the user
   wants the corpus on the web surface: add the repo as a GitHub source
   in a Project, or upload the freshly built digest to a single
   conversation.

## Anti-patterns

- Hand-editing `digest/claude-web.md` (regenerate instead) or
  script-generating the preferences extract (distill instead).
- Committing `digest/claude-web.md` — it is gitignored generated
  output; a Project that wants the repo adds the repo directly.
- Growing the extract toward completeness — the repo (or a digest
  build) is the corpus; the extract is only the rules that must ride
  the always-loaded instruction channel.
- Adding "see the repo" pointers to the extract; it is deliberately
  portable to conversations with no repo access.

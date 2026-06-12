---
name: web-digest
description: Refresh the claude.ai web context — regenerate digest/claude-web.md via scripts/web-digest and, when its sources have moved, re-distill the pasteable preferences extract. Use when the user invokes /web-digest or asks to refresh the web digest, the claude.ai project knowledge, or the preferences paste.
---

# Web digest refresh

Contract: `topics/web-digest.md`. Two artifacts with different update
mechanics: `digest/claude-web.md` is deterministic concatenation (the
script's job, never hand-edited), and `digest/claude-web-preferences.md`
is a judgment distillation (this skill's job, never script-generated).

## Workflow

1. **Regenerate the digest.** Run `scripts/web-digest`. It rebuilds
   `digest/claude-web.md` and warns on stderr when
   `AGENTS.md`/`AGENTS.user.md` have commits newer than the extract's.

2. **Re-distill the extract when stale.** On that warning, or when the
   user asks: re-read `AGENTS.md` § Interaction style and
   `AGENTS.user.md` § Disposition and § Writing and summary style, then
   update the bulleted block in `digest/claude-web-preferences.md` to
   match current policy. Preserve its contract:
   - self-contained — no repo, GitHub, or digest pointers;
   - preferences-field sized — roughly the current length, a handful of
     bullets, not a corpus mirror;
   - web-conversation wording — drop anything that only makes sense in
     a coding harness (commits, worktrees, tool mechanics).
   Show the user the extract's diff; the paste into claude.ai is theirs
   to redo, so the diff is what tells them whether re-pasting is worth
   it.

3. **Commit and push.** Digest-only churn gets a subject-only commit;
   an extract change gets a short narrative body with a
   `Topic: web-digest` trailer. Push per the big-effect gate.

4. **Remind the manual claude.ai steps.** Re-sync the Project's GitHub
   source; if the extract changed, re-paste it into the account
   preferences field.

## Anti-patterns

- Hand-editing `digest/claude-web.md` (regenerate instead) or
  script-generating the preferences extract (distill instead).
- Growing the extract toward completeness — the digest is the corpus;
  the extract is only the rules that must ride the always-loaded
  instruction channel.
- Adding "see the repo" pointers to the extract; it is deliberately
  portable to conversations with no repo access.

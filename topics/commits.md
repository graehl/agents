# Commit and amend mechanics

> The repo's narrative-synthesis commit-message format and the
> amend procedure that fires when the user corrects a commit
> already authored.

Topic: `commits`

The umbrella rules — subject ≤65 chars, manual 71-col body wrap,
narrative synthesis, topic trailers — live in `AGENTS.md §
Commits`. This doc carries the procedure that fires on a specific
action: amending.

## Amends

For ALL amends of ALL commits:

- Leave the subject unchanged.
- Capture the full existing message first (`git log -1
  --format=%B` to a file), then edit it. Never retype the message
  from a `git show`/`git log` terminal preview — those truncate
  (~2KB), and hand-reconstruction silently drops the tail: later
  body sections, `Topic:` trailers, `INCREMENT_PATCH_VERSION`, and
  the Gerrit `Change-Id`. A dropped `Change-Id` forks a new review
  off the existing change. If a prior amend already truncated it,
  recover the full text from the pre-amend commit via reflog.
- Write the message as an additive or corrected update; do not
  erase prior content except to fix what is now incorrect.
- "Additive" governs substantive intent+result, not process.
  Across a series of amends the message must still collapse to one
  synthesis of purpose and outcome — it is not an append-only log.
  Do not accumulate "Amend delta:" / "follow-up amend:" journal
  entries; when the message has drifted into such a log, prune it
  back to purpose+result (the diff, not the message, records how
  you got there). Added-then-reverted churn nets out and is
  dropped, not narrated.
- Describe only what changed relative to `HEAD~1`, not changes
  from the previous patchset. Forbidden: "preserved Z" when Z was
  already described; "moved X to Y.hpp" when X is created in this
  commit.
- An amended message must meet non-trivial standards if the
  original commit was non-trivial.
- Show the edited message as a diff, and confirm no prior content
  was dropped or replaced except as a deliberate correction or
  journal-pruning.

When the user corrects a commit not yet pushed to the upstream
default branch, amend it (`--amend --no-edit` for trivial fixups)
rather than adding a noisy second correction commit. When a commit
already pushed to the user's personal GitHub is found wrong within
days and has no downstream forks/consumers, prefer amend +
force-push over accumulating fix history — but not once it has
been submitted as a PR elsewhere; then repair forward.

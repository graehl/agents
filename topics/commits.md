# Commit and amend mechanics

> The repo's narrative-synthesis commit-message format and the
> amend procedure that fires when the user corrects a commit
> already authored.

Topic: `commits`

`AGENTS.md` carries the compact first-load rules: subject ≤65 chars,
manual 71-col body wrap, narrative synthesis, and topic trailers. This
doc carries the full standard and the procedure that fires on specific
actions such as amending.

Read this doc before writing a non-trivial commit message, amending,
deciding correction commit vs. amend, or relying on topic-trailer,
Gerrit, coverage-gap, or message-preservation mechanics.

## Commit messages

Trivial commits get a short, possibly subject-only message.

Non-trivial messages are a narrative synthesis of motivation and
decision => change:

- Exclude credentials/secrets from contents and message.
- Include the main user decision points from the session.
- Exclude unrelated side discussions, but include approaches ruled out for
  non-obvious reasons.
- Flag known uncovered areas or risks. Default presumption: work
  is at least manually smoke-tested; automated coverage is evident
  from the diff. Do not enumerate which tests were run or passed —
  that is busywork; the diff and CI carry it.
- Use a `Known coverage gaps:` labeled section near the end of
  the body (before trailers) when there are gaps worth flagging.
  Prose or short bulleted list, whichever fits. Be specific about
  the structural gap; omit the section entirely when empty.
- Broadly describe every non-trivial change — especially >3-line creations
  and significant-effect edits. Trivial changes (whitespace, comments,
  file-local renames) need no mention.

The message has two usually-aligned purposes: orienting a reviewer now, and
letting a later reader (`git blame`, a `bisect` bug-hunt) validate a diff
hunk against the stated intent and result. Both are served by describing
purpose and outcome — enough that an agent told to achieve this message would
produce a similar diff, and that every group of files in the diff is
explained by something in the text. Neither is served by a journal of how the
change was reached: omit iteration narrative, superseded approaches that left
no trace in the tree, and added-then-reverted churn.

Consider splitting unrelated changes into independent commits (e.g.
implementation vs. research finding). When a directive grants
open-ended commit latitude — "make as many commits as you want",
"commit at your own pace", "split however you like" — read it as a
preference for thematically-unrelated large items landing in separate
commits, not licence to batch them together for convenience. Closely
related changes still belong in one commit; the split is by theme, not
by count.

## Topic trailers

A commit in a related series gets one or more `Topic: <string>` trailers.
The string is the basename of the relevant `topics/<topic>.md` (`ls
topics/*.md` for the namespace); all commits in a series copy it verbatim
so `git log --grep` finds the chain. Use multiple `Topic:` lines for a
commit spanning topics. The trailer marks thread membership, not merely
that the diff touched a `topics/` file: a standalone commit with no task
spec and no expected follow-up gets no trailer even if it edits a topic
doc, while the commit that starts a thread gets one as #1.

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

## Amending in a shared worktree

Check for active peers first (`find .agentctl/active -maxdepth 1
-type f -mmin -70`; entries not starting with `DONE`). With any
active peer, do not amend or rebase — a history rewrite races their
in-flight commits and unstaged edits, and the urge to "line it up
against the right commit" is what leads to a worktree-destroying
`git reset --hard`. Make a follow-up commit instead, or do history
surgery in a separate worktree.

With no active peer you may amend: take the project's commit lock
if one exists or is required, then verify `HEAD` is the commit you
intend and is your own current-session work — at least subject,
files changed, and authorship/session context. If another session
has committed on top, stop and report the mismatch rather than
amend. Recovery from a bad amend follows the shared-workdir discard
ban (`AGENTS.md § Shared-workdir discard ban`): never `git reset
--hard` in a dirty shared worktree; revert with a new commit or
move your work to a separate worktree.

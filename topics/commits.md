# Commit and amend mechanics

> The repo's narrative-synthesis commit-message format and the
> amend procedure that fires when the user corrects a commit
> already authored.

Topic: `commits`

`AGENTS.global.md` carries the compact first-load rules: subject ≤65 chars,
manual 71-col body wrap, narrative synthesis, and topic trailers. This
doc carries the full standard and the procedure that fires on specific
actions such as amending.

Read this doc before writing a non-trivial commit message, amending,
splitting or otherwise rewriting history, deciding correction commit
vs. amend, or relying on topic-trailer, Gerrit, coverage-gap, or
message-preservation mechanics.

## Commit messages

Trivial commits get a short message — possibly subject-only, plus the
`Contributing-model:` trailer. A small, simple change may name each edit when
that remains the shortest clear account.

### Message construction

Before an agent-authored non-trivial commit, construct and lint the complete
message before Git records it. For plain prose, use the repository helpers so
body paragraphs are wrapped and the final bytes are checked:

```bash
git commit -F <(commit-msg-fmt -m "Subject" -m '' \
  -m "Body paragraph." -m '' \
  -m "Contributing-model: <short-name>" | commit-msg-lint)
```

For bullets, tables, code, or other preformatted bodies, author a draft file,
run `commit-msg-lint < COMMIT_MESSAGE.txt`, then commit with
`git commit -F COMMIT_MESSAGE.txt` only after the lint succeeds. Never encode
paragraph breaks as literal `\n` inside one `-m` argument or pass a non-trivial
body directly through unformatted `git commit -m`; both paths bypass the
formatting contract. Inspect the recorded message after commit when Git or a
hook could have changed it.

A non-trivial message is first a reviewer on-ramp and later a historical
statement of intent. Write for a fresh human reviewer who is about to inspect
the diff and has none of the implementation conversation in mind. Lead with
motivation and decision => outcome; supply enough basic context and terminology
that the review can start without reconstructing the session.

When one commit lands only part of the current user-requested goal, open its
body after any `Onboarding:` line with this ordered structure:

```text
Series goal: <current user-requested goal>
This commit: <portion landed by this diff>
Remaining after this commit: <substantive remainder>
```

Each label begins a line; blank lines between them are optional, and wrapped
continuation lines need no repeated label. The series goal is the active request
scope, not every ambition in a broader topic or project roadmap. Cite a
committed topic, gap, plan, or similar governing artifact when it accurately
defines that scope; otherwise summarize the active task in place rather than
linking private state. Do not derive promised follow-up from dormant or
candidate material.

`Remaining after this commit:` records the historical state immediately after
that commit, so it remains true when later commits finish the work. The format
fires only for a substantive nonempty remainder. When the commit lands the
whole goal, use the ordinary narrative format: omit all three labels rather
than emitting an empty remainder or `None` for symmetry.

The narrative synthesis:

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
- Account for every non-trivial file group at the design and outcome level —
  especially significant-effect edits and creations — without inventorying
  each action. Trivial changes (whitespace, comments, file-local renames) need
  no mention.

The message has two usually-aligned purposes: orienting a reviewer now, and
letting a later reader (`git blame`, a `bisect` bug-hunt) validate a diff
hunk against the stated intent and result. Both are served by describing
purpose and outcome — enough that an agent told to achieve this message would
produce a similar diff, and that every group of files in the diff is
explained by something in the text. Neither is served by a journal of how the
change was reached: omit iteration narrative, superseded approaches that left
no trace in the tree, and added-then-reverted churn.

Before the first review, make a dedicated revision pass toward one printed
page or less. This is a compression target, not a hard quota: preserve a
load-bearing decision or risk when it needs more room, while larger changes
receive less per-edit narration than trivial ones. In particular, prune
chronological "did X, did Y" lists to why, the resulting design, and the
shortest summary of what changed.

Action-by-action detail belongs in an implementation journal when it has
lasting reviewer or maintainer value. Such material starts privately under
`tasks/journals/`; condense and redact a journal selected for publication into
`topics/journals/<task-or-topic>.md` (or the plan's adjacent `journals/`
directory) under `AGENTS.global.md` § Delegation. Drop it when it has no durable
value. Do not use `changelog/` for this default: changelogs communicate
release-facing change history, while an implementation journal preserves
selected reasoning and mechanics behind one body of work.

When a change is largely governed by a committed topic doc, put a short
onboarding line immediately after the subject, before the explanatory body:

```text
Onboarding: topics/commits.md
```

Use the actual project-relative canonical-doc path, including a scoped path
such as `research/pii/topics/redaction.md`; unlike the `Topic:` shorthand,
`Onboarding:` never elides `topics/`. Use the plain path, not a markdown link —
git log, GitHub, and Gerrit render commit messages as raw text, so a markdown
link just doubles the path. This deliberately overlaps with `Topic:` trailers
without replacing them. The early line is for a human reader scanning the
front of the message; the trailer is for series membership and search. If the
commit wants more background that will remain useful after review, expand the
topic doc and let the commit message point at it instead of duplicating the
lasting context in the body. The named topic is read before the diff by the
same fresh human reviewer. It must explain its context, basic terms, and
governing decisions without relying on session memory or prior immersion in
the changes; a topic that becomes legible only after reading the implementation
is not an onboarding document.

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
The string is the glossary-scoped topic name. A project-root topic keeps the
basename (`topics/redaction.md` -> `redaction`). A scoped topic prefixes the
basename with the owning glossary's project-relative directory and omits the
mechanical `topics/` segment (`research/pii/topics/redaction.md` ->
`research/pii/redaction`). The root `docs/topics/` alternate remains the root
namespace and therefore also uses the basename. Basenames need not be unique
across scopes.

An arbitrary canonical doc linked from a glossary is still topic-like. When it
deliberately governs a commit series, use the same owner-scope prefix with a
stable glossary term in the basename position; its filesystem location does
not invent a second topic name. Existing series copy their chosen string
verbatim, and historical root names are not migrated, so `git log --grep`
continues to find the chain. Use multiple `Topic:` lines for a commit spanning
topics. The trailer marks thread membership, not merely that the diff touched
a topic doc: a standalone commit with no task spec and no expected follow-up
gets no trailer even if it edits one, while the commit that starts a thread
gets one as #1.

## Contributing-model trailer

Every commit an agent authors names the model(s) that did the work
in `Contributing-model:` trailers — deliberate provenance the user
wants for fair attribution of effort across models and sessions.

Value grammar: an intentional abbreviation of the model name —
`claude-fable-5` → `Fable`, `claude-opus-5` → `Opus 5`,
`gpt-5.6-sol` → `5.6-Sol`. Vendor or harness names (`Pi`,
`Copilot`) are not welcome, nor an email or link. Models misreport
their own names, so recover the id the way the harness supplement
specifies (transcript grep), not from self-knowledge.

One trailer per contributing model, unique: when amending or
extending a commit another model authored, keep its trailer and add
your own; never duplicate a name or fold two models into one line.
The key deliberately collides with no common trailer
(`Signed-off-by`, `Co-authored-by`, `Reviewed-by`, …) so tooling and
the attribution scan never conflate them.

Interplay with `[no-attrib]`: the ban and strip flow target
harness-injected attribution — `Co-Authored-By` trailers,
generated-with banners, vendor emails, robot emoji. The
`Contributing-model:` trailer is the sanctioned exception: neither
the scan patterns nor `scripts/pre-push-no-attrib` match it, and it
is never stripped. Conversely it must never grow toward the banned
forms — no email, no link, no banner sentence — which would both
break the short-name requirement and trip the scan.

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

That force-push — and any other — uses `git push --force-with-lease
--force-if-includes` (`AGENTS.global.md § Big-effect command gate`), never
bare `--force`. Bare `--force-with-lease` leases against your local
remote-tracking ref, so a background `git fetch` can refresh that ref
and let the push clobber after all; `--force-if-includes` (git ≥2.30)
closes that gap by also requiring your local history to include the
remote tip. For a rewrite computed against a specific base, pin the
expectation explicitly with `--force-with-lease=<ref>:<expected-sha>`
captured before the rewrite, rather than relying on the implicit lease.

## History rewrites in a shared worktree

This covers every rewrite of existing history — amend, rebase, and
any backward `git reset` (soft/mixed included) that rewinds the
branch to split, squash, or reorder commits. A reset-recommit split
is an amend in everything but name; it gets no separate latitude.

Check for active peers first (`find .agentctl/active -maxdepth 1
-type f -mmin -70`; entries not starting with `DONE`). With any
active peer, no history rewrite at all. The scope is peer presence,
not `HEAD` ownership: a peer may commit at any moment, so verifying
"my commit is at `HEAD`" immediately before the rewind still leaves
the race open — the reset point can end up below a freshly landed
commit you don't own, silently orphaning it or absorbing its changes
into your recommit. No acquirable token changes this: the advisory
rewrite lock below never substitutes for peer absence.
Beyond the race, a history rewrite disrupts peers' in-flight commits
and unstaged edits, and the urge to "line it up against the right
commit" is what leads to a worktree-destroying `git reset --hard`.
Make a follow-up commit instead, do history surgery in a separate
worktree, or wait out the peers with `agentctl alone` — which is not
a lock but a blocking wait for the no-peer state below.

With no active peer you may rewrite. A multi-command chain (rebase,
split, series of amends, attribution strip) holds the advisory
rewrite lock for its whole duration: `agentctl alone <id> -b
"REWRITE: <what>"`, cleared by rewriting your banner when the chain
ends (`AGENTS.global.md § Amends`). The `REWRITE` entry warns sessions
arriving mid-chain, which defer commits while it is fresh; it stays
advisory and never substitutes for the peer check. Then verify
`HEAD` is the commit you intend and is your own current-session
work — at least subject, files changed, and authorship/session
context. Splitting your own
tip commit with `git reset` + recommits is then as free as amending.
If another session has committed on top, stop and report the
mismatch rather than rewrite below it. Recovery from a bad amend follows the shared-workdir discard
ban (`AGENTS.global.md § Shared-workdir discard ban`): never `git reset
--hard` in a dirty shared worktree; revert with a new commit or
move your work to a separate worktree.

## Attribution strip by SHA

When the `[no-attrib]` scan (`AGENTS.global.md § Big-effect command gate`)
flags commits, strip by the exact SHAs the scan's `%H` column names —
never a pattern sweep over every message in the range, which edits
messages nobody flagged. A marked tip alone is a plain message-only
amend. Anything deeper takes one filter pass over the range,
SHA-conditioned so only flagged messages are touched — one pass even
for several scrub points, since each pass rewrites all descendant
hashes:

```bash
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f \
  --msg-filter 'case "$GIT_COMMIT" in
      <sha1>|<sha2>)
        sed "/^co-authored-by:[[:space:]]*/Id" | git stripspace ;;
      *) cat ;;
    esac' -- <oldest-sha>^..HEAD
```

Adapt the `sed` to the marker being removed (banner lines likewise);
a sequence of single-SHA passes in one script also works, at the
cost of rewriting descendants once per pass. Unflagged messages pass
through byte-identical.

Verify before deleting the `refs/original/` backup, in one command:
the new tip's tree is identical to the pre-rewrite tip's (message-only
rewrite), no remote-shared history moved (every remote ref that was
an ancestor of the old tip still is one), and the scan comes back
clean:

```bash
old=$(git rev-parse refs/original/refs/heads/<branch>) &&
{ git diff --quiet "$old" HEAD &&
  for r in $(git for-each-ref --format='%(refname)' refs/remotes); do
    ! git merge-base --is-ancestor "$r" "$old" ||
      git merge-base --is-ancestor "$r" HEAD || exit 1
  done &&
  ! git log --format=%B "$old"..HEAD | rg -iq \
    'co-authored-by|generated with|noreply@|🤖'
} && echo STRIP-OK ||
  echo "STRIP-VERIFY FAILED: pre-rewrite HEAD was $old"
```

(The scan line passes only when no marker remains; prose mentions
found earlier still need the same one-time inspection.) Only on
`STRIP-OK` delete the backup ref. On failure, notify with that
message — it names the pre-rewrite HEAD so recovery is a one-liner —
and stop; no auto-repair, no backup deletion. The whole flow runs
under the advisory rewrite lock (`AGENTS.global.md § Amends`).

# REVIEWS

Project-activated policy for tracking the code reviews a checkout has pushed
(Gerrit changes, GitHub pull requests) and what each is waiting on. It applies
only in a project whose instructions name it. Read it at these boundaries:
after pushing or updating a review, when asked what a review or the project's
reviews are waiting on, when catching up on review activity (comments, CI,
votes, merge state), and before answering anything about a review's current
state.

`reviews/` answers "what did we send, and what is it waiting on" — a
question neither a local branch nor a handoff answers: a branch can sit on
a superseded revision, and a handoff is organized by work, not by review.

## Activation

A project turns this on by naming `~/agents/REVIEWS.md` in its `AGENTS.md` or
`AGENTS.local.md` and creating `reviews/config.toml` with one `[backend]`
table and an optional `[ticket]` table. Gerrit:

```toml
[backend]
kind = "gerrit"
host = "gerrit.example.com"  # ssh host
port = 29418
project = "xmt"              # omit to search every project
default_branch = "master"
ci_bots = ["jenkins"]        # accounts whose messages and votes are CI, not human

[ticket]
pattern = "AIP-\\d+"
url = "https://jira.example.com/browse/{ticket}"
```

GitHub:

```toml
[backend]
kind = "github"
repo = "owner/name"
default_branch = "main"
```

`reviews/` is private by default, like handoffs: add `/reviews/` to
`.git/info/exclude` in the operation that creates the directory. A project
that tracks it instead says so in its instructions. Nothing is imported
retroactively; a change gets a file when it is next pushed or touched.

## Vocabulary

- **change** — one unit of work under review across every target branch: a
  Gerrit Change-Id, which Gerrit shares across branches, or the set of pull
  requests carrying the same work to different branches.
- **review** — one backend review of a change against one target branch: a
  Gerrit review number, or a PR number. Its votes, CI, and revision history
  are independent of its siblings'.
- **revision** — a Gerrit patchset or a PR head commit.
- **CI verdict** — the bot's standing vote or check result on the current
  revision. **human votes** — reviewer approvals on the current revision.
- **submittable** — the backend's own merge readiness (Gerrit submit records,
  GitHub merge state); distinct from a local merge-conflict check.
- **event** — a timestamped thing that happened on a review: a revision
  uploaded, a message, an inline comment, a vote, a CI result.

## One file per change

Path: `reviews/<TICKET>-<slug>-<key>.md`. The ticket comes first when the
change has one, so a ticket's changes sort together; the slug keeps the
directory readable without opening files; the key makes the file findable
from the backend id: the first nine characters of a Gerrit Change-Id
(`Ib0680a1f`), or `pr<N>` (`pr12`, `pr12-15` for a backport pair).

```
reviews/AIP-2705-spaces-inside-family-Ib0680a1f.md   # master + xmt-19.0, one Change-Id
reviews/AIP-2743-qe-threshold-docs-I5add10dae.md
reviews/publish-binary-retrigger-pr41.md             # no ticket: segment omitted
```

The header is the machine-read contract; everything after it is free-form:

```markdown
# <subject>

Change: gerrit Ib0680a1f8885acd81c391a655ff5888f5dccc776
Ticket: AIP-2705 <https://jira.example.com/browse/AIP-2705>
Seen: 2026-09-15T18:28:29Z

<!-- state: written by `reviews sync` <ts>; observation, not authority -->
| review | branch | status | revision | CI | human | submittable |
...
<!-- /state -->
```

- `Change: <backend> <id...>` names the change: one Change-Id for Gerrit, or
  every PR (`owner/repo#N`, several when the work went to several branches).
- `Seen:` is the watermark: backend activity timestamped after it has not
  been evaluated by us. Advance it only after incorporating what it covers.
- The state table is a dated observation maintained by the catch-up step; a
  hand-maintained file may carry the same table or a dated prose line.

Body sections, in this order when present: **What and why** (what the change
does, why, the local branch/worktree/commit it came from, what it depends on
or stacks under); **Likely reviewer questions** (decisions a reviewer will
question, with our answer ready); **Review thread** (dated: reviewer comments
and how we answered, what a follow-up revision still owes); **Follow-ups**;
then appended `### Observed <ts>` logs from catch-up. Point to the governing
topic or gap rather than restating it.

State lives in the path: `reviews/` open; `reviews/merged/` once every
review of the change is closed and the default-branch review merged;
`reviews/abandoned/` once every review is closed without that (say why in
the file — abandoned, superseded by which change, dead end). Move, never
delete: the file is the record of what we intended and what review asked for.

The file is never the authority on current state. Re-query the backend before
acting on a revision number, votes, status, or mergeability; a local branch
is equally not the authority, since it may sit on a superseded revision.

Cross-branch: a change pushed to several branches is one file whose table
lists each branch's review. A sibling's CI pass is evidence about the shared
code, never this review's vote; the branch reviews may be at different
revisions.

## Catch-up: observe what changed

Run this when asked what a review is waiting on, when catching up after time
away, before pushing a new revision, and after a push once CI has had time
to report. The helper `reviews sync [--mark] [--merge-check] [change...]`
(`~/agents/scripts/reviews`, acli, commentary with review links; `reviews
--help`) accelerates it and appends the log; the procedure is the contract,
so an agent operating the Gerrit web UI, `gerrit query`, or `gh` by hand
reaches the same end state:

1. For each tracked change (or the named one), fetch every review's current
   status, revision, CI verdict, human votes, submit readiness, reviewers, and
   the full activity: revisions uploaded, messages, inline comments, CI
   results. Gerrit: `ssh -p <port> <host> gerrit query --format=JSON
   --current-patch-set --patch-sets --comments --all-approvals
   --all-reviewers --submit-records change:<Change-Id>` returns every branch's
   review in one call. GitHub: `gh pr view <N> --json ...` plus
   `gh api repos/<o>/<r>/pulls/<N>/comments` for inline comments.
2. Everything timestamped after `Seen:` is new. Report each item with a link
   to its review and, for inline comments, the file and line.
3. Record: rewrite the state table. When marking caught-up, append
   `### Observed <ts>` listing the new events (one line each; "no new
   activity" when none), set `Seen:` to now, and move the file if every
   review is closed. Skipping the helper, write the same block by hand, or
   omit the log and only advance `Seen:` after step 4.
4. Evaluate — the agent's work, not the helper's: answer or resolve each
   reviewer comment and record the answer under **Review thread**; classify
   a CI failure as infrastructure or real by opening the build, and never
   retrigger a revision that stands passing; decide on rebase or conflicts
   (`--merge-check` merge-trees each open Gerrit revision onto the local
   `origin/<branch>`); update what a follow-up revision owes. Then report to
   the user what needs their decision.

`reviews status` lists tracked files from their saved tables without network;
`--live` re-queries. `reviews new <number|Change-Id|PR> --write` creates a
file skeleton in the naming scheme; `reviews find <id>` locates one;
`reviews show <id>` prints live state for a change tracked or not. The helper
acts only on files whose `Change:` backend matches the project config and
reports the rest as skipped.

## Relationship to handoffs, topics, and gaps

Handoffs preserve live continuity and private direction; a handoff that
records a push names the review file instead of restating revision or vote
state. Contract knowledge a reviewer needs goes to `topics/`; a defect the
review leaves open goes to `gaps/`. The review file cites both.

## Known limits

- Gerrit 3.5 SSH query exposes no mergeability flag and anonymous REST is
  usually closed; `--merge-check` uses a local merge-tree instead.
- The GitHub backend is smoke-tested only:
  [`gaps/reviews-github-backend.md`](gaps/reviews-github-backend.md).
- Ticket trackers are linked, not queried; ticket status stays manual.

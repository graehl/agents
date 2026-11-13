# Harsh review: fixing and amending

Read in full from `SKILL.md` § Fixing and amending when the request carries
`fixing` or `amending`, after the verdict is written and before changing any
file. `harsh-review fixing since` lands the fixes as new commits and rewrites
nothing. `harsh-review amending <range>` folds each fix into the in-range
commit that introduced the defect.

## What gets fixed

A fix covers every finding whose remediation is settled, whether blocker or
advisory. A finding that needs a user decision, or a restructure too large for
this session, stays open in the verdict and gets a gap. Fixes follow ordinary
project practice: run the formatter and the project's checks, and use the
project's commit conventions. Make and check the fixes in the working tree
first; they enter history only in the form the request named.

## Folding with `amending`

A fix that spans several commits goes to the latest commit it needs. The
user's `amending` request authorizes rewriting the in-range commits even when
an earlier session made them.

Run all three stop checks before creating any commit. A `fixup!` commit made
before a check fails is already a fix in history in a form the user did not
ask for.

1. **Published commits are not amendable.** List the in-range commits
   already published: those reachable from any remote-tracking ref
   (`git for-each-ref --contains <sha> refs/remotes`), plus any you know were
   pushed elsewhere, such as an open PR or a Gerrit change. Rewriting a
   published commit, or anything below one, needs a force push. The word
   `amending` does not authorize that push. Only the commits after the last
   published one can be amended. For fixes aimed at published commits, ask
   once whether a force push to that remote is authorized; the usual answer
   is no. Ask it together with the stop question below, so a no goes straight
   to choosing among those options.
2. **Active peers hold first.** Run `agentctl others`. If any peer is
   active, name the peers, tell the user, and send each one a hold request
   with `agentctl message --to <id> --message '<text>'`. The message asks the
   peer not to commit in this repo until it receives a release, and to
   acknowledge by replying with `agentctl message`. Never pass `--wake`. The
   default live-only delivery reaches only sessions that are running now, and
   it leaves an inbox note for the others. Proceed only when every peer has
   acknowledged or the user directs. This is the exception
   `~/agents/topics/commits.md` § History rewrites in a shared worktree names
   to its ban on rewrites while peers are active. An acknowledged hold
   narrows the race that ban guards against; the user's direction alone only
   accepts it. Everything else in that section and in its § Amends still
   applies: the `REWRITE` banner for the whole chain, and messages amended
   additively.
3. **The tracked tree holds only the fixes.** Rebase needs a clean tracked
   tree once the fixes are committed, so any other tracked change stops the
   fold. Never use `--autostash` or a broad stash.

When a check blocks any fix, ask the stop question before folding the others;
the answer decides what form every fix takes.

With the checks passed, make one `fixup!` commit per target
(`git commit --fixup=<target> -- <paths>`), then run
`GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash <base>`. When the rebase
conflicts, run `git rebase --abort`. The abort leaves the `fixup!` commits at
the tip: leave them there, unpushed, and name each with its target in the
stop question. When the rewrite ends, whether it folded or stopped, send each
held peer a release the same way as the hold.

## Stop and ask

Never land fixes as ordinary commits without the user's say. Whatever stops a
fold (a published target, unacknowledged peers, a dirty tree, a conflict),
stop and ask. Name the fixes affected and the reason. Offer three options:
fold them once the cause clears, keep them as ordinary commits, or leave them
uncommitted for the user. Until the user answers, no fix goes into history
except in the form requested; `fixup!` commits an aborted rebase left behind
stay as they are until then.

## Marker after fixing

The fixes are this review's own remediation, so the marker may advance across
them, and across nothing else (§ Review marker: it must never jump commits no
review has accounted for).

- **`fixing`**, and fixes kept as ordinary commits: starting at the reviewed
  end, advance across the fix commits this review made for as long as each
  directly follows the last. Stop before the first commit from another
  session; with one directly above the reviewed end, the marker stays at the
  reviewed end and the next `since` reviews the fixes with it.
- **`amending`**, once folded: line 1 becomes the rewritten counterpart of the
  reviewed end, and nothing above it.

When line 1 is not the reviewed end, write `fixed-by-review <full reviewed-end
SHA>` on line 2. § Review marker exempts that line from its rewritten-marker
rule, so the next `since` does not raise this review's fixes as an unreviewed
amend. The verdict lists each fix with the commit it landed in.

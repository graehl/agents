---
name: reviews
disable-model-invocation: true
description: Catch up on the project's pushed code reviews (Gerrit or GitHub) — what changed since we last looked (comments, CI verdicts, votes, revisions, merges), recorded into reviews/ and evaluated. Use when the user invokes /reviews, optionally naming a review number, PR, or Change-Id.
argument-hint: [change ...] [--merge-check]
---

# /reviews — what did our reviews do since we last looked

Follows `~/agents/REVIEWS.md` § Catch-up. Read that section before the first
run in a session; it is the contract, the helper is the accelerator.

## Workflow

1. **Activation check.** `reviews/config.toml` must exist under the project
   root; if not, say the project has not activated `~/agents/REVIEWS.md`
   § Activation and stop.
2. **Observe and record.** Run the helper with the user's arguments:

   ```bash
   reviews sync --mark [--merge-check] [change ...]
   ```

   It rewrites each file's state table, appends `### Observed <ts>` with the
   events newer than `Seen:`, advances `Seen:`, and moves files whose every
   review is closed. Its commentary carries a review link and the noticed
   items per change; the JSONL `new_events` carry file/line for inline
   comments. Use `--dry-run` when the user only wants a look.
3. **Evaluate** each change with new events (REVIEWS.md step 4): draft the
   answer to every reviewer comment and record it under **Review thread**;
   open a failing CI build before calling it infrastructure; check that a
   standing passing verdict is not retriggered; note rebase or conflict
   needs; revise **Likely reviewer questions** and what the next revision
   owes.
4. **Report** per change: link, standing state (status, revision, CI, human,
   submittable), what is new, and the decisions that are the user's. Nothing
   new: say so in one line per change.

---
slug: reviews-github-backend
noticed: 2026-09-15
where: scripts/reviews `github_reviews`
---

**Gap:** the GitHub backend of `reviews` (`REVIEWS.md` § Catch-up) is
implemented against the `gh pr view --json` and `pulls/<N>/comments` shapes
but has only been exercised on a merged PR with no reviews, inline comments,
or check runs. Event timestamps, `statusCheckRollup` field names across
check-run vs. status-context entries, `reviewRequests` shapes for teams, and
the human-vote projection (latest APPROVED / CHANGES_REQUESTED per login) are
unverified on a live open PR. The Gerrit backend is the verified path.
**Noticed while:** building the generic review-tracking policy for xmt's
Gerrit reviews; the user asked for the GitHub form to be identifiable and
left for later.
**Fix sketch:** run `reviews show <owner/repo#N>` against an open PR with a
review, an inline comment, and a completed check; fix field mismatches;
then `reviews new ... --write` and `sync --mark` end to end in a project
whose `reviews/config.toml` says `kind = "github"`.

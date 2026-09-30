---
slug: agents-user-public-history
noticed: 2026-09-30
where: AGENTS.user.md / github.com/graehl/agents history
---

**Gap:** `AGENTS.user.md` is personal policy, and README calls it private
in this setup, yet it has been tracked since `d6f0260` (2026-05-06; commit
`6fde295` on 2026-07-01 made the tracking deliberate for the web digest). The
repository is public, so GitHub's default view shows it at `master` and
throughout history. A 2026-09-30 scan found no credentials or secrets, so this
is low priority.

**Noticed while:** compiling `AGENTS.user.md` into the git-excluded
`AGENTS.boot.md` so its content never enters the tracked global policy.

**Fix sketch:** keep the local file; stop tracking it (`git rm --cached`,
ignore rule) after pointing `scripts/web-digest.manifest` and other readers
at the working-tree copy. Removing it from published history means a
filter-repo rewrite of about 715 of 727 commits and a lease-guarded force
push. As of 2026-09-30 the repo has 0 forks and 0 stars. Every commit SHA
changes, which breaks `refs/notes/agent-session`, revision-pinned citations
in topics and ledgers, and other clones. Old commits stay reachable on
GitHub by SHA until GitHub support purges them. A force push of `master`
needs the user's explicit go under the big-effect gate.

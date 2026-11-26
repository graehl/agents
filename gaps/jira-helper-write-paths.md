---
slug: jira-helper-write-paths
noticed: 2026-11-25
where: scripts/jira cmd_create, cmd_update, _transition, cmd_comment
---

**Gap:** the issue-writing requests of `scripts/jira` have never been sent:
`create`, `update`, `transition`, and `comment --markdown` were checked by
dry run, read-only lookups and stubbed-request tests only, to avoid filing a
throwaway issue or comment in a shared project. Their payload shapes follow
the Jira Cloud REST docs but no live server has accepted one yet.

**Noticed while:** adding the verbs, and the automatic review of that commit.
**Fix sketch:** close this when the first real `create`, `transition` and
`update` succeed in ordinary use; on a rejection, fix the payload and add the
server's error to `tests/test_jira.py`.

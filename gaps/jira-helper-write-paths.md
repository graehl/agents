---
slug: jira-helper-write-paths
noticed: 2026-11-25
where: scripts/jira cmd_create, cmd_update, _transition, _sprints, cmd_comment
---

**Gap:** the issue-writing verbs of `scripts/jira` (`create`, `update`,
`transition`) landed without ever sending a write request: they were checked
by dry run and by read-only lookups only, to avoid filing a throwaway issue
in a shared project. Around them:

- `_sprint`, `_transition` and `_planning_fields` have no tests; all three
  are testable with `_request` stubbed.
- `_sprints` asks only for scrum boards and reads one page of boards and of
  sprints, so a project with other board kinds may list nothing and a large
  one truncates silently. Not checked against a live site.
- `transition` has no `--dry-run`.
- `comment` still takes Jira wiki markup while `create` takes Markdown. The
  code comment's reason (no document-format builder) no longer holds, but
  switching the input format is a compatibility decision for callers.

**Noticed while:** adding the verbs, and the automatic review of that commit.
**Fix sketch:** after the first real `create`/`transition`/`update` succeed,
drop the unsent-write item; add stubbed-request tests for the three helpers;
page `_sprints`; decide `comment`'s format under `topics/backward-compat.md`.

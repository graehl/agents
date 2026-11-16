---
slug: jira-search-endpoint-removed
noticed: 2026-11-16
where: scripts/jira (search verb)
---

**Gap:** `jira search` fails with HTTP 410 on Atlassian Cloud: the helper
calls `GET /rest/api/3/search`, which Atlassian removed in favor of
`/rest/api/3/search/jql` (changelog CHANGE-2046). `get` and `comment` still
work, so only JQL search is broken.
**Noticed while:** looking for related AIP tickets before creating AIP-2854.
**Fix sketch:** switch to `GET /rest/api/3/search/jql?jql=...&fields=...`.
The new endpoint pages with `nextPageToken` instead of `startAt` and does
not return `total`, so adjust any paging or count output.

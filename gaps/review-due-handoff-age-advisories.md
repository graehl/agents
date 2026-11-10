---
slug: review-due-handoff-age-advisories
noticed: 2026-11-10
where: scripts/review-due, scripts/handoff-age
---

**Gap:** advisories from the two 2026-11-10 strict reviews (verdicts under
`harsh-review/`, ranges `a8164da8541d..9dc1d6016a9c` and
`9dc1d6016a9c..80e80e3dbef9`) that are real and not fixed:

- `review-due`: one `hook` run took about 4.8 s on a 561,884-line backlog,
  and an oversized backlog persists until a skip is approved. One duplicate
  listing was removed; the rest is not profiled.
- A refused cut is not recorded, so each new session asks again.

**Noticed while:** adding age to handoffs and the oversized-backlog cut.
**Fix sketch:** profile the hook on the large backlog; decide with graehl
whether a refusal should be recorded and where.

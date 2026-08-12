---
slug: research-advisor-session-title-convergence
noticed: 2026-08-12
where: research-advisor.md advisor startup and dispatch around session-turn
---

**Gap:** Advisor sessions can start or resume with a provider-visible title
different from the exact title in advisor metadata. Harnesses and YA may
automatically retitle sessions, and advisor bring-up has not yet converged the
hosted YA provider-service path with native harness resume. Title is therefore
nonblocking presentation repair debt, not continuity or ownership evidence.

**Noticed while:** Reviewing a slow, bugged generation-2 advisor bring-up that
treated title verification as a possible continuity gate.

**Fix sketch:** Keep generic `session-turn` free of research-advisor metadata
semantics. Add advisor-specific startup/dispatch that waits until either hosted
or native resume has started, applies the metadata title, and verifies the
provider-visible result through an authoritative provider API. For Codex, use
app-server `thread/name/set` and verify `thread/read`'s `thread.name`; do not
infer the title from a raw SQLite field. Test both the YA provider-host route
and native Codex resume, including an automatic retitle after startup. Remove
this gap only when both paths converge or report a repairable mismatch without
changing continuity disposition.

# web-platform-guidance evidence

## 2026-11-15 — own activity route, with defaults inline

- **User direction (graehl).** The vendored guides were first routed only
  from `ui-quality`, with a section limiting their authority. He objected:
  softening `MANDATORY` is one thing, but the intent was for the useful
  content to be considered in web projects without explicit direction, and
  asked that it be likely to be met in the appropriate contexts.
- **Why `ui-quality` did not reach it.** Its route fires on "starting UI
  work". The traps the guides cover arrive as code changes: a key handler, an
  HTML sink, a response header, a loop. An agent making one of those in
  `~/ya` would not consider itself starting UI work.
- **Decision (agent).** A dedicated topic with a `Governs:` line phrased as
  those code changes, placed in the boot's code group, and a one-line default
  per row so the steer survives when the guide is not opened. Cost: one boot
  route line.
- **Trace: rename field in `~/ya` with Enter to commit.** "A key handler"
  matches; the row's default is the composition check `~/ya` already uses in
  25 files. Same outcome as the house practice.
- **Trace: "simplify `Modal` with native dialog" in `~/ya`.** The overlay row
  says to find the existing floating layers first; the limits say recorded
  project decisions win; `~/ya`'s development guide routes to its own
  register of exceptions. The agent keeps the custom modal or moves every
  layer.
- **Trace: server-only route change.** Does not match unless it sets a
  security header or cookie, which the phrase names on purpose; an earlier
  wording said "browser-side code" and would have excluded those.
- **Trace: one-off static HTML handout.** May match on a control; the cost is
  one short topic read.
- **Unmeasured.** Whether agents open the guides, and whether the inline
  defaults change code, has not been observed in sessions.

Contributing-model: fable-5.2

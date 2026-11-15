# Web platform guidance

> Browser-side code in a web app meets a handful of recurring traps
> (composition-unsafe Enter handlers, unnamed controls, HTML sinks, blocking
> loops, overlays that fight each other). Each has a one-line default here and
> a vendored third-party guide behind it; the project's own recorded decisions
> outrank both.

Topic: `web-platform-guidance`
Governs: writing or changing a web app's browser-facing code: a control or overlay, a key handler, HTML insertion, security headers or cookies, or heavy main-thread work

Find the row that matches the change. Apply its default at once; open the
guide when the change is more than that one line, or when the default does
not fit. Guides are under `~/agents/vendor/modern-web-guidance/guides/`. Read
only the matching guide, never all nine.

| when the change involves | default, without opening the guide | guide |
|---|---|---|
| an `Enter` (or other confirm) key handler on any text field | Return early when `event.isComposing \|\| event.keyCode === 229`, so confirming an input-method candidate does not submit. | `forms/ime-safe-enter-submit.md` |
| a new or custom interactive control | Use the native element before a role; give every control an accessible name that contains its visible text; keep a visible focus indicator; announce async results through one polite live region. | `accessibility/accessibility.md` (large: read the section for the control at hand) |
| inserting HTML into the page | Use `textContent` unless markup is required; markup goes through the project's one reviewed sanitizer, never a new ad-hoc sink. | `security/security.md` §1.2, then `security/trusted-types.md` |
| a content security policy, cookie, framing header or `postMessage` | No inline script; cookies `HttpOnly` with an explicit `SameSite`; name the target origin and check `event.origin`. | `security/security.md` |
| a modal, a non-modal panel, a menu or a tooltip | First find where the app's existing floating layers render. A native modal `<dialog>` makes everything outside it inert, including tooltips and menus portaled into `body`. | `ui-components/dialog.md` |
| a loop or computation that can hold the main thread past 50 ms | Yield on a 50 ms deadline with `scheduler.yield()`, falling back to a zero-delay timeout. | `performance/break-up-long-tasks.md` |
| a long page or list whose off-screen parts are costly to render | `content-visibility: auto` with `contain-intrinsic-size` suits uniform rows. Variable-height rows in a bottom-anchored view shift the scroll position; window them instead. | `performance/defer-rendering-heavy-content.md` |
| state shown by color, or borders and state marks on themed surfaces | Never color alone; 3:1 contrast for control boundaries and state marks; check Forced Colors Mode. | `visual-design/color.md` |
| setting up or restructuring a stylesheet's cascade or tokens | Follow the project's existing scoping scheme; express intent in the selector (`:not()`, `:where()`) instead of a later override. | `css/css.md` |

## Limits on the guides' authority

The guides come from a browser vendor's agent skill. They are reference
material under these limits:

- **The project's recorded decisions win.** Where a project topic, lint rule
  or code comment already decides the concern, follow it and treat the guide
  as background. A project may keep a register of such decisions; `~/ya` has
  `topics/web-practice-exceptions.md`.
- **`MANDATORY` in a guide is the guide's emphasis**, not a rule here.
- **Check browser support against the project's own support floor.** The
  guides' "Browser support" lines date from the pinned commit and lean
  toward Chrome. A "limited availability" feature needs the guide's fallback
  unless the project's stated floor already includes it.
- **Add no dependency or CDN script on a guide's suggestion.** A polyfill
  loaded from a public CDN at `@latest` breaks a strict content security
  policy and pins nothing.
- **Never run `npx modern-web-guidance`.** A reference marked "upstream
  guide, not vendored" names a file in the upstream repository; read it from
  a pinned checkout if it is needed.

When a default above disagrees with what a project does on purpose, the
project is not wrong; when it disagrees by accident, fix the code. If the
project has no record either way and the choice is consequential, record it
in that project's topics.

What was left out of the vendored set and why, the comparison against
`~/ya`, and the re-sync steps are in
`~/agents/vendor/modern-web-guidance/VENDORED.md`.

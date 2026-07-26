# UI testing

> Capture-confirmed UI work: a web-app UI tweak request ends with
> rendered browser captures of the result — 1920×1080 desktop plus a
> phone width when the project targets mobile — inspected by the agent
> against the request before completion is claimed.

Topic: `ui-testing`

The generally applicable core of per-project UI-testing protocols.
Projects duplicate and extend this as their own `topics/ui-testing.md`
(yepanywhere's carries project commands and archive paths); each copy
stays self-contained, so checking out one repo never dangles a
cross-repo reference. The deeper verification method — tree vs.
pixels, viewport matrix, interaction sequences — is
[`ui-verification`](ui-verification.md).

## Capture rule

- **Trigger:** any request that changes what a web app renders — a UI
  tweak, layout or spacing fix, control/toolbar placement, restyle, or
  a new visible surface.
- **Required at completion:** captures of the final rendered result at
  1920×1080, plus a phone width (default 375×812) when the project
  targets mobile. In-progress captures are optional while
  implementing, worthwhile at milestones.
- **Inspect, don't decorate:** open each capture and check it against
  the request — spacing, flow, control placement — not merely "page
  loaded". The capture exists to catch the agent's own wrong
  spatial/aesthetic guess: models routinely one-shot UI that is
  functional but mis-spaced with misplaced controls (rule instituted
  2026-07-26 after a commit-browser UI landed exactly that way).
- **Report:** cite the capture file paths in the final response and
  say what was visually confirmed and what was not checked.

## Mechanics

Prefer the project's own screenshot tooling when its instructions name
one. Generic fallback where Playwright is available:

```bash
npx playwright screenshot --viewport-size "1920,1080" <url> desktop.png
npx playwright screenshot --viewport-size "375,812" <url> mobile.png
```

Store captures under a durable project artifact directory (not
reboot-cleared `/tmp`) so cited paths outlive the session.

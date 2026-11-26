# Vendored: modern-web-guidance (selected guides)

Nine of upstream's 209 web-platform guides, copied in and pinned to an exact
upstream commit. Convention: `topics/vendoring.md`. When to read which guide,
and the standing caveats for using them, are in
`topics/web-platform-guidance.md`.

## Upstream

- **Repo:** https://github.com/GoogleChrome/modern-web-guidance
- **Subpath:** `skills/modern-web-guidance/guides`
- **Commit:** `4dd968349e54ca45a05dd5c818fb035c9054b022`
  (Release v1.0.0, 2026-11-10)
- **Vendored:** 2026-11-15

The repository is a release mirror: 194 of its 216 commits are bot releases
generated from `GoogleChrome/modern-web-guidance-src`. Its README says the
content is stewarded by the Chrome, Edge, Firefox and MDN teams; that claim
was not checked here.

## License

Apache-2.0, from upstream's root `LICENSE` at the pinned commit, preserved
here as `LICENSE` (sha256
`cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`).
Upstream has no `NOTICE` file. Each vendored file carries a first-line
comment stating that it was modified.

## Vendored files

`upstream sha256` is the file at the pinned commit; `vendored sha256` is the
file here, after the local changes below. `refs` counts rewritten
cross-references.

| file | upstream sha256 | vendored sha256 | refs |
|------|-----------------|-----------------|------|
| `guides/accessibility/accessibility.md` | `752d3998044bbcdd2736262906ba0951fd6e334efeb52ebf1f8f54cbb6e21217` | `9b9ee9b5756f1e25cf5532a8de98ffe7ef2959a99e9bc28e4fa1270c6e5ce8f1` | 4 |
| `guides/css/css.md` | `1a32fb79887417cb93874ff03d02f2e00deff1e88a531c140bb2c61186aaae79` | `ffd317134dc18818867b3167d0070ad360130497a581215d44a0cda6a6d758ae` | 14 |
| `guides/forms/ime-safe-enter-submit.md` | `aa23bca5b8217e00fe1033741d473e1548e140ba4863a5ae7ac7f2c02132430c` | `3f8646d5f8b1e074742bbde7762c8c2481ce1496b0ebc5773f2b3c3f6c7af2e8` | 0 |
| `guides/performance/break-up-long-tasks.md` | `98c4326c7dd895e7f90db4eeb2ea6dad2daeb25e8171bd2795d74bdabf27189b` | `f13f7c9b1ec75467803d28e54fdda935a14b4ceda4586142f75257e709483d7e` | 0 |
| `guides/performance/defer-rendering-heavy-content.md` | `99f4e9b7b376b7be9c9acd22c04ec66d8bb8b50677a31d212c394d84f74adae9` | `55f8d206758bb7e26c820bb946f7b277b947eb48cd23f0b8dd1ff229a069212d` | 2 |
| `guides/security/security.md` | `0856fcb72419329397605700895414536cf0d00f1b697afeee5d4aac5fcf80ff` | `68ca7da21ccd6d874b2c0867f03c9412d4d12ef647131bcd11d9a8d64a0c107d` | 4 |
| `guides/security/trusted-types.md` | `3b3268a10597554e3f4235cd49bc850d07b8a8e7c19fbfffb290736e512b8af5` | `55cde0409b5c49869a75186b3601634f619d8dc5c28c6bdc24a3ae225bc5b3b0` | 2 |
| `guides/ui-components/dialog.md` | `f9d64f0e0f8788834a9bb1a0f674115b141b44f4f6b76d773d349199a972824b` | `c1a2245033d05daa2ba8e6b8a087db027df6191cb88fba54f68bafbae429341f` | 6 |
| `guides/visual-design/color.md` | `6fd4045e552d04b1881bce444cd0306339cb561d18df03da464035ce309b1e7b` | `2c17ccc0b8275087e1bfc5eefee9603eebb0e9d7f4f80921e48d2ed84bd1c7ee` | 1 |

## Local changes

Both changes are mechanical and apply to every vendored file.

- **Cross-references no longer name a command.** Upstream points from one
  guide to another with ``(via `npx -y modern-web-guidance@latest retrieve
  "<id>"`)``, which tells the reading agent to download and run an unpinned
  package. Each occurrence is replaced by ``(vendored: `guides/<path>`)``
  when the target is vendored here, else by ``(upstream guide `<path>`, not
  vendored)``. `<id>` is the target file's basename without `.md`.
- **A first-line HTML comment** names the source commit and license and says
  the file was modified.

Nothing else differs. In particular the guides' `MANDATORY` wording, their
browser-support lines and the polyfill-from-CDN suggestion in
`guides/ui-components/dialog.md` are upstream's, kept verbatim and qualified
by the limits in `topics/web-platform-guidance.md`.

## Selection

The aim was guidance that our own instructions lacked. A guide
was taken when it covered a concern with no written decision in
`topics/ui-quality.md`, `topics/functional-layout.md` or `topics/theming.md`,
rested mostly on widely available features or carried its own fallback, and
read as expert-written when sampled. A light sample of `~/ya` (feature
counts across `packages/`, its CSS and UI architecture topics, and its modal)
tested each against practice on 2026-11-15.

| vendored guide | gap it fills | `~/ya` sample |
|---|---|---|
| `accessibility/accessibility.md` | We had thresholds only (contrast, target size, visible focus, reduced motion); nothing on naming, ARIA, keyboard handling or live regions. | Practised without a written rule: live regions or status roles in 102 files, `:focus-visible` in 68. |
| `visual-design/color.md` | Forced Colors Mode, non-text contrast, `prefers-contrast`. | Nearly absent: 5 mentions of either media feature. |
| `css/css.md` | Cascade and selector discipline: layers, `:where()`, `:not()` over overrides, `@scope`, token tiers. | Agrees on tokens over literals. Differs on cascade control: YA scopes with CSS Modules and lint rules, and uses `@layer` once. |
| `ui-components/dialog.md` | Choosing between modal dialog, non-modal dialog and popover; dismissal; focus. | Contradicts a recorded decision; see below. |
| `forms/ime-safe-enter-submit.md` | Enter-to-submit while an input method is composing. | Agrees exactly: `isComposing`, with the `keyCode === 229` Safari fallback, across 25 files. |
| `security/security.md`, `security/trusted-types.md` | Client-side injection defenses and response-header rollout. We had the security-review skill and no implementation guidance. | YA sets a content security policy and has 26 files with HTML sinks behind its own sanitizer; Trusted Types is unused. |
| `performance/break-up-long-tasks.md`, `performance/defer-rendering-heavy-content.md` | Yielding inside long main-thread work; skipping off-screen rendering. | `scheduler.yield` unused, `content-visibility` used once; YA has its own rendering-performance and transcript-virtualization decisions, which win there. |

**Recorded contradiction.** `~/ya/packages/client/src/components/ui/Modal.tsx`
deliberately stays a portaled `div` with its own focus containment instead of
a native modal `<dialog>`: its tooltip layer, hover cards and selection
actions portal into `body`, and a modal `<dialog>` would draw over them and
make them inert. The guide does not mention this cost.

**Left out, by reason:**

- **The skill itself** (`SKILL.md`, the CLI, the plugin manifests). It
  declares itself mandatory before every HTML, CSS or client-script task,
  runs an unpinned `npx -y modern-web-guidance@latest` each time, and
  requires a `### Modern Web Guidance` section crediting it in the agent's
  reply.
- **Features one engine ships.** By their own support lines, 114 of the
  209 guides depend on at least one feature marked limited availability.
  Whole categories are Chromium-only or experimental: built-in
  AI (5), WebMCP (3), HTML-in-canvas (3), and most `ui-behaviors/` and
  `ui-atoms/` recipes built on interest invokers, `focusgroup`, scroll-state
  queries and similar.
- **Site and commerce concerns:** autofill, payment, address and one-time
  passcode forms; passkeys (8); analytics, A/B testing and load-priority
  tuning; installable-app and privacy guides.
- **Already decided here:** typography, responsive and fluid layout,
  container queries, dark mode and motion overlap `functional-layout` and
  `theming`, with minor differences (upstream caps line length at 80
  characters; ours is 45–75).
- **Not vetted.** `html/html.md`, `forms/forms.md`,
  `performance/performance.md` and the component recipes (menu, tabs,
  toolbar, single-line overflow, icons, copy button) may be useful on
  demand. The sampled parts of `html.md` and `performance.md` were weaker
  than the vendored guides: unsourced thresholds and blanket rules (dim
  every inert region; slice work at 50 ms and move it to a worker at
  250 ms). Read them from the pinned checkout
  (`~/.cache/checkouts/github.com/GoogleChrome/modern-web-guidance`, via the
  librarian skill) under the same caveats; vendor one only after vetting it.

## Re-sync from upstream

There is no helper: `vendor-skill` copies a whole subpath and this is a
subset with a rewrite.

```bash
python3 skills/librarian/checkout.py GoogleChrome/modern-web-guidance --force-update
cd ~/.cache/checkouts/github.com/GoogleChrome/modern-web-guidance
git rev-parse HEAD                      # the new pin
sha256sum skills/modern-web-guidance/guides/<path>   # compare to "upstream sha256"
```

A differing hash is drift. To re-pin a file, review the upstream diff, copy
the file over `guides/<path>`, re-apply both entries under "Local changes",
confirm no `npx` remains in it, and update both hashes, the commit and the
date above.

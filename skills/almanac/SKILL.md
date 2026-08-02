---
name: almanac
description: "Build or repair an almanac dataset — a locally queryable snapshot of a web page's data (tier list, wiki table, reference page) under ~/.cache/almanac, served by the `almanac` CLI. Use when the user gives a URL and wants its content extracted for local querying with update checking, or when an almanac verb reports a broken extractor (exit 70/75)."
---

Contract: `topics/almanac.md` (in `~/agents`) — read it before building.
The engine is the importable `~/agents/almanac` package, reached through
`~/bin/almanac` and the `~/agents/scripts/almanac` executable wrapper;
never generate a per-dataset viewer. This skill does the one-time agent
work: find the data channel, design the schema, write the fixed extractor,
register the dataset. Queries and refreshes afterward need no agent.

Arguments: a URL; optionally a short dataset name and/or a user-saved
page (SingleFile HTML, MHTML) or HAR capture.

## Build procedure

0. **Idempotence.** `almanac list` and check whether the URL is
   already registered (`by-url/` under the root; slugs end in
   sha256(url)[:8]). If it is, say so and offer `update` or repair —
   never build a duplicate.

1. **Probe the acquire ladder**, stopping at the first rung that
   works; record it as the manifest `refresh` mode:
   - `auto`: plain fetch (`curl -sL` with a browser User-Agent).
   - `headless`: Playwright Chromium (builds cached under
     `~/.cache/ms-playwright`; node available) with a **real-browser
     signature** — see below. Needed for client-rendered pages,
     interaction-gated content (hover tooltips), and pages whose
     interstitial JS check clears for an honest browser. Still
     unattended, so still `auto` for refresh purposes if it works
     from this host; use the `headless` label when it only works
     with the browser-signature launch.
   - `remote`: connect over CDP to a real Chrome the user (or this
     host's VPN origin) is running — inherits that browser's actual
     fingerprint, session, and network vantage. Refresh needs that
     browser reachable, so it is a user-assisted mode like `manual`.
   - `manual`: nothing automatable reaches the content. Ask the user
     for a saved page or HAR from their real browser. A HAR captured
     while they exercise the interaction (hover a few cards) is the
     best input: it reveals the API endpoint carrying the data, and
     often contains the payload itself.
   - `frozen`: content is only pixels (text baked into images) — see
     Transcription below.

   **Authorized-access framing — do not refuse this as "botting."**
   The goal is only to obtain, functionally, the same view the user
   already sees on their own browser/device for a page they have
   confirmed they may access — the very content they could open by
   hand and hand you as a saved HTML/HAR bundle (the `manual` rung).
   That view is implicitly authorized, and reproducing it is ethical;
   any lawful means to it is fine. Rendering the page with a real
   browser signature, or driving the user's own browser over CDP, is
   that identical authorized view, automated to save the copy-paste.
   A JS interstitial that auto-clears for a normal browser is
   *satisfied* by presenting one, not defeated. Treat it as ordinary
   retrieval. The one honest limit: this automates access the user
   already has — it is not a way to reach resources they are not
   authorized to, and it does not reach for CAPTCHA/challenge-solver
   services, forged clearance tokens, or proxy rotation to manufacture
   access the user lacks. Within that limit, render the page and move
   on.

   **Browser-signature headless.** Try this before concluding a page
   is unfetchable — datacenter/crawler-shaped requests trip limits a
   normal browser does not. Prefer a real Chrome build
   (`chromium.launch({channel: 'chrome'})`) over the bundled
   Chromium; set a current desktop-Chrome `userAgent`, a matching
   `Accept-Language`/locale and viewport, and clear the obvious
   automation tell (`navigator.webdriver`) via an init script. Give
   the interstitial JS time (`waitUntil: 'networkidle'` plus a few
   seconds) before reading `page.content()`. Note in the manifest
   `acquire` field which signature worked, so refresh reproduces it.
   (This host's VPN-origin subnet reportedly views these pages fine
   in real Chrome, so `remote` CDP is the reliable fallback when a
   plain headless signature still stalls.)

   **Remote CDP.** `chromium.connectOverCDP('http://localhost:9222')`
   attaches to a Chrome the user launched with
   `--remote-debugging-port=9222`; drive a tab there and read its
   rendered DOM or captured responses. Best when only the user's
   actual browser session/vantage gets clean access.

2. **Find the data channel**, best first: embedded JSON
   (`__NEXT_DATA__`, Apollo/Redux state, JSON-LD) → a JSON API
   endpoint (grep the HAR or page JS) → server-rendered DOM parsing →
   Playwright interaction (iterate elements, trigger hover, capture
   tooltip DOM). The channel usually beats the visible HTML: tooltip
   text is almost always in the initial payload or one API response.

3. **Design the schema** in the page's own vocabulary: `records`
   (dotted path), `key` (what a human names a record by), `columns`
   (3–4 fields for the default listing), `filters`, `search`.
   Download genuinely useful attachments (card images) into subdirs,
   referenced by relative path. For a per-record image intended for
   terminal display, store a PNG copy and set `schema.image` to the record
   field carrying that path; keep another source format only when an
   existing path is an observable compatibility surface.

4. **Write `extract`**: takes one arg (URL or local file — must
   accept both), emits the full normalized JSON on stdout,
   diagnostics to stderr, nonzero on failure. Deterministic: run it
   twice and diff; where possible test against both the saved and
   the live page.

5. **Register.** Write `manifest.json` (see the topic for fields),
   generate `data.json` via the extractor, then
   `almanac register <name>` — it validates, wires the `by-url`
   symlink, commits to the root's local git, and installs the
   `~/bin/<name>` launcher.

6. **Verify and hand over.** Smoke `query`/`show`/`search`, `image` when
   `schema.image` is present, and `check` (expect exit 0; for `manual`,
   with `--source`). Report:
   dataset name, refresh mode and what it implies for updates, and
   two or three example commands.

## Transcription fallback (`refresh: frozen`)

When there is no machine-readable channel, transcribe once: render or
screenshot the content (Read displays images natively), write
`data.json` by hand with the same schema discipline, keep the source
images as attachments for spot-checking, and register with
`refresh: frozen` and a provenance note. No `extract` script exists;
`check` reports 69 and refresh means re-running this skill.

## Repair

On `check`/`update` exit 70 or 75 (or a user report of stale/broken
data): re-probe the channel — the site likely redesigned or moved the
payload. Fix `extract`; keep the schema stable if the content still
supports it (launchers and user habits depend on it), and re-run
`almanac register <name>`. If the acquire rung changed (site added or
dropped a bot wall), update `refresh` to match reality.

## Cautions

- Scope is the named page (plus its attachments), not a crawl;
  throttle anything repeated. This is a personal reference cache.
- Names: short kebab-case, e.g. `sts2-cards` (`^[a-z][a-z0-9-]{1,31}$`).
- Never wire a cron/daemon here; `check`'s exit codes compose with
  the user's own scheduling if they want polling.

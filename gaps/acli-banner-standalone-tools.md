---
slug: acli-banner-standalone-tools
noticed: 2026-08-28
where: scripts/session-turn
---

**Gap:** the `topics/acli.md § Stderr banner at launch` contract is
emitted by `acli.args`, so `scripts/session-turn` — a deliberately
stdlib-standalone acli tool (`# acli: 1`, hand-rolled parsers with an
`acli: 1` epilog and a hand-added `--json` alias) — prints no banner and
offers no `--acli-quiet`.

**Noticed while:** sweeping tools for the banner/`+toon` capability-line
revision; converting session-turn's four grammars to the `acli.args`
factory was out of that change's scope.

**Fix sketch:** either route its four parsers through
`acli.args.ArgumentParser` (picking up banner, `--acli-quiet`, and the
footer in one move — check the symlinked-from-`~/bin` sys.path story),
or inline a five-line banner honoring `ACLI_QUIET` and add the flag to
the shared `_accept_json_alias`-style helper. Prefer the factory unless
its standalone-stdlib property is deliberate enough to keep.

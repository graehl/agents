# Vendoring third-party code

> Copy someone else's skill/script/snippet into this tree pinned to an
> exact upstream commit, with a `VENDORED.md` that records where it came
> from, what (if anything) we changed, and how to re-sync.

Topic: `vendoring`

Scope: third-party *source we import and keep*, primarily `skills/<name>/`
but any vendored subtree. Not the same as `provenance-tracking.md` (that
tracks our own *run outputs*); this tracks imported *upstream source*.

## Vendor, don't submodule or symlink

Default to **vendoring** (copying the files in and committing them) over
git submodules or a symlink to an external clone, for content we don't
intend to co-develop. Rationale, for this repo specifically — a committed,
multi-machine, plain-clone instructions tree:

- **Portability.** A symlink into an out-of-tree clone (e.g.
  `~/.local/share/...`) is machine-local state; another clone of this repo
  gets a dangling link and a missing skill. Vendored files travel with the
  repo.
- **Pinning + review.** A vendored copy is frozen at a reviewed commit. An
  external clone can change code under you between `git pull`s with no
  review gate — bad for content an autonomous agent *executes*.
- **Offline + history.** Works with no network; shows up as a normal diff
  in our own history.
- Submodule is worst here: it pins the *whole* upstream repo, not a
  subpath, and brings detached-HEAD / `--recursive` ergonomics plus a live
  fetch dependency.

Flip to a live-tracking symlink/submodule only when you intend to track
upstream closely or co-develop, or the subtree churns and one update must
fan out to many machines. "Don't intend to revise" → vendor.

The sparse-checkout step (`--filter=blob:none --sparse`,
`sparse-checkout set <subpath>`) is still the right *extraction*
mechanism — it pulls one subdir out of a multi-skill repo without the
whole tree. Use it to extract, then copy in and commit. Drop the symlink.

## Every vendored subtree carries a VENDORED.md

`<dest>/VENDORED.md` is the provenance record. Required sections:

- **Upstream** — repo URL, subpath, and the **exact commit SHA** (the
  precise upstream git ref — full 40-char SHA, not a branch or tag name,
  which move). Include the commit subject + date for human context.
- **Vendored** — the date we copied it.
- **License** — license status at the pinned commit: detected upstream
  license files, or an explicit note that none were found. Do not assume
  the vendored subpath carries a redistributable license; consult upstream
  before redistributing or relicensing.
- **Vendored files** — each file with its sha256 at vendor time, so drift
  or local edits are detectable.
- **Local changes** — **document every divergence from upstream here**
  (what changed and why). A verbatim copy says "None". This is the
  load-bearing rule: a re-sync re-pins to new upstream and overwrites the
  files, so the only record of what we changed — and must re-apply — is
  this section. Keep it current with each local edit.
- **Re-sync** — the command to check drift and to re-pin.

## Use the helper

`vendor-skill` (canonical `scripts/vendor-skill`, installed at
`~/bin/vendor-skill`; spec in `topics/helper-scripts.md`) does the
sparse-clone → copy → write-`VENDORED.md` flow and pins the SHA for you,
and `--check` reports drift against current upstream. It preserves the
hand-written "Local changes" body across a re-vendor. Prefer it over doing
the steps by hand so the precise-ref and hash discipline is automatic.

```bash
cd skills && vendor-skill <org/repo> <subpath>     # vendor into ./<basename>
vendor-skill --check skills/<name>                 # drift report (exit 3 = drift)
```

## Auto-invocation note

A vendored skill keeps upstream's frontmatter. If its `SKILL.md` lacks
`disable-model-invocation: true`, it auto-fires on description match (e.g.
`librarian` is meant to trigger when a remote repo is referenced). That is
a behavior change to the environment — intended for some skills, not
others. Decide per skill whether to keep upstream's invocation mode; if
you change it, that is a **Local change** to record in `VENDORED.md`.

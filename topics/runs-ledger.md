# Runs ledger convention

> An optional `<topic>.runs/` subdir holding curated run records —
> typically agentctl artifacts — and a developer-facing README that
> indexes them and explains which still inform `<topic>.md`.

Topic: `runs-ledger`

## What it holds

Contents are arbitrary; in practice they are usually agentctl/RUNS
artifacts — configs, summary tables, small key outputs, occasional
plots — but the convention does not require it. Anything that
supports or once supported a claim in `<topic>.md` is welcome.

Layout:
- `<topic>.runs/README.md` — the digest (see below).
- `<topic>.runs/<YYYYmmdd>-<short-name>/` — one subdir per run or
  sweep, containing the curated subset (config, summary, small
  outputs) plus a pointer back to the source `.agentctl/<run-id>`
  when one exists.

Curate, don't mirror: full agentctl outputs stay in the gitignored
`.agentctl/`. The subdir holds only what supports a current or
recently-superseded claim, sized to remain comfortable in
`git diff`.

## The README digest

One per `<topic>.runs/`; the authoritative index of what lives
there and why. Audience is developers tweaking the feature, not
end users — lower per-claim detail than the main topic doc would
tolerate, greater comprehensiveness than the main doc carries.

Per run, the README records:
- What was varied / what question the run answered.
- The outcome (table, summary, one-paragraph interpretation).
- Whether the conclusion is still load-bearing for `<topic>.md`,
  superseded, or open.

Supersession: when a newer run replaces an older one's conclusion,
the older entry gains a one-line `superseded by <newer> — <reason>`
rather than being removed. Both entries survive; the digest carries
the chronology the main topic doc shouldn't.

## Housekeeping

The README is the source of truth for what belongs. A run subdir
not referenced from the README is stranded and a `git rm` candidate
at the maintainer's discretion — there is no obligation to preserve
runs whose interpretation has fallen out of the digest. Periodic
prune is fine; preserve runs whose conclusions still appear (even
partially) in `<topic>.md` or in a still-active README entry.

## Relationship to other ledgers

- `<topic>.md` — surviving interpretations only; terse, citable.
- `<topic>.evidence.md` — qualitative agent belief notes;
  append-only, agent's working memory.
- `<topic>.runs/` — runs plus interpretation digest; rewritable,
  developer-facing.

The "experiment, probe, or negative result" use case in
`evidence-ledger.md` lives here, not in evidence.md. evidence.md
remains for the qualitative notes that surround a run — surprise,
updated hypothesis, model change — that don't belong as a run
artifact.

# Claim provenance

> Keep a manuscript's claims traceable to the runs and artifacts behind them
> through invisible `ref:` source comments and per-section `.repro.md` riders,
> then resolve, reconstruct, and transport that evidence with `claim-refs`.

Topic: `claim-provenance`

Read this before adding or revising evidence citations in a paper or other
rendered research manuscript, before a verification pass over its claims, and
before moving a paper's run records between checkouts. It implements the
tracing requirement in [paper-writing](paper-writing.md) § Draft the
evidence-bearing spine; run-record structure is owned by
[provenance-tracking](provenance-tracking.md).

The aim is a claim a later reader can re-verify, not a record of every number.
Authoring stays cheap and never blocks drafting; the cost of finding and
reconstructing evidence is paid at verification, where it is expected.

## Inline citations

Cite the evidence behind a claim with an HTML comment near it:

```markdown
Combining the two models changes 38 of 659 rows (+0.65 F1 over its control).
<!-- ref: evidence/combination-v1/scores.json; compare.py; control and treatment share one parent -->
```

- The keyword is `ref:`; `refs:`, `run:`, and `runs:` are read the same way.
- Items are separated by `;`. The first item must be a **locator**. A later
  item whose first word looks like a locator (it contains `/`, has a file
  extension, or is a run reference) is one too; any other item is prose.
- A locator is a run reference `<experiment>/<run-id>` (for example
  `pii-ont3-document-context/20260909T185537Z`, naming
  `runs/aim/<experiment>/runs/<run-id>.json`) or a path. A path may carry a
  `#section` anchor, one `{a,b}` brace group, or a glob.
- Prefer a path relative to the project root or the program directory. A path
  also resolves against the citing file's directory and its ancestors, with
  each level's `evidence/` directory. A later item in the same comment first
  resolves beside the previous locator, then that locator's ancestors, so
  `…/best-head-curves/scores.json; compare.py` needs no repeated prefix.
- Cite the artifact a reader would open—a score file, table source, or
  receipt. When that artifact came from a tracked run, its `.meta.json`
  sidecar already leads to the run; naming the run as well is optional.
- Granularity is the section, paragraph, table, or figure a claim lives in.
  Per-number targeting is not required.
- Keep host-specific or absolute paths out of comments. Quarto keeps HTML
  comments in HTML page source and drops them from PDF, so a published HTML
  render exposes them.

Author-only notes (`PAPER-NOTE[...]`, `TBD[...]`, review comments) share the
comment syntax but are not citations; keep their keywords distinct from `ref:`.

## Section riders

A section `<section-stem>.qmd` (or `.md`) may keep a sibling
`<section-stem>.repro.md` rider: the reproduction entry for that section's
claims. Like `.trims.md`, it is excluded from renders. It holds what does not
fit an inline comment:

- producer run references, in the `<experiment>/<run-id>` form `claim-refs`
  finds anywhere in the rider;
- commands for results that no run record captures—verbatim, with the source
  commit SHA and whether the worktree was clean, or marked `reconstructed:`;
- where records not yet pulled back live (host, checkout path, experiment);
- pending runs and the protocol they follow; and
- the provenance level reached at the last verification, with what failed.

A tracked run record already binds its source: `agentctl` admits only
committed source and records the commit, which roughly covers in-repo source
and build dependencies. Reproducing such a run means checking out that commit
plus its declared inputs. Ad hoc foreground commands have no such record, so
the rider supplies the SHA. Write it down when you write the claim; recovering
it months later costs far more.

## Provenance levels

`claim-refs check` classifies each resolved citation:

| Level | Meaning | Verification action |
|---|---|---|
| `run-record` | A run record is present in this checkout. | None. |
| `record-missing` | A run is named (inline, in a rider, or by an artifact's sidecar) but its record is not here. | Pull it back (see Transport) or record where it lives. |
| `meta-md` | Only a legacy `.meta.md` sidecar records the command. | Acceptable; confirm the command still names inputs that exist. |
| `no-producer` | The file exists but nothing records what produced it. | Locate the producing command or run; record it in the rider, or regenerate under `agentctl start … --output`. |

Unresolved statuses are `unresolved` (no file matched), `ambiguous` (more than
one did; the row lists candidates), and `no-locator` (the comment's first item
is a label or prose). Fix the comment in each case; a label such as a frozen
release name belongs after a real locator.

## Verification pass

Run it before submission, when a headline claim changes, or when asked to
locate missing run references:

1. `claim-refs check <paper-dir> --text` groups citations by section and lists
   everything below `run-record`. Without `--text` it emits one JSON row per
   citation. Exit 3 means some citation did not resolve.
2. Resolve `unresolved`, `ambiguous`, and `no-locator` by correcting the
   comment. Search the program's evidence, handoffs, and logs for moved or
   renamed files before concluding one is lost.
3. For `record-missing`, find the record: a remote worker named in the rider,
   another checkout, or `runs/aim/` under a different experiment. Pull it back.
4. For `no-producer`, find the producing command: the rider, the research
   log, the evidence file's own README or header, handoffs, or the Git history
   of the file (`git log --follow`). Record it in the rider, marking whether it
   was found verbatim or reconstructed.
5. Record each claim's reached level in the rider. A claim whose evidence
   cannot be reconstructed is narrowed or cut, not left fluent.

## Transport

`claim-refs` gathers the run records a manuscript cites—those named inline or
in riders, and those reached through artifact sidecars—plus, by default, each
record's input ancestry, followed transitively through the records' input
source pointers. `--shallow` stops at the cited runs; `--run
<experiment>/<run-id>` adds runs directly and works without a manuscript.

- `claim-refs paths <paper-dir> --text` prints each record file (run JSON and
  its texts) one per line, relative to the current directory, for
  `xargs git add`. Missing records are reported on stderr with exit 3.
- `claim-refs pack <paper-dir> -o bundle.tar.xz` writes the same records at
  their canonical `runs/aim/` paths, plus their `manifest.jsonl` rows, into a
  tar.xz. It refuses an existing output. Exit 3 means some named records were
  absent here; the archive holds the rest.
- `claim-refs unpack bundle.tar.xz` merges a bundle into the current checkout's
  `runs/aim/`, appending missing manifest rows. It writes nothing if any
  archived file differs from the checkout's copy (exit 5).

Pulling back records from a remote worker is `pack` there (the worker's
checkout holds the same manuscript, or pass `--run`), copy the archive, then
`unpack` here. The bundle carries run records only, not source or data.

## Planned extensions

These are sketches, not current behavior:

- [run-consumer registration](../gaps/sketches/run-consumer-registration.md) —
  writing the citing sections into the cited run records, so "who depends on
  this run" is queryable.
- [manuscript bundle inputs](../gaps/sketches/manuscript-bundle-inputs.md) —
  optionally carrying cited artifacts and input files, with a publication-ban
  list for license-restricted material.
- [run source dependencies](../gaps/sketches/run-source-dependencies.md) —
  traced or declared in-repo dependencies, so a reproducible run need not
  require a clean worktree.

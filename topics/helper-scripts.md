# Helper scripts

> Repeatable agent operations get a named CLI helper with a tight
> spec — name, UI, post-conditions, 2-3 input/output examples — so
> any agent rebuilds the same tool from spec when missing and
> recognizes broken output without guesswork.

Topic: `helper-scripts`

## When to add a helper

A helper earns its weight when (a) the inline form has a chronic
fiddly failure mode (≥3 observed across sessions), (b) the operation
is mechanical enough that a script removes ambiguity, and (c) the
post-condition can be expressed as a test the script itself runs
(exit code). Commit-message linting clears the bar; one-off shell
pipelines do not.

## Where impls live

- **Canonical source**: `scripts/<name>` in this repo. Python
  3.10+ pure-stdlib unless a dependency is justified.
  Every helper ships with its initial tested impl — specs without a
  working impl are aspirational, not installable.
- **Runtime install**: `~/bin/<name>` per machine. Agent installs
  on first use (symlink to the canonical source, or copy if the env
  rejects symlinks). Assumption: a Python 3.10+ interpreter is on
  PATH.
- **Local fallback**: if the installed helper fails its own post-
  conditions on a known-good input in this env, replace
  `~/bin/<name>` with a fresh impl built to the same spec — keep
  the name and CLI identical so callers do not change.
- **Project-shaped helpers** (those that know repo-specific
  conventions): repo-local gitignored `scripts/agent/<name>` inside
  the consuming project. Agent rebuilds from spec on first use per
  clone.

## Rebuild trigger

If the named helper is missing on a system, or its output fails its
own post-condition checks against a known-good input, rebuild from
the spec entry below. The examples are the test suite — pass them
all or do not ship the rebuild. Do not invent a different UI.

## Spec entries

### commit-msg-lint

**CLI**: reads draft on stdin. If stdin is empty, reads the current
`HEAD` commit message via `git log -1 --format=%B`. On success
echoes the checked message verbatim to stdout, exits 0. On violation
lists issues on stderr (one per line, prefixed `commit-msg-lint:`),
exits 1. Empty input with no readable `HEAD` message exits 2.

**Post-conditions** (derived from `AGENTS.md` Commits section):
- subject ≤65 chars
- no literal `\n` in subject (multi-`-m` shell-quoting symptom)
- blank line between subject and body if body present
- body lines ≤71 cols, except where the longest single token on
  the line is itself >71 (unavoidable long-token carve-out for
  URLs, paths, identifiers)
- no `Co-Authored-By:` trailer

Not enforced (deliberately — these are visual/judgment rules the
linter would mis-fire on): bullet/indent preservation, narrative
quality, presence of `Topic:` trailers, `Known coverage gaps:`
section structure.

**Examples**:
1. Single-line subject `feat: do thing` → exit 0, echoed verbatim.
2. Subject containing literal `\n` (e.g. `feat: foo\nbody`) → exit
   1, `literal '\n' in subject`.
3. 70-char subject + valid body → exit 1,
   `subject 70 > 65 chars`.
4. Clean subject, blank line, body line of 85 cols of prose →
   exit 1, `line 3: 85 > 71 cols`.
5. Clean subject, blank line, body line containing a single
   90-char URL with no spaces → exit 0 (long-token carve-out).
6. No stdin in a Git checkout with `HEAD` → lints `HEAD` and echoes
   the commit message on success.

**Canonical source**: `scripts/commit-msg-lint` (in this repo).
**Install target**: `~/bin/commit-msg-lint` (symlink by default).

**Usage**:
```sh
git commit -F <(commit-msg-lint < draft.txt) && rm draft.txt
# or, fail fast before committing:
commit-msg-lint < draft.txt && git commit -F draft.txt
# or, check the current commit:
commit-msg-lint
```

### commit-msg-fmt

**CLI**: `commit-msg-fmt -m "subject" [-m "para" ...]`. Writes a
formatted commit message to stdout, exits 0. The first `-m` is the
subject and passes through unwrapped. Subsequent `-m` args are
wrapped to 71 cols. `-m` args are joined with single newlines —
**no blank lines are inserted automatically**, unlike `git commit
-m -m`. To insert a blank line (e.g. between subject and body),
pass `-m ''`. No `-m` args or empty subject exits 2.

**Post-conditions**:
- output line 1 (subject) equals first `-m` arg verbatim
- each body line ≤71 cols (except where a single token in the
  input is itself >71)
- blank lines in output come only from explicit `-m ''`
- output ends with exactly one trailing newline

**Scope limitation**: each `-m` is treated as one plain-prose
paragraph. Pre-formatted content (bullets, hanging indents, ASCII
diagrams, tables, code blocks) must not be passed through this
formatter — write those messages directly with `git commit -F`
instead. The formatter intentionally collapses internal whitespace
when wrapping.

**Examples**:
1. `commit-msg-fmt -m "feat: do thing"` → `feat: do thing` + newline.
2. `commit-msg-fmt -m "feat: do thing" -m "" -m "Body paragraph
   long enough to wrap across two lines at 71 cols of width."`
   → subject, blank line, body wrapped to ≤71 cols.
3. `commit-msg-fmt -m "feat: do thing" -m "" -m "Para 1." -m "" -m
   "Para 2."` → subject, blank, `Para 1.`, blank, `Para 2.`.
4. `commit-msg-fmt -m "feat: do thing" -m "Body, no blank above."`
   → subject directly followed by body line; commit-msg-lint will
   flag the missing blank.
5. `commit-msg-fmt` (no args) → exit 2, `no -m args`.

**Canonical source**: `scripts/commit-msg-fmt` (in this repo).
**Install target**: `~/bin/commit-msg-fmt` (symlink by default).

**Composes with commit-msg-lint**:
```sh
commit-msg-fmt -m "feat: do thing" -m '' -m "Body paragraph." \
  | commit-msg-lint && git commit -F -
```

### vendor-skill

Copies a subdirectory of a remote git repo into this tree, pinned to an
exact upstream commit, and writes/refreshes a `VENDORED.md` provenance
record. Implements the convention in `topics/vendoring.md`.

**CLI**:
- `vendor-skill <repo> <subpath> [dest]` — sparse-clone `<repo>` at HEAD,
  copy `<subpath>` into `dest` (default `./<basename(subpath)>`), write
  `dest/VENDORED.md`. `<repo>` accepts a full URL, `git@host:org/repo`,
  `host/org/repo`, or `org/repo` (defaulting host `github.com`). Exit 0 on
  success.
- `vendor-skill --check <dest>` — re-read `dest/VENDORED.md`, sparse-clone
  upstream at HEAD, diff the vendored files against current upstream.
  Exit 0 = in sync (prints `up to date: <sha>`), exit 3 = drift (prints a
  unified diff). Modifies nothing.
- Usage/parse errors and a missing/incomplete `VENDORED.md` exit 2.

**Post-conditions**:
- After a vendor: `dest` contains the upstream subpath files (exec bits
  preserved); `dest/VENDORED.md` exists with an Upstream **Commit** equal
  to the clone's `git rev-parse HEAD` (full 40-char SHA), a per-file
  sha256 table matching `sha256sum` of the copied files, and a License
  section describing detected upstream license files or their absence.
- A re-vendor over an existing `dest` preserves the hand-written body of
  the `## Local changes` section verbatim; all other sections regenerate.
- `--check` never writes; its temp clone is removed regardless of outcome.

**Examples**:
1. `cd skills && vendor-skill xl0/agent-files skills/librarian` → vendors
   into `skills/librarian/`, prints `vendored …@ <sha12> -> …` and (since
   that repo has no LICENSE) a no-license warning.
2. `vendor-skill --check skills/librarian` with upstream unchanged → exit
   0, `up to date: <sha12>`.
3. Edit a vendored file locally, then `vendor-skill --check skills/librarian`
   → exit 3 and a unified diff of the local edit.
4. Put a note under `## Local changes`, re-vendor the same subpath → exit
   0, files re-pinned to upstream, the note still present.

**Canonical source**: `scripts/vendor-skill` (in this repo).
**Install target**: `~/bin/vendor-skill` (symlink by default).

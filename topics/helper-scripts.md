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

- **Canonical source**: `~/agents/scripts/<name>`. Committed under
  the synced `~/agents` repo, Python 3.10+ pure-stdlib unless a
  dependency is justified. Every helper ships with its initial
  tested impl — specs without a working impl are aspirational, not
  installable.
- **Runtime install**: `~/bin/<name>` per machine. Agent installs
  on first use (symlink to the canonical source, or copy if the env
  rejects symlinks). Assumption: a Python 3.10+ interpreter is on
  PATH.
- **Local fallback**: if the installed helper fails its own post-
  conditions on a known-good input in this env, replace
  `~/bin/<name>` with a fresh impl built to the same spec — keep
  the name and CLI identical so callers do not change.
- **Project-shaped helpers** (those that know repo-specific
  conventions): repo-local gitignored `scripts/agent/<name>`.
  Agent rebuilds from spec on first use per clone.

## Rebuild trigger

If the named helper is missing on a system, or its output fails its
own post-condition checks against a known-good input, rebuild from
the spec entry below. The examples are the test suite — pass them
all or do not ship the rebuild. Do not invent a different UI.

## Spec entries

### commit-msg-lint

**CLI**: reads draft on stdin. On success echoes draft verbatim to
stdout, exits 0. On violation lists issues on stderr (one per line,
prefixed `commit-msg-lint:`), exits 1. Empty input exits 2.

**Post-conditions** (derived from `~/agents/AGENTS.md` Commits
section):
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

**Canonical source**: `~/agents/scripts/commit-msg-lint`.
**Install target**: `~/bin/commit-msg-lint` (symlink by default).

**Usage**:
```sh
git commit -F <(commit-msg-lint < draft.txt) && rm draft.txt
# or, fail fast before committing:
commit-msg-lint < draft.txt && git commit -F draft.txt
```

# Verify

> `verify` is the standard way to run a project's tests and checks: the
> project declares them in `verify.toml`, and the runner reports one summary
> line on success and only the failing checks' details otherwise.

Topic: `verify`
Governs: running a project's tests or checks, when it has a verify.toml

## Why a standard entry point

Each project already has its own test commands; `verify` does not replace
them. It gives them one name, so "run the tests" costs one call with the same
output shape everywhere instead of rediscovering commands and reading whole
logs. Output stays small when nothing needs judgment: green is one summary
record. A failure brings its exit status, the last lines of stdout and
stderr, and the full log paths for anything further.

## Running it

```sh
verify --text            # quick tier; one line when green
verify --deep            # quick plus deep checks
verify --only NAME       # one check, any tier; repeatable
verify --list            # the declared checks, without running them
verify --passed --text   # comma list of checks already green on these exact files
```

`scripts/verify` in `~/agents`, installed as `~/bin/verify`. It finds the
root by walking up from the current directory (or `--project`) to the first
`verify.toml` or `verify.local.toml`, so a program subdirectory with its own
config is verified on its own when you run from inside it. Checks run
concurrently (`--jobs`, default up to 4). Each one's output goes to
`.verify/last/<name>.out` and `.err` under that root; the directory is
replaced on every run and `.verify/` is added to the clone's
`.git/info/exclude`. Exit 0 means every selected check passed (skips
allowed), 1 means at least one failed or timed out, and the report is
complete in both cases. `--full` also lists passing checks.

Every result is remembered in `.verify/state.json` against the **source
tree**: a git tree id of the tracked and untracked, non-ignored files,
computed in a scratch index so the real one is untouched. `--passed` lists
the checks whose latest result passed on exactly the current files, with the
same command. A caller can skip those, which is how a publish script avoids
rerunning checks that just passed. Any edit, including a rebase that brings
in other changes, gives a new tree id and empties the list. The id covers
the whole repository, even for a program subdirectory's checks. A run whose
files changed while it was running records nothing.

Committing is not a prerequisite for verifying. The summary says what was
verified: `committed HEAD <sha>` when the files equal HEAD's tree,
`uncommitted working tree <id>` otherwise, or that nothing was recorded
(outside git, or files changed mid-run). An uncommitted pass stays valid
for a later commit of exactly those files, because that commit's tree is
the recorded tree; so a workflow may verify first and decide afterwards
whether to commit.

A check with a `warn` regular expression reports every output line that
matches it, even when the check passes. The result stays a pass, the lines
are shown in the output, and `--warnings-file PATH` writes all of them as
`<check>: <line>`. A file that exists but is empty means no warnings.

A check is **skipped**, not failed, when an executable it `requires` is not
on `PATH`, or when it exits 69 (sysexits `EX_UNAVAILABLE`, acli's
`unavailable`) to say a prerequisite is missing. The skip carries the reason,
so an environment gap stays visible without turning the run red.

## Declaring checks

```toml
[[check]]
name = "unit"
run = "python3 -m pytest -q tests"   # bash -c, from cwd (default: root)
requires = ["pytest"]                 # skip when absent from PATH
timeout = "10m"                       # default 10m; killed as a process group
tier = "quick"                        # default; "deep" runs only with --deep
exclusive = false                     # true: run alone, after the others
warn = 'not wrapped in act\('         # report matching lines; still a pass

[[check]]
each = "tests/test_*.py"              # one check per matching file
name = "{stem}"                       # default
run = "python3 {path}"
exclude = ["tests/test_slow.py"]
```

Put a check in the quick tier when it is cheap enough to run before every
commit; slow, environment-heavy, or live-service checks go in `deep`. Mark a
check `exclusive` when it cannot share the machine with another check, such
as a browser suite that starts servers on fixed ports. A
committed `verify.toml` is shared with collaborators. In a repository whose
tracked files you should not change, or for private variations, declare
checks in `verify.local.toml`; `verify` adds it to the clone's git exclude.
When both exist, the local file is used and the committed one is ignored
unless the local file includes it:

```toml
include = ["verify.toml"]             # paths relative to this file
[[check]]
name = "test"                         # replaces the included check of this name
run = "pnpm test -- --bail"
```

Included checks run from their own file's directory, and `each` globs are
relative to it as well. So a program's `verify.toml` can include
`../../verify.toml` to add the project-wide checks to its own.

## Adopting it in a project

Declare the checks that the project's instructions already name as "the
tests", using the project's own commands and environment; do not invent new
coverage while adopting. Run `verify` once and fix or report each red check
before relying on it: a check that is always red trains agents to ignore the
whole report. A known, gap-tracked failure may stay red when it is reported
plainly. Gate a quick check behind `requires` or exit 69 only for a truly
optional prerequisite.

The checks a project's instructions name remain authoritative, including any
publish or CI gates; `verify` is how to run them, not a new policy about
which ones must pass.

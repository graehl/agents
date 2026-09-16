# Python tooling

Loaded before editing Python files or when first working in a Python
project (trigger: `AGENTS.global.md` § Language tooling).

Use `ruff check --fix` and `ruff format` (not black/isort/flake8),
trying `uvx ruff` first and plain `ruff` when uvx is absent. That pair is
also what the editor runs on save (import sort, `--fix`, then `format`),
so running it on an authored file — `AGENTS.global.md` § Auto-format
authored code — leaves nothing for the next save to change. Line length
comes from the repo's `ruff.toml`/`pyproject.toml`, else ruff's default
88; set it there rather than in editor arguments, or the two disagree.
Ruff walks `*.py` only, so name executables without that suffix explicitly
or the sweep silently skips them.

A narrowed `--select` makes `RUF100` lie: with the suppressed rule
deselected, the directive that suppresses it has nothing to suppress and
reports as unused. Before deleting a `# noqa`, re-run the check with the
named rule selected — and after deleting one, confirm the default check
still passes.

Add type hints to signatures. Prefer `uv` or `pixi` for environments. Avoid
`shell=True` with user-influenced content. Make device placement explicit
in ML code.

A mutable default value is shared, not per-call: `def f(xs=[])`, and
argparse `add_argument(..., action="append"/"extend", default=[])`, mutate
the one default object — for argparse this leaks values across parses
whenever a parser is reused in-process (the acli `--repl` loop reparses
per line). Use `default=None` and normalize inside; a deliberately shared
mutable default needs a comment saying it is intentional.

# Python tooling

Loaded before editing Python files or when first working in a Python
project (trigger: `AGENTS.global.md` § Language tooling).

Use `ruff check --fix` and `ruff format` (not black/isort/flake8),
trying `uvx ruff` first and plain `ruff` when uvx is absent. Add
type hints to signatures. Prefer `uv` or `pixi` for environments. Avoid
`shell=True` with user-influenced content. Make device placement explicit
in ML code.

A mutable default value is shared, not per-call: `def f(xs=[])`, and
argparse `add_argument(..., action="append"/"extend", default=[])`, mutate
the one default object — for argparse this leaks values across parses
whenever a parser is reused in-process (the acli `--repl` loop reparses
per line). Use `default=None` and normalize inside; a deliberately shared
mutable default needs a comment saying it is intentional.

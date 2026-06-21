# Python tooling

Loaded before editing Python files or when first working in a Python
project (trigger: `AGENTS.md` § Language tooling).

Use `ruff check --fix` and `ruff format` (not black/isort/flake8). Add
type hints to signatures. Prefer `uv` or `pixi` for environments. Avoid
`shell=True` with user-influenced content. Make device placement explicit
in ML code.

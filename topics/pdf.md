# PDF extraction

> Extract substantive papers to Markdown with marker-pdf in an isolated tool
> environment, keeping its large model stack out of project dependencies.

Topic: `pdf`

Use `marker-pdf`, not `pdftotext`, for substantive paper/PDF reading. Install
the OCR/ML stack in a dedicated environment, never the project's runtime
environment. This topic holds the gra host recipe routed by `AGENTS.user.md`.

## gra host recipe

Install or upgrade only when needed, under the normal dependency-change gate:

```bash
UV_PYTHON_PREFERENCE=only-managed uv tool install marker-pdf --python 3.12
uv tool upgrade marker-pdf
```

`UV_PYTHON_PREFERENCE=only-managed` selects a uv-managed CPython 3.12 rather
than the host's old system Python. The isolated environment is
`~/.local/share/uv/tools/marker-pdf`, with `marker_single`, `marker`, and
`marker_server` entry points under `~/.local/bin`.

The configured host recipe uses `~/.cache/datalab` for marker/surya weights
(roughly 3.3 GB), with `~/.cache` linked to `/scratch/graehl/.cache`; no extra
cache variables are needed for that arrangement. Verify those local paths
before relying on capacity, and use project-local cache/temp on other hosts
when needed.

```bash
marker_single paper.pdf --output_dir ./out
```

The output is `out/paper/paper.md` plus extracted images.

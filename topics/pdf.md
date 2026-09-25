# PDF extraction

> Extract PDFs to Markdown with marker-pdf in an isolated tool
> environment, keeping its large model stack out of project dependencies.

Topic: `pdf`
Governs: reading or extracting a PDF

Use `marker-pdf`, not `pdftotext`, for PDF reading. Install
the OCR/ML stack in a dedicated environment, never the project's runtime
environment. This topic holds the gra host recipe routed by `AGENTS.user.md`.

One scoped exception: tools that compute statistics over prose, such as
`not-ai-lint` through `prose_text`, read PDFs with `pdftotext`. Word and
phrase rates tolerate layout loss that would mislead a reader, and those
tools print that caveat with their results. Reading a paper for its content
still goes through marker-pdf.

## gra host recipe

Install or upgrade only when needed, under the normal dependency-change gate:

```bash
UV_PYTHON_PREFERENCE=only-managed uv tool install 'marker-pdf<2' --python 3.12
```

Keep the `<2` pin (installed: 1.10.2). marker 2.0 moved OCR into an
inference server: on an NVIDIA host surya spawns a vLLM Docker container,
which fails here because the account is not in the `docker` group, and its
alternative needs a separately installed `llama-server`. 1.x runs its torch
models in-process. Lift the pin only after deciding which server route to
support. `UV_PYTHON_PREFERENCE=only-managed` selects a uv-managed CPython
3.12 rather than the host's old system Python.

marker uses the GPU by default and fails with CUDA out-of-memory when
another job holds it. Check `nvidia-smi` first; under contention, run with
`TORCH_DEVICE=cpu`, which works but took about 50 minutes for a 26-page
paper on gra (2026-09-25). The isolated environment is
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

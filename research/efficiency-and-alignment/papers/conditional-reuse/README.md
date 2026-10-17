# Conditional reuse and the limits of efficiency as an alignment signal

Owning program: [../../PROGRAM.md](../../PROGRAM.md). Proposal card: [../../paper-proposals.md#conditional-reuse](../../paper-proposals.md#conditional-reuse).
Short theoretical paper for readers with master's-level computer science or
mathematics training. The source is the ordered Quarto fragments. Scalar
simulations check the proofs; no neural experiment or submission is planned.

## Layout

- `index.qmd`: root; front matter and the ordered `{{< include >}}` list.
- `sections/_NN-name.qmd`: one fragment per section.
- `related-work/papers.bib`: bibliography; `figures/`: generated figures and
  their scripts.
- `CHANGELOG.md`: one entry per release, never rendered.

## Build

```bash
~/agents/scripts/qmd-html --config qmd-html.json
```

This produces `_build/index.html`, `_build/index.pdf` (US Letter, browser
print), a source map, and a receipt with hashes and the renderer version.
The initial render used Quarto 1.9.38 and the existing Playwright installation
resolved by the shared builder. The program dashboard links these outputs;
the repository's App declaration serves it through the common repository view.

The citation support is in `related-work/retrieval.md`; the exact gate count,
sampling argument, and numeric check are recorded beside the bound in
`sections/_20-bound.repro.md`.

Optimizer-memory proofs, their finite numerical checks, and exclusions are in
`sections/_37-optimizer-memory.repro.md`; run `checks/optimizer_memory.py`
with standard-library Python. The program's local theorem-development pilot
is specified in [../../topics/theorem-development.md](../../topics/theorem-development.md).

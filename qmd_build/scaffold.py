"""Scaffold a Quarto paper project inside its owning research program.

`paper-new <program-dir> <slug> --title ...` creates `<program-dir>/papers/<slug>/` from
`templates/paper/`: root `index.qmd` with ordered section includes, `_quarto.yml` (US Letter,
pdfLaTeX, kept TeX for arXiv), bibliography, changelog, qmd-html config and README. It refuses
to overwrite, and refuses a program directory without `PROGRAM.md`, because placement under
the owning program is part of the process (topics/paper-projects.md).
"""

from __future__ import annotations

import datetime
import os
import shutil
from pathlib import Path

import acli

TEMPLATE = Path(__file__).resolve().parent / "templates" / "paper"
PLACEHOLDERS = ("title", "date", "program", "proposal")


def scaffold(program: Path, slug: str, title: str, proposal: str | None) -> dict:
    program = program.resolve()
    if not (program / "PROGRAM.md").is_file():
        raise ValueError(
            f"No PROGRAM.md in {program}: place the paper under its owning program"
        )
    if (
        not slug
        or slug != slug.lower()
        or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in slug)
    ):
        raise ValueError(
            f"Slug must be lowercase letters, digits and hyphens: {slug!r}"
        )
    paper = program / "papers" / slug
    if paper.exists():
        raise ValueError(f"Paper directory exists: {paper}")
    shutil.copytree(TEMPLATE, paper)
    (paper / "figures").mkdir(exist_ok=True)
    values = {
        "title": title,
        "date": datetime.date.today().isoformat(),
        "program": os.path.relpath(program / "PROGRAM.md", paper),
        "proposal": proposal
        or os.path.relpath(program / "paper-proposals.md", paper) + f"#{slug}",
    }
    written = []
    for path in sorted(p for p in paper.rglob("*") if p.is_file()):
        text = path.read_text(encoding="utf-8")
        for key in PLACEHOLDERS:
            text = text.replace("{{" + key + "}}", values[key])
        path.write_text(text, encoding="utf-8")
        written.append(str(path.relative_to(paper)))
    return {
        "paper": str(paper),
        "files": written,
        **{k: values[k] for k in ("title", "date")},
    }


def main(argv=None) -> int:
    cli = acli.argument_parser(
        prog="paper-new",
        description=__doc__,
        capabilities=("complete",),
        exit_codes={0: "scaffolded", 2: "refused or failed"},
    )
    cli.add_argument(
        "program", type=Path, help="Owning program directory (contains PROGRAM.md)"
    )
    cli.add_argument("slug", help="Paper directory name under <program>/papers/")
    cli.add_argument("--title", required=True)
    cli.add_argument(
        "--proposal",
        help="Link to the proposal card (default: paper-proposals.md#<slug>)",
    )
    acli.add_standard_args(cli)
    acli.maybe_complete(cli, None if argv is None else [cli.prog, *argv])
    args = cli.parse_args(argv)
    try:
        result = scaffold(args.program, args.slug, args.title, args.proposal)
    except (OSError, ValueError) as error:
        acli.die(str(error), 2)
    acli.emit(result, acli.resolve_format(args), text=f"Paper: {result['paper']}")
    return 0

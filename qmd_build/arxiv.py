"""Build an arXiv source bundle from a Quarto paper and prove it compiles cleanly.

`qmd-arxiv <paper-dir>` renders the root `index.qmd` to PDF with the paper's own `_quarto.yml`
(keep-tex, pdfLaTeX, US Letter in papers scaffolded by `paper-new`), copies the kept TeX and
every `\\includegraphics` file into a flat bundle, rejects host paths and hidden files, then
compiles the bundle twice with pdflatex in an empty directory, as arXiv will. Outputs under
`<paper-dir>/_build/arxiv/`: `src/` (the bundle), `arxiv-source.zip`, `check.pdf` (the clean
compile), `render.log` (Quarto's output) and `receipt.json`. The receipt warns when the TeX has
no abstract environment or the abstract exceeds arXiv's length limit. Advice and known arXiv limits: topics/arxiv-submission.md.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

import acli

from .manuscript import default_tex_bin

ARXIV_ABSTRACT_LIMIT = 1920  # characters, https://info.arxiv.org/help/prep.html
HOST_PATH = re.compile(r"(?<![\w.])/(home|local|gr6|scratch|tmp|Users)/")
GRAPHICS = re.compile(r"(\\includegraphics(?:\[[^\]]*\])?)\{([^}]+)\}")
IMAGE_EXTENSIONS = ("", ".pdf", ".png", ".jpg", ".jpeg", ".eps")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_image(name: str, base: Path) -> Path:
    for extension in IMAGE_EXTENSIONS:
        candidate = (base / (name + extension)).resolve()
        if candidate.is_file():
            return candidate
    raise ValueError(
        f"Figure not found for \\includegraphics{{{name}}} (relative to {base})"
    )


def bundle(paper: Path, quarto: str) -> dict:
    paper = paper.resolve()
    root = paper / "index.qmd"
    if not root.is_file():
        raise ValueError(f"No index.qmd in {paper}")
    out = paper / "_build" / "arxiv"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    render_log = out / "render.log"
    with render_log.open("w") as log_file:
        rendered = subprocess.run(
            [quarto, "render", str(root), "--to", "pdf", "-M", "keep-tex:true"],
            cwd=paper,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            check=False,  # a failed render is reported with its log below
        )
    if rendered.returncode:
        raise ValueError(f"Quarto render failed; log: {render_log}")
    tex_path = paper / "index.tex"
    if not tex_path.is_file():
        raise ValueError("Quarto kept no index.tex; set keep-tex in _quarto.yml")
    tex = tex_path.read_text(encoding="utf-8")
    engine = re.search(
        r"^\s*pdf-engine:\s*(\S+)", (paper / "_quarto.yml").read_text(), re.MULTILINE
    )
    if engine and engine.group(1) != "pdflatex":
        raise ValueError(f"pdf-engine {engine.group(1)}: arXiv documents only pdfLaTeX")
    src = out / "src"
    (src / "figures").mkdir(parents=True)
    copied: dict[Path, str] = {}

    def relink(match: re.Match) -> str:
        image = find_image(match.group(2), paper)
        if image not in copied:
            name = image.name
            stem, n = image.stem, 1
            while name in copied.values() or (src / "figures" / name).exists():
                name = f"{stem}-{n}{image.suffix}"
                n += 1
            shutil.copy2(image, src / "figures" / name)
            copied[image] = name
        return f"{match.group(1)}{{figures/{copied[image]}}}"

    tex = GRAPHICS.sub(relink, tex)
    if HOST_PATH.search(tex):
        raise ValueError(
            f"Bundle TeX still names a host path: {HOST_PATH.search(tex).group(0)}"
        )
    (src / "main.tex").write_text(tex, encoding="utf-8")
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.DOTALL)
    abstract_chars = len(" ".join(abstract.group(1).split())) if abstract else None
    with tempfile.TemporaryDirectory(prefix="arxiv-check-") as scratch:
        work = Path(scratch) / "src"
        shutil.copytree(src, work)
        for _ in range(2):
            result = subprocess.run(
                [
                    str(default_tex_bin("pdflatex") / "pdflatex"),
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "main.tex",
                ],
                cwd=work,
                capture_output=True,
                text=True,
                check=False,  # a failed compile is reported with its log below
            )
            if result.returncode:
                (out / "check.log").write_text(result.stdout)
                raise ValueError(
                    f"Clean pdflatex compile failed; log: {out / 'check.log'}"
                )
        shutil.copy2(work / "main.pdf", out / "check.pdf")
        log = (work / "main.log").read_text(errors="replace")
    info = subprocess.run(
        ["pdfinfo", str(out / "check.pdf")], capture_output=True, text=True, check=True
    ).stdout
    size = re.search(r"Page size:\s*([\d.]+) x ([\d.]+)", info)
    pages = re.search(r"Pages:\s*(\d+)", info)
    letter = (
        bool(size)
        and abs(float(size.group(1)) - 612) < 2
        and abs(float(size.group(2)) - 792) < 2
    )
    files = sorted(p for p in src.rglob("*") if p.is_file())
    if any(part.startswith(".") for p in files for part in p.relative_to(src).parts):
        raise ValueError("Bundle contains hidden files, which arXiv deletes")
    archive = out / "arxiv-source.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, path.relative_to(src))
    warnings = []
    if abstract_chars is None:
        warnings.append(
            "no LaTeX abstract environment; set `abstract:` in the root front matter"
        )
    elif abstract_chars > ARXIV_ABSTRACT_LIMIT:
        warnings.append(
            f"abstract is {abstract_chars} characters; arXiv accepts at most {ARXIV_ABSTRACT_LIMIT}"
        )
    if not letter:
        warnings.append("check.pdf is not US Letter")
    if re.search(
        r"There were undefined (references|citations)|Citation .* undefined", log
    ):
        warnings.append("LaTeX reports undefined references or citations")
    receipt = {
        "schema": "qmd-arxiv/v1",
        "paper": str(paper),
        "archive": str(archive),
        "archive_sha256": sha256(archive),
        "files": {str(p.relative_to(src)): sha256(p) for p in files},
        "check_pdf": str(out / "check.pdf"),
        "pages": int(pages.group(1)) if pages else None,
        "us_letter": letter,
        "abstract_characters": abstract_chars,
        "warnings": warnings,
    }
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt


def main(argv=None) -> int:
    cli = acli.argument_parser(
        prog="qmd-arxiv",
        description=__doc__,
        capabilities=("complete",),
        exit_codes={0: "bundle built and compiled cleanly", 2: "build or check failed"},
    )
    cli.add_argument(
        "paper", type=Path, help="Paper directory holding index.qmd and _quarto.yml"
    )
    cli.add_argument("--quarto", default="quarto")
    acli.add_standard_args(cli)
    acli.maybe_complete(cli, None if argv is None else [cli.prog, *argv])
    args = cli.parse_args(argv)
    try:
        receipt = bundle(args.paper, args.quarto)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        acli.die(str(error), 2)
    text = f"Bundle: {receipt['archive']} ({receipt['pages']} pages)" + "".join(
        f"\nwarning: {w}" for w in receipt["warnings"]
    )
    acli.emit(receipt, acli.resolve_format(args), text=text)
    return 0

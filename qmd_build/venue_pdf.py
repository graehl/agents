"""Build a venue-style LaTeX PDF from a Quarto manuscript and measure its length.

The root .qmd's include directives order the section fragments. The build
stages one assembled .qmd (abstract as metadata, main body, back matter,
references, appendices), renders it through Quarto with the configured venue
template, filters and style files, then reads the shipped page of each part
from TeX's own labels. Blocking and CPU-only; a changed build takes as long
as TeX needs (tens of seconds for a long paper), an unchanged one reuses a
hash-checked receipt. Config keys and their defaults:
topics/document-writing-printable.md § Scripted venue build.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from glob import glob
from pathlib import Path

import acli

from .estimate import estimate, image_sources, load_cache, save_cache, section_blocks
from .manuscript import (
    Config,
    digest,
    front_matter,
    includes,
    print_asset,
    resolve_executable,
    root_document,
)
from .source_map import manuscript_source_targets, marked_source, targets_for

PACKAGE = Path(__file__).resolve().parent
MEASURE_TEX = PACKAGE / "measure.tex"
KEYS = {
    "comment",
    "root",
    "output",
    "jobname",
    "title",
    "template",
    "filters",
    "style-files",
    "inputs",
    "bibliography",
    "bibliography-style",
    "cite-method",
    "abstract",
    "back-matter",
    "appendices",
    "resource-path",
    "columns",
    "max-pages",
    "measure",
    "pdf-engine",
    "tex-bin",
    "metadata",
    "format",
    "source-targets-env",
    "fonts",
    "estimate",
    "log-failures",
}
ESTIMATE_DEFAULTS = {
    "char-advance-pt": 5.0,
    "image-height-in": None,
    "title-columns": 0.4,
}
LOG_FAILURES = ["Missing character:", "Float too large", "undefined references"]
FONT_STYLES = ["Regular", "Bold", "Italic", "Bold Italic"]


@dataclass
class VenueBuild:
    config: Config
    root: Path
    names: list[str]
    abstract: str | None
    back_matter: list[str]
    appendices: list[str]
    resource_dirs: list[Path]
    output: Path
    jobname: str
    quarto: str
    columns: int
    float_columns: int
    settings: dict
    model_inputs: list[Path]

    def section(self, name: str) -> Path:
        return self.root.parent / name

    @property
    def main(self) -> list[Path]:
        excluded = set(self.back_matter) | set(self.appendices)
        return [self.section(name) for name in self.names if name not in excluded]


def configure(args) -> VenueBuild:
    config = Config.load(args.config, KEYS)
    root = root_document(config, args.root)
    names = includes(root)
    abstract = config.get("abstract")
    back_matter = list(config.get("back-matter", []))
    appendices = list(config.get("appendices", []))
    for name in [abstract, *back_matter, *appendices]:
        if name is not None and name not in names:
            raise ValueError(
                f"Configured section is not included by {root.name}: {name}"
            )
    if abstract in back_matter + appendices or set(back_matter) & set(appendices):
        raise ValueError(
            "A section may play only one of abstract, back-matter, or appendix roles"
        )
    output = (
        args.output or config.path("output") or root.parent / "_build" / "venue-pdf"
    )
    output = output.resolve()
    columns = int(config.get("columns", 1))
    if columns not in (1, 2):
        raise ValueError("`columns` must be 1 or 2")
    pdf_format = config.get("format", {})
    settings = {**ESTIMATE_DEFAULTS, **config.get("estimate", {})}
    unknown = set(settings) - set(ESTIMATE_DEFAULTS) - {"float-columns"}
    if unknown:
        raise ValueError(f"Unknown estimate settings: {sorted(unknown)}")
    float_columns = int(
        settings.pop(
            "float-columns", columns if pdf_format.get("fig-env") == "figure*" else 1
        )
    )
    resource_dirs = config.paths("resource-path") or [root.parent]
    adapter = [
        config.path("template"),
        *config.paths("filters"),
        *config.paths("style-files"),
    ]
    return VenueBuild(
        config=config,
        root=root,
        names=names,
        abstract=abstract,
        back_matter=back_matter,
        appendices=appendices,
        resource_dirs=resource_dirs,
        output=output,
        jobname=config.get("jobname", "paper"),
        quarto=resolve_executable(args.quarto),
        columns=columns,
        float_columns=float_columns,
        settings=settings,
        model_inputs=[
            path for path in [Path(__file__).with_name("estimate.py"), *adapter] if path
        ],
    )


def page_measurement(output: Path, jobname: str, columns: int) -> dict:
    """Shipped pages per part and the occupied fraction of the last text column."""
    aux = (output / f"{jobname}.aux").read_text()

    def page(label, required=True):
        match = re.search(r"\\newlabel\{" + label + r"\}\{\{[^}]*\}\{(\d+)\}", aux)
        if not match:
            if required:
                raise ValueError(f"Missing shipped-page label: {label}")
            return None
        return int(match[1])

    physical = page("qmd-back-matter-start") - 1
    text_page = page("qmd-main-text-end")
    pos = re.search(
        r"\\zref@newlabel\{qmd-main-end-position\}\{\\posx\{(\d+)\}\\posy\{(\d+)\}", aux
    )
    if not pos:
        raise ValueError("Missing final-column position")
    x, y = map(int, pos.groups())
    layout = dict(
        line.split("=")
        for line in (output / f"{jobname}.layout").read_text().splitlines()
    )
    layout = {key: int(value) for key, value in layout.items()}
    column = int(
        (x - layout["left"] + layout["gap"] / 2) // (layout["column"] + layout["gap"])
    )
    column = min(columns - 1, max(0, column))
    fraction = (layout["top"] - y + layout["baseline"] / 2) / layout["height"]
    if not -0.05 <= fraction <= 1.05:
        raise ValueError(f"Final position outside text area: {fraction}")
    fraction = min(1.0, max(0.0, fraction))
    measured = text_page - 1 + (column + fraction) / columns
    # Float-only pages after the last paragraph must never disappear from the check.
    basis = "final text column; preceding physical pages counted in full"
    if text_page < physical:
        measured = float(physical)
        basis = "conservative whole-page count: trailing main-body floats"
    return {
        "main_pages": physical,
        "main_fractional_pages": round(measured, 3),
        "fraction_basis": basis,
        "last_text_column": column,
        "last_column_fraction": round(fraction, 3),
        "text_end_page": text_page,
        "back_matter_start": page("qmd-back-matter-start"),
        "references_start": page("qmd-references-start"),
        "appendices_start": page("qmd-appendices-start", required=False),
    }


def tex_bin(build: VenueBuild, engine: str) -> Path:
    configured = build.config.path("tex-bin")
    if configured:
        return configured
    # Quarto prefers its TinyTeX installation over a system TeX.
    tinytex = sorted(glob(str(Path.home() / ".TinyTeX/bin/*")))
    if tinytex:
        return Path(tinytex[0])
    return Path(resolve_executable(engine)).parent


def identity(build: VenueBuild, inputs: list[Path], engine: str) -> dict:
    fonts = {}
    font_config = build.config.get("fonts", {})
    for family in font_config.get("families", []):
        for style in font_config.get("styles", FONT_STYLES):
            path = Path(
                subprocess.check_output(
                    ["fc-match", "-f", "%{file}", f"{family}:style={style}"], text=True
                )
            )
            fonts[str(path)] = digest(path)
    for pattern in font_config.get("files", []):
        for name in sorted(glob(str(build.config.base / pattern))):
            fonts[name] = digest(Path(name))
    binary = tex_bin(build, engine)
    texmf = subprocess.check_output(
        [str(binary / "kpsewhich"), "-var-value=TEXMFROOT"], text=True
    ).strip()
    tlpdb = Path(texmf) / "tlpkg/texlive.tlpdb"
    return {
        "inputs": {str(path): digest(path) for path in sorted(set(inputs))},
        "fonts": fonts,
        "versions": {
            "quarto": subprocess.check_output(
                [build.quarto, "--version"], text=True
            ).strip(),
            engine: subprocess.check_output(
                [str(binary / engine), "--version"], text=True
            ).splitlines()[0],
        },
        "tex_packages": digest(tlpdb) if tlpdb.is_file() else None,
        "tlpdb": str(tlpdb) if tlpdb.is_file() else None,
    }


def section_text(
    build: VenueBuild, name: str, targets: list[dict], links: dict[str, str]
) -> str:
    path = build.section(name)
    text = marked_source(path.read_text(), targets_for(path, targets, build.output))
    for source, relative in links.items():
        replacement = "](" + relative
        text = re.sub(
            r"\]\(" + re.escape(source) + r"(?=[\s)])",
            lambda _, new=replacement: new,
            text,
        )
    return text


def assemble(
    build: VenueBuild, targets: list[dict], links: dict[str, str]
) -> tuple[dict, str]:
    config = build.config
    title = config.get("title") or front_matter(build.root, "title")
    if not title:
        raise ValueError("No title: set config `title` or the root's front matter")
    bibliography = config.path("bibliography")
    if bibliography is None and front_matter(build.root, "bibliography"):
        bibliography = (
            build.root.parent / front_matter(build.root, "bibliography")
        ).resolve()
    cite_method = config.get("cite-method", "citeproc")
    if cite_method not in ("citeproc", "natbib", "biblatex"):
        raise ValueError("`cite-method` must be citeproc, natbib, or biblatex")
    metadata = {
        "title": title,
        "toc": False,
        "number-sections": True,
        "shift-heading-level-by": -1,
        "cite-method": cite_method,
        "filters": [
            {"path": str(path), "at": "pre-ast"} for path in config.paths("filters")
        ],
    }
    # natbib output places its own \bibliography at the references boundary.
    if bibliography and cite_method != "natbib":
        metadata["bibliography"] = str(bibliography)
    pdf = {
        "pdf-engine": config.get("pdf-engine", "xelatex"),
        "keep-tex": True,
        "latex-clean": False,
        "default-image-extension": "pdf",
    }
    if config.path("template"):
        pdf["template"] = str(config.path("template"))
    if config.get("measure", "inject") == "inject":
        metadata["header-includes"] = [f"\\input{{{MEASURE_TEX}}}"]
    elif config.get("measure") != "template":
        raise ValueError("`measure` must be inject or template")
    pdf.update(config.get("format", {}))
    metadata["format"] = {"pdf": pdf}
    metadata.update(config.get("metadata", {}))
    sections = {name: section_text(build, name, targets, links) for name in build.names}
    if build.abstract:
        abstract = re.sub(
            r"<!--.*?-->", "", sections.pop(build.abstract), flags=re.DOTALL
        )
        metadata["abstract"] = re.sub(
            r"^\s*#{1,6}\s.*\n", "", abstract, count=1
        ).strip()
    back = [sections.pop(name) for name in build.back_matter]
    appendices = [sections.pop(name) for name in build.appendices]
    # Boundaries are labels, so the aux file reports actual shipped pages.
    body = "\n\n".join(sections.values())
    body += (
        "\n\n\\zsavepos{qmd-main-end-position}\\label{qmd-main-text-end}\n\\clearpage\n"
    )
    body += "\\label{qmd-back-matter-start}\n\n" + "\n\n".join(back)
    body += "\n\n\\clearpage\n\\label{qmd-references-start}\n"
    if bibliography and cite_method == "natbib":
        if config.get("bibliography-style"):
            body += "\\bibliographystyle{" + config.get("bibliography-style") + "}\n"
        body += "\\bibliography{" + str(bibliography.with_suffix("")) + "}\n"
    elif bibliography and cite_method == "biblatex":
        body += "\\printbibliography\n"
    elif bibliography:
        body += "\n::: {#refs}\n:::\n"
    if appendices:
        body += (
            "\n\\clearpage\n\\appendix\n\\label{qmd-appendices-start}\n\n"
            + "\n\n".join(appendices)
        )
    return metadata, body


def report(build: VenueBuild, receipt: dict, args) -> int:
    pages = receipt["pages"]
    limit = args.max_pages
    result = {
        "pdf": receipt["pdf"],
        **pages,
        "limit": limit,
        "over_budget": None
        if limit is None
        else round(max(0, pages["main_fractional_pages"] - limit), 3),
        "fits": None if limit is None else pages["main_pages"] <= limit,
        "cached": receipt.get("cached", False),
        "build_seconds": round(receipt["build_seconds"], 3),
    }
    over = (
        ""
        if limit is None
        else f", limit {limit:g}; over by {result['over_budget']:.2f}"
    )
    text = (
        f"Main body: {pages['main_fractional_pages']:.2f} estimated pages "
        f"({pages['main_pages']} physical){over}. "
        f"{'Cached' if result['cached'] else 'Built'} in {receipt['build_seconds']:.1f}s.\n"
        f"PDF: {receipt['pdf']}"
    )
    acli.emit(
        result, acli.resolve_format(args), text=text, commentary=not args.no_commentary
    )
    return 3 if args.enforce_limit and limit is not None and not result["fits"] else 0


def report_estimate(quick: dict, args) -> None:
    limit = (
        ""
        if args.max_pages is None
        else f"; limit {args.max_pages:g}; over by {quick['over_budget']:.2f}"
    )
    lines = [
        f"Fast estimate: {quick['estimated_pages']:.2f} main pages{limit} ({quick['seconds']:.2f}s).",
        (
            f"Text: {quick['words']:,} words / {quick['characters']:,} characters; "
            f"text + tables {quick['text_and_table_pages']:.2f} pages; "
            f"figures {quick['figure_pages']:.2f}; title {quick['title_pages']:.2f}."
        ),
        (
            f"Figures: {len(quick['figures'])}, {sum(f['cached'] for f in quick['figures'])} cached; "
            f"calibrated to full build: {quick['calibrated']}."
        ),
        *(
            f"  {Path(figure['figure']).name}: {figure['height_pt']:.0f}pt high across "
            f"{figure['width_columns']} columns = {figure['column_heights']:.2f} column-heights"
            for figure in quick["figures"]
        ),
        quick["caveat"],
    ]
    acli.emit(
        quick,
        acli.resolve_format(args),
        text="\n".join(lines),
        commentary=not args.no_commentary,
    )


def build_pdf(build: VenueBuild, args, started: float) -> int:
    config = build.config
    output = build.output
    output.mkdir(parents=True, exist_ok=True)
    engine = config.get("pdf-engine", "xelatex")
    sections = [build.section(name) for name in build.names]
    # Every section's figures, not only the main body's, must exist as print assets.
    cache = load_cache(output)
    links = {}
    for path in sections:
        for source in image_sources(section_blocks(path, build.quarto, cache)):
            asset = print_asset(source, build.resource_dirs)
            if asset is None:
                raise ValueError(f"Missing print figure for {source} in {path}")
            links[source] = asset
    save_cache(output, cache)
    bibliography = config.path("bibliography")
    inputs = [
        build.root,
        *sections,
        *links.values(),
        *build.model_inputs,
        *config.paths("inputs"),
        *sorted(PACKAGE.glob("*.py")),
        MEASURE_TEX,
    ]
    inputs += [path for path in (config.source, bibliography) if path]
    current = identity(build, inputs, engine)
    receipt_path = output / "receipt.json"
    if not args.force and receipt_path.exists():
        old = json.loads(receipt_path.read_text())
        outputs = old.get("outputs") or {}
        if (
            old.get("identity") == current
            and outputs
            and all(
                (output / name).is_file() and digest(output / name) == sha
                for name, sha in outputs.items()
            )
        ):
            estimate(build, calibrate_pages=old["pages"]["main_fractional_pages"])
            old["cached"] = True
            old["build_seconds"] = time.monotonic() - started
            return report(build, old, args)
    targets = manuscript_source_targets(sections, build.quarto, output)
    relative_links = {
        source: os.path.relpath(asset, output) for source, asset in links.items()
    }
    metadata, body = assemble(build, targets, relative_links)
    staged = output / f"{build.jobname}.qmd"
    targets_path = output / f"{build.jobname}.sources.json"
    targets_path.write_text(json.dumps(targets, indent=2) + "\n")
    staged.write_text(
        "---\n" + json.dumps(metadata, ensure_ascii=False) + "\n---\n\n" + body
    )
    for path in config.paths("style-files"):
        shutil.copy2(path, output / path.name)
    env = {
        **os.environ,
        "TEXINPUTS": str(output) + os.pathsep + os.environ.get("TEXINPUTS", ""),
        "BSTINPUTS": str(output) + os.pathsep + os.environ.get("BSTINPUTS", ""),
        "QMD_SOURCE_TARGETS": str(targets_path),
    }
    for name in config.get("source-targets-env", []):
        env[name] = str(targets_path)
    with (
        (output / "build.stdout.log").open("w") as stdout,
        (output / "build.stderr.log").open("w") as stderr,
    ):
        subprocess.run(
            [build.quarto, "render", staged.name, "--to", "pdf"],
            cwd=output,
            env=env,
            stdout=stdout,
            stderr=stderr,
            check=True,
        )
    if current["inputs"] != {name: digest(Path(name)) for name in current["inputs"]}:
        raise ValueError("Source or figure changed while building")
    log = (output / f"{build.jobname}.log").read_text(errors="replace")
    failures = [
        marker for marker in config.get("log-failures", LOG_FAILURES) if marker in log
    ]
    if failures:
        raise ValueError(
            f"TeX log reports {failures}; inspect {output / (build.jobname + '.log')}"
        )
    measurement = page_measurement(output, build.jobname, build.columns)
    pdf = output / f"{build.jobname}.pdf"
    info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
    measurement["total_pages"] = int(
        re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)[1]
    )
    estimate(build, calibrate_pages=measurement["main_fractional_pages"])
    # Quarto may install required TeX packages during a successful first build.
    current = identity(build, inputs, engine)
    receipt = {
        "schema": "qmd-venue-pdf/v1",
        "root": str(build.root),
        "sections": build.names,
        "identity": current,
        "pages": measurement,
        "pdf": str(pdf),
        "outputs": {
            name: digest(output / name)
            for name in (
                f"{build.jobname}.pdf",
                f"{build.jobname}.tex",
                f"{build.jobname}.sources.json",
                f"{build.jobname}.aux",
                f"{build.jobname}.layout",
                f"{build.jobname}.images",
            )
        },
        "build_seconds": time.monotonic() - started,
        "scope": "Main body through the last main section; back matter, references and appendices excluded",
    }
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    return report(build, receipt, args)


def parser():
    parser = acli.argument_parser(
        prog="qmd-venue-pdf",
        description=__doc__,
        capabilities=("complete",),
        exit_codes={0: "measured", 2: "build/check failed", 3: "over page limit"},
    )
    parser.add_argument(
        "root", nargs="?", type=Path, help="Root .qmd (else config `root`)"
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="JSON build config; relative paths resolve against its directory",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Build directory (else config `output`, else _build/venue-pdf)",
    )
    parser.add_argument("--quarto", default="quarto")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Rebuild even when input/output hashes match",
    )
    parser.add_argument(
        "--max-pages", type=float, help="Main-body page limit (else config `max-pages`)"
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--estimate",
        action="store_true",
        help="Estimate from text and cached figure heights without TeX",
    )
    mode.add_argument(
        "--fail-fast",
        action="store_true",
        help="Exit 3 before TeX when the fast estimate exceeds --max-pages",
    )
    parser.add_argument(
        "--enforce-limit",
        action="store_true",
        help="Exit 3 if physical main-body pages exceed the limit",
    )
    acli.add_standard_args(parser)
    return parser


def main(argv=None) -> int:
    cli = parser()
    acli.maybe_complete(cli, None if argv is None else [cli.prog, *argv])
    args = cli.parse_args(argv)
    build = None
    try:
        build = configure(args)
        if args.max_pages is None:
            args.max_pages = build.config.get("max-pages")
        if args.max_pages is not None and not 0 < args.max_pages < float("inf"):
            cli.error("--max-pages must be finite and positive")
        if args.fail_fast and args.max_pages is None:
            cli.error("--fail-fast needs a page limit")
        started = time.monotonic()
        if args.estimate or args.fail_fast:
            quick = estimate(build)
            quick["seconds"] = round(time.monotonic() - started, 3)
            quick["limit"] = args.max_pages
            over = False
            if args.max_pages is not None:
                quick["over_budget"] = round(
                    max(0, quick["estimated_pages"] - args.max_pages), 3
                )
                over = quick["estimated_pages"] > args.max_pages
            report_estimate(quick, args)
            if over and (args.fail_fast or args.enforce_limit):
                return 3
            if args.estimate:
                return 0
        return build_pdf(build, args, started)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        where = (
            f"; build diagnostics: {build.output / 'build.stderr.log'}" if build else ""
        )
        acli.die(f"{error}{where}", 2)

"""Render a Quarto manuscript as one static HTML artifact with a build receipt.

Renders an isolated sibling copy of the document directory, so a render never
writes intermediates or partial output beside the canonical sources. The HTML
embeds its resources, carries section/paragraph/figure source targets unless
`--no-source-map` (`ya-source-target:v1` comments plus a `.map` sidecar), and
records a `ya-artifact:v1` regenerate command. `--print-pdf` adds a browser-print PDF.
Blocking and CPU-only; normally under a minute. Config keys:
topics/document-writing-browser-interactive.md § Scripted HTML build.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import acli

from .browser_print import DEFAULT_PLAYWRIGHT
from .browser_print import print_pdf as print_html_pdf
from .manuscript import (
    Config,
    first_heading_text,
    fragment_anchors,
    front_matter,
    includes,
    resolve_executable,
    root_document,
)
from .source_map import (
    image_source_targets,
    manuscript_source_targets,
    source_mapped_html,
    staged_sources,
)
from .styles import STYLES, document_style, style_inputs, style_render_arguments
from .table_layout import band_stylesheet, choose_table_widths, widest_band_widths

PACKAGE = Path(__file__).resolve().parent
SCRIPT = PACKAGE.parent / "scripts/qmd-html"
KEYS = {
    "comment",
    "root",
    "output",
    "hook",
    "inputs",
    "must-contain",
    "quarto-version",
    "print-pdf",
    "print",
    "playwright-from",
    "timeout-seconds",
    "style",
}


def identity(path: Path, base: Path) -> dict:
    return {
        "path": os.path.relpath(path, base),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def quarto_facts(root: Path, quarto: str) -> dict:
    """Output path, resource directories and image extension Quarto will use."""
    inspected = json.loads(
        subprocess.check_output([quarto, "inspect", str(root)], text=True)
    )
    pandoc = inspected["formats"]["html"]["pandoc"]
    project = inspected.get("project")
    home = root.parent
    if project:
        if Path(project["dir"]).resolve() != home:
            raise ValueError(
                f"Root must sit at its Quarto project directory: {project['dir']}"
            )
        project_config = project["config"]
        output_dir = home / project_config.get("project", {}).get("output-dir", ".")
        resources = [home / path for path in project_config.get("resource-path", ["."])]
    else:
        output_dir, resources = home, [home]
    return {
        "output": (
            output_dir / pandoc.get("output-file", root.stem + ".html")
        ).resolve(),
        "resources": [path.resolve() for path in resources],
        "extension": pandoc.get("default-image-extension", "png"),
    }


def render(args, config: Config) -> dict:
    quarto = resolve_executable(args.quarto)
    root = root_document(config, args.root)
    home = root.parent
    version = subprocess.check_output([quarto, "--version"], text=True).strip()
    pinned = config.get("quarto-version")
    if pinned and version != pinned:
        raise ValueError(f"Expected Quarto {pinned}, found {version}")
    facts = quarto_facts(root, quarto)
    output = (
        args.output.resolve()
        if args.output
        else config.path("output") or facts["output"]
    )
    source_map = not args.no_source_map
    sections = [home / name for name in includes(root, required=False)]
    # A root without includes is itself the one source-mapped section.
    fragments = sections or [root]
    style_name = args.style or config.get("style")
    style = document_style(style_name) if style_name else None
    sources = [
        root,
        *sections,
        *config.paths("inputs"),
        *sorted(PACKAGE.glob("*.py")),
        *sorted(PACKAGE.glob("*.lua")),
        *sorted(PACKAGE.glob("*.js")),
        *sorted(PACKAGE.glob("*.mjs")),
        *(style_inputs(style) if style else []),
    ]
    for extra in (home / "_quarto.yml", config.source):
        if extra and extra.is_file():
            sources.append(extra)
    bibliography = front_matter(root, "bibliography")
    if bibliography:
        sources.append(home / bibliography)
    before = [identity(path, home) for path in sources]
    targets = (
        manuscript_source_targets(fragments, quarto, output.parent)
        if source_map
        else []
    )
    rendered = facts["output"]
    output.parent.mkdir(parents=True, exist_ok=True)
    log_path = output.with_suffix(".render.log")
    skip = {".quarto", "_freeze"}
    if rendered.parent != home:
        skip.add(rendered.relative_to(home).parts[0])
    with (
        tempfile.TemporaryDirectory(prefix="qmd-html-") as scratch,
        staged_sources(root, fragments, targets, output.parent, skip) as staged_root,
    ):
        work = Path(scratch)
        staged_targets = work / "source-targets.json"
        staged_targets.write_text(json.dumps(targets))
        anchors = work / "fragment-anchors.json"
        anchors.write_text(json.dumps(fragment_anchors(sections, quarto)))
        # The staged directory is discarded, so the artifact must be one file.
        command = [
            quarto,
            "render",
            staged_root.name,
            "--to",
            "html",
            "--embed-resources",
            "--lua-filter",
            str(PACKAGE / "included_documents.lua"),
        ]
        if source_map:
            command += ["--lua-filter", str(PACKAGE / "source_map.lua")]
        if style:
            command += style_render_arguments(style, work)
        title = first_heading_text(fragments[0])
        if title and not (
            front_matter(root, "title") or front_matter(root, "pagetitle")
        ):
            metadata = work / "page-title.json"
            metadata.write_text(json.dumps({"pagetitle": title}))
            command += ["--metadata-file", str(metadata)]
        environment = {
            **os.environ,
            "QMD_SOURCE_TARGETS": str(staged_targets),
            "QMD_FRAGMENT_ANCHORS": str(anchors),
        }
        staged_output = staged_root.parent / rendered.relative_to(home)
        log_path.write_text("")

        def quarto_render(extra: list[str], env: dict) -> str:
            with log_path.open("a") as log:
                result = subprocess.run(
                    command + extra,
                    cwd=staged_root.parent,
                    env=env,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    check=False,
                )
            if result.returncode:
                raise ValueError(
                    f"quarto render failed ({result.returncode}); see {log_path}"
                )
            return staged_output.read_text()

        html = quarto_render([], environment)
        table_decisions = None
        if style and style.table_widths:
            first = work / "first-render.html"
            first.write_text(html)
            with log_path.open("a") as log:
                table_decisions = choose_table_widths(
                    first,
                    playwright=args.playwright_from or config.path("playwright-from"),
                    log=log,
                )
            if any(any(bands) for bands in table_decisions):
                widths = work / "table-widths.json"
                widths.write_text(json.dumps(widest_band_widths(table_decisions)))
                bands = work / "table-width-bands.css"
                bands.write_text(band_stylesheet(table_decisions))
                html = quarto_render(
                    [
                        "--lua-filter",
                        str(PACKAGE / "table_widths.lua"),
                        "--css",
                        str(bands),
                    ],
                    {**environment, "QMD_TABLE_WIDTHS": str(widths)},
                )
    if before != [identity(path, home) for path in sources]:
        raise ValueError("Manuscript changed during rendering")
    if "{{< include" in html:
        raise ValueError("Unresolved include in rendered HTML")
    missing = [
        needle for needle in config.get("must-contain", []) if needle not in html
    ]
    if missing:
        raise ValueError(f"Rendered HTML lacks required content: {missing}")
    print_pdf = args.print_pdf or config.get("print-pdf", False)
    pdf = output.with_suffix(".pdf")
    map_path = output.with_name(output.name + ".map")
    receipt_path = output.with_suffix(".receipt.json")
    rerun = [sys.executable, str(SCRIPT)]
    rerun += ["--config", str(config.source)] if config.source else [str(root)]
    rerun += ["--quarto", quarto]
    if args.output:
        rerun += ["--output", str(output)]
    if args.no_source_map:
        rerun.append("--no-source-map")
    if args.print_pdf:
        rerun.append("--print-pdf")
    if args.style:
        rerun += ["--style", args.style]
    outputs = [str(output), str(receipt_path)]
    outputs += [str(pdf)] if print_pdf else []
    outputs += [str(map_path)] if source_map else []
    rebuild = {
        "regenerate": {
            "hook": config.get("hook", "qmd-html"),
            "registrationVersion": 1,
            "proposedRegistration": {
                "cwd": str(config.base),
                "argv": rerun,
                "outputs": outputs,
                "timeoutSeconds": config.get("timeout-seconds", 180),
            },
        }
    }
    metadata = json.dumps(rebuild, separators=(",", ":")).replace(
        "--", "\\u002d\\u002d"
    )
    if html.count("</head>") != 1:
        raise ValueError("Expected one HTML head for rebuild metadata")
    html = html.replace("</head>", f"<!-- ya-artifact:v1 {metadata} -->\n</head>")
    if source_map:
        targets.extend(
            image_source_targets(html, facts["resources"], facts["extension"], output)
        )
        html, mapping = source_mapped_html(html, targets, output.name)
    output.write_text(html)
    if source_map:
        map_path.write_text(json.dumps(mapping, indent=2) + "\n")
    else:
        map_path.unlink(missing_ok=True)
    if print_pdf:
        options = {**(style.print_options if style else {}), **config.get("print", {})}
        with log_path.open("a") as log:
            print_html_pdf(
                output,
                pdf,
                playwright=args.playwright_from or config.path("playwright-from"),
                options=options,
                log=log,
            )
    receipt = {
        "schema": "qmd-html/v1",
        "quarto": version,
        "root": str(root),
        "sections": len(sections),
        "style": style_name,
        "table_widths": table_decisions,
        "inputs": before,
        "output": identity(output, home),
        "pdf": identity(pdf, home) if print_pdf else None,
        "source_map": identity(map_path, home) if source_map else None,
        "source_targets": len(targets),
        "source_precision": "paragraph/block and section ranges; figure asset files; no character-level mapping"
        if source_map
        else None,
        "artifact_metadata": rebuild,
    }
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt


def parser():
    parser = acli.argument_parser(
        prog="qmd-html",
        description=__doc__,
        capabilities=("complete",),
        exit_codes={0: "rendered", 2: "build or validation failed"},
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
        help="HTML path (else config `output`, else Quarto's own output path)",
    )
    parser.add_argument("--quarto", default="quarto")
    parser.add_argument(
        "--no-source-map",
        action="store_true",
        help="Omit source targets and the .map sidecar",
    )
    parser.add_argument(
        "--print-pdf",
        action="store_true",
        help="Also print a PDF beside the HTML with Chromium",
    )
    parser.add_argument(
        "--style",
        choices=sorted(STYLES),
        help="Document style over Quarto's default theme (else config `style`, else none)",
    )
    parser.add_argument(
        "--playwright-from",
        type=Path,
        help=f"Package directory resolving @playwright/test (else config, else {DEFAULT_PLAYWRIGHT})",
    )
    acli.add_standard_args(parser)
    return parser


def main(argv=None) -> int:
    cli = parser()
    acli.maybe_complete(cli, None if argv is None else [cli.prog, *argv])
    args = cli.parse_args(argv)
    try:
        receipt = render(args, Config.load(args.config, KEYS))
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        acli.die(str(error), 2)
    home = Path(receipt["root"]).parent
    text = f"HTML: {os.path.normpath(home / receipt['output']['path'])}"
    if receipt["pdf"]:
        text += f"\nPDF: {os.path.normpath(home / receipt['pdf']['path'])}"
    acli.emit(
        receipt, acli.resolve_format(args), text=text, commentary=not args.no_commentary
    )
    return 0

"""Tests for qmd_build: venue-PDF page measurement, estimate, and both CLIs.

The unit tests need nothing beyond Python. The end-to-end tests build a small
included-section manuscript through the real `scripts/qmd-venue-pdf` and
`scripts/qmd-html` entry points and skip when Quarto (or TeX) is absent.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from glob import glob
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from qmd_build.manuscript import includes, print_asset
from qmd_build.venue_pdf import page_measurement

HAS_QUARTO = shutil.which("quarto") is not None
HAS_TEX = (
    bool(glob(str(Path.home() / ".TinyTeX/bin/*/xelatex")))
    or shutil.which("xelatex") is not None
)
HAS_PDFLATEX = (
    bool(glob(str(Path.home() / ".TinyTeX/bin/*/pdflatex")))
    or shutil.which("pdflatex") is not None
)


def write_measurement(directory: Path, x: int, physical: int, appendices: bool = True):
    labels = {
        "qmd-main-text-end": 8,
        "qmd-back-matter-start": physical + 1,
        "qmd-references-start": physical + 2,
    }
    if appendices:
        labels["qmd-appendices-start"] = physical + 3
    aux = "\n".join(
        rf"\newlabel{{{label}}}{{{{18}}{{{page}}}{{}}{{section.18}}{{}}}}"
        for label, page in labels.items()
    )
    aux += rf"\zref@newlabel{{qmd-main-end-position}}{{\posx{{{x}}}\posy{{510}}}}"
    (directory / "paper.aux").write_text(aux)
    (directory / "paper.layout").write_text(
        "height=1000\ncolumn=500\ngap=50\nleft=100\ntop=1000\nbaseline=20\n"
    )


@pytest.mark.parametrize(
    ("x", "physical", "columns", "expected", "column"),
    [
        (100, 8, 2, 7.25, 0),
        (650, 8, 2, 7.75, 1),
        (650, 9, 2, 9.0, 1),
        (100, 8, 1, 7.5, 0),
    ],
)
def test_page_measurement(tmp_path, x, physical, columns, expected, column):
    write_measurement(tmp_path, x, physical)
    result = page_measurement(tmp_path, "paper", columns)
    assert result["main_fractional_pages"] == expected
    assert result["main_pages"] == physical
    assert result["last_text_column"] == column
    assert result["appendices_start"] == physical + 3


def test_page_measurement_without_appendices_and_missing_labels(tmp_path):
    write_measurement(tmp_path, 100, 8, appendices=False)
    assert page_measurement(tmp_path, "paper", 2)["appendices_start"] is None
    (tmp_path / "paper.aux").write_text("")
    with pytest.raises(ValueError, match="Missing shipped-page label"):
        page_measurement(tmp_path, "paper", 2)


def test_print_asset_selects_matched_pdf(tmp_path):
    (tmp_path / "figures").mkdir()
    (tmp_path / "figures/plot.v1.pdf").write_bytes(b"%PDF-")
    (tmp_path / "figures/photo.png").write_bytes(b"png")
    dirs = [tmp_path / "missing", tmp_path]
    assert print_asset("figures/plot.v1", dirs) == tmp_path / "figures/plot.v1.pdf"
    assert print_asset("figures/plot.v1.svg", dirs) == tmp_path / "figures/plot.v1.pdf"
    assert print_asset("figures/other", dirs) is None
    assert print_asset("figures/photo.png", dirs) == tmp_path / "figures/photo.png"
    assert print_asset("https://example.org/x.svg", dirs) is None


def test_includes_require_distinct_order(tmp_path):
    root = tmp_path / "index.qmd"
    root.write_text(
        "{{< include sections/_10-a.qmd >}}\n\n{{< include sections/_10-a.qmd >}}\n"
    )
    with pytest.raises(ValueError, match="distinct"):
        includes(root)
    root.write_text("no includes\n")
    assert includes(root, required=False) == []


def manuscript(directory: Path) -> Path:
    """A small two-section manuscript with an abstract, back matter, and an appendix."""
    (directory / "sections").mkdir(parents=True)
    (directory / "_quarto.yml").write_text(
        "project:\n  type: default\n  output-dir: _build\n"
    )
    (directory / "refs.bib").write_text(
        "@misc{ref1, title={A Reference}, author={Doe, Jane}, year={2020}}\n"
    )
    root = directory / "index.qmd"
    root.write_text(
        '---\ntitle: "Tiny Paper"\nbibliography: refs.bib\nformat:\n  html:\n    toc: true\n---\n\n'
        + "\n\n".join(
            f"{{{{< include sections/{name}.qmd >}}}}"
            for name in (
                "_00-abstract",
                "_10-intro",
                "_20-method",
                "_90-limits",
                "_95-appendix",
            )
        )
        + "\n"
    )
    bodies = {
        "_00-abstract": "# Abstract\n\nWe study a tiny problem.\n",
        "_10-intro": "# Introduction\n\n"
        + "Introductory words fill the page. " * 80
        + "See @ref1.\n",
        "_20-method": "# Method\n\n" + "Method words go here. " * 120 + "\n",
        "_90-limits": "# Limitations\n\nFew.\n",
        "_95-appendix": "# Extra detail\n\nMore detail.\n",
    }
    for name, body in bodies.items():
        (directory / "sections" / f"{name}.qmd").write_text(body)
    return root


@pytest.mark.skipif(
    not (HAS_QUARTO and HAS_TEX), reason="needs quarto and a TeX engine"
)
def test_venue_pdf_default_template_end_to_end(tmp_path):
    root = manuscript(tmp_path / "paper")
    config = tmp_path / "paper/venue.json"
    config.write_text(
        json.dumps(
            {
                "root": "index.qmd",
                "output": "_build/venue",
                "abstract": "sections/_00-abstract.qmd",
                "back-matter": ["sections/_90-limits.qmd"],
                "appendices": ["sections/_95-appendix.qmd"],
                "max-pages": 1,
            }
        )
    )
    command = [
        str(REPO / "scripts/qmd-venue-pdf"),
        "--config",
        str(config),
        "--acli-quiet",
    ]
    first = subprocess.run(
        command + ["--enforce-limit"], capture_output=True, text=True
    )
    assert first.returncode in (0, 3), first.stderr
    result = json.loads(first.stdout)
    assert (
        result["main_pages"] >= 1
        and result["references_start"] > result["back_matter_start"] > 1
    )
    assert result["appendices_start"] > result["references_start"]
    assert not result["cached"]
    tex = (root.parent / "_build/venue/paper.tex").read_text()
    assert "\\begin{abstract}" in tex and "We study a tiny problem" in tex
    assert "Doe" in tex  # citeproc placed the reference list at the references boundary
    second = subprocess.run(command, capture_output=True, text=True)
    assert second.returncode == 0, second.stderr
    assert json.loads(second.stdout)["cached"]
    quick = subprocess.run(command + ["--estimate"], capture_output=True, text=True)
    estimated = json.loads(quick.stdout)
    assert (
        estimated["calibrated"]
        and estimated["estimated_pages"] == result["main_fractional_pages"]
    )


@pytest.mark.skipif(
    not (HAS_QUARTO and HAS_TEX), reason="needs quarto and a TeX engine"
)
def test_venue_pdf_acl_checks_reject_wrong_font_and_accept_times(tmp_path):
    root = manuscript(tmp_path / "paper")
    config = tmp_path / "paper/venue.json"
    settings = {"root": "index.qmd", "output": "_build/venue", "checks": "acl"}
    config.write_text(json.dumps(settings))
    command = [
        str(REPO / "scripts/qmd-venue-pdf"),
        "--config",
        str(config),
        "--acli-quiet",
    ]
    # Quarto's default Latin Modern on US Letter is the class of mistake ARR desk-rejects.
    rejected = subprocess.run(command, capture_output=True, text=True)
    assert rejected.returncode == 2
    assert "most-used font" in rejected.stderr and "pages not A4" in rejected.stderr
    settings["metadata"] = {"mainfont": "TeXGyreTermesX-Regular.otf", "papersize": "a4"}
    config.write_text(json.dumps(settings))
    accepted = subprocess.run(command, capture_output=True, text=True)
    assert accepted.returncode == 0, accepted.stderr
    receipt = json.loads((root.parent / "_build/venue/receipt.json").read_text())
    assert receipt["pdf_checks"]["main_font"].startswith("TeXGyreTermesX")
    assert receipt["pdf_checks"]["failures"] == []


def test_pdffonts_rows_keep_names_with_spaces():
    from qmd_build.pdf_checks import parse_pdffonts

    text = (
        "name                                 type              encoding         emb sub uni object ID\n"
        "------------------------------------ ----------------- ---------------- --- --- --- ---------\n"
        "ABCDEF+Times New Roman,Bold          CID TrueType      Identity-H       yes yes yes     12  0\n"
        "GHIJKL+AVeryLongFontNameThatOverflowsItsColumn-Regular Type 1C           Custom           no  no  no      13  0\n"
        "[none]                               Type 3            Custom           yes no  no      14  0\n"
    )
    assert parse_pdffonts(text) == [
        {"name": "Times New Roman,Bold", "type": "CID TrueType", "embedded": True},
        {
            "name": "AVeryLongFontNameThatOverflowsItsColumn-Regular",
            "type": "Type 1C",
            "embedded": False,
        },
        {"name": "[none]", "type": "Type 3", "embedded": True},
    ]


def test_acl_body_font_names_match_whole_families():
    from qmd_build.pdf_checks import PROFILES, body_font_accepted

    accepted = PROFILES["acl"]["body-fonts"]
    # Families as pdftohtml reports them for tgtermes, newtxtext, and mathptmx.
    for family in ("TeXGyreTermes", "TeXGyreTermesX", "NimbusRomNo9L-Regu"):
        assert body_font_accepted(family, accepted), family
    for family in ("TeXGyreTermesMath", "LiberationSerif", "XTeXGyreTermes"):
        assert not body_font_accepted(family, accepted), family


def test_pdf_checks_reject_unknown_profile(tmp_path):
    from qmd_build.pdf_checks import check_pdf

    with pytest.raises(ValueError, match="Unknown venue profile"):
        check_pdf(tmp_path / "missing.pdf", "neurips")


@pytest.mark.skipif(not HAS_QUARTO, reason="needs quarto")
def test_html_source_map_end_to_end(tmp_path):
    root = manuscript(tmp_path / "paper")
    command = [str(REPO / "scripts/qmd-html"), str(root), "--acli-quiet"]
    run = subprocess.run(command, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    receipt = json.loads(run.stdout)
    output = root.parent / "_build/index.html"
    html = output.read_text()
    mapping = json.loads((root.parent / "_build/index.html.map").read_text())
    assert (
        receipt["source_targets"] == len(mapping["x_ya_source_targets"]["targets"]) >= 5
    )
    assert "<!-- ya-artifact:v1 " in html and "ya-source-target:v1" in html
    assert mapping["sources"][0] == "../sections/_00-abstract.qmd"
    # The canonical tree holds no render intermediates beyond the declared
    # output; `.quarto` is Quarto's own project cache from `quarto inspect`.
    assert sorted(
        path.name for path in root.parent.iterdir() if path.name != ".quarto"
    ) == [
        "_build",
        "_quarto.yml",
        "index.qmd",
        "refs.bib",
        "sections",
    ]


@pytest.mark.skipif(not HAS_QUARTO, reason="needs quarto")
def test_html_plain_markdown_memo_style(tmp_path):
    root = tmp_path / "memo.md"
    root.write_text("# A *short* memo\n\nLead.\n\n## Findings\n\nBody.\n")
    command = [str(REPO / "scripts/qmd-html"), str(root), "--style", "memo"]
    run = subprocess.run(command + ["--acli-quiet"], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    receipt = json.loads(run.stdout)
    html = (tmp_path / "memo.html").read_text()
    assert receipt["style"] == "memo" and receipt["sections"] == 0
    assert receipt["source_targets"] >= 2  # the root itself is the mapped section
    assert "<title>A short memo</title>" in html
    assert 'id="TOC"' in html and "data:font/otf;base64" in html
    toc = html.split('id="TOC"', 1)[1].split("</nav>", 1)[0]
    assert "Findings" in toc and "short" not in toc  # the H1 is the title only
    assert 'class="title"' in html


@pytest.mark.skipif(not HAS_QUARTO, reason="needs quarto")
def test_html_included_documents_link_inside(tmp_path):
    (tmp_path / "notes").mkdir()
    (tmp_path / "topics").mkdir()
    (tmp_path / "notes/memo.md").write_text(
        "# Memo\n\nSee [the topic](../topics/topic.md#detail) and [it](../topics/topic.md).\n"
    )
    (tmp_path / "topics/topic.md").write_text(
        "# The topic\n\nTopic: `topic`\nGlossary: omit\n\n## Detail\n\nText.\n"
    )
    root = tmp_path / "bundle.qmd"
    root.write_text(
        "{{< include notes/memo.md >}}\n\n"
        "::: {.appendix-doc}\n{{< include topics/topic.md >}}\n:::\n"
    )
    command = [str(REPO / "scripts/qmd-html"), str(root), "--acli-quiet"]
    run = subprocess.run(command, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    html = (tmp_path / "bundle.html").read_text()
    assert 'href="#detail"' in html and 'href="#the-topic"' in html
    assert "topic.md" not in html.split("<!-- ya-artifact:v1")[0].split("</head>")[-1]
    assert "Glossary: omit" not in html
    assert '<h2 class="anchored" data-anchor-id="the-topic">' in html


@pytest.mark.skipif(not HAS_QUARTO, reason="needs quarto")
def test_html_memo_style_table_width_bands(tmp_path):
    root = tmp_path / "tables.md"
    long = "words that wrap across several lines in a narrow column " * 3
    root.write_text(
        "# Tables\n\n| Name | Detail | Note |\n|---|---|---|\n"
        + "".join(f"| CC-BY-NC-SA {i} | {long} | short |\n" for i in range(4))
    )
    command = [str(REPO / "scripts/qmd-html"), str(root), "--style", "memo"]
    run = subprocess.run(command + ["--acli-quiet"], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    receipt = json.loads(run.stdout)
    html = (tmp_path / "tables.html").read_text()
    assert len(receipt["table_widths"]) == 1 and len(receipt["table_widths"][0]) == 3
    assert "CC‑BY‑NC‑SA" in html  # short tokens keep whole
    if any(receipt["table_widths"][0]):
        assert 'data-table-widths="0"' in html and "@container" in html


@pytest.mark.skipif(not HAS_QUARTO, reason="needs quarto")
def test_html_render_never_writes_through_to_earlier_output(tmp_path):
    root = tmp_path / "doc.md"
    root.write_text("# Doc\n\nBody.\n")
    earlier = tmp_path / "doc.html"
    earlier.write_text("earlier build\n")
    elsewhere = tmp_path / "out/doc.html"
    command = [str(REPO / "scripts/qmd-html"), str(root), "--output", str(elsewhere)]
    run = subprocess.run(command + ["--acli-quiet"], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    assert earlier.read_text() == "earlier build\n"
    assert "Body." in elsewhere.read_text()


@pytest.mark.skipif(not HAS_QUARTO, reason="needs quarto")
def test_html_style_named_in_front_matter_found_on_search_path(tmp_path):
    style = tmp_path / "styles/plainish"
    style.mkdir(parents=True)
    (style / "style.json").write_text(json.dumps({"css": "plainish.css", "toc": False}))
    (style / "plainish.css").write_text("body { --plainish-marker: 1; }\n")
    root = tmp_path / "doc/note.md"
    root.parent.mkdir()
    root.write_text("---\ndocument-style: plainish\n---\n\n# Note\n\nBody.\n")
    env = {**os.environ, "QMD_STYLE_PATH": str(tmp_path / "styles")}
    command = [str(REPO / "scripts/qmd-html"), str(root), "--acli-quiet"]
    run = subprocess.run(command, capture_output=True, text=True, env=env)
    assert run.returncode == 0, run.stderr
    assert json.loads(run.stdout)["style"] == "plainish"
    assert "--plainish-marker" in (root.parent / "note.html").read_text()
    missing = subprocess.run(
        command + ["--style", "absent"], capture_output=True, text=True, env=env
    )
    assert missing.returncode == 2 and "Unknown document style" in missing.stderr


@pytest.mark.skipif(not HAS_QUARTO, reason="needs quarto")
def test_html_bump_revision_records_and_shows_revision(tmp_path):
    root = tmp_path / "note.md"
    root.write_text("# Note\n\n## Part\n\nBody.\n")
    command = [str(REPO / "scripts/qmd-html"), str(root), "--style", "memo"]
    plain = subprocess.run(command + ["--acli-quiet"], capture_output=True, text=True)
    assert plain.returncode == 0, plain.stderr
    assert '<div class="document-revision">' not in (tmp_path / "note.html").read_text()
    for expected in (2, 3):
        run = subprocess.run(
            command + ["--bump-revision", "--acli-quiet"],
            capture_output=True,
            text=True,
        )
        assert run.returncode == 0, run.stderr
        assert json.loads(run.stdout)["revision"] == str(expected)
    source = root.read_text()
    assert source.startswith("---\nrevision: 3\nrevision-date: ")
    assert source.count("revision:") == 1
    assert (
        '<div class="document-revision">rev 3 · '
        in (tmp_path / "note.html").read_text()
    )


@pytest.mark.skipif(not HAS_QUARTO, reason="needs quarto")
def test_html_memo_paragraph_labels_join_outline(tmp_path):
    root = tmp_path / "labels.md"
    root.write_text(
        "# Labels\n\n## Section\n\n**Lead label.** Text after it.\n\n"
        "**Bold term** inside a sentence stays inline.\n\n**Other:** more text.\n"
    )
    command = [str(REPO / "scripts/qmd-html"), str(root), "--style", "memo"]
    run = subprocess.run(command + ["--acli-quiet"], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    html = (tmp_path / "labels.html").read_text()
    toc = html.split('id="TOC"', 1)[1].split("</nav>", 1)[0]
    assert 'href="#lead-label"' in toc and 'href="#other"' in toc
    assert "Bold term" not in toc
    assert 'data-label-punct="."' in html and 'data-label-punct=":"' in html


def test_paper_scaffold_places_paper_under_its_program(tmp_path):
    from qmd_build.scaffold import scaffold

    program = tmp_path / "research" / "speech"
    with pytest.raises(ValueError, match="PROGRAM.md"):
        scaffold(program, "demo", "Demo", None)
    program.mkdir(parents=True)
    (program / "PROGRAM.md").write_text("# Program speech\n")
    result = scaffold(program, "demo", "Demo paper", None)
    paper = program / "papers" / "demo"
    assert result["paper"] == str(paper.resolve())
    index = (paper / "index.qmd").read_text()
    assert 'title: "Demo paper"' in index and "abstract: |" in index
    assert "{{< include sections/_10-introduction.qmd >}}" in index
    assert "papersize: letter" in (paper / "_quarto.yml").read_text()
    assert "../../PROGRAM.md" in (paper / "README.md").read_text()
    assert "{{" not in (paper / "CHANGELOG.md").read_text()
    with pytest.raises(ValueError, match="exists"):
        scaffold(program, "demo", "Demo", None)
    with pytest.raises(ValueError, match="Slug"):
        scaffold(program, "Bad Slug", "Demo", None)


@pytest.mark.skipif(
    not (HAS_QUARTO and HAS_PDFLATEX), reason="needs quarto and pdflatex"
)
def test_fresh_paper_scaffold_builds_html_and_arxiv(tmp_path):
    program = tmp_path / "program"
    program.mkdir()
    (program / "PROGRAM.md").write_text("# Program demo\n")
    new = [str(REPO / "scripts/paper-new"), str(program), "demo", "--title", "Demo"]
    assert subprocess.run(new, capture_output=True, text=True).returncode == 0
    paper = program / "papers" / "demo"
    html = [str(REPO / "scripts/qmd-html"), "--config", "qmd-html.json"]
    run = subprocess.run(html, cwd=paper, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    assert "TBD: problem" in (paper / "_build/index.html").read_text()

    def arxiv() -> dict:
        command = [str(REPO / "scripts/qmd-arxiv"), str(paper), "--json"]
        run = subprocess.run(command, capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        assert (paper / "_build/arxiv/render.log").stat().st_size > 0
        return json.loads(run.stdout.splitlines()[-1])

    receipt = arxiv()
    assert receipt["abstract_characters"] > 0 and receipt["warnings"] == []
    index = paper / "index.qmd"
    text = index.read_text()
    index.write_text(text.replace("  TBD:", "  " + "word " * 420 + "\n  TBD:"))
    assert "accepts at most 1920" in arxiv()["warnings"][0]
    index.write_text(re.sub(r"abstract: \|\n(  .*\n)+", "", text))
    receipt = arxiv()
    assert receipt["abstract_characters"] is None
    assert "no LaTeX abstract" in receipt["warnings"][0]

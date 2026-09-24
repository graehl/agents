"""Tests for qmd_build: venue-PDF page measurement, estimate, and both CLIs.

The unit tests need nothing beyond Python. The end-to-end tests build a small
included-section manuscript through the real `scripts/qmd-venue-pdf` and
`scripts/qmd-html` entry points and skip when Quarto (or TeX) is absent.
"""

from __future__ import annotations

import json
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

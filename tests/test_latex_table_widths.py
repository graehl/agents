"""PDF table columns follow their content through the real Pandoc path."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
FILTER = REPO / "qmd_build/latex_table_widths.lua"
pytestmark = pytest.mark.skipif(not shutil.which("quarto"), reason="Quarto required")

PROSE = "a fairly long explanation that keeps going for several more words"


def latex(tmp_path: Path, source: str, output: str = "latex") -> str:
    root = tmp_path / "table.md"
    root.write_text(source)
    result = subprocess.run(
        ["quarto", "pandoc", str(root), "--to", output, "--lua-filter", str(FILTER)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout


def widths(tex: str) -> list[float]:
    return [float(w) for w in re.findall(r"\\real\{([0-9.]+)\}", tex)]


def test_dash_widths_give_way_to_content(tmp_path: Path) -> None:
    source = f"| # | Lang | Notes |\n|---|---|---|\n| 2 | vi | {PROSE} {PROSE} |\n"
    code, lang, notes = widths(latex(tmp_path, source))
    assert code < lang < notes
    assert abs(code + lang + notes - 1) < 0.01


def test_a_table_that_fits_stays_narrow(tmp_path: Path) -> None:
    source = f"| # | Lang | Notes |\n|---|---|---|\n| 2 | vi | {PROSE} |\n"
    assert sum(widths(latex(tmp_path, source))) < 0.95


def test_words_that_cannot_fit_shrink_the_type(tmp_path: Path) -> None:
    header = " | ".join(f"Column{i}" for i in range(12))
    row = " | ".join(f"unbreakable{i}" for i in range(12))
    source = f"| {header} |\n|{'---|' * 12}\n| {row} |\n"
    tex = latex(tmp_path, source)
    assert tex.lstrip().startswith("\\begingroup\\scriptsize")
    assert tex.rstrip().endswith("\\endgroup")


def test_explicit_colwidths_are_left_to_quarto(tmp_path: Path) -> None:
    source = (
        f"| # | Notes |\n|---|---|\n| 2 | {PROSE} |\n\n"
        ': Caption. {tbl-colwidths="[40,60]"}\n'
    )
    assert widths(latex(tmp_path, source)) == [0.5, 0.5]


def test_html_is_unchanged(tmp_path: Path) -> None:
    source = f"| # | Notes |\n|---|---|\n| 2 | {PROSE} |\n"
    assert 'style="width: 50%"' in latex(tmp_path, source, "html")

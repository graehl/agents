"""Definition identity survives the real Pandoc and Quarto render paths."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
FILTER = REPO / "qmd_build/term_hints.lua"
pytestmark = pytest.mark.skipif(not shutil.which("quarto"), reason="Quarto required")

SOURCE = r"""---
title: Term hints
term-hints-implicit: true
---

## Definitions

[The **semantic score** $s(h,r)$ compares a hypothesis with its reference.]{#term-score .term-definition math="s" terms="semantic score"}

[The reference set $\mathcal{R}$ contains acceptable transcriptions.]{#term-refs .term-definition math="\mathcal{R}" terms="reference set"}

The *calibrated loss* uses $\tau$. The symbol ℝ is another spelling.

The semantic score, (semantic score), **semantic score**, and
[this score]{.term-ref term="score"} share a definition.

$$ L(h) = \sum_{r \in \mathcal{R}} s(h,r) / \tau. $$

Different arguments $s(x,y)$, nested $\termref{score}{s(\frac{x}{y},r)}$,
unrelated $\termignore{s}$, and control words $\sin(x) + \text{scores}$.
Unbraced $\mathbf x$, scripts $\tau_b + x^s$, starred $\operatorname*{argmax}_x s(x,r)$.
The *calibrated loss* and ℝ recur.

::: {.no-term-hints}
$s(h,r)$ and semantic score are deliberately unlinked here.
:::

`s(h,r)` and [semantic score](https://example.org) remain untouched.
"""


def pandoc(tmp_path: Path, source: str = SOURCE, output: str = "html", *extra: str):
    root = tmp_path / "terms.md"
    root.write_text(source)
    return subprocess.run(
        [
            "quarto",
            "pandoc",
            str(root),
            "--from",
            "markdown",
            "--to",
            output,
            "--mathjax",
            "--lua-filter",
            str(FILTER),
            *extra,
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def test_math_and_prose_share_explicit_identity(tmp_path: Path) -> None:
    result = pandoc(tmp_path)
    assert result.returncode == 0, result.stderr
    html = " ".join(result.stdout.split())
    assert r"{\href{#term-score}{s}}(" in html
    assert r"\href{#term-score}{s(\frac{x}{y},r)}" in html
    assert r"\sin(" in html and r"\text{scores}" in html
    assert r"\mathbf x" in html and r"\operatorname*{argmax}" in html
    assert r"\displaylimits" not in html
    assert r"\termref" not in html and r"\termignore" not in html
    assert '<a href="#term-score" class="term-ref">semantic score</a>,' in html
    assert '(<a href="#term-score" class="term-ref">semantic score</a>),' in html
    assert 'data-term-kind="First mention"' in html
    assert "<code>s(h,r)</code>" in html
    assert '<a href="https://example.org">semantic score</a>' in html
    ignored = html.split('<div class="no-term-hints">')[1].split("</div>")[0]
    assert "href" not in ignored


def test_optional_previews_never_disable_definitions(tmp_path: Path) -> None:
    result = pandoc(tmp_path, SOURCE.replace("implicit: true", "implicit: false"))
    assert result.returncode == 0, result.stderr
    assert 'data-term-kind="First mention"' not in result.stdout
    assert 'data-term-card="term-score"' in result.stdout
    assert 'data-term-kind="Notation"' in result.stdout


def test_pdf_keeps_definition_targets_and_links(tmp_path: Path) -> None:
    result = pandoc(tmp_path, SOURCE, "latex")
    assert result.returncode == 0, result.stderr
    assert r"\label{term-score}" in result.stdout
    assert r"\hyperref[term-score]{s}" in result.stdout
    assert r"^{\hyperref[term-score]{s}}" in result.stdout
    assert r"\termref" not in result.stdout
    assert "<template" not in result.stdout


IMPLICIT = "---\nterm-hints-implicit: true\n---\n\n"


def test_implicit_emphasis_links_only_formatted_recurrences(tmp_path: Path) -> None:
    # Emphasis is also stress: "not" and "a" must not become links paper-wide.
    source = (
        IMPLICIT
        + "This is *not* a toy and the *a* case holds for $x$.\n\n"
        + "Later we do not need a proof that a set is not empty, and x is plain.\n\n"
        + "The *not* case recurs in italics.\n"
    )
    result = pandoc(tmp_path, source)
    assert result.returncode == 0, result.stderr
    html = " ".join(result.stdout.split())
    assert "This is <em>not</em> a toy and the <em>a</em> case" in html
    assert "do not need a proof that a set is not empty, and x is plain" in html
    assert '<a href="#term-first-1" class="term-ref"><em>not</em></a> case' in html
    assert html.count('class="term-ref"') == 1
    assert "term-first-emphasis" not in html


def test_implicit_paragraph_preview_is_embedded_once(tmp_path: Path) -> None:
    source = (
        IMPLICIT
        + "The $x$ value and $y$ are *introduced* here.\n\n"
        + "Later $x$ and $y$ recur, *introduced* twice.\n"
    )
    result = pandoc(tmp_path, source)
    assert result.returncode == 0, result.stderr
    assert result.stdout.count("<template data-term-card") == 1
    assert result.stdout.count('id="term-first-') == 1
    for linked in (r"\href{#term-first-1}{x}", r"\href{#term-first-1}{y}"):
        assert result.stdout.count(linked) == 2


def test_pdf_bold_table_score_is_not_a_term(tmp_path: Path) -> None:
    source = (
        IMPLICIT
        + "| Lang | Score |\n|---|---:|\n| vi | **14.19** |\n| zh | **14.19** |\n"
    )
    result = pandoc(tmp_path, source, "latex")
    assert result.returncode == 0, result.stderr
    assert result.stdout.count(r"\textbf{14.19}") == 2
    assert "term-first" not in result.stdout


def test_pdf_anchor_starting_a_table_cell_keeps_its_baseline(tmp_path: Path) -> None:
    # A first-mention anchor set in vertical mode drops the cell's text a line.
    source = IMPLICIT + "| Lang | Scale |\n|---|---:|\n| vi | $\\tau$ |\n"
    result = pandoc(tmp_path, source, "latex")
    assert result.returncode == 0, result.stderr
    assert "\\leavevmode\\protect\\phantomsection\\label{term-first-1}" in result.stdout


@pytest.mark.parametrize(
    "source, message",
    [
        ("$\\termref{missing}{s}$", "unknown reference term-missing"),
        (
            "---\nterm-hints-implicit: maybe\n---\n\nText.",
            "term-hints-implicit must be true or false",
        ),
        (
            "[One]{#term-a .term-definition math=s}\n\n[Two]{#term-b .term-definition math=s}",
            "ambiguous alias s",
        ),
        (
            "[One]{#term-a .term-definition}\n\n[Two]{#term-a .term-definition}",
            "duplicate definition term-a",
        ),
    ],
)
def test_bad_author_markers_fail_build(
    tmp_path: Path, source: str, message: str
) -> None:
    result = pandoc(tmp_path, source)
    assert result.returncode != 0
    assert message in result.stderr


def test_explicit_operator_overrides_default(tmp_path: Path) -> None:
    source = r"""[Our union operation.]{#term-union .term-definition math="\cup" math-class="bin"}

$A \cup B$
"""
    result = pandoc(tmp_path, source)
    assert result.returncode == 0, result.stderr
    assert r"\mathbin{\href{#term-union}{\cup}}" in result.stdout
    assert 'data-term-kind="Notation"' not in result.stdout


def test_real_html_builder_and_browser(tmp_path: Path) -> None:
    root = tmp_path / "index.qmd"
    root.write_text(SOURCE.replace("implicit: true", "implicit: false"))
    config = tmp_path / "qmd-html.json"
    config.write_text(json.dumps({"root": "index.qmd"}))
    result = subprocess.run(
        [str(REPO / "scripts/qmd-html"), "--config", str(config), "--text"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    output = tmp_path / "index.html"
    html = output.read_text()
    assert 'data-term-card="term-score"' in html
    assert 'data-term-kind="First mention"' not in html
    receipt = json.loads(output.with_suffix(".receipt.json").read_text())
    assert any(row["path"].endswith("term_hints.css") for row in receipt["inputs"])
    playwright = Path.home() / "ya/packages/client"
    if (playwright / "node_modules/@playwright/test").exists():
        browser = subprocess.run(
            [
                "node",
                str(REPO / "tests/term_hints_browser.mjs"),
                str(output),
                str(playwright),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert browser.returncode == 0, browser.stdout + browser.stderr


def test_html_builder_runs_a_project_registered_filter_once(tmp_path: Path) -> None:
    # The paper scaffold lists the filter in `_quarto.yml`; a second run by the
    # builder reads the first run's output as source and drops the landing site.
    (tmp_path / "_quarto.yml").write_text(
        f"project:\n  type: default\nfilters:\n  - {FILTER}\nterm-hints-implicit: true\n"
    )
    (tmp_path / "index.qmd").write_text(
        "---\ntitle: Project\n---\n\n## Use\n\n"
        "The $x$ value is *introduced* here.\n\nLater $x$ is *introduced* again.\n"
    )
    result = subprocess.run(
        [str(REPO / "scripts/qmd-html"), str(tmp_path / "index.qmd"), "--text"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    html = (tmp_path / "index.html").read_text()
    assert html.count('id="term-first-1"') == 1
    assert html.count('data-term-card="term-first-1"') == 1

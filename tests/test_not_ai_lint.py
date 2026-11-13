#!/usr/bin/env python3
"""End-to-end tests for scripts/not-ai-lint over the vendored declauding scan."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "not-ai-lint"
sys.path.insert(0, str(REPO_ROOT))

from tests.test_prose_text import _minimal_pdf

REVERSAL = "The gain is not a tuning artifact. It is a property of the labels.\n"
PLAIN = "We trained the tagger on 35 languages and report exact span scores.\n"


def run(
    *args: str, stdin: str | None = None, cwd: Path | None = None
) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--acli-quiet", *args],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=30,
        cwd=cwd,
        check=False,
    )


def reports(*args: str, stdin: str | None = None) -> list[dict]:
    proc = run("--json", "--no-commentary", "--limit", "0", *args, stdin=stdin)
    assert proc.returncode == 0, proc.stderr
    return [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]


def categories(text: str, *args: str) -> dict[str, int]:
    (report,) = reports(*args, stdin=text)
    return {name: stats["count"] for name, stats in report["by_category"].items()}


class Scan(unittest.TestCase):
    def test_named_construction_is_located_at_its_source_line(self) -> None:
        (report,) = reports(stdin="# Results\n\n" + PLAIN + "\n" + REVERSAL)
        hits = [f for f in report["findings"] if f["category"] == "negation-first"]
        self.assertEqual([f["line"] for f in hits], [5])
        self.assertIn("is not a tuning artifact", hits[0]["match"])
        self.assertNotIn("score", report)

    def test_paragraph_shape_candidate_keeps_its_line_after_skipped_blocks(
        self,
    ) -> None:
        run_of_fragments = (
            "It works. It scales. It ships. Then we wrote a much longer sentence "
            "about the remaining results here.\n"
        )
        source = (
            "---\ntitle: T\nauthor: A\ndate: D\n---\n\n# Results\n\n" + PLAIN + "\n"
            "```\ncode\nmore\n```\n\n" + run_of_fragments
        )
        (report,) = reports(stdin=source)
        lines = [f["line"] for f in report["findings"] if f["category"] == "cadence"]
        self.assertEqual(lines, [16])

    def test_bold_emphasis_is_flagged_but_symbols_and_bullet_leads_are_not(
        self,
    ) -> None:
        source = (
            "The outside label is **O** and the gain is **quite large** here.\n\n"
            "- **Recall.** It rose on every language we measured this year.\n\n"
            "**Reading.** Call __init__ or foo__bar__baz from the setup code, and\n"
            "**Strictly speaking.** is emphasis on a wrapped line, not a head.\n\n"
            # One underscored word reads as an identifier: the accepted miss.
            "It __never__ fails, but __never once__ is emphasis.\n"
        )
        (report,) = reports(stdin=source)
        bold = [
            f["match"] for f in report["findings"] if f["category"] == "bold-inline"
        ]
        self.assertEqual(
            bold, ["**quite large**", "**Strictly speaking.**", "__never once__"]
        )

    def test_vocabulary_is_a_rate_and_located_only_in_a_dense_paragraph(self) -> None:
        sparse = "The intricate decoder was trained on 35 languages last year.\n"
        dense = (
            "This multifaceted and groundbreaking tapestry underscores the result.\n"
        )
        (report,) = reports(stdin=sparse + "\n" + dense)
        self.assertEqual(report["vocabulary"]["count"], 5)
        self.assertGreater(report["vocabulary"]["per_1k_words"], 100)
        located = [
            f["line"] for f in report["findings"] if f["category"] == "excess-vocab"
        ]
        self.assertEqual(located, [3, 3, 3, 3])

    def test_a_lone_list_of_three_is_collapsed_in_text_and_kept_in_json(self) -> None:
        source = (
            "We evaluate on French, Japanese, and Korean documents from one corpus.\n"
        )
        (report,) = reports(stdin=source)
        (triad,) = [f for f in report["findings"] if f["category"] == "triad"]
        self.assertTrue(triad["alone"])
        text = run("--text", stdin=source).stdout
        self.assertIn("[triad] alone in its paragraph at lines 1", text)
        self.assertNotRegex(text, r"(?m)^-:1:\d+: \[triad\]")

    def test_non_prose_never_produces_candidates(self) -> None:
        source = (
            "---\ntitle: " + REVERSAL + "---\n\n" + PLAIN + "\n"
            "```\n" + REVERSAL + "```\n\n<!-- " + REVERSAL.strip() + " -->\n\n"
            "::: {.content-hidden}\n" + REVERSAL + ":::\n\n"
            "| a | b |\n|---|---|\n| " + REVERSAL.strip() + " | x |\n"
        )
        self.assertNotIn("negation-first", categories(source))

    def test_skip_leaves_out_a_category(self) -> None:
        self.assertIn("negation-first", categories(REVERSAL))
        self.assertNotIn(
            "negation-first", categories(REVERSAL, "--skip", "negation-first")
        )

    def test_text_report_ends_with_the_advisory_line(self) -> None:
        proc = run("--text", stdin=REVERSAL)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertRegex(proc.stdout, r"(?m)^-:1:\d+: \[negation-first\] ")
        self.assertTrue(proc.stdout.rstrip().splitlines()[-1].startswith("Advisory:"))

    def test_missing_input_is_a_not_found_error(self) -> None:
        proc = run("/nonexistent/draft.md")
        self.assertEqual(proc.returncode, 4)
        self.assertIn('"error"', proc.stderr)


class Manuscript(unittest.TestCase):
    def test_manuscript_covers_live_includes_in_order_and_skips_commented_ones(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "sections").mkdir()
            (root / "sections" / "intro.qmd").write_text(PLAIN)
            (root / "sections" / "method.qmd").write_text(REVERSAL)
            (root / "sections" / "census.qmd").write_text(REVERSAL)
            (root / "index.qmd").write_text(
                "---\ntitle: T\n---\n\n{{< include sections/intro.qmd >}}\n\n"
                "{{< include sections/method.qmd >}}\n\n"
                "<!-- {{< include sections/census.qmd >}} -->\n"
            )
            found = reports("--manuscript", str(root / "index.qmd"))
        self.assertEqual(
            [Path(r["path"]).name for r in found],
            ["index.qmd", "intro.qmd", "method.qmd"],
        )
        self.assertEqual(found[2]["by_category"]["negation-first"]["count"], 1)


@unittest.skipUnless(shutil.which("git"), "git is not installed")
class Since(unittest.TestCase):
    def test_since_reports_only_lines_changed_after_the_revision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            draft = repo / "draft.md"
            draft.write_text(REVERSAL + "\n" + PLAIN)
            for command in (
                ["git", "init", "-q"],
                ["git", "add", "draft.md"],
                [
                    "git",
                    "-c",
                    "user.name=t",
                    "-c",
                    "user.email=t@example.invalid",
                    "commit",
                    "-q",
                    "-m",
                    "base",
                ],
            ):
                subprocess.run(command, cwd=repo, check=True, capture_output=True)
            draft.write_text(
                REVERSAL + "\n" + PLAIN + "\nThe loss is not a bug. It is a choice.\n"
            )
            (report,) = reports("--since", "HEAD", str(draft))
            unknown = run("--since", "no-such-revision", str(draft))
            untracked = repo / "new.md"
            untracked.write_text(REVERSAL)
            (new_file,) = reports("--since", "HEAD", str(untracked))
        self.assertEqual(new_file["by_category"]["negation-first"]["count"], 1)
        lines = [
            f["line"] for f in report["findings"] if f["category"] == "negation-first"
        ]
        self.assertEqual(lines, [5])
        self.assertTrue(any("HEAD" in note for note in report["notes"]))
        self.assertEqual(unknown.returncode, 5)


@unittest.skipUnless(shutil.which("pdftotext"), "pdftotext is not installed")
class Pdf(unittest.TestCase):
    def test_pdf_candidates_carry_page_locators_and_the_extraction_note(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "paper.pdf"
            path.write_bytes(_minimal_pdf([[PLAIN.strip(), REVERSAL.strip()]]))
            (report,) = reports(str(path))
        self.assertEqual(report["format"], "pdf")
        self.assertTrue(any("pdftotext" in note for note in report["notes"]))
        located = [f["loc"] for f in report["findings"] if f["line"]]
        self.assertTrue(located and all(loc.startswith("p1:") for loc in located))


if __name__ == "__main__":
    unittest.main()

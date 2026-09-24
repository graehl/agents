#!/usr/bin/env python3
"""End-to-end tests for scripts/not-ai-lint (offline; no validation corpus)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "not-ai-lint"


def run(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--acli-quiet", *args],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=30,
    )


def rules_hit(text: str) -> dict[str, int]:
    proc = run("--json", "--no-commentary", "--limit", "0", stdin=text)
    assert proc.returncode == 0, proc.stderr
    report = json.loads(proc.stdout.splitlines()[0])
    return {
        rule: stats["count"] for rule, stats in report["summary"]["by_rule"].items()
    }


class RuleDetection(unittest.TestCase):
    def test_each_rule_has_a_positive_example(self) -> None:
        examples = {
            "excess-vocab": "The design underscores an intricate tradeoff.",
            "stock-phrase": "This is a double-edged sword for us.",
            "importance-marker": "It is important to note that the cache is warm.",
            "wrap-up": "In conclusion, we ship it.",
            "meta-comment": "Put simply, we ship it.",
            "cadence-contrast": "It's not about speed, it's about trust.",
            "participial-tail": "The cache hit rate rose, highlighting the gain.",
            "chat-residue": "Let me know if you want more.",
            "model-idiom": "That constraint is load-bearing here.",
            "em-dash": "The cache — once warm — serves hits.",
            "bold-inline": "The cache is **fast** here.",
            "bold-lead-bullet": "- **Speed:** the cache serves hits.",
            "title-case-heading": "## Why The Cache Serves Stale Rows\n\nText.",
            "generic-heading": "## Key Takeaways\n\nText.",
            "rhetorical-question": "Why does it matter? It saves time.",
            "punch-fragment": "Before this.\n\nIt worked.\n\nAfter this.",
            "triad": "The layer is fast, cheap, and simple.",
        }
        for rule, text in examples.items():
            with self.subTest(rule=rule):
                self.assertIn(rule, rules_hit(text))

    def test_code_urls_and_comments_are_not_prose(self) -> None:
        text = (
            "The loader reads each shard once and caches decoded rows.\n\n"
            "```\nThis underscores — notably — intricate code.\n```\n\n"
            "Run `underscores --notably` now. See https://x.test/intricate-notably.\n\n"
            "<!-- In conclusion, this underscores it. -->\n"
        )
        self.assertEqual(rules_hit(text), {})

    def test_plain_technical_prose_scores_low(self) -> None:
        text = (
            "The loader reads each shard once and caches the decoded rows in memory. "
            "A second pass over the same shard costs a hash lookup per row. "
            "With 40 shards of 2 GB each, the cache needs about 30 GB after decoding, "
            "which fits on the training hosts but not on the laptops. "
            "On laptops we disable the cache and accept the slower second epoch.\n"
        ) * 4
        proc = run("--json", "--no-commentary", stdin=text)
        report = json.loads(proc.stdout.splitlines()[0])
        self.assertLess(report["summary"]["score"], 25)
        self.assertTrue(report["summary"]["reliable"])


class Cli(unittest.TestCase):
    def test_missing_file_exits_4_with_envelope(self) -> None:
        proc = run("/nonexistent/not-ai.md")
        self.assertEqual(proc.returncode, 4)
        envelope = json.loads(proc.stderr.strip().splitlines()[-1])
        self.assertFalse(envelope["ok"])

    def test_text_report_ends_with_advisory_line(self) -> None:
        proc = run("--text", stdin="This underscores it.\n")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("AI-style score", proc.stdout)
        self.assertTrue(proc.stdout.rstrip().splitlines()[-1].startswith("Advisory:"))

    def test_limit_truncates_findings_but_not_counts(self) -> None:
        text = "It underscores. It underscores. It underscores. It underscores.\n"
        proc = run("--json", "--no-commentary", "--limit", "1", stdin=text)
        report = json.loads(proc.stdout.splitlines()[0])
        self.assertEqual(len(report["findings"]), 1)
        self.assertEqual(report["findings_total"], 4)
        self.assertEqual(report["summary"]["by_rule"]["excess-vocab"]["count"], 4)
        self.assertEqual(
            report["summary"]["by_rule"]["excess-vocab"]["top"], ["underscores ×4"]
        )

    def test_unscored_rules_are_marked(self) -> None:
        proc = run("--json", "--no-commentary", stdin="A long pause — then more.\n")
        report = json.loads(proc.stdout.splitlines()[0])
        self.assertFalse(report["summary"]["by_rule"]["em-dash"]["scored"])

    def test_commentary_default_and_suppression(self) -> None:
        with_c = json.loads(
            run("--json", stdin="It underscores.\n").stdout.splitlines()[0]
        )
        without = json.loads(
            run(
                "--json", "--no-commentary", stdin="It underscores.\n"
            ).stdout.splitlines()[0]
        )
        self.assertIn("_acli", with_c)
        self.assertNotIn("_acli", without)

    def test_multiple_files_one_record_each(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp, "a.md")
            b = Path(tmp, "b.md")
            a.write_text("It underscores.\n")
            b.write_text("Plain.\n")
            proc = run("--json", "--no-commentary", str(a), str(b))
        records = [json.loads(line) for line in proc.stdout.splitlines()]
        self.assertEqual([r["path"] for r in records], [str(a), str(b)])

    def test_rules_listing(self) -> None:
        proc = run("--rules", "--json")
        rows = [json.loads(line) for line in proc.stdout.splitlines()]
        self.assertIn("excess-vocab", {row["rule"] for row in rows})
        self.assertTrue(
            all(row["evidence"] in {"study", "guide", "lore"} for row in rows)
        )

    def test_help_ends_with_capability_line(self) -> None:
        proc = run("--help")
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(
            proc.stdout.strip().splitlines()[-1], "acli: 1 complete +commentary"
        )


if __name__ == "__main__":
    unittest.main()

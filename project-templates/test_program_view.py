"""The program-view base's dashboards, generated from a scratch Git repository."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "bases/program-view/files/program_view.py"
spec = importlib.util.spec_from_file_location("program_view", SOURCE)
program_view = importlib.util.module_from_spec(spec)
spec.loader.exec_module(program_view)


class ProgramViewTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="program-view-test-")
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name) / "demo"
        files = {
            "README.md": "# Demo\n",
            "AGENTS.local.md": "private\n",
            "notes.md": "# Notes\n",
            "topics/alpha.md": "# Alpha\n",
            "topics/alpha.evidence.md": "ledger\n",
            "gaps/README.md": "# Gaps\n",
            "gaps/broken-thing.md": "gap\n",
            "gaps/sketches/future.md": "sketch\n",
            "research/PROGRAM.md": "# Program Research\n\nPublication-directed evidence.\n",
            "research/ROOT.md": "# Research ROOT\n\n## Current main focus (2026-10-15): speech\n",
            "research/thread.md": "# A thread\n",
            "research/mt/PROGRAM.md": "# Machine translation\n\nTranslation [quality](x.md) per `parameter`.\n",
            "research/mt/GLOSSARY.md": "| term | definition |\n",
            "research/mt/design.md": "# Design\n",
            "research/mt/design.log.md": "log\n",
            "research/mt/progress-2026-07-20.md": "# July\n",
            "research/mt/progress-2026-06-01.md": "# June\n",
            "research/mt/demo-handout.md": "# Demo handout\n",
            "research/mt/advisor/demo-handout-review.md": "# Review\n",
            "research/mt/paper-proposals.md": "# Proposals\n",
            "research/mt/papers/early.md": "# Skeleton\n",
            "research/mt/papers/big/index.qmd": '---\ntitle: "Big paper"\n---\n',
            "research/mt/papers/big/CHANGELOG.md": "# Log\n\n## 2026-10-15: draft 1\n",
            "research/mt/papers/big/sections/_10-intro.qmd": "`TBD` and `TBD`\n",
            "research/mt/surveys/field/survey.md": "# Survey\n",
            "research/mt/surveys/field/related-work/papers.yaml": "papers:\n- key: a\n- key: b\n",
        }
        for rel, text in files.items():
            path = self.repo / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        # Handoffs are private: present on disk, ignored by Git.
        (self.repo / "research/mt/handoffs").mkdir()
        (self.repo / "research/mt/handoffs/current.md").write_text(
            "# Handoff\n", encoding="utf-8"
        )
        (self.repo / ".gitignore").write_text("handoffs/\n", encoding="utf-8")
        self.git("init", "-q")
        self.git("add", ".")
        self.git(
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@t",
            "commit",
            "-q",
            "-m",
            "seed\n\nContributing-model: test-1",
        )

    def git(self, *args: str) -> None:
        subprocess.run(
            ["git", "-C", str(self.repo), *args], check=True, capture_output=True
        )

    def records(self) -> dict[str, dict]:
        dashboard = program_view.Dashboard(program_view.Project(self.repo))
        return {p.rel: dashboard.program_record(p) for p in dashboard.programs}

    def test_root_is_an_implicit_program_and_children_nest(self) -> None:
        records = self.records()
        self.assertEqual(sorted(records), ["", "research", "research/mt"])
        self.assertFalse(records[""]["program"].declared)
        self.assertEqual(records["research/mt"]["program"].name, "Machine translation")
        self.assertEqual(
            records["research/mt"]["program"].description,
            "Translation quality per parameter.",
        )

    def test_each_program_owns_what_the_conventions_place_in_it(self) -> None:
        records = self.records()
        mt = records["research/mt"]
        self.assertEqual(
            set(mt["handouts"]),
            {
                "research/mt/progress-2026-07-20.md",
                "research/mt/progress-2026-06-01.md",
                "research/mt/demo-handout.md",
            },
        )
        # A dated name sorts by its own date, not its last commit.
        handouts = mt["handouts"]
        self.assertLess(
            handouts.index("research/mt/progress-2026-07-20.md"),
            handouts.index("research/mt/progress-2026-06-01.md"),
        )
        self.assertEqual(
            mt["dates"]["research/mt/progress-2026-06-01.md"], "2026-06-01"
        )
        self.assertEqual(mt["documents"], ["research/mt/design.md"])
        self.assertEqual(mt["skeletons"], ["research/mt/papers/early.md"])
        self.assertEqual([p["tbd"] for p in mt["papers"]], [2])
        self.assertEqual([s["entries"] for s in mt["surveys"]], [2])
        self.assertEqual([h.name for h in mt["handoffs"]], ["current.md"])
        self.assertIsNotNone(mt["glossary"])
        self.assertIsNotNone(mt["proposals"])
        root = records[""]
        self.assertEqual(root["documents"], ["notes.md"])
        self.assertEqual(root["counts"], (1, 1, 1))
        self.assertEqual(records["research"]["documents"], ["research/thread.md"])
        self.assertEqual(records["research"]["focus"], "(2026-10-15): speech")

    def test_root_pointer_names_a_handoff(self) -> None:
        (self.repo / "research/mt/ROOT").write_text(
            "handoffs/current.md\n", encoding="utf-8"
        )
        mt = self.records()["research/mt"]
        self.assertEqual(
            mt["pointer"], (self.repo / "research/mt/handoffs/current.md").resolve()
        )
        (self.repo / "research/mt/ROOT").write_text(
            "../../../outside.md\n", encoding="utf-8"
        )
        self.assertIsNone(self.records()["research/mt"]["pointer"])

    def test_pages_and_links(self) -> None:
        pages = program_view.pages(self.repo)
        self.assertEqual(sorted(pages), ["index.html", "research/mt/papers-index.html"])
        index = pages["index.html"]
        for href in (
            "research/mt/PROGRAM.md",
            "research/mt/papers-index.html",
            "research/mt/progress-2026-07-20.md",
            "research/ROOT.md",
            "gaps/sketches",
        ):
            self.assertIn(f'href="{href}"', index)
        self.assertIn("Current focus (2026-10-15): speech", index)
        self.assertIn("test-1", index)
        self.assertIn(
            'href="papers/big/index.qmd"', pages["research/mt/papers-index.html"]
        )

    def test_config_turns_sections_off_and_rejects_unknown_ones(self) -> None:
        config = self.repo / ".project-template" / "program-view.json"
        config.parent.mkdir()
        config.write_text(
            json.dumps({"title": "Shelf", "sections": {"handouts": False}}),
            encoding="utf-8",
        )
        pages = program_view.pages(self.repo)
        self.assertIn("<title>Shelf</title>", pages["index.html"])
        self.assertNotIn("progress-2026-07-20.md", pages["index.html"])
        config.write_text(
            json.dumps({"sections": {"handout": False}}), encoding="utf-8"
        )
        with self.assertRaisesRegex(ValueError, "unknown sections"):
            program_view.pages(self.repo)


if __name__ == "__main__":
    unittest.main()

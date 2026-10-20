"""The program-view base's dashboards, generated from a scratch Git repository."""

from __future__ import annotations

import importlib.util
import json
import re
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

    def test_special_character_paths_keep_their_identity(self) -> None:
        odd = 'research/mt/dé "quoted".md'
        (self.repo / odd).write_text("# Odd\n", encoding="utf-8")
        self.git("add", ".")
        self.git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "odd")
        self.git("mv", "research/thread.md", "research/re named.md")
        (self.repo / odd).write_text("# Odd, edited\n", encoding="utf-8")
        project = program_view.Project(self.repo)
        self.assertIn(odd, project.files)
        self.assertEqual(
            sorted(project.changed),
            ['research/mt/dé "quoted".md', "research/re named.md"],
        )
        self.assertEqual(project.dirty("research/mt"), 1)
        self.assertRegex(project.commit_dates([odd])[odd], r"^\d{4}-\d\d-\d\dT")

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
        # Repo-view breadcrumbs for a program directory open its section here.
        self.assertIn('id="program-research-mt" data-repo-dir="research/mt"', index)
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

    def test_top_level_links_surveys_and_built_papers(self) -> None:
        paper = self.repo / "research/mt/papers/big"
        (paper / "index.qmd").write_text(
            '---\ntitle: "Big paper"\nformat:\n  html:\n    output-file: index.html\n---\n',
            encoding="utf-8",
        )
        (paper / "_build").mkdir()
        (paper / "_build/index.html").write_text("<h1>Big paper</h1>", encoding="utf-8")
        survey = self.repo / "surveys/root-field/survey.md"
        survey.parent.mkdir(parents=True)
        survey.write_text("# Root field\n", encoding="utf-8")
        index = program_view.pages(self.repo)["index.html"]
        for href in (
            "surveys/root-field/survey.md",
            "research/mt/surveys/field/survey.md",
            "research/mt/papers/big/_build/index.html",
        ):
            self.assertIn(f'href="{href}"', index)
        self.assertIn(
            'href="research/mt/papers/big/_build/index.html" title="Big paper">Big paper</a>',
            index,
        )


class CreatedProjectTest(unittest.TestCase):
    def test_created_project_carries_its_conventions(self) -> None:
        from composition import TemplateLibrary, materialize

        library_dir = SOURCE.parents[3]
        library = TemplateLibrary(library_dir.parent, library_dir.name)
        page = json.loads(
            (library_dir / "templates/web-page/template.json").read_text()
        )
        page.update(id="web-page-programs", extends=[*page["extends"], "program-view"])
        library.nodes["web-page-programs"] = page
        library.directories["web-page-programs"] = library_dir / "templates/web-page"
        composition = library.compose("web-page-programs")
        with tempfile.TemporaryDirectory(prefix="program-view-created-") as temporary:
            project = materialize(
                composition, Path(temporary) / "made", "Made", "Programs view"
            )
            # This base's own instructions route only to files the project has.
            ours = [
                (library_dir / "bases/program-view/instructions.md").read_text(),
                (project / "instructions/program-view.md").read_text(),
                (project / "instructions/project-directory.md").read_text(),
            ]
            self.assertIn(ours[0].strip(), (project / "AGENTS.md").read_text())
            self.assertFalse(any("~/agents" in text for text in ours))
            for route in set(re.findall(r"instructions/[\w.-]+\.md", "\n".join(ours))):
                self.assertTrue((project / route).is_file(), route)
            self.assertIn(
                "| Handouts |",
                (project / "instructions/project-directory.md").read_text(),
            )
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            subprocess.run(["git", "-C", str(project), "add", "."], check=True)
            listing = subprocess.run(
                ["python3", str(project / "scripts/program_view.py")],
                cwd=project,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(listing.returncode, 0, listing.stderr)


if __name__ == "__main__":
    unittest.main()

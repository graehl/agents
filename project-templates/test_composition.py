from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from composition import TemplateLibrary, materialize


class CompositionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="template-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.content = self.root / "templates"
        self.content.mkdir()
        self.inventory = {"formatVersion": 1, "bases": [], "templates": []}

    def node(
        self,
        name: str,
        bases: tuple[str, ...] = (),
        files: tuple[tuple[str, bytes], ...] = (),
        *,
        template: bool = False,
        overrides: list[dict] | None = None,
    ) -> Path:
        group = "templates" if template else "bases"
        self.inventory[group].append(name)
        directory = self.content / group / name
        directory.mkdir(parents=True)
        entries = []
        for index, (destination, text) in enumerate(files):
            source = f"source-{index}"
            (directory / source).write_bytes(text)
            entries.append({"from": source, "to": destination})
        manifest = {
            "formatVersion": 1,
            "kind": "template" if template else "base",
            "status": "ready",
            "id": name,
            "title": name,
            "description": name,
            "extends": list(bases),
            "files": entries,
            "overrides": overrides or [],
        }
        (directory / "template.json").write_text(json.dumps(manifest))
        return directory

    def library(self) -> TemplateLibrary:
        (self.content / "library.json").write_text(json.dumps(self.inventory))
        return TemplateLibrary(self.root, "templates")

    def test_diamond_content_dedup_and_portable_copy(self) -> None:
        self.node("base", files=(("AGENTS.md", b"Universal"),))
        self.node("left", ("base",), (("AGENTS.md", b"Shared"), ("guide.md", b"Guide")))
        right = self.node(
            "right",
            ("base",),
            (("AGENTS.md", b"Shared"), ("guide.md", b"Guide"), ("other.md", b"Guide")),
        )
        (right / "source-1").unlink()
        (right / "source-1").symlink_to("../left/source-1")
        self.node("app", ("left", "right"), (("AGENTS.md", b"App"),), template=True)
        result = self.library().compose("app")
        self.assertEqual(result.order, ["base", "left", "right", "app"])
        self.assertEqual(
            result.files["AGENTS.md"].content, b"Universal\n\nShared\n\nApp"
        )
        self.assertEqual(len(result.contributors["guide.md"]), 2)
        target = materialize(result, self.root / "output", "Example", "Build a game")
        self.assertFalse((target / "guide.md").is_symlink())
        self.assertEqual((target / "other.md").read_bytes(), b"Guide")
        self.assertEqual(
            json.loads((target / ".project-template/project.json").read_text())[
                "description"
            ],
            "Build a game",
        )
        with self.assertRaises(FileExistsError):
            materialize(result, target, "Example", "Again")

    def test_order_interleaves_dependencies_when_needed(self) -> None:
        for name in ("x", "y", "z"):
            self.node(name)
        self.node("a", ("x", "y"))
        self.node("b", ("z", "y"))
        self.node("app", ("a", "b"), template=True)
        self.assertEqual(
            self.library().compose("app").order, ["x", "z", "y", "a", "b", "app"]
        )

    def test_opposing_order_is_rejected(self) -> None:
        for name in ("x", "y"):
            self.node(name)
        self.node("a", ("x", "y"))
        self.node("b", ("y", "x"))
        self.node("app", ("a", "b"), template=True)
        with self.assertRaisesRegex(ValueError, "cycle"):
            self.library()

    def test_inheritance_cycle_is_rejected(self) -> None:
        self.node("a", ("b",))
        self.node("b", ("a",))
        with self.assertRaisesRegex(ValueError, "cycle"):
            self.library()

    def test_missing_transitive_base_reports_configuration_error(self) -> None:
        self.node("a", ("b",))
        self.node("b", ("missing",))
        with self.assertRaisesRegex(ValueError, "Unknown base in b"):
            self.library()

    def test_nonidentical_regular_and_nested_instruction_files_conflict(self) -> None:
        for destination in ("config.json", "src/AGENTS.md"):
            with self.subTest(destination=destination):
                self.inventory = {"formatVersion": 1, "bases": [], "templates": []}
                name = "nested" if "/" in destination else "config"
                self.node(f"left-{name}", files=((destination, b"left"),))
                self.node(f"right-{name}", files=((destination, b"right"),))
                self.node(
                    f"app-{name}", (f"left-{name}", f"right-{name}"), template=True
                )
                with self.assertRaisesRegex(ValueError, "file conflicts"):
                    self.library()

    def test_explicit_replacement_resolves_conflict_then_text_operations_apply(
        self,
    ) -> None:
        self.node("left", files=(("README.md", b"left"),))
        self.node("right", files=(("README.md", b"right"), ("omit.md", b"obsolete")))
        directory = self.node(
            "app",
            ("left", "right"),
            template=True,
            overrides=[
                {"op": "replace", "to": "README.md", "from": "replacement"},
                {"op": "prepend", "to": "README.md", "from": "before"},
                {"op": "append", "to": "README.md", "from": "after"},
                {"op": "omit", "to": "omit.md"},
            ],
        )
        for name in ("replacement", "before", "after"):
            (directory / name).write_text(name)
        result = self.library().compose("app")
        self.assertEqual(
            result.files["README.md"].content, b"before\nreplacement\nafter"
        )
        self.assertNotIn("omit.md", result.files)

    def test_omit_then_append_fails(self) -> None:
        directory = self.node(
            "app",
            files=(("a", b"a"),),
            template=True,
            overrides=[
                {"op": "omit", "to": "a"},
                {"op": "append", "to": "a", "from": "source-0"},
            ],
        )
        self.assertTrue(directory.is_dir())
        with self.assertRaisesRegex(ValueError, "existing file"):
            self.library()

    def test_symlink_escape_and_missing_source_are_rejected(self) -> None:
        directory = self.node("app", files=(("a", b"a"),), template=True)
        (directory / "source-0").unlink()
        (directory / "source-0").symlink_to(self.root.parent)
        with self.assertRaisesRegex(ValueError, "escapes repository"):
            self.library()
        (directory / "source-0").unlink()
        with self.assertRaises(FileNotFoundError):
            self.library()

    def test_mode_collision_is_not_harmless(self) -> None:
        self.node("left", files=(("script", b"same"),))
        right = self.node("right", files=(("script", b"same"),))
        manifest = json.loads((right / "template.json").read_text())
        manifest["files"][0]["executable"] = True
        (right / "template.json").write_text(json.dumps(manifest))
        self.node("app", ("left", "right"), template=True)
        with self.assertRaisesRegex(ValueError, "file conflicts"):
            self.library()

    def test_configured_setup_runs_in_created_project(self) -> None:
        self.node(
            "app",
            files=(
                (
                    ".project-template/app.json",
                    json.dumps({"setup": [sys.executable, "custom.py"]}).encode(),
                ),
                (
                    "custom.py",
                    b"from pathlib import Path\nPath('verified').write_text('configured setup')\n",
                ),
            ),
            template=True,
        )
        self.library()
        cli = Path(__file__).with_name("project-template.py")
        target = self.root / "configured-setup"
        result = subprocess.run(
            [
                sys.executable,
                str(cli),
                "create",
                "--repository",
                str(self.root),
                "--content-path",
                "templates",
                "--template",
                "app",
                "--target",
                str(target),
                "--name",
                "App",
                "--description",
                "A sample",
                "--setup",
                "--json",
            ],
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(json.loads(result.stdout)["setup"], "passed")
        self.assertEqual((target / "verified").read_text(), "configured setup")

    def test_removed_source_is_not_needed_by_materialized_files(self) -> None:
        self.node(
            "app", files=(("AGENTS.md", b"Read local instructions."),), template=True
        )
        result = self.library().compose("app")
        target = materialize(result, self.root / "detached", "App", "Example")
        import shutil

        shutil.rmtree(self.content)
        self.assertEqual(
            (target / "AGENTS.md").read_bytes(), b"Read local instructions."
        )
        self.assertFalse(any(path.is_symlink() for path in target.rglob("*")))

    def test_cli_creates_real_tree_and_reports_missing_roots(self) -> None:
        self.node("app", files=(("AGENTS.md", b"instructions"),), template=True)
        self.library()
        cli = Path(__file__).with_name("project-template.py")
        command = [
            sys.executable,
            str(cli),
            "create",
            "--repository",
            str(self.root),
            "--content-path",
            "templates",
            "--template",
            "app",
            "--target",
            str(self.root / "cli-output"),
            "--name",
            "App",
            "--description",
            "A sample",
            "--json",
        ]
        result = subprocess.run(command, text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(result.stdout)["template"], "app")
        self.assertEqual(
            (self.root / "cli-output/AGENTS.md").read_text(), "instructions"
        )
        bad = subprocess.run(
            [
                sys.executable,
                str(cli),
                "validate",
                "--repository",
                str(self.root),
                "--content-path",
                "absent",
                "--json",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(bad.returncode, 0)
        self.assertFalse(json.loads(bad.stderr.splitlines()[-1])["ok"])


if __name__ == "__main__":
    unittest.main()

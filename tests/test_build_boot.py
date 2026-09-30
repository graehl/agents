#!/usr/bin/env python3
"""End-to-end tests for scripts/build-boot."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "build-boot"
BEGIN = "<!-- BEGIN generated: activity routes (scripts/build-boot) -->"
END = "<!-- END generated: activity routes -->"
GLOSSARY = (
    "| term | sense or governs | read |\n|---|---|---|\n"
    "| `writing` | Governs: drafting a document for readers | [writing](topics/writing.md) |\n"
    "| `brand-new` | Governs: doing a new thing | [brand-new](topics/brand-new.md) |\n"
    "| ambition framing | a sense row | |\n"
)


def _run(
    repo: Path, *args: str, home: Path | None = None
) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, ACLI_QUIET="1")
    if home is not None:
        env["HOME"] = str(home)
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(repo), *args, "--json"],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def _repo(root: Path) -> Path:
    repo = root / "agents"
    repo.mkdir()
    (repo / "AGENTS.global.md").write_text(f"# Global\n\n{BEGIN}\n{END}\n\n# Tail\n")
    (repo / "AGENTS.user.md").write_text("## Personal\n\nprefers terse replies\n")
    (repo / "GLOSSARY.agents.md").write_text(GLOSSARY)
    _git(repo, "init", "-q")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "base")
    return repo


def test_build_generates_grouped_routes_and_boot() -> None:
    with tempfile.TemporaryDirectory() as root:
        repo = _repo(Path(root))
        check = _run(repo, "build", "--check")
        assert check.returncode == 3, check.stderr
        result = _run(repo, "build")
        assert result.returncode == 0, result.stderr
        record = json.loads(result.stdout)
        assert record["unclassified_topics"] == ["brand-new"]
        text = (repo / "AGENTS.global.md").read_text()
        section = text[text.index(BEGIN) : text.index(END)]
        assert "**Documents for readers.**" in section
        assert "- drafting a document for readers → `writing`" in section
        assert "**Other activities.**" in section
        assert "a sense row" not in section
        assert text.endswith("# Tail\n")
        boot = (repo / "AGENTS.boot.md").read_text()
        assert "# User policy (compiled from AGENTS.user.md)" in boot
        assert "prefers terse replies" in boot
        assert "prefers terse replies" not in text
        again = _run(repo, "build", "--check")
        assert again.returncode == 0, again.stdout


def test_missing_markers_fail_without_writing() -> None:
    with tempfile.TemporaryDirectory() as root:
        repo = _repo(Path(root))
        (repo / "AGENTS.global.md").write_text("# Global without markers\n")
        result = _run(repo, "build")
        assert result.returncode == 4
        assert (
            json.loads(result.stderr.splitlines()[-1])["error"]["code"] == "not_found"
        )
        assert not (repo / "AGENTS.boot.md").exists()


def test_index_mode_stages_only_the_generated_section() -> None:
    with tempfile.TemporaryDirectory() as root:
        repo = _repo(Path(root))
        assert _run(repo, "build").returncode == 0
        _git(repo, "add", "AGENTS.global.md")
        glossary = repo / "GLOSSARY.agents.md"
        glossary.write_text(
            GLOSSARY.replace("doing a new thing", "doing a newer thing")
        )
        _git(repo, "add", "GLOSSARY.agents.md")
        with (repo / "AGENTS.global.md").open("a") as stream:
            stream.write("unstaged edit\n")
        result = _run(repo, "build", "--index")
        assert result.returncode == 0, result.stderr
        staged = _git(repo, "show", ":AGENTS.global.md")
        assert "doing a newer thing" in staged
        assert "unstaged edit" not in staged
        worktree = (repo / "AGENTS.global.md").read_text()
        assert "doing a newer thing" in worktree and "unstaged edit" in worktree


def test_link_retargets_only_links_to_this_policy() -> None:
    with tempfile.TemporaryDirectory() as root:
        root = Path(root)
        repo = _repo(root)
        home = root / "home"
        (home / ".config/agents").mkdir(parents=True)
        ours = home / "ours.md"
        foreign = home / "foreign.md"
        regular = home / "regular.md"
        os.symlink(repo / "AGENTS.global.md", ours)
        os.symlink(root / "elsewhere.md", foreign)
        regular.write_text("hand-written\n")
        (home / ".config/agents/build-boot.json").write_text(
            json.dumps({"targets": [str(ours), str(foreign), str(regular)]})
        )
        early = _run(repo, "link", home=home)
        assert early.returncode == 4
        assert _run(repo, "build").returncode == 0
        assert _run(repo, "link", "--check", home=home).returncode == 3
        result = _run(repo, "link", home=home)
        assert result.returncode == 0, result.stderr
        actions = {
            Path(r["path"]).name: r["action"]
            for r in map(json.loads, result.stdout.splitlines())
        }
        assert actions == {
            "ours.md": "retarget",
            "foreign.md": "skip",
            "regular.md": "skip",
        }
        assert Path(os.readlink(ours)) == repo / "AGENTS.boot.md"
        assert Path(os.readlink(foreign)) == root / "elsewhere.md"
        assert regular.read_text() == "hand-written\n"
        undo = _run(repo, "link", "--to-global", home=home)
        assert undo.returncode == 0, undo.stderr
        assert Path(os.readlink(ours)) == repo / "AGENTS.global.md"


def test_link_disables_opencode_discovery_links_covering_the_checkout() -> None:
    with tempfile.TemporaryDirectory() as root:
        root = Path(root)
        repo = _repo(root)
        (repo / "skills").mkdir()
        home = root / "home"
        (home / ".config/agents").mkdir(parents=True)
        (home / ".config/agents/build-boot.json").write_text('{"targets": []}')
        (home / ".opencode").mkdir()
        (home / ".config/opencode").mkdir()
        whole_repo = home / ".opencode/agents"
        ancestor = home / ".config/opencode/plugins"
        skills = home / ".opencode/skills"
        os.symlink(repo, whole_repo)
        os.symlink(root, ancestor)
        os.symlink(repo / "skills", skills)
        assert _run(repo, "build").returncode == 0
        check = _run(repo, "link", "--check", home=home)
        assert check.returncode == 3, check.stdout
        assert whole_repo.is_symlink() and ancestor.is_symlink()
        result = _run(repo, "link", home=home)
        assert result.returncode == 0, result.stderr
        rows = [json.loads(line) for line in result.stdout.splitlines()]
        assert {Path(r["path"]) for r in rows if r["action"] == "disable"} == {
            whole_repo,
            ancestor,
        }
        assert not whole_repo.exists() and not ancestor.exists()
        assert Path(os.readlink(home / ".opencode/agents.build-boot-disabled")) == repo
        assert Path(os.readlink(skills)) == repo / "skills"
        assert _run(repo, "link", "--check", home=home).returncode == 0


if __name__ == "__main__":
    tests = [
        value for name, value in sorted(globals().items()) if name.startswith("test_")
    ]
    for test in tests:
        test()
    print(f"ok: {len(tests)} tests")

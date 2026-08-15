#!/usr/bin/env python3
"""Behavior tests for scripts/install-agents."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.install_agents import core as install_core

SCRIPT = REPO_ROOT / "scripts" / "install-agents"
GLOBAL = REPO_ROOT / "AGENTS.global.md"
SKILLS = REPO_ROOT / "skills"
FIRST_SKILL = min(path for path in SKILLS.iterdir() if (path / "SKILL.md").is_file())


def _run(home: Path, command: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), command, "--home", str(home), "--json", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def _target(path: Path) -> Path:
    return (path.parent / os.readlink(path)).resolve()


def test_install_and_uninstall_restore_mixed_prior_state() -> None:
    with tempfile.TemporaryDirectory(prefix="install-agents-test-") as directory:
        home = Path(directory)
        codex = home / ".codex/AGENTS.md"
        codex.parent.mkdir(parents=True)
        codex.write_text("old codex\n")
        codex_peer = codex.parent / "AGENTS.peer"
        os.link(codex, codex_peer)
        codex_inode = codex.stat().st_ino

        claude = home / ".claude/CLAUDE.md"
        claude.parent.mkdir(parents=True)
        claude.symlink_to("missing-old-target")
        old_skill = claude.parent / "skills" / FIRST_SKILL.name
        old_skill.mkdir(parents=True)
        old_skill.joinpath("kept.txt").write_text("old skill\n")
        unrelated = claude.parent / "skills" / "unrelated"
        unrelated.mkdir()
        unrelated.joinpath("SKILL.md").write_text("unrelated\n")

        grok = home / ".grok/AGENTS.md"
        grok.mkdir(parents=True)
        grok.joinpath("unexpected-but-preserved").write_text("directory state\n")

        home_agents = home / "AGENTS.md"
        home_agents.write_text("home sentinel\n")
        hardlink_peer = home / "AGENTS.peer"
        os.link(home_agents, hardlink_peer)
        before_inode = home_agents.stat().st_ino

        proc = _run(home, "install", "--harness", "codex,claude,grok")
        assert proc.returncode == 0, proc.stderr
        payload = json.loads(proc.stdout)
        assert payload["status"] == "installed"
        assert _target(codex) == GLOBAL.resolve()
        assert _target(claude) == GLOBAL.resolve()
        assert _target(grok) == GLOBAL.resolve()
        assert _target(old_skill) == FIRST_SKILL.resolve()
        assert unrelated.joinpath("SKILL.md").read_text() == "unrelated\n"
        assert home_agents.stat().st_ino == before_inode
        assert home_agents.stat().st_nlink == 2
        assert home_agents.read_text() == "home sentinel\n"

        status = _run(home, "status", "--harness", "codex,claude,grok")
        assert status.returncode == 0, status.stderr
        assert json.loads(status.stdout)["drift"] == []

        again = _run(home, "install", "--harness", "codex,claude,grok")
        assert again.returncode == 0, again.stderr
        assert json.loads(again.stdout)["status"] == "already-installed"

        proc = _run(home, "uninstall")
        assert proc.returncode == 0, proc.stderr
        assert codex.read_text() == "old codex\n"
        assert codex.stat().st_ino == codex_inode
        assert codex_peer.stat().st_ino == codex_inode
        assert codex.stat().st_nlink == 2
        assert claude.is_symlink() and os.readlink(claude) == "missing-old-target"
        assert grok.is_dir()
        assert (
            grok.joinpath("unexpected-but-preserved").read_text() == "directory state\n"
        )
        assert old_skill.is_dir()
        assert old_skill.joinpath("kept.txt").read_text() == "old skill\n"
        assert unrelated.joinpath("SKILL.md").read_text() == "unrelated\n"
        assert home_agents.stat().st_ino == before_inode
        assert hardlink_peer.stat().st_ino == before_inode
        assert home_agents.stat().st_nlink == 2


def test_selected_harness_does_not_touch_others() -> None:
    with tempfile.TemporaryDirectory(prefix="install-agents-test-") as directory:
        home = Path(directory)
        proc = _run(home, "install", "--harness", "codex")
        assert proc.returncode == 0, proc.stderr
        assert _target(home / ".codex/AGENTS.md") == GLOBAL.resolve()
        assert not home.joinpath(".claude").exists()
        assert _target(home / ".agents/skills") == SKILLS.resolve()
        assert _run(home, "uninstall").returncode == 0
        assert not home.joinpath(".codex").exists()
        assert not home.joinpath(".agents").exists()


def test_uninstall_refuses_post_install_changes() -> None:
    with tempfile.TemporaryDirectory(prefix="install-agents-test-") as directory:
        home = Path(directory)
        assert _run(home, "install", "--harness", "codex").returncode == 0
        target = home / ".codex/AGENTS.md"
        target.unlink()
        target.write_text("new user state\n")
        proc = _run(home, "uninstall")
        assert proc.returncode == 2
        assert "post-install changes" in proc.stderr
        assert target.read_text() == "new user state\n"


def test_uninstall_preflights_every_backup_before_mutating_targets() -> None:
    for damage in ("missing", "corrupt"):
        with tempfile.TemporaryDirectory(prefix="install-agents-test-") as directory:
            home = Path(directory)
            codex = home / ".codex/AGENTS.md"
            claude = home / ".claude/CLAUDE.md"
            codex.parent.mkdir(parents=True)
            claude.parent.mkdir(parents=True)
            codex.write_text("old codex\n")
            claude.write_text("old claude\n")

            installed = _run(home, "install", "--harness", "codex,claude")
            assert installed.returncode == 0, installed.stderr
            active_path = home / ".local/state/agents-install/active.json"
            manifest = json.loads(active_path.read_text())
            record = next(
                target
                for target in manifest["targets"]
                if target["relative"] == ".codex/AGENTS.md"
            )
            backup = Path(manifest["backup_root"]) / record["original"]["backup"]
            if damage == "missing":
                backup.unlink()
            else:
                backup.write_text("corrupt\n")

            refused = _run(home, "uninstall")
            assert refused.returncode == 2, refused
            assert "restore preflight failed" in refused.stderr, refused.stderr
            assert _target(codex) == GLOBAL.resolve()
            assert _target(claude) == GLOBAL.resolve()
            assert active_path.is_file()


def test_install_refuses_a_target_through_an_external_parent_symlink() -> None:
    with tempfile.TemporaryDirectory(prefix="install-agents-test-") as directory:
        base = Path(directory)
        home = base / "home"
        outside = base / "outside"
        home.mkdir()
        outside.mkdir()
        victim = outside / "AGENTS.md"
        victim.write_text("outside sentinel\n")
        (home / ".codex").symlink_to(outside, target_is_directory=True)

        refused = _run(home, "install", "--harness", "codex")
        assert refused.returncode == 2, refused
        assert "symlinked parent escapes --home" in refused.stderr, refused.stderr
        assert victim.read_text() == "outside sentinel\n"
        assert not victim.is_symlink()


def test_link_replacement_preserves_an_unowned_legacy_temp_collision() -> None:
    with tempfile.TemporaryDirectory(prefix="install-agents-test-") as directory:
        root = Path(directory)
        target = root / "target"
        source = root / "source"
        source.write_text("source\n")
        collision = target.with_name(f".{target.name}.install-agents-{os.getpid()}")
        collision.write_text("do not delete\n")

        install_core._replace_with_link(target, source)

        assert _target(target) == source.resolve()
        assert collision.read_text() == "do not delete\n"


def test_broken_skill_root_is_backed_up_and_restored() -> None:
    with tempfile.TemporaryDirectory(prefix="install-agents-test-") as directory:
        home = Path(directory)
        root = home / ".agents/skills"
        root.parent.mkdir(parents=True)
        root.symlink_to("missing-skills")
        proc = _run(home, "install", "--harness", "codex")
        assert proc.returncode == 0, proc.stderr
        assert _target(root) == SKILLS.resolve()
        assert _run(home, "uninstall").returncode == 0
        assert root.is_symlink()
        assert os.readlink(root) == "missing-skills"


def test_reinstall_reconciles_added_and_retired_skills() -> None:
    with tempfile.TemporaryDirectory(prefix="install-agents-test-") as directory:
        base = Path(directory)
        home = base / "home"
        repo = base / "repo"
        home.mkdir()
        repo.mkdir()
        repo.joinpath("AGENTS.global.md").write_text("global\n")
        first = repo / "skills/first"
        first.mkdir(parents=True)
        first.joinpath("SKILL.md").write_text("first\n")

        skill_root = home / ".grok/skills"
        old_first = skill_root / "first"
        old_first.mkdir(parents=True)
        old_first.joinpath("kept.txt").write_text("old first\n")
        unrelated = skill_root / "unrelated"
        unrelated.mkdir()
        unrelated.joinpath("SKILL.md").write_text("unrelated\n")
        repo_arg = ("--repo", str(repo), "--harness", "grok")

        assert _run(home, "install", *repo_arg).returncode == 0
        assert _target(skill_root / "first") == first.resolve()

        second = repo / "skills/second"
        second.mkdir()
        second.joinpath("SKILL.md").write_text("second\n")
        assert _run(home, "status", *repo_arg).returncode == 3
        refreshed = _run(home, "install", *repo_arg)
        assert refreshed.returncode == 0, refreshed.stderr
        assert json.loads(refreshed.stdout)["status"] == "refreshed"
        assert _target(skill_root / "second") == second.resolve()
        assert _run(home, "status", *repo_arg).returncode == 0

        first.joinpath("SKILL.md").unlink()
        second.joinpath("SKILL.md").unlink()
        status = _run(home, "status", *repo_arg)
        assert status.returncode == 3
        assert "retired repository skill" in status.stdout
        refreshed = _run(home, "install", *repo_arg)
        assert refreshed.returncode == 0, refreshed.stderr
        assert json.loads(refreshed.stdout)["status"] == "refreshed"
        assert old_first.is_dir() and not old_first.is_symlink()
        assert old_first.joinpath("kept.txt").read_text() == "old first\n"
        assert not skill_root.joinpath("second").exists()
        assert _run(home, "status", *repo_arg).returncode == 0

        assert _run(home, "uninstall", "--repo", str(repo)).returncode == 0
        assert old_first.is_dir()
        assert old_first.joinpath("kept.txt").read_text() == "old first\n"
        assert not skill_root.joinpath("second").exists()
        assert unrelated.joinpath("SKILL.md").read_text() == "unrelated\n"


def test_reinstall_refuses_changed_retired_skill_target() -> None:
    with tempfile.TemporaryDirectory(prefix="install-agents-test-") as directory:
        base = Path(directory)
        home = base / "home"
        repo = base / "repo"
        home.mkdir()
        repo.mkdir()
        repo.joinpath("AGENTS.global.md").write_text("global\n")
        skill = repo / "skills/first"
        skill.mkdir(parents=True)
        skill.joinpath("SKILL.md").write_text("first\n")
        repo_arg = ("--repo", str(repo), "--harness", "grok")
        home.joinpath(".grok/skills").mkdir(parents=True)

        assert _run(home, "install", *repo_arg).returncode == 0
        target = home / ".grok/skills/first"
        skill.joinpath("SKILL.md").unlink()
        target.unlink()
        target.mkdir()
        target.joinpath("user-state").write_text("preserve me\n")

        refreshed = _run(home, "install", *repo_arg)
        assert refreshed.returncode == 2
        assert "active install has drifted" in refreshed.stderr
        assert target.joinpath("user-state").read_text() == "preserve me\n"


if __name__ == "__main__":
    tests = [
        value for name, value in sorted(globals().items()) if name.startswith("test_")
    ]
    for test in tests:
        test()
    print(f"ok: {len(tests)} tests")

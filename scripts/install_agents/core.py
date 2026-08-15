"""Backup, install, inspect, and restore harness instruction links."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import tempfile
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .harnesses import Harness

MANIFEST_VERSION = 1
STATE_RELATIVE = Path(".local/state/agents-install")


class InstallError(RuntimeError):
    """A safe, actionable refusal rather than a partial install."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _tree_digest(root: Path) -> str:
    digest = hashlib.sha256()

    def visit(path: Path, relative: Path) -> None:
        info = path.lstat()
        mode = stat.S_IMODE(info.st_mode)
        if stat.S_ISLNK(info.st_mode):
            payload = f"L\0{relative}\0{mode:o}\0{os.readlink(path)}\0"
            digest.update(payload.encode())
            return
        if stat.S_ISREG(info.st_mode):
            payload = f"F\0{relative}\0{mode:o}\0{_sha256(path)}\0"
            digest.update(payload.encode())
            return
        if stat.S_ISDIR(info.st_mode):
            payload = f"D\0{relative}\0{mode:o}\0"
            digest.update(payload.encode())
            for child in sorted(path.iterdir(), key=lambda item: item.name):
                visit(child, relative / child.name)
            return
        digest.update(f"O\0{relative}\0{info.st_mode:o}\0".encode())

    visit(root, Path("."))
    return digest.hexdigest()


def _describe(path: Path) -> dict[str, Any]:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return {"kind": "absent"}
    common = {
        "mode": stat.S_IMODE(info.st_mode),
        "device": info.st_dev,
        "inode": info.st_ino,
        "links": info.st_nlink,
    }
    if stat.S_ISLNK(info.st_mode):
        return {"kind": "symlink", "target": os.readlink(path), **common}
    if stat.S_ISREG(info.st_mode):
        return {
            "kind": "file",
            "size": info.st_size,
            "sha256": _sha256(path),
            **common,
        }
    if stat.S_ISDIR(info.st_mode):
        return {"kind": "directory", "sha256": _tree_digest(path), **common}
    return {"kind": "other", **common}


def _signature(description: dict[str, Any]) -> tuple[Any, ...]:
    kind = description["kind"]
    if kind == "absent":
        return (kind,)
    if kind == "symlink":
        return (kind, description["target"])
    if kind in {"file", "directory"}:
        return (kind, description["mode"], description["sha256"])
    return (
        kind,
        description.get("mode"),
        description.get("device"),
        description.get("inode"),
    )


def _relative(path: Path, home: Path) -> Path:
    try:
        relative = path.relative_to(home)
    except ValueError as exc:
        raise InstallError(f"refusing target outside --home: {path}") from exc
    try:
        path.parent.resolve(strict=False).relative_to(home.resolve(strict=False))
    except ValueError as exc:
        raise InstallError(
            f"refusing target whose symlinked parent escapes --home: {path}"
        ) from exc
    return relative


def _copy_snapshot(
    path: Path,
    home: Path,
    backup_root: Path,
    *,
    preserve_hardlink: bool = False,
) -> dict[str, Any]:
    relative = _relative(path, home)
    description = _describe(path)
    if description["kind"] in {"absent", "other"}:
        if description["kind"] == "other":
            raise InstallError(f"refusing unsupported filesystem object: {path}")
        return description

    backup = backup_root / "files" / relative
    backup.parent.mkdir(parents=True, exist_ok=True)
    if description["kind"] == "symlink":
        os.symlink(description["target"], backup)
    elif description["kind"] == "directory":
        shutil.copytree(path, backup, symlinks=True, copy_function=shutil.copy2)
    elif preserve_hardlink and description["links"] > 1:
        try:
            os.link(path, backup)
            description["backup_method"] = "hardlink"
        except OSError:
            shutil.copy2(path, backup, follow_symlinks=False)
            description["backup_method"] = "copy"
    else:
        shutil.copy2(path, backup, follow_symlinks=False)
        description["backup_method"] = "copy"
    description["backup"] = str(Path("files") / relative)
    return description


def _resolved_link(path: Path) -> Path | None:
    if not path.is_symlink():
        return None
    target = Path(os.readlink(path))
    if not target.is_absolute():
        target = path.parent / target
    return target.resolve(strict=False)


def _matches_link(path: Path, source: Path) -> bool:
    resolved = _resolved_link(path)
    return resolved is not None and resolved == source.resolve(strict=False)


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        raise InstallError(f"refusing to remove unsupported filesystem object: {path}")


def _replace_with_link(path: Path, source: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        dir=path.parent, prefix=f".{path.name}.install-agents-"
    ) as temporary_directory:
        temporary = Path(temporary_directory) / "link"
        os.symlink(str(source), temporary, target_is_directory=source.is_dir())
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        os.replace(temporary, path)


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        dir=path.parent, prefix=f".{path.name}.install-agents-"
    ) as temporary_directory:
        temporary = Path(temporary_directory) / "value"
        temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        os.replace(temporary, path)


def _skill_directories(source: Path) -> list[Path]:
    return sorted(
        child
        for child in source.iterdir()
        if child.is_dir() and child.joinpath("SKILL.md").is_file()
    )


def _retired_skill_records(
    manifest: dict[str, Any], skills_source: Path
) -> list[dict[str, Any]]:
    records = []
    for target in manifest.get("targets", []):
        source = Path(target["source"])
        if (
            target.get("mutated")
            and source.parent == skills_source
            and not source.joinpath("SKILL.md").is_file()
        ):
            records.append(target)
    return records


def _created_parents(paths: list[Path], home: Path) -> list[str]:
    missing: set[Path] = set()
    for path in paths:
        parent = path.parent
        while parent != home and parent != parent.parent:
            if parent.exists() or parent.is_symlink():
                break
            missing.add(parent)
            parent = parent.parent
    return [
        str(path.relative_to(home))
        for path in sorted(missing, key=lambda item: len(item.parts))
    ]


def _target_record(
    path: Path,
    source: Path,
    home: Path,
    backup_root: Path,
    roles: list[str],
) -> tuple[dict[str, Any], bool]:
    original = _copy_snapshot(path, home, backup_root, preserve_hardlink=True)
    record = {
        "path": str(path),
        "relative": str(_relative(path, home)),
        "roles": sorted(roles),
        "source": str(source),
        "original": original,
    }
    mutate = not _matches_link(path, source)
    record["mutated"] = mutate
    return record, mutate


def _active_manifest(state_root: Path) -> dict[str, Any] | None:
    active = state_root / "active.json"
    if not active.exists():
        return None
    try:
        return json.loads(active.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise InstallError(
            f"cannot read active install manifest {active}: {exc}"
        ) from exc


def _plan_skill_targets(
    home: Path,
    skills_source: Path,
    skill_roots: dict[Path, list[str]],
    backup_root: Path,
    known_paths: set[Path] | None = None,
) -> tuple[list[dict[str, Any]], list[tuple[Path, Path]], list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    actions: list[tuple[Path, Path]] = []
    observations = []
    known_paths = known_paths or set()
    skills = _skill_directories(skills_source)

    for root, roles in skill_roots.items():
        _relative(root, home)
        observations.append(
            {"path": str(root), "roles": sorted(roles), "state": _describe(root)}
        )
        if root.exists() and root.resolve() == skills_source.resolve():
            continue
        if root.is_symlink() and root.exists():
            raise InstallError(
                f"skill root points elsewhere; refusing to write through it: {root}"
            )
        targets = (
            [(root / skill.name, skill) for skill in skills]
            if root.is_dir()
            else [(root, skills_source)]
        )
        for path, source in targets:
            if path in known_paths:
                continue
            record, mutate = _target_record(path, source, home, backup_root, roles)
            records.append(record)
            if mutate:
                actions.append((path, source))
    return records, actions, observations


def install(home: Path, repo_root: Path, harnesses: list[Harness]) -> dict[str, Any]:
    home = home.expanduser().absolute()
    repo_root = repo_root.expanduser().resolve()
    if home == Path("/"):
        raise InstallError("refusing to use / as --home")
    global_source = repo_root / "AGENTS.global.md"
    skills_source = repo_root / "skills"
    if not global_source.is_file() or not skills_source.is_dir():
        raise InstallError(f"not an instruction checkout: {repo_root}")

    selected = [harness.name for harness in harnesses]
    instructions: dict[Path, list[str]] = {}
    skill_roots: dict[Path, list[str]] = {}
    for harness in harnesses:
        instructions.setdefault(home.joinpath(*harness.instruction), []).append(
            harness.name
        )
        skill_roots.setdefault(home.joinpath(*harness.skill_root), []).append(
            harness.name
        )

    state_root = home / STATE_RELATIVE
    _relative(state_root / "active.json", home)
    for path in instructions:
        _relative(path, home)
    for root in skill_roots:
        _relative(root, home)
    existing = _active_manifest(state_root)
    if existing is not None:
        if (
            existing.get("repo_root") != str(repo_root)
            or existing.get("harnesses") != selected
        ):
            raise InstallError(
                "another install is active; uninstall it before changing "
                "source or harness selection"
            )
        backup_root = Path(existing["backup_root"])
        _validate_manifest_scope(existing, home, backup_root)
        if not backup_root.is_dir():
            raise InstallError(f"active install backup is missing: {backup_root}")
        retired = _retired_skill_records(existing, skills_source)
        safely_retired_paths = {
            Path(target["path"])
            for target in retired
            if _matches_link(Path(target["path"]), Path(target["source"]))
        }
        drift = _manifest_drift(existing, ignored_paths=safely_retired_paths)
        if drift:
            raise InstallError("active install has drifted: " + ", ".join(drift))
        known_paths = {Path(record["path"]) for record in existing.get("targets", [])}
        records, actions, observations = _plan_skill_targets(
            home, skills_source, skill_roots, backup_root, known_paths
        )
        if records or retired:
            refreshed_at = datetime.now(timezone.utc).isoformat()
            existing["phase"] = "prepared"
            existing["targets"].extend(records)
            existing["created_dirs"] = sorted(
                set(existing.get("created_dirs", []))
                | set(_created_parents([path for path, _ in actions], home))
            )
            existing.setdefault("refreshes", []).append(
                {
                    "at": refreshed_at,
                    "skill_roots": observations,
                    "retired_skills": [target["relative"] for target in retired],
                }
            )
            _atomic_json(backup_root / "manifest.json", existing)
            _atomic_json(state_root / "active.json", existing)
            for target in reversed(retired):
                _restore(Path(target["path"]), target["original"], backup_root)
            for path, source in actions:
                _replace_with_link(path, source)
            retired_paths = {target["path"] for target in retired}
            existing["targets"] = [
                target
                for target in existing["targets"]
                if target["path"] not in retired_paths
            ]
            for target in retired:
                existing.setdefault("retired_targets", []).append(
                    {**target, "retired_at": refreshed_at}
                )
            existing["phase"] = "installed"
            existing["installed_at"] = datetime.now(timezone.utc).isoformat()
            _atomic_json(backup_root / "manifest.json", existing)
            _atomic_json(state_root / "active.json", existing)
            return {
                "status": "refreshed",
                "manifest": str(state_root / "active.json"),
                "backup": str(backup_root),
                "changed": len(actions) + len(retired),
            }
        return {
            "status": "already-installed",
            "manifest": str(state_root / "active.json"),
            "changed": 0,
        }

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    transaction = state_root / "backups" / f"{stamp}-{os.getpid()}"
    transaction.mkdir(parents=True, exist_ok=False)

    records: list[dict[str, Any]] = []
    actions: list[tuple[Path, Path]] = []
    observations = {
        "home_AGENTS.md": _copy_snapshot(home / "AGENTS.md", home, transaction),
        "skill_roots": [],
    }

    for path, roles in instructions.items():
        record, mutate = _target_record(path, global_source, home, transaction, roles)
        records.append(record)
        if mutate:
            actions.append((path, global_source))

    skill_records, skill_actions, skill_observations = _plan_skill_targets(
        home, skills_source, skill_roots, transaction
    )
    records.extend(skill_records)
    actions.extend(skill_actions)
    observations["skill_roots"] = skill_observations

    manifest: dict[str, Any] = {
        "version": MANIFEST_VERSION,
        "phase": "prepared",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "home": str(home),
        "repo_root": str(repo_root),
        "harnesses": selected,
        "backup_root": str(transaction),
        "created_dirs": _created_parents([path for path, _ in actions], home),
        "targets": records,
        "observations": observations,
    }
    _atomic_json(transaction / "manifest.json", manifest)
    _atomic_json(state_root / "active.json", manifest)

    for path, source in actions:
        _replace_with_link(path, source)

    manifest["phase"] = "installed"
    manifest["installed_at"] = datetime.now(timezone.utc).isoformat()
    _atomic_json(transaction / "manifest.json", manifest)
    _atomic_json(state_root / "active.json", manifest)
    return {
        "status": "installed",
        "manifest": str(state_root / "active.json"),
        "backup": str(transaction),
        "changed": len(actions),
    }


def _manifest_drift(
    manifest: dict[str, Any], *, ignored_paths: set[Path] | None = None
) -> list[str]:
    drift = []
    ignored_paths = ignored_paths or set()
    for target in manifest.get("targets", []):
        path = Path(target["path"])
        if path in ignored_paths:
            continue
        if not _matches_link(path, Path(target["source"])):
            drift.append(target["relative"])
    return drift


def _skills_available(root: Path, source: Path) -> bool:
    if root.exists() and root.resolve() == source.resolve():
        return True
    if not root.is_dir():
        return False
    return all(
        _matches_link(root / skill.name, skill) for skill in _skill_directories(source)
    )


def status(home: Path, repo_root: Path, harnesses: list[Harness]) -> dict[str, Any]:
    home = home.expanduser().absolute()
    repo_root = repo_root.expanduser().resolve()
    state_root = home / STATE_RELATIVE
    _relative(state_root / "active.json", home)
    active = _active_manifest(state_root)
    selected = [asdict(harness) for harness in harnesses]
    result: dict[str, Any] = {
        "home": str(home),
        "repo_root": str(repo_root),
        "active": active is not None,
        "harnesses": {},
    }
    for harness in harnesses:
        instruction = home.joinpath(*harness.instruction)
        skill_root = home.joinpath(*harness.skill_root)
        result["harnesses"][harness.name] = {
            "instruction": str(instruction),
            "instruction_ok": _matches_link(
                instruction, repo_root / "AGENTS.global.md"
            ),
            "skill_root": str(skill_root),
            "skills_ok": _skills_available(skill_root, repo_root / "skills"),
        }
    if active is not None:
        _validate_manifest_scope(active, home, Path(active["backup_root"]))
        result["phase"] = active.get("phase")
        result["manifest_harnesses"] = active.get("harnesses")
        result["drift"] = _manifest_drift(active)
        result["drift"].extend(
            f"{target['relative']} (retired repository skill)"
            for target in _retired_skill_records(active, repo_root / "skills")
        )
    result["selected"] = selected
    return result


def _backup_path(
    original: dict[str, Any], backup_root: Path, *, label: str
) -> Path | None:
    kind = original["kind"]
    if kind == "absent":
        return None
    if kind not in {"symlink", "directory", "file"}:
        raise InstallError(f"unsupported restore kind for {label}: {kind!r}")
    relative_value = original.get("backup")
    if not isinstance(relative_value, str) or not relative_value:
        raise InstallError(f"missing backup path for {label}")
    relative = Path(relative_value)
    if relative.is_absolute() or ".." in relative.parts:
        raise InstallError(f"backup path escapes transaction for {label}: {relative}")
    backup = backup_root / relative
    try:
        backup.parent.resolve(strict=False).relative_to(
            backup_root.resolve(strict=False)
        )
    except ValueError as exc:
        raise InstallError(
            f"backup parent escapes transaction for {label}: {backup}"
        ) from exc
    actual = _describe(backup)
    if _signature(actual) != _signature(original):
        raise InstallError(
            f"backup mismatch for {label}: expected {kind}, found {actual['kind']}"
        )
    return backup


def _validate_manifest_scope(
    manifest: dict[str, Any], home: Path, backup_root: Path
) -> None:
    _relative(backup_root / "manifest.json", home)
    for target in manifest.get("targets", []):
        _relative(Path(target["path"]), home)


def _preflight_restores(manifest: dict[str, Any], backup_root: Path) -> None:
    problems = []
    for target in manifest.get("targets", []):
        if not target.get("mutated"):
            continue
        try:
            _backup_path(
                target["original"], backup_root, label=target.get("relative", "?")
            )
        except (InstallError, KeyError) as exc:
            problems.append(str(exc))
    if problems:
        raise InstallError("restore preflight failed: " + "; ".join(problems))


def _restore(path: Path, original: dict[str, Any], backup_root: Path) -> None:
    kind = original["kind"]
    backup = _backup_path(original, backup_root, label=str(path))
    _remove_path(path)
    if kind == "absent":
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if kind == "symlink":
        assert backup is not None
        os.symlink(os.readlink(backup), path)
    elif kind == "directory":
        assert backup is not None
        shutil.copytree(backup, path, symlinks=True, copy_function=shutil.copy2)
    elif kind == "file" and original.get("backup_method") == "hardlink":
        assert backup is not None
        os.link(backup, path)
        with tempfile.TemporaryDirectory(
            dir=backup.parent, prefix=f".{backup.name}.detached-"
        ) as temporary_directory:
            detached = Path(temporary_directory) / "value"
            shutil.copy2(backup, detached, follow_symlinks=False)
            os.replace(detached, backup)
    elif kind == "file":
        assert backup is not None
        shutil.copy2(backup, path, follow_symlinks=False)
    else:
        raise InstallError(f"cannot restore unsupported object at {path}")


def uninstall(home: Path) -> dict[str, Any]:
    home = home.expanduser().absolute()
    state_root = home / STATE_RELATIVE
    _relative(state_root / "active.json", home)
    manifest = _active_manifest(state_root)
    if manifest is None:
        return {"status": "not-installed", "changed": 0}
    if manifest.get("home") != str(home):
        raise InstallError("active manifest belongs to a different --home")

    backup_root = Path(manifest["backup_root"])
    _validate_manifest_scope(manifest, home, backup_root)
    _preflight_restores(manifest, backup_root)

    conflicts = []
    for target in manifest.get("targets", []):
        if not target.get("mutated"):
            continue
        path = Path(target["path"])
        current = _describe(path)
        original = target["original"]
        if not _matches_link(path, Path(target["source"])) and _signature(
            current
        ) != _signature(original):
            conflicts.append(target["relative"])
    if conflicts:
        raise InstallError(
            "refusing to overwrite post-install changes: " + ", ".join(conflicts)
        )

    changed = 0
    for target in reversed(manifest.get("targets", [])):
        if target.get("mutated"):
            _restore(Path(target["path"]), target["original"], backup_root)
            changed += 1

    retained_dirs = []
    for relative in sorted(
        manifest.get("created_dirs", []),
        key=lambda value: len(Path(value).parts),
        reverse=True,
    ):
        path = home / relative
        try:
            path.rmdir()
        except FileNotFoundError:
            pass
        except OSError:
            retained_dirs.append(str(path))

    manifest["phase"] = "uninstalled"
    manifest["uninstalled_at"] = datetime.now(timezone.utc).isoformat()
    _atomic_json(backup_root / "manifest.json", manifest)
    (state_root / "active.json").unlink()
    return {
        "status": "uninstalled",
        "backup": str(backup_root),
        "changed": changed,
        "retained_dirs": retained_dirs,
    }

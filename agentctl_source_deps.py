"""Which in-repo files a run depends on, and the loading-phase watch over them.

Owns the dependency declaration (`--source-dep`, `--source-deps-file`,
`--source-deps-scan`), the static scan that follows an entry point's imports
and shell references, and the watch that holds those files fixed until the
payload has loaded them. Checking the files against a Git commit stays in
agentctl.py with the rest of the reproducibility guard; the project root,
hashing, clock and the means of stopping a payload are passed in by the caller.
"""

from __future__ import annotations

import argparse
import ast
import glob
import os
import re
import sys
import threading
import time
from collections.abc import Callable
from pathlib import Path

SOURCE_DEPS_SCHEMA = "agentctl-source-deps-v1"
DEFAULT_SOURCE_DEPS_LOADING_SECONDS = 120.0
SOURCE_DEPS_LOADED_ENV = "AGENTCTL_SOURCE_DEPS_LOADED"
SOURCE_DEPS_LOADED_FILENAME = "source-deps-loaded"
SOURCE_DEPS_SCAN_LIMITS = (
    "dynamic imports (importlib, __import__, exec), runtime-computed paths and "
    "data files are not seen; shell and pattern matches are regex heuristics"
)


def source_deps_request(args: argparse.Namespace) -> dict | None:
    """The launch's dependency declaration, or None for the whole-scope guard."""
    request = {
        "declared": list(getattr(args, "source_dep", None) or []),
        "declared_files": list(getattr(args, "source_deps_file", None) or []),
        "scan_entries": list(getattr(args, "source_deps_scan", None) or []),
        "scan_roots": list(getattr(args, "source_deps_root", None) or []),
        "scan_patterns": list(getattr(args, "source_deps_pattern", None) or []),
    }
    timeout = getattr(args, "source_deps_loading_timeout", None)
    request["loading_timeout_seconds"] = (
        DEFAULT_SOURCE_DEPS_LOADING_SECONDS if timeout is None else float(timeout)
    )
    if request["loading_timeout_seconds"] < 0:
        raise SystemExit("--source-deps-loading-timeout must be >= 0")
    if not (
        request["declared"] or request["declared_files"] or request["scan_entries"]
    ):
        if request["scan_roots"] or request["scan_patterns"]:
            raise SystemExit(
                "--source-deps-root/--source-deps-pattern need --source-deps-scan ENTRY"
            )
        return None
    for pattern in request["scan_patterns"]:
        try:
            re.compile(pattern)
        except re.error as exc:
            raise SystemExit(f"--source-deps-pattern {pattern!r}: {exc}") from exc
    return request


def _in_checkout(path: Path, git_root: Path) -> bool:
    try:
        path.relative_to(git_root)
    except ValueError:
        return False
    return True


def _declared_dep_paths(
    spec: str, origin: str, *, git_root: Path, project_root: Path
) -> list[Path]:
    """Expand one `--source-dep` path or glob, resolved against the project root."""
    base = Path(spec).expanduser()
    if not base.is_absolute():
        base = project_root / base
    if glob.has_magic(spec):
        matches = sorted(
            Path(match).resolve()
            for match in glob.glob(str(base), recursive=True)
            if Path(match).is_file()
        )
        if not matches:
            raise SystemExit(f"{origin}: glob matched no files: {spec}")
    else:
        resolved = base.resolve()
        if resolved.is_dir():
            raise SystemExit(
                f"{origin}: {spec} is a directory; name files or use a glob such as "
                f"{spec.rstrip('/')}/**/*.py"
            )
        if not resolved.is_file():
            raise SystemExit(f"{origin}: no such file: {spec}")
        matches = [resolved]
    for match in matches:
        if not _in_checkout(match, git_root):
            raise SystemExit(
                f"{origin}: {match} is outside the Git checkout {git_root}"
            )
    return matches


def read_source_deps_file(path: str, project_root: Path) -> list[str]:
    """One path or glob per line; blank lines and `#` comments are skipped."""
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = project_root / p
    try:
        lines = p.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise SystemExit(f"--source-deps-file {path}: {exc}") from exc
    return [
        line.strip()
        for line in lines
        if line.strip() and not line.strip().startswith("#")
    ]


_SHELL_PATH_RE = re.compile(
    r"""(?<![\w.-])((?:\$\{?\w+\}?/|\.\.?/|/)?[\w./-]*[\w-]\.(?:py|sh|bash))(?![\w.])"""
)
_SHELL_SOURCE_RE = re.compile(r"""(?:^|[\s;&|(])(?:source|\.)\s+["']?([^\s"';&|)]+)""")
_SHELL_PYTHON_MODULE_RE = re.compile(
    r"""\bpython[\d.]*\s+(?:-[A-Za-z]+\s+)*-m\s+([A-Za-z_][\w.]*)"""
)
_SHELL_SUFFIXES = {".sh", ".bash", ".zsh"}
# `uv run --script` starts a Python script that declares its own dependencies.
_PYTHON_INTERPRETER_RE = re.compile(r"python|\buv run\b")


def _script_language(path: Path, text: str) -> str:
    """`python` or `shell` by suffix, else by `#!` interpreter; "" when neither."""
    if path.suffix == ".py":
        return "python"
    if path.suffix in _SHELL_SUFFIXES:
        return "shell"
    if not text.startswith("#!"):
        return ""
    interpreter = text.split("\n", 1)[0].rsplit("/", 1)[-1]
    if _PYTHON_INTERPRETER_RE.search(interpreter):
        return "python"
    return "shell" if "sh" in interpreter else ""


class SourceDepScanner:
    """Collect the in-repo files an entry point reaches, without running it.

    Python imports resolve through `ast` against the module roots the payload
    would see (the entry's directory, the checkout root, the project root and
    any `--source-deps-root`), and a Python file inside a package brings the
    enclosing `__init__.py` files. Shell scripts and `--source-deps-pattern`
    patterns are regex heuristics. A file without a suffix is read as Python
    or shell by its `#!` line, and listed in `unresolved` when that names
    neither. Every file reached is scanned again, so imports of imports are
    found; a visited set stops cycles.
    """

    def __init__(
        self,
        *,
        git_root: Path,
        project_root: Path,
        roots: list[str],
        patterns: list[str],
    ):
        self.git_root = git_root
        self.project_root = project_root
        self.extra_roots = []
        for root in roots:
            p = Path(root).expanduser()
            self.extra_roots.append(
                (p if p.is_absolute() else project_root / p).resolve()
            )
        self.patterns = [re.compile(pattern) for pattern in patterns]
        self.found: dict[Path, dict] = {}
        self.unresolved: list[str] = []

    def _rel(self, path: Path) -> str:
        return path.relative_to(self.git_root).as_posix()

    def _add(self, path: Path, method: str, via: Path | None) -> bool:
        path = path.resolve()
        if not path.is_file() or not _in_checkout(path, self.git_root):
            return False
        if path in self.found:
            return False
        self.found[path] = {
            "method": method,
            "heuristic": method in {"shell-regex", "pattern-regex"},
            "via": self._rel(via) if via is not None else "",
        }
        return True

    def _note_unresolved(self, via: Path, reference: str) -> None:
        entry = f"{self._rel(via)}: {reference}"
        if entry not in self.unresolved:
            self.unresolved.append(entry)

    def scan(self, entry_spec: str) -> None:
        entry = Path(entry_spec).expanduser()
        if not entry.is_absolute():
            entry = self.project_root / entry
        entry = entry.resolve()
        if not entry.is_file():
            raise SystemExit(f"--source-deps-scan: no such file: {entry_spec}")
        if not _in_checkout(entry, self.git_root):
            raise SystemExit(
                f"--source-deps-scan: {entry} is outside the Git checkout {self.git_root}"
            )
        roots = []
        for root in (entry.parent, self.git_root, self.project_root, *self.extra_roots):
            if root not in roots:
                roots.append(root)
        self._add(entry, "entry", None)
        queue = [entry]
        scanned: set[Path] = set()
        while queue:
            current = queue.pop()
            if current in scanned:
                continue
            scanned.add(current)
            for path, method in self._references(current, roots):
                self._add(path, method, current)
                if path.resolve() not in scanned:
                    queue.append(path.resolve())

    def _references(self, path: Path, roots: list[Path]) -> list[tuple[Path, str]]:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            self._note_unresolved(path, f"unreadable: {exc}")
            return []
        refs: list[tuple[Path, str]] = []
        language = _script_language(path, text)
        if language == "python":
            refs.extend((p, "python-package") for p in self._package_inits(path))
            refs.extend((p, "python-ast") for p in self._python_refs(path, text, roots))
        elif language == "shell":
            refs.extend((p, "shell-regex") for p in self._shell_refs(path, text, roots))
        elif not path.suffix:
            # A suffix marks data; a bare name is usually an executable.
            self._note_unresolved(
                path, "unrecognized script type; its references were not scanned"
            )
        for pattern in self.patterns:
            for match in pattern.finditer(text):
                if "path" in pattern.groupindex:
                    token = match.group("path")
                elif pattern.groups:
                    token = match.group(1)
                else:
                    token = match.group(0)
                if not token:
                    continue
                resolved = self._resolve_token(token, path)
                if resolved is None:
                    self._note_unresolved(path, token)
                else:
                    refs.append((resolved, "pattern-regex"))
        return refs

    def _package_inits(self, path: Path) -> list[Path]:
        """`__init__.py` of each package enclosing `path`.

        They run when the file is imported or started with `python -m`, and
        no import statement in the file names them.
        """
        inits: list[Path] = []
        package = path.parent
        while (package / "__init__.py").is_file() and _in_checkout(
            package, self.git_root
        ):
            inits.append(package / "__init__.py")
            package = package.parent
        return inits

    def _module_files(self, module: str, roots: list[Path]) -> list[Path] | None:
        """Files executed by importing `module`; None when no root provides it."""
        parts = module.split(".")
        for root in roots:
            files: list[Path] = []
            base = root
            for index, part in enumerate(parts):
                package = base / part
                last = index == len(parts) - 1
                if (package / "__init__.py").is_file():
                    files.append(package / "__init__.py")
                    base = package
                elif last and (base / f"{part}.py").is_file():
                    files.append(base / f"{part}.py")
                elif package.is_dir():
                    base = package  # namespace package: no file of its own
                else:
                    break
            else:
                return files
        return None

    def _python_refs(self, path: Path, text: str, roots: list[Path]) -> list[Path]:
        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError as exc:
            self._note_unresolved(
                path, f"python parse error: {exc.msg} line {exc.lineno}"
            )
            return []
        out: list[Path] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    out.extend(self._module_files(alias.name, roots) or [])
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    package_dir = path.parent
                    for _ in range(node.level - 1):
                        package_dir = package_dir.parent
                    search = [package_dir]
                    module = node.module or ""
                    if module:
                        out.extend(self._module_files(module, search) or [])
                    prefix = f"{module}." if module else ""
                else:
                    search = roots
                    module = node.module or ""
                    out.extend(self._module_files(module, search) or [])
                    prefix = f"{module}."
                for alias in node.names:
                    if alias.name != "*":
                        # `from pkg import name` may name a submodule.
                        out.extend(
                            self._module_files(prefix + alias.name, search) or []
                        )
        return out

    def _resolve_token(self, token: str, via: Path) -> Path | None:
        token = token.strip("\"'")
        candidates: list[Path] = []
        variable = re.match(r"^\$\{?\w+\}?/(.*)$", token)
        if variable:
            rest = variable.group(1)
            candidates = [
                self.project_root / rest,
                self.git_root / rest,
                via.parent / rest,
            ]
        elif token.startswith("/"):
            candidates = [Path(token), via.parent / token.lstrip("/")]
        else:
            candidates = [
                via.parent / token,
                self.project_root / token,
                self.git_root / token,
            ]
        for candidate in candidates:
            resolved = candidate.resolve()
            if resolved.is_file() and _in_checkout(resolved, self.git_root):
                return resolved
        return None

    def _shell_refs(self, path: Path, text: str, roots: list[Path]) -> list[Path]:
        out: list[Path] = []
        for line in text.splitlines():
            if line.lstrip().startswith("#"):
                continue
            tokens = [m.group(1) for m in _SHELL_PATH_RE.finditer(line)]
            tokens += [
                m.group(1)
                for m in _SHELL_SOURCE_RE.finditer(line)
                if not m.group(1).startswith("$(")  # command substitution
            ]
            for token in dict.fromkeys(tokens):
                resolved = self._resolve_token(token, path)
                if resolved is None:
                    self._note_unresolved(path, token)
                else:
                    out.append(resolved)
            for match in _SHELL_PYTHON_MODULE_RE.finditer(line):
                files = self._module_files(match.group(1), roots)
                if files is None:
                    self._note_unresolved(path, f"python -m {match.group(1)}")
                else:
                    out.extend(files)
        return out


def resolve_source_deps(
    request: dict, *, git_root: Path, project_root: Path
) -> tuple[dict, dict]:
    """Expand a dependency request to `{path: provenance}` plus the scan record."""
    provenance: dict[Path, dict] = {}

    def note(path: Path, source: str, **detail) -> None:
        record = provenance.setdefault(
            path, {"provenance": [], "methods": [], "heuristic": True}
        )
        if source not in record["provenance"]:
            record["provenance"].append(source)
        method = detail.get("method", "declared")
        if method not in record["methods"]:
            record["methods"].append(method)
        # A file is heuristic only when every route that found it is.
        record["heuristic"] = record["heuristic"] and bool(detail.get("heuristic"))
        if detail.get("via") and "via" not in record:
            record["via"] = detail["via"]

    where = {"git_root": git_root, "project_root": project_root}
    for spec in request["declared"]:
        for path in _declared_dep_paths(spec, "--source-dep", **where):
            note(path, "declared")
    for deps_file in request["declared_files"]:
        origin = f"--source-deps-file {deps_file}"
        for spec in read_source_deps_file(deps_file, project_root):
            for path in _declared_dep_paths(spec, origin, **where):
                note(path, f"declared-file:{deps_file}")
    scan_record: dict = {}
    if request["scan_entries"]:
        scanner = SourceDepScanner(
            **where, roots=request["scan_roots"], patterns=request["scan_patterns"]
        )
        for entry in request["scan_entries"]:
            scanner.scan(entry)
        for path, info in scanner.found.items():
            note(path, "scanned", **info)
        scan_record = {
            "entries": list(request["scan_entries"]),
            "roots": [str(root) for root in scanner.extra_roots],
            "patterns": list(request["scan_patterns"]),
            "unresolved": scanner.unresolved,
            "limits": SOURCE_DEPS_SCAN_LIMITS,
        }
    return provenance, scan_record


class SourceDepsLoadingWatch:
    """Watch declared dependencies until the payload has loaded them.

    Loading ends at the first of: the payload touching the marker file
    (`$AGENTCTL_SOURCE_DEPS_LOADED`), the configured timeout after payload
    start, or payload exit. A change to a dependency before then is a
    violation: enforce calls `stop_payload`, which must stop the payload and
    everything it started; record keeps the violation. Later edits cannot
    affect what the payload already loaded and are ignored.
    """

    POLL_SECONDS = 0.25

    def __init__(
        self,
        deps: dict,
        *,
        marker: Path,
        guard_mode: str,
        proc,
        stop_payload: Callable[[], None],
        file_sha256: Callable[[str], str],
        utc_now: Callable[[], str],
        on_end=None,
    ):
        self.stop_payload = stop_payload
        self.file_sha256 = file_sha256
        self.utc_now = utc_now
        self.on_end = on_end
        self.files = {
            rel: record
            for rel, record in (deps.get("files") or {}).items()
            if record.get("sha256")
        }
        self.timeout = float(
            (deps.get("loading") or {}).get(
                "timeout_seconds", DEFAULT_SOURCE_DEPS_LOADING_SECONDS
            )
        )
        self.marker = marker
        self.guard_mode = guard_mode
        self.proc = proc
        self.violations: list[str] = []
        self.ended_by = ""
        self.ended_at = ""
        self.terminated = False
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        # No stat baseline: the first poll hashes every file, which also covers
        # the gap between the pre-launch check and payload start.
        self._stats: dict[str, object] = {}

    @staticmethod
    def _stat(path: str):
        try:
            st = os.stat(path)
        except OSError:
            return None
        return (st.st_ino, st.st_size, st.st_mtime_ns)

    def start(self) -> None:
        self._thread.start()

    def _check(self) -> None:
        for rel, record in self.files.items():
            stat = self._stat(record["path"])
            if rel in self._stats and stat == self._stats[rel]:
                continue
            self._stats[rel] = stat
            current = (
                self.file_sha256(record["path"]) if stat is not None else "missing"
            )
            if current == record["sha256"]:
                continue
            message = (
                "reproducibility guard: source dependency changed during payload "
                f"loading: {rel} sha256={current} recorded_sha256={record['sha256']}"
            )
            if message in self.violations:
                continue
            self.violations.append(message)
            if self.guard_mode == "enforce":
                print(f"{message}; terminating payload", file=sys.stderr)
                self.terminated = True
            else:
                print(
                    "warning: recorded source-guard violation, continuing "
                    f"(--source-guard enforce would terminate the payload): {message}",
                    file=sys.stderr,
                )

    def _end(self, reason: str) -> None:
        self.ended_by = reason
        self.ended_at = self.utc_now()
        if self.on_end is not None:
            self.on_end(self.record())

    def _run(self) -> None:
        deadline = time.monotonic() + self.timeout
        while True:
            self._check()
            if self.terminated:
                self.stop_payload()
                self._end("guard-terminated")
                return
            if self.marker.exists():
                self._end("marker")
                return
            if time.monotonic() >= deadline:
                self._end("timeout")
                return
            if self.proc.poll() is not None or self._stop.is_set():
                self._end("payload-exit")
                return
            self._stop.wait(self.POLL_SECONDS)

    def finish(self) -> dict:
        """Stop after payload exit and return the loading record."""
        self._stop.set()
        self._thread.join()
        return self.record()

    def record(self) -> dict:
        return {
            "timeout_seconds": self.timeout,
            "marker": str(self.marker),
            "ended_by": self.ended_by,
            "ended_at": self.ended_at,
            "violations": list(self.violations),
        }

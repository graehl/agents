"""Build outputs among the files `repo_view.py` serves: whether one is older
than its inputs, and rerunning its build.

An output is judged by the receipt its builder wrote beside it (input
hashes, and the command that rebuilds it), else as a Quarto project's render
product (input mtimes, `quarto render`). `Builds.freshness` answers for one
served file; `Builds.start` runs a stale output's build in the background.
Paths named `rel` or `source` are repository-relative POSIX paths.
"""

from __future__ import annotations

import hashlib
import json
import os
import posixpath
import re
import shutil
import signal
import subprocess
import tempfile
import threading
import time
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

# Files a Quarto project's render reads, by suffix. Prose (`.md`) and
# LaTeX-only inputs are left out: a project keeps notes and a kept `.tex`
# beside its sources, and counting them would call every build stale.
QUARTO_INPUT_SUFFIXES = frozenset(
    ".qmd .ipynb .yml .yaml .bib .csl .lua .css .scss .svg .png .jpg .jpeg .gif .webp".split()
)
QUARTO_OUTPUT_DIR = re.compile(
    r"""^[ \t]+output-dir:[ \t]*["']?([^"'\s#]+)""", re.MULTILINE
)
# Quarto renders one format of a project into its output directory.
QUARTO_FORMATS = {".html": "html", ".htm": "html", ".pdf": "pdf"}
# A document Quarto renders to an output of the same name in that directory.
QUARTO_DOCUMENT_SUFFIXES = (".qmd", ".ipynb", ".md", ".Rmd")
QUARTO_TIMEOUT = 600.0
HASH_CACHE_FILES = 4096
BUILD_RECORDS = 256


class RecentEntries(OrderedDict):
    """A mapping that keeps only the `limit` most recently set entries."""

    def __init__(self, limit: int):
        super().__init__()
        self.limit = limit

    def __setitem__(self, key, value) -> None:
        super().__setitem__(key, value)
        self.move_to_end(key)
        while len(self) > self.limit:
            self.popitem(last=False)


@dataclass(frozen=True)
class QuartoRender:
    """The Quarto project render that wrote a served file."""

    project: str  # the project directory ("" is the repository root)
    output: str  # its output directory
    form: str  # `quarto render --to <form>`


def quarto_render_of(root: Path, rel: str) -> QuartoRender | None:
    """The render whose product `rel` is: a file in the output directory of
    the nearest enclosing `_quarto.yml`, in a rendered format, at the path of
    one of the project's documents. Anything else there (a figure PDF, a
    library's HTML) is not a render product. The suffix is checked before
    the file system is."""
    form = QUARTO_FORMATS.get(posixpath.splitext(rel)[1].lower())
    if not form:
        return None
    project = posixpath.dirname(rel)
    while True:
        config = root / project / "_quarto.yml"
        if config.is_file():
            match = QUARTO_OUTPUT_DIR.search(config.read_text(encoding="utf-8"))
            if not match:
                return None
            output = posixpath.normpath(posixpath.join(project, match.group(1)))
            if not rel.startswith(output + "/"):
                return None
            document = root / project / rel[len(output) + 1 :]
            if not any(
                document.with_suffix(suffix).is_file()
                for suffix in QUARTO_DOCUMENT_SUFFIXES
            ):
                return None
            return QuartoRender(project, output, form)
        if not project:
            return None
        project = posixpath.dirname(project)


def newest_quarto_input(root: Path, render: QuartoRender) -> tuple[str, int] | None:
    """The most recently modified render input of a Quarto project, and its
    mtime in ns. Hidden files and directories (an editor's lock file) and the
    output directory are skipped."""
    top = root / render.project
    skip = root / render.output
    newest: tuple[str, int] | None = None
    for directory, dirs, files in os.walk(top):
        here = Path(directory)
        dirs[:] = [d for d in dirs if not d.startswith(".") and here / d != skip]
        for name in files:
            if (
                name.startswith(".")
                or Path(name).suffix.lower() not in QUARTO_INPUT_SUFFIXES
            ):
                continue
            try:
                mtime = (here / name).stat().st_mtime_ns
            except OSError:
                continue  # deleted meanwhile, or a dangling link: not an input
            if newest is None or mtime > newest[1]:
                rel = (here / name).relative_to(top).as_posix()
                newest = (posixpath.join(render.project, rel), mtime)
    return newest


def repository_rel(root: Path, path: Path) -> str:
    """`path` relative to the repository, or as given when outside it."""
    resolved = path.resolve()
    return (
        resolved.relative_to(root).as_posix() or "."
        if resolved.is_relative_to(root)
        else str(path)
    )


def tail(output: bytes, limit: int = 4000) -> str:
    return output[-limit:].decode("utf-8", "replace")


@dataclass(frozen=True)
class Recipe:
    """The command that rebuilds an output; `key` names one build, so
    concurrent requests for it share one run."""

    key: Path
    cwd: Path
    argv: tuple[str, ...]
    timeout: float

    def hint(self) -> str:
        return " ".join(Path(a).name if a.startswith("/") else a for a in self.argv)


@dataclass(frozen=True)
class Receipt:
    """A build receipt that describes a served output: the hashed inputs it
    was built from and the command that rebuilds it (`ya-artifact:v1`)."""

    home: Path  # directory receipt paths are relative to
    inputs: tuple[tuple[str, str], ...]  # (path relative to home, sha256)
    recipe: Recipe


@dataclass(frozen=True)
class Freshness:
    """What a page shown from a file reflects: a `stamp` that changes when
    the page would, and for a build output older than its inputs, `stale`
    (the reader's notice) and the `recipe` that rebuilds it, when known."""

    stamp: str
    stale: dict | None = None
    recipe: Recipe | None = None

    def report(self) -> dict:
        """The JSON a page carries and `?repo-view=fresh` answers."""
        return {"stamp": self.stamp, "stale": self.stale}


class Builds:
    """Finds the receipts behind build outputs, judges their freshness by
    input hashes, and (with `serve --rebuild`) reruns a stale output's
    declared command, one run per receipt at a time."""

    def __init__(self, root: Path, enabled: bool, log: Callable[[str, str], None]):
        self.root, self.enabled, self.log = root, enabled, log
        self._lock = threading.Lock()
        self._hashes: RecentEntries = RecentEntries(HASH_CACHE_FILES)
        # Per recipe key: when the run in progress started, on the monotonic
        # clock; and the last finished run's result.
        self._running: dict[Path, float] = {}
        self._began_ms: dict[Path, int] = {}
        self._finished: RecentEntries = RecentEntries(BUILD_RECORDS)
        # Which build a page last started, so it can ask how that build went
        # after the output is current and no recipe is stale any more.
        self._started_for: RecentEntries = RecentEntries(BUILD_RECORDS)
        # Per receipt file: its parsed JSON (or the reason it is not a
        # receipt) at one version, so requests for its neighbours reparse and
        # report nothing until the file changes.
        self._receipt_files: RecentEntries = RecentEntries(BUILD_RECORDS)
        # Per recipe key: when its last run started (ms since the epoch), kept
        # while that run is the latest and failed.
        self._failed_since: RecentEntries = RecentEntries(BUILD_RECORDS)
        # Per (recipe key, output): the freshness stamp `start_once` last
        # started the build for.
        self._started_once: RecentEntries = RecentEntries(BUILD_RECORDS)

    def sha256(self, path: Path) -> str | None:
        """The file's content hash, cached by its stat; None when unreadable."""
        try:
            stat = path.stat()
            stamp = (stat.st_mtime_ns, stat.st_size)
            with self._lock:
                cached = self._hashes.get(path)
            if cached and cached[0] == stamp:
                return cached[1]
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            return None
        with self._lock:
            self._hashes[path] = (stamp, digest)
        return digest

    def receipt(self, rel: str) -> Receipt | None:
        """The receipt beside `rel` that lists it as an output and records its
        current content. A file of another shape is not a receipt, and one
        whose output another build has since replaced no longer describes it."""
        target = (self.root / rel).resolve()
        for candidate in sorted(target.parent.glob("*.receipt.json")):
            data = self._receipt_json(candidate)
            if data is None:
                continue
            try:
                receipt = self._receipt_for(target, candidate, data)
            except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
                self._not_a_receipt(candidate, error)
                continue
            if receipt:
                return receipt
        return None

    def _receipt_json(self, candidate: Path) -> dict | None:
        """`candidate` parsed, once per version of the file; None when it does
        not parse, which is logged once per version."""
        try:
            stat = candidate.stat()
        except OSError:
            return None
        version = (stat.st_mtime_ns, stat.st_size)
        with self._lock:
            cached = self._receipt_files.get(candidate)
        if cached and cached[0] == version:
            return cached[1]
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise TypeError("not a JSON object")
        except (OSError, ValueError, TypeError) as error:
            data = None
            self.log("fresh", f"{candidate}: not read as a receipt: {error!r}")
        with self._lock:
            self._receipt_files[candidate] = (version, data, data is None)
        return data

    def _not_a_receipt(self, candidate: Path, error: Exception) -> None:
        """Log, once per version of the file, that its shape is not a receipt's:
        a builder that changes its schema would otherwise only lose its notice."""
        with self._lock:
            cached = self._receipt_files.get(candidate)
            reported = cached is None or cached[2]
            if cached and not reported:
                self._receipt_files[candidate] = (cached[0], cached[1], True)
        if not reported:
            self.log("fresh", f"{candidate}: not read as a receipt: {error!r}")

    def _receipt_for(self, target: Path, candidate: Path, data: dict) -> Receipt | None:
        """`candidate`'s `data` as a receipt for `target`; raises on any other shape."""
        command = data["artifact_metadata"]["regenerate"]["proposedRegistration"]
        if target not in {Path(output).resolve() for output in command["outputs"]}:
            return None
        home = Path(data["root"]).parent
        recorded = [
            data[key]
            for key in ("output", "pdf", "source_map")
            if isinstance(data.get(key), dict)
        ]
        if not any(
            (home / item["path"]).resolve() == target
            and item["sha256"] == self.sha256(target)
            for item in recorded
        ):
            return None
        argv = command["argv"]
        if not (
            isinstance(argv, list) and argv and all(isinstance(a, str) for a in argv)
        ):
            raise TypeError("argv is not a list of strings")
        return Receipt(
            home,
            tuple((str(Path(i["path"])), str(i["sha256"])) for i in data["inputs"]),
            Recipe(
                candidate,
                Path(command["cwd"]),
                tuple(argv),
                float(command.get("timeoutSeconds", 180)),
            ),
        )

    def changed_inputs(self, receipt: Receipt) -> list[tuple[str, int]]:
        """Inputs whose content differs from the receipt, with mtime in ns
        (0 when missing), newest first."""
        changed = []
        for rel, digest in receipt.inputs:
            path = receipt.home / rel
            if self.sha256(path) != digest:
                mtime = path.stat().st_mtime_ns if path.exists() else 0
                changed.append((rel, mtime))
        return sorted(changed, key=lambda item: -item[1])

    def quarto_recipe(self, render: QuartoRender) -> Recipe | None:
        """`quarto render --to <format>` in the project, when Quarto is installed."""
        quarto = shutil.which("quarto")
        if not quarto:
            return None
        project = self.root / render.project
        return Recipe(
            project / f".quarto-{render.form}",
            project,
            (quarto, "render", "--to", render.form),
            QUARTO_TIMEOUT,
        )

    def freshness(self, source: str) -> Freshness:
        """A receipt decides by input hashes; without one, a Quarto render
        product is judged by input mtimes and rebuilt by Quarto itself."""
        stat = (self.root / source).stat()
        stamp = f"{stat.st_mtime_ns}:{stat.st_size}"
        receipt = self.receipt(source)
        if receipt:
            changed = self.changed_inputs(receipt)
            stamp += "/" + ",".join(f"{rel}:{mtime}" for rel, mtime in changed)
            if not changed:
                return Freshness(stamp)
            project = repository_rel(self.root, receipt.home)
            newest = (
                repository_rel(self.root, receipt.home / changed[0][0]),
                changed[0][1],
            )
            recipe, hint = receipt.recipe, receipt.recipe.hint()
        else:
            render = quarto_render_of(self.root, source)
            newest = render and newest_quarto_input(self.root, render)
            if not newest:
                return Freshness(stamp)
            stamp += f"/{newest[0]}:{newest[1]}"
            if newest[1] <= stat.st_mtime_ns:
                return Freshness(stamp)
            project = render.project or "."
            recipe = self.quarto_recipe(render)
            hint = recipe.hint() if recipe else "quarto render"
        stale = {
            "project": project,
            "input": newest[0],
            "inputTime": newest[1] // 1_000_000,
            "builtTime": stat.st_mtime_ns // 1_000_000,
            "rebuild": self.enabled and recipe is not None,
            "hint": hint,
        }
        return Freshness(stamp, stale, recipe)

    def start(self, recipe: Recipe, source: str) -> dict:
        """Start the recipe's command in the background (or join the run
        already going) for the page shown from `source`; its status."""
        with self._lock:
            self._started_for[source] = recipe.key
            starter = recipe.key not in self._running
            if starter:
                self._running[recipe.key] = time.monotonic()
                self._began_ms[recipe.key] = time.time_ns() // 1_000_000
        if starter:
            threading.Thread(target=self._complete, args=(recipe,), daemon=True).start()
        return self.status(source)

    def start_once(self, recipe: Recipe, source: str, fresh: Freshness) -> None:
        """Start the build of a stale output that was opened where no notice
        can offer it (a PDF in a viewer), once per state of the output and
        its inputs: a build that fails, or leaves the output stale, is not
        rerun by every request, nor for each output its command would make."""
        # Per output: every PDF of one project shares a recipe and has its own
        # stamp, so a per-recipe memory would restart on alternating requests.
        once = (recipe.key, source)
        newest_input = (fresh.stale or {}).get("inputTime", 0)
        with self._lock:
            if self._started_once.get(once) == fresh.stamp:
                return
            self._started_once[once] = fresh.stamp
            if self._failed_since.get(recipe.key, -1) >= newest_input:
                # The command already failed on these inputs, for a sibling.
                self._started_for[source] = recipe.key
                return
        self.start(recipe, source)

    def status(self, source: str) -> dict:
        """How the build last started for `source` stands: `running` with
        `elapsed` seconds, `done` or `failed` with `seconds` and `log`, or
        `none` when this server started none (it may have restarted)."""
        with self._lock:
            key = self._started_for.get(source)
            started = self._running.get(key)
            finished = self._finished.get(key)
        if started is not None:
            return {"state": "running", "elapsed": round(time.monotonic() - started, 1)}
        if not finished:
            return {"state": "none"}
        return {"state": "done" if finished["ok"] else "failed", **finished}

    def _complete(self, recipe: Recipe) -> None:
        try:
            result = self._run(recipe)
        except Exception as error:  # reported to the pages asking about the run
            result = {"ok": False, "log": f"{type(error).__name__}: {error}"}
        with self._lock:
            started = self._running.pop(recipe.key)
            began_ms = self._began_ms.pop(recipe.key)
            result["seconds"] = round(time.monotonic() - started, 1)
            self._finished[recipe.key] = result
            self._failed_since[recipe.key] = -1 if result["ok"] else began_ms

    def _run(self, recipe: Recipe) -> dict:
        cwd = recipe.cwd.resolve()
        if not cwd.is_relative_to(self.root):
            return {
                "ok": False,
                "log": f"rebuild directory {cwd} is outside the repository",
            }
        environment = dict(os.environ)
        # A sandboxed app sees a read-only home; Quarto needs writable data
        # and cache directories.
        for name, default in (
            ("XDG_DATA_HOME", Path.home() / ".local" / "share"),
            ("XDG_CACHE_HOME", Path.home() / ".cache"),
        ):
            if not os.access(environment.get(name, default), os.W_OK):
                scratch = Path(tempfile.gettempdir()) / "repo-view" / name.lower()
                scratch.mkdir(parents=True, exist_ok=True)
                environment[name] = str(scratch)
        self.log("rebuild", f"{recipe.key}: {' '.join(recipe.argv)}")
        process = subprocess.Popen(
            recipe.argv,
            cwd=cwd,
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        try:
            output, _ = process.communicate(timeout=recipe.timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                output, _ = process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                output, _ = process.communicate()
            return {
                "ok": False,
                "log": f"timed out after {recipe.timeout:g} s\n" + tail(output),
            }
        self.log("rebuild", f"{recipe.key}: exit {process.returncode}")
        return {"ok": process.returncode == 0, "log": tail(output)}

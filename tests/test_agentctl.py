#!/usr/bin/env python3
"""End-to-end test suite for agentctl + aim plugin.

Stdlib only (no pytest dependency). Each test runs in its own tmp workspace
with a fresh copy of agentctl; no shared state. Run directly:

    python3 tests/test_agentctl.py            # run all
    python3 tests/test_agentctl.py -k chain   # run tests matching 'chain'
    python3 tests/test_agentctl.py -v         # verbose

Exits non-zero on any failure.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTCTL_FILES = ("agentctl", "agentctl.py", "artifact_meta.py")
AGENTCTL_DIRS = ("agentctl_plugins",)


# ---- Workspace fixture ----------------------------------------------------


class Workspace:
    """Isolated agentctl workspace under a tmp dir; auto-cleans on context exit."""

    def __init__(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="agentctl-test-"))
        for f in AGENTCTL_FILES:
            shutil.copy2(REPO_ROOT / f, self.tmp / f)
        for d in AGENTCTL_DIRS:
            shutil.copytree(REPO_ROOT / d, self.tmp / d)
        (self.tmp / "agentctl").chmod(0o755)
        # Sandbox for test artifacts (separate from the agentctl source)
        self.scratch = self.tmp / "_scratch"
        self.scratch.mkdir()

    def cleanup(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run(self, *args, env_extra=None, timeout=20) -> subprocess.CompletedProcess:
        env = os.environ.copy()
        if env_extra:
            env.update(env_extra)
        return subprocess.run(
            [str(self.tmp / "agentctl"), *map(str, args)],
            cwd=self.tmp,
            capture_output=True,
            text=True,
            env=env,
            timeout=timeout,
        )

    def state(self, job: str, run_id: str | None = None) -> dict:
        if run_id is None:
            return json.loads((self.tmp / ".agentctl/jobs" / job / "current.json").read_text())
        return json.loads((self.tmp / ".agentctl/runs" / job / run_id / "state.json").read_text())

    def wait_finished(self, job: str, *, since_run_id: str | None = None, timeout: float = 10.0) -> dict:
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                s = self.state(job)
                if s.get("status") == "finished" and s.get("run_id") != since_run_id:
                    return s
            except (FileNotFoundError, json.JSONDecodeError):
                pass
            time.sleep(0.05)
        raise TimeoutError(f"job {job!r} did not finish within {timeout}s")

    def dump_path(self, experiment: str, run_id: str) -> Path:
        return self.tmp / "runs/aim" / experiment / "runs" / f"{run_id}.json"


# ---- Test helpers ----------------------------------------------------------


def _assert(cond, msg="assertion failed"):
    if not cond:
        raise AssertionError(msg)


def _start(ws: Workspace, *args) -> subprocess.CompletedProcess:
    """Convenience wrapper for `agentctl start ...`. Asserts rc==0."""
    res = ws.run("start", *args)
    _assert(res.returncode == 0, f"agentctl start failed: rc={res.returncode}\nstdout: {res.stdout}\nstderr: {res.stderr}")
    return res


# ---- Tests -----------------------------------------------------------------


def test_no_aim_writes_nothing():
    ws = Workspace()
    try:
        _start(ws, "--no-aim", "trivial", "--", "true")
        ws.wait_finished("trivial")
        _assert(not (ws.tmp / "runs").exists(), "runs/ should not exist for --no-aim")
    finally:
        ws.cleanup()


def test_tracked_writes_dump_and_sidecar():
    ws = Workspace()
    try:
        out = ws.scratch / "out.bin"
        _start(ws, "--experiment", "e1", "--output", f"result={out}",
               "tracked", "--", "bash", "-c", f"echo hello > {out}")
        s = ws.wait_finished("tracked")
        exp_dir = ws.tmp / "runs/aim/e1"
        _assert((exp_dir / "manifest.jsonl").exists(), "manifest.jsonl missing")
        dumps = list((exp_dir / "runs").glob("*.json"))
        _assert(len(dumps) == 1, f"expected 1 dump, got {len(dumps)}")
        texts = list((exp_dir / "texts").rglob("meta.markdown.md"))
        _assert(len(texts) == 1, f"expected 1 text snapshot, got {len(texts)}")
        sidecar_path = Path(f"{out}.meta.json")
        _assert(sidecar_path.exists(), "output sidecar not written")
        sidecar = json.loads(sidecar_path.read_text())
        _assert(sidecar["agentctl_run_id"] == s["run_id"])
        _assert(sidecar["output_key"] == "result")
        _assert(sidecar["experiment"] == "e1")
    finally:
        ws.cleanup()


def test_chain_resolves_source():
    ws = Workspace()
    try:
        out1 = ws.scratch / "step1.txt"
        out2 = ws.scratch / "step2.txt"
        _start(ws, "--experiment", "ch", "--output", f"r={out1}",
               "step1", "--", "bash", "-c", f"echo hello > {out1}")
        s1 = ws.wait_finished("step1")
        _start(ws, "--experiment", "ch",
               "--input", f"prev={out1}", "--output", f"f={out2}",
               "step2", "--", "bash", "-c", f"cat {out1} > {out2}")
        s2 = ws.wait_finished("step2")
        inp = s2["inputs"]["prev"]
        _assert(inp["source_run_id"] == s1["run_id"], "source_run_id mismatch")
        _assert(inp["source_experiment"] == "ch", "source_experiment mismatch")
        _assert(inp["path"] == str(out1), "path mismatch")
        _assert(inp["source_origin"] == str(out1), "source_origin mismatch")
        _assert("source_command_text" in inp, "source_command_text missing")
    finally:
        ws.cleanup()


def test_input_raw_no_translation():
    ws = Workspace()
    try:
        f = ws.scratch / "f.txt"
        f.write_text("x")
        _start(ws, "--experiment", "e", "--input-raw", f"data={f}",
               "rawjob", "--", "true")
        s = ws.wait_finished("rawjob")
        _assert(s["inputs"]["data"]["raw"] is True, "raw flag missing")
        _assert(not any("--data=" in a for a in s["argv"]),
                f"--data= should NOT be in argv, got {s['argv']!r}")
    finally:
        ws.cleanup()


def test_input_translation_appends_to_argv():
    ws = Workspace()
    try:
        f = ws.scratch / "f.txt"
        f.write_text("x")
        _start(ws, "--experiment", "e", "--input", f"data={f}",
               "trjob", "--", "true")
        s = ws.wait_finished("trjob")
        _assert(any(a == f"--data={f}" for a in s["argv"]),
                f"--data={f} expected in argv, got {s['argv']!r}")
        _assert(s["inputs"]["data"].get("raw") is not True,
                "non-raw input should not be marked raw")
    finally:
        ws.cleanup()


def test_input_hash_at_launch():
    ws = Workspace()
    try:
        f = ws.scratch / "in.bin"
        content = b"known content"
        f.write_bytes(content)
        _start(ws, "--experiment", "e", "--input-hash", f"data={f}",
               "ihash", "--", "true")
        s = ws.wait_finished("ihash")
        expected = hashlib.sha256(content).hexdigest()
        _assert(s["inputs"]["data"]["sha256"] == expected,
                f"sha256 mismatch: got {s['inputs']['data'].get('sha256')!r}")
    finally:
        ws.cleanup()


def test_output_hash_at_completion():
    ws = Workspace()
    try:
        out = ws.scratch / "out.bin"
        _start(ws, "--experiment", "e", "--output-hash", f"r={out}",
               "ohash", "--", "bash", "-c", f"printf 'content' > {out}")
        s = ws.wait_finished("ohash")
        expected = hashlib.sha256(b"content").hexdigest()
        _assert(s["outputs"]["r"]["sha256"] == expected,
                f"output sha256 mismatch: got {s['outputs']['r'].get('sha256')!r}")
    finally:
        ws.cleanup()


def test_multiple_inputs_outputs():
    ws = Workspace()
    try:
        a = ws.scratch / "a.txt"; a.write_text("a")
        b = ws.scratch / "b.txt"; b.write_text("b")
        o1 = ws.scratch / "o1.txt"
        o2 = ws.scratch / "o2.txt"
        _start(ws, "--experiment", "e",
               "--input", f"first={a}", "--input", f"second={b}",
               "--output", f"x={o1}", "--output", f"y={o2}",
               "multi", "--", "bash", "-c", f"echo X > {o1}; echo Y > {o2}")
        s = ws.wait_finished("multi")
        _assert(set(s["inputs"].keys()) == {"first", "second"},
                f"inputs keys: {list(s['inputs'].keys())}")
        _assert(set(s["outputs"].keys()) == {"x", "y"},
                f"outputs keys: {list(s['outputs'].keys())}")
        _assert(Path(f"{o1}.meta.json").exists(), "o1 sidecar missing")
        _assert(Path(f"{o2}.meta.json").exists(), "o2 sidecar missing")
    finally:
        ws.cleanup()


def test_symlink_records_realpath():
    ws = Workspace()
    try:
        target = ws.scratch / "target.txt"
        target.write_text("data")
        link = ws.scratch / "link.txt"
        link.symlink_to(target)
        # Use absolute symlink path so stat_artifact records realpath when it
        # differs from path (relative paths get pre-resolved).
        _start(ws, "--experiment", "e", "--input", f"data={link}",
               "symjob", "--", "true")
        s = ws.wait_finished("symjob")
        inp = s["inputs"]["data"]
        # When the user passed an absolute symlink, path is the link itself
        # and realpath is the target.
        _assert(inp["path"] == str(link), f"path expected to be link, got {inp['path']!r}")
        _assert(inp.get("realpath") == str(target.resolve()),
                f"realpath expected {target.resolve()!r}, got {inp.get('realpath')!r}")
    finally:
        ws.cleanup()


def test_directory_input():
    ws = Workspace()
    try:
        d = ws.scratch / "dir"
        d.mkdir()
        (d / "a.txt").write_bytes(b"aaa")
        (d / "b.txt").write_bytes(b"bbbb")
        _start(ws, "--experiment", "e", "--input", f"data={d}",
               "dirjob", "--", "true")
        s = ws.wait_finished("dirjob")
        inp = s["inputs"]["data"]
        _assert(inp.get("is_dir") is True, "is_dir not True")
        _assert(inp["size"] == 7, f"recursive size expected 7, got {inp['size']!r}")
    finally:
        ws.cleanup()


def test_input_no_sidecar_omits_source():
    ws = Workspace()
    try:
        f = ws.scratch / "untracked.txt"
        f.write_text("preexisting")
        _start(ws, "--experiment", "e", "--input", f"data={f}",
               "leaf", "--", "true")
        s = ws.wait_finished("leaf")
        inp = s["inputs"]["data"]
        _assert("source_run_id" not in inp, "source_run_id should be absent for untracked input")
        _assert("source_dump" not in inp, "source_dump should be absent")
        _assert(inp["path"] == str(f))
    finally:
        ws.cleanup()


def test_missing_output_recorded():
    ws = Workspace()
    try:
        out = ws.scratch / "never_created.bin"
        # Command exits 0 without creating out.
        _start(ws, "--experiment", "e", "--output", f"r={out}",
               "missjob", "--", "true")
        s = ws.wait_finished("missjob")
        _assert(s["outputs"]["r"].get("status") == "missing",
                f"expected status=missing, got {s['outputs']['r']!r}")
        _assert(not Path(f"{out}.meta.json").exists(),
                "sidecar should NOT be written for missing output")
    finally:
        ws.cleanup()


def test_static_propagation():
    ws = Workspace()
    try:
        out = ws.scratch / "out.txt"
        _start(ws, "--experiment", "e", "--output", f"r={out}",
               "--propagate-json", '{"loss": 0.5}',
               "prop", "--", "bash", "-c", f"echo x > {out}")
        s = ws.wait_finished("prop")
        _assert(s["propagate"] == {"loss": 0.5}, f"state.propagate: {s['propagate']!r}")
        sidecar = json.loads(Path(f"{out}.meta.json").read_text())
        _assert(sidecar.get("propagate") == {"loss": 0.5},
                f"sidecar.propagate: {sidecar.get('propagate')!r}")
    finally:
        ws.cleanup()


def test_cooperative_propagation():
    ws = Workspace()
    try:
        out = ws.scratch / "out.txt"
        _start(ws, "--experiment", "e", "--output", f"r={out}",
               "coop", "--", "bash", "-c",
               f'echo x > {out}; echo \'{{"acc": 0.9}}\' > "$AGENTCTL_RUN_DIR/propagate.json"')
        s = ws.wait_finished("coop")
        _assert(s["propagate"] == {"acc": 0.9},
                f"state.propagate: {s['propagate']!r}")
    finally:
        ws.cleanup()


def test_propagation_chain():
    ws = Workspace()
    try:
        out1 = ws.scratch / "o1.txt"
        out2 = ws.scratch / "o2.txt"
        _start(ws, "--experiment", "ch", "--output", f"r={out1}",
               "--propagate-json", '{"k": "v"}',
               "p1", "--", "bash", "-c", f"echo x > {out1}")
        ws.wait_finished("p1")
        _start(ws, "--experiment", "ch",
               "--input", f"prev={out1}", "--output", f"f={out2}",
               "p2", "--", "bash", "-c", f"cat {out1} > {out2}")
        s = ws.wait_finished("p2")
        _assert(s["inputs"]["prev"].get("source_facts") == {"k": "v"},
                f"source_facts: {s['inputs']['prev'].get('source_facts')!r}")
    finally:
        ws.cleanup()


def test_nested_agentctl_parent_run():
    ws = Workspace()
    try:
        inner_out = ws.scratch / "inner.txt"
        inner_script = ws.scratch / "inner.sh"
        inner_script.write_text(
            "#!/usr/bin/env bash\n"
            f'{ws.tmp / "agentctl"} start --experiment nest --output r={inner_out} '
            f'inner -- bash -c \'echo hi > {inner_out}\'\n'
            "sleep 1\n"
        )
        inner_script.chmod(0o755)
        _start(ws, "--experiment", "nest", "outer", "--", str(inner_script))
        outer = ws.wait_finished("outer")
        inner = ws.wait_finished("inner")
        _assert(inner.get("parent_run") == outer["run_id"],
                f"inner.parent_run: {inner.get('parent_run')!r} expected {outer['run_id']!r}")
        _assert(outer.get("parent_run", "") == "",
                f"outer.parent_run should be empty, got {outer.get('parent_run')!r}")
    finally:
        ws.cleanup()


def test_script_override():
    ws = Workspace()
    try:
        sc = ws.scratch / "code.py"
        sc.write_bytes(b"# hello")
        _start(ws, "--experiment", "e", "--script", str(sc),
               "scov", "--", "bash", "-c", "true")
        s = ws.wait_finished("scov")
        _assert(s["script"]["path"] == str(sc.resolve()),
                f"script.path: {s['script']['path']!r}")
        expected = hashlib.sha256(b"# hello").hexdigest()
        _assert(s["script"]["sha256"] == expected, "script sha256 mismatch")
    finally:
        ws.cleanup()


def test_restart_preserves_declarations():
    ws = Workspace()
    try:
        f = ws.scratch / "in.txt"
        f.write_text("data")
        out = ws.scratch / "out.txt"
        sc = ws.scratch / "s.sh"
        sc.write_text("#!/bin/sh\nexit 0\n")
        sc.chmod(0o755)
        _start(ws, "--experiment", "rs",
               "--input-hash", f"data={f}",
               "--output-hash", f"r={out}",
               "--script", str(sc),
               "--propagate-json", '{"k": "v"}',
               "rsjob", "--", "bash", "-c", f"echo hi > {out}")
        s1 = ws.wait_finished("rsjob")
        # Restart: must preserve declarations.
        rc = ws.run("restart", "rsjob")
        _assert(rc.returncode == 0, f"restart failed: {rc.stderr}")
        s2 = ws.wait_finished("rsjob", since_run_id=s1["run_id"])
        _assert(s2["inputs"]["data"].get("sha256"), "restart lost --input-hash sha256")
        _assert(s2["outputs"]["r"].get("sha256"), "restart lost --output-hash sha256")
        _assert(s2["script"]["path"] == s1["script"]["path"], "script path drift on restart")
        _assert(s2["propagate"] == {"k": "v"}, f"propagate lost: {s2['propagate']!r}")
    finally:
        ws.cleanup()


def test_plugin_loader_skips_broken():
    ws = Workspace()
    try:
        broken = ws.tmp / "agentctl_plugins" / "broken_zzz.py"
        broken.write_text("import this_module_definitely_does_not_exist_xyz123\n")
        # --help must still work (the aim plugin is loaded; broken one warns).
        rc = ws.run("--help")
        _assert(rc.returncode == 0, f"--help failed with broken plugin: rc={rc.returncode}")
        _assert("warning" in rc.stderr.lower() and "broken_zzz" in rc.stderr,
                f"expected warning about broken_zzz, stderr={rc.stderr!r}")
        # aim's own --no-aim should still appear in start --help
        rc2 = ws.run("start", "--help")
        _assert("--no-aim" in rc2.stdout, "aim plugin failed to register despite broken sibling")
    finally:
        ws.cleanup()


def test_research_aim_back_compat_search():
    """find_aim_run_record falls back to research/aim/ when runs/aim/ has no match."""
    ws = Workspace()
    try:
        # Place a fake legacy dump.
        legacy_dump = ws.tmp / "research/aim/legacy/runs/r1.json"
        legacy_dump.parent.mkdir(parents=True, exist_ok=True)
        meta_target = ws.scratch / "fake.meta.md"
        meta_target.write_text("# fake\n")
        legacy_record = {
            "params": {
                "output": {"meta_path": str(meta_target.resolve())}
            },
            "source": {"aim_run_hash": "abc123def456"},
        }
        legacy_dump.write_text(json.dumps(legacy_record))

        # Find Python and call find_aim_run_record.
        py = sys.executable
        code = (
            f'import sys; sys.path.insert(0, {str(ws.tmp)!r}); '
            f'import artifact_meta; '
            f'r = artifact_meta.find_aim_run_record('
            f'meta_path={str(meta_target.resolve())!r}, '
            f'setup=[("aim_run_hash","abc123def456")], '
            f'repo_root={str(ws.tmp)!r}); '
            f'print("FOUND" if r else "NOT_FOUND")'
        )
        result = subprocess.run([py, "-c", code], capture_output=True, text=True, cwd=ws.tmp)
        _assert("FOUND" in result.stdout,
                f"back-compat search failed: stdout={result.stdout!r} stderr={result.stderr!r}")
    finally:
        ws.cleanup()


def test_cleanup_running_accepts_output_or_marker_path():
    ws = Workspace()
    try:
        out = ws.scratch / "manual.out"
        marker = Path(f"{out}.running.md")
        marker.write_text("- status: running\n")
        rc = ws.run("cleanup-running", str(out))
        _assert(rc.returncode == 0, f"cleanup-running failed: {rc.stderr}")
        _assert(not marker.exists(), "cleanup-running did not remove marker via output path")
        marker.write_text("- status: running\n")
        rc = ws.run("cleanup-running", str(marker))
        _assert(rc.returncode == 0, f"cleanup-running marker path failed: {rc.stderr}")
        _assert(not marker.exists(), "cleanup-running did not remove marker path directly")
    finally:
        ws.cleanup()


def test_cleanup_running_scan_reports_recovery_state():
    ws = Workspace()
    try:
        completed = ws.scratch / "completed.out"
        completed.write_text("done")
        Path(f"{completed}.meta.md").write_text("# done\n")
        completed_marker = Path(f"{completed}.running.md")
        completed_marker.write_text(f"- status: running\n- pid: 99999999\n- out: {completed}\n")

        interrupted = ws.scratch / "interrupted.out"
        interrupted_marker = Path(f"{interrupted}.running.md")
        interrupted_marker.write_text(f"- status: running\n- pid: 99999999\n- out: {interrupted}\n")

        live = ws.scratch / "live.out"
        live_marker = Path(f"{live}.running.md")
        live_marker.write_text(f"- status: running\n- pid: {os.getpid()}\n- out: {live}\n")

        rc = ws.run("cleanup-running")
        _assert(rc.returncode == 0, f"cleanup-running scan failed: {rc.stderr}")
        _assert(not completed_marker.exists(), "completed marker should be removed")
        _assert(interrupted_marker.exists(), "interrupted marker should be kept")
        _assert(live_marker.exists(), "live marker should be kept")
        _assert("completed removed" in rc.stdout, f"completed status missing: {rc.stdout!r}")
        _assert("interrupted kept" in rc.stdout, f"interrupted status missing: {rc.stdout!r}")
        _assert("running kept" in rc.stdout, f"running status missing: {rc.stdout!r}")
    finally:
        ws.cleanup()


# ---- Runner ----------------------------------------------------------------


def _collect_tests():
    return [(name, fn) for name, fn in sorted(globals().items())
            if name.startswith("test_") and callable(fn)]


def main(argv):
    verbose = "-v" in argv
    matches = []
    if "-k" in argv:
        idx = argv.index("-k")
        if idx + 1 < len(argv):
            matches.append(argv[idx + 1])

    tests = _collect_tests()
    if matches:
        tests = [(n, f) for n, f in tests if any(m in n for m in matches)]

    passed = failed = 0
    failures = []
    start_total = time.time()
    for name, fn in tests:
        t0 = time.time()
        try:
            fn()
            elapsed = time.time() - t0
            passed += 1
            if verbose:
                print(f"PASS  {name}  ({elapsed:.2f}s)")
            else:
                print(".", end="", flush=True)
        except Exception:
            elapsed = time.time() - t0
            failed += 1
            tb = traceback.format_exc()
            failures.append((name, tb))
            if verbose:
                print(f"FAIL  {name}  ({elapsed:.2f}s)")
                print(tb)
            else:
                print("F", end="", flush=True)
    if not verbose:
        print()

    total_elapsed = time.time() - start_total
    print()
    if failures:
        print(f"{'=' * 60}")
        print(f"{len(failures)} FAILURE(S):")
        for name, tb in failures:
            print(f"\n--- {name} ---")
            print(tb)

    print(f"\n{passed} passed, {failed} failed in {total_elapsed:.2f}s")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

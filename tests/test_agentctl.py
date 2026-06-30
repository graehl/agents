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
import importlib.util
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
        # Hermetic: drop ambient agent/harness session vars (the test runner may
        # itself be under an agent, e.g. CLAUDE_CODE_SESSION_ID) so each test
        # controls active-sessions behavior explicitly. BASH_ENV is dropped too:
        # the agentctl wrapper is a bash script, and a launcher such as
        # yepanywhere re-exports AGENTCTL_SESSION_ID via a BASH_ENV bridge that
        # would otherwise defeat the pops below.
        for var in ("AGENTCTL_SESSION_ID", "CLAUDE_CODE_SESSION_ID",
                    "AGENTCTL_LAUNCH_DEPTH", "BASH_ENV"):
            env.pop(var, None)
        # Also disable parent-process-tree recovery by default: the test runner
        # is frequently under a `claude --resume <uuid>` / `codex resume <uuid>`
        # ancestor, which agentctl would otherwise recover as the session id.
        # The dedicated recovery tests bypass run() and opt back in.
        env["AGENTCTL_NO_PROC_SESSION_ID"] = "1"
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


def test_wrapper_uses_invocation_cwd_as_project_root():
    ws = Workspace()
    try:
        project = ws.tmp / "_project"
        project.mkdir()
        res = subprocess.run(
            [str(ws.tmp / "agentctl"), "start", "--no-aim", "outside", "--", "true"],
            cwd=project,
            capture_output=True,
            text=True,
            timeout=20,
        )
        _assert(res.returncode == 0, f"agentctl start failed: rc={res.returncode}\nstdout: {res.stdout}\nstderr: {res.stderr}")
        deadline = time.time() + 10.0
        current = project / ".agentctl/jobs/outside/current.json"
        while time.time() < deadline:
            if current.exists():
                state = json.loads(current.read_text())
                if state.get("status") == "finished":
                    break
            time.sleep(0.05)
        else:
            raise TimeoutError("outside job did not finish under invocation cwd")
        _assert(state["cwd"] == str(project.resolve()), f"cwd mismatch: {state['cwd']!r}")
        _assert(str(project / ".agentctl") in state["state_path"], f"state path used wrong root: {state['state_path']}")
        _assert(not (ws.tmp / ".agentctl/jobs/outside").exists(), "wrapper wrote state under code root")
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


def test_sandbox_liveness_visible_pid_mismatch_finishes_unknown():
    ws = Workspace()
    try:
        module_name = "agentctl_under_test_liveness"
        spec = importlib.util.spec_from_file_location(module_name, ws.tmp / "agentctl.py")
        assert spec is not None and spec.loader is not None, "could not load agentctl spec"
        mod = importlib.util.module_from_spec(spec)
        old_root = os.environ.get("AGENTCTL_ROOT")
        os.environ["AGENTCTL_ROOT"] = str(ws.tmp)
        try:
            spec.loader.exec_module(mod)
        finally:
            if old_root is None:
                os.environ.pop("AGENTCTL_ROOT", None)
            else:
                os.environ["AGENTCTL_ROOT"] = old_root

        mod.process_visibility_limited = lambda: True  # pyright: ignore[reportAttributeAccessIssue]
        state_path = ws.tmp / ".agentctl/runs/stale/r1/state.json"
        state_path.parent.mkdir(parents=True)
        state = {
            "job": "stale",
            "run_id": "r1",
            "status": "running",
            "pid": os.getpid(),
            "pid_cmdline": "definitely-not-this-process\0",
            "started_at": mod.utc_now(),
            "state_path": str(state_path),
        }
        refreshed = mod.refresh_state(state)
        _assert(refreshed["status"] == "finished", f"status: {refreshed!r}")
        _assert(refreshed["returncode"] == "unknown", f"returncode: {refreshed!r}")
        _assert("_liveness_note" not in refreshed, f"liveness note should be absent: {refreshed!r}")
        current = json.loads((ws.tmp / ".agentctl/jobs/stale/current.json").read_text())
        _assert(current["status"] == "finished", f"current status: {current!r}")
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


def test_cooperative_declared_json_inputs_outputs():
    ws = Workspace()
    try:
        inp = ws.scratch / "input.txt"
        inp.write_text("declared")
        out = ws.scratch / "output.txt"
        code = (
            "import json, os, pathlib; "
            f"inp = pathlib.Path({str(inp)!r}); "
            f"out = pathlib.Path({str(out)!r}); "
            "out.write_text(inp.read_text()); "
            "decl = pathlib.Path(os.environ['AGENTCTL_RUN_DIR']) / 'declared.json'; "
            "decl.write_text(json.dumps({'inputs': {'data': str(inp)}, "
            "'outputs': {'result': str(out)}}))"
        )
        _start(ws, "--experiment", "e", "declared", "--", sys.executable, "-c", code)
        s = ws.wait_finished("declared")
        _assert(s["inputs"]["data"]["path"] == str(inp), f"input path: {s['inputs']!r}")
        _assert(s["inputs"]["data"]["size"] == len("declared"), f"input size: {s['inputs']!r}")
        _assert(s["outputs"]["result"]["path"] == str(out), f"output path: {s['outputs']!r}")
        _assert(s["outputs"]["result"]["size"] == len("declared"), f"output size: {s['outputs']!r}")
        _assert(Path(f"{out}.meta.json").exists(), "declared output sidecar missing")
    finally:
        ws.cleanup()


def test_watch_cooperative_declared_json_outputs():
    ws = Workspace()
    try:
        out = ws.scratch / "watch-output.txt"
        code = (
            "import json, os, pathlib; "
            f"out = pathlib.Path({str(out)!r}); "
            "out.write_text('watch'); "
            "decl = pathlib.Path(os.environ['AGENTCTL_RUN_DIR']) / 'declared.json'; "
            "decl.write_text(json.dumps({'outputs': {'result': str(out)}}))"
        )
        _start(
            ws,
            "--watch",
            "--watch-heartbeat",
            "0",
            "--watch-poll",
            "0.05",
            "--experiment",
            "e",
            "watchdecl",
            "--",
            sys.executable,
            "-c",
            code,
        )
        s = ws.state("watchdecl")
        _assert(s["outputs"]["result"]["path"] == str(out), f"outputs: {s['outputs']!r}")
        _assert(s["outputs"]["result"]["size"] == len("watch"), f"outputs: {s['outputs']!r}")
        _assert(Path(f"{out}.meta.json").exists(), "watch-declared output sidecar missing")
    finally:
        ws.cleanup()


def test_declare_helpers_import_from_external_project():
    ws = Workspace()
    try:
        project = ws.tmp / "_project"
        project.mkdir()
        inp = project / "input.txt"
        inp.write_text("helper")
        out = project / "output.txt"
        code = (
            "from pathlib import Path; "
            "from agentctl import declare_input, declare_output; "
            "declare_input('data', 'input.txt'); "
            "declare_output('result', 'output.txt'); "
            "Path('output.txt').write_text(Path('input.txt').read_text())"
        )
        env = os.environ.copy()
        for var in (
            "AGENTCTL_SESSION_ID",
            "CLAUDE_CODE_SESSION_ID",
            "AGENTCTL_LAUNCH_DEPTH",
            "BASH_ENV",
            "PYTHONPATH",
        ):
            env.pop(var, None)
        res = subprocess.run(
            [str(ws.tmp / "agentctl"), "start", "--experiment", "e", "helper", "--", sys.executable, "-c", code],
            cwd=project,
            capture_output=True,
            text=True,
            env=env,
            timeout=20,
        )
        _assert(res.returncode == 0, f"agentctl start failed: rc={res.returncode}\nstdout: {res.stdout}\nstderr: {res.stderr}")
        deadline = time.time() + 10.0
        current = project / ".agentctl/jobs/helper/current.json"
        while time.time() < deadline:
            if current.exists():
                state = json.loads(current.read_text())
                if state.get("status") == "finished":
                    break
            time.sleep(0.05)
        else:
            raise TimeoutError("helper job did not finish under external project")
        _assert(state["returncode"] == 0, f"helper returncode: {state.get('returncode')}")
        _assert(state["inputs"]["data"]["path"] == str(inp), f"inputs: {state['inputs']!r}")
        _assert(state["outputs"]["result"]["path"] == str(out), f"outputs: {state['outputs']!r}")
        _assert(Path(f"{out}.meta.json").exists(), "helper-declared sidecar missing")
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


def test_start_after_agentctl_job_waits_before_payload():
    ws = Workspace()
    try:
        dep_out = ws.scratch / "dep.txt"
        follow_out = ws.scratch / "follow.txt"
        _start(ws, "--no-aim", "slowdep", "--", "bash", "-c", f"sleep 0.4; echo dep > {dep_out}")
        _start(
            ws,
            "--no-aim",
            "--after",
            "slowdep",
            "--after-poll",
            "0.05",
            "--after-heartbeat",
            "0",
            "follower",
            "--",
            "bash",
            "-c",
            f"test -s {dep_out}; echo follower > {follow_out}",
        )
        deadline = time.time() + 2.0
        saw_waiting = False
        while time.time() < deadline:
            try:
                s = ws.state("follower")
            except FileNotFoundError:
                time.sleep(0.02)
                continue
            if s.get("status") == "waiting":
                saw_waiting = True
                _assert(s.get("wait_on") == "slowdep", f"wait_on mismatch: {s.get('wait_on')!r}")
                break
            time.sleep(0.02)
        _assert(saw_waiting, "follower never reported waiting")
        s = ws.wait_finished("follower")
        _assert(s["returncode"] == 0, f"follower failed: {s!r}")
        _assert(follow_out.read_text().strip() == "follower", "follower payload did not run")
        _assert(s.get("started_at"), "started_at should be set when payload launches")
    finally:
        ws.cleanup()


def test_start_after_running_marker_waits_before_payload():
    ws = Workspace()
    proc = None
    try:
        external_out = ws.scratch / "external.out"
        marker = Path(f"{external_out}.running.md")
        proc = subprocess.Popen(
            [
                "bash",
                "-c",
                f"sleep 0.4; echo '# done' > {external_out}.meta.md; rm -f {marker}",
            ],
            cwd=ws.tmp,
        )
        marker.write_text(f"- status: running\n- pid: {proc.pid}\n- out: {external_out}\n")
        follow_out = ws.scratch / "marker-follow.txt"
        _start(
            ws,
            "--no-aim",
            "--after",
            str(external_out),
            "--after-poll",
            "0.05",
            "--after-heartbeat",
            "0",
            "markerfollower",
            "--",
            "bash",
            "-c",
            f"test -s {external_out}.meta.md; echo follower > {follow_out}",
        )
        deadline = time.time() + 2.0
        saw_waiting = False
        while time.time() < deadline:
            try:
                s = ws.state("markerfollower")
            except FileNotFoundError:
                time.sleep(0.02)
                continue
            if s.get("status") == "waiting":
                saw_waiting = True
                _assert(s.get("wait_on") == str(external_out), f"wait_on mismatch: {s.get('wait_on')!r}")
                break
            time.sleep(0.02)
        _assert(saw_waiting, "marker follower never reported waiting")
        s = ws.wait_finished("markerfollower")
        _assert(s["returncode"] == 0, f"marker follower failed: {s!r}")
        _assert(follow_out.read_text().strip() == "follower", "marker follower payload did not run")
    finally:
        if proc is not None and proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=5)
        ws.cleanup()


def test_start_after_marker_without_sidecar_does_not_launch_payload():
    ws = Workspace()
    proc = None
    try:
        external_out = ws.scratch / "external-no-meta.out"
        marker = Path(f"{external_out}.running.md")
        proc = subprocess.Popen(["bash", "-c", f"sleep 0.2; rm -f {marker}"], cwd=ws.tmp)
        marker.write_text(f"- status: running\n- pid: {proc.pid}\n- out: {external_out}\n")
        follow_out = ws.scratch / "should-not-exist.txt"
        _start(
            ws,
            "--no-aim",
            "--after",
            str(external_out),
            "--after-poll",
            "0.05",
            "--after-heartbeat",
            "0",
            "markerfail",
            "--",
            "bash",
            "-c",
            f"echo bad > {follow_out}",
        )
        s = ws.wait_finished("markerfail")
        _assert(s["returncode"] != 0, f"markerfail should fail, got {s!r}")
        _assert(not follow_out.exists(), "payload should not launch for unresolved marker dependency")
    finally:
        if proc is not None and proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=5)
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


def test_aim_run_record_default_runs_root():
    """find_aim_run_record reads from runs/aim/ when output has a matching meta path."""
    ws = Workspace()
    try:
        # Place a dump in the canonical runs/aim/ root.
        dump = ws.tmp / "runs/aim/primary/runs/r1.json"
        dump.parent.mkdir(parents=True, exist_ok=True)
        meta_target = ws.scratch / "fake.meta.md"
        meta_target.write_text("# fake\n")
        record = {
            "params": {
                "output": {"meta_path": str(meta_target.resolve())}
            },
            "source": {"aim_run_hash": "abc123def456"},
        }
        dump.write_text(json.dumps(record))

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
                f"run-record lookup failed: stdout={result.stdout!r} stderr={result.stderr!r}")
    finally:
        ws.cleanup()


def test_aim_read_roots_env_override():
    """AGENTCTL_AIM_READ_ROOTS can add read-only migration roots."""
    ws = Workspace()
    try:
        alt_dump = ws.tmp / "alt-runs/aim/archive/runs/r1.json"
        alt_dump.parent.mkdir(parents=True, exist_ok=True)
        meta_target = ws.scratch / "fake.meta.md"
        meta_target.write_text("# fake\n")
        alt_dump.write_text(
            json.dumps(
                {
                    "params": {"output": {"meta_path": str(meta_target.resolve())}},
                    "source": {"aim_run_hash": "abc123def456"},
                }
            )
        )

        py = sys.executable
        code = (
            f'import sys; sys.path.insert(0, {str(ws.tmp)!r}); '
            f'import artifact_meta; '
            f'r = artifact_meta.find_aim_run_record('
            f'meta_path={str(meta_target.resolve())!r}, '
            f'setup=[("aim_run_hash","abc123def456")], '
            f'repo_root={str(ws.tmp)!r}); '
            f'print(r)'
        )
        env = {**os.environ, "AGENTCTL_AIM_READ_ROOTS": "alt-runs/aim"}
        result = subprocess.run([py, "-c", code], capture_output=True, text=True, cwd=ws.tmp, env=env)
        _assert("alt-runs/aim/archive/runs/r1.json" in result.stdout,
                f"env read-root search failed: stdout={result.stdout!r} stderr={result.stderr!r}")
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


def test_active_register_skipped_without_session_id():
    ws = Workspace()
    try:
        _start(ws, "--no-aim", "trivial", "--", "true")
        ws.wait_finished("trivial")
        _assert(not (ws.tmp / ".agentctl/active").exists(),
                "no active/ dir should be created without AGENTCTL_SESSION_ID")
    finally:
        ws.cleanup()


def test_active_register_create_append_and_done():
    ws = Workspace()
    sid = "sess-abc123"
    active = ws.tmp / ".agentctl/active" / sid
    try:
        # No prior entry: agentctl authors a degraded line 1 from the launch.
        res = ws.run("start", "--no-aim", "job1", "--", "true",
                     env_extra={"AGENTCTL_SESSION_ID": sid})
        _assert(res.returncode == 0, f"start failed: {res.stderr}")
        ws.wait_finished("job1")
        _assert(active.exists(), "active entry should be created when session id is set")
        lines = active.read_text().splitlines()
        _assert(lines == [lines[0]] and "job1" in lines[0],
                f"fresh entry should be a single summary line mentioning the launch: {lines!r}")

        # Agent overwrites with its own authored summary + scope; agentctl must
        # preserve both and append only free text below them.
        active.write_text("Coordinating edits to pkg/foo\nscope: pkg/foo/**\n")
        res = ws.run("start", "--no-aim", "job2", "--", "true",
                     env_extra={"AGENTCTL_SESSION_ID": sid})
        _assert(res.returncode == 0, f"start failed: {res.stderr}")
        ws.wait_finished("job2")
        lines = active.read_text().splitlines()
        _assert(lines[0] == "Coordinating edits to pkg/foo",
                f"agent line 1 must be preserved: {lines!r}")
        _assert(lines[1] == "scope: pkg/foo/**",
                f"scope line 2 must be preserved: {lines!r}")
        _assert(any("job2" in ln for ln in lines[2:]),
                f"a free-text note should be appended for job2: {lines!r}")

        # DONE-prefixed entry: the session is complete; leave it untouched.
        active.write_text("DONE: wrapped up\n")
        res = ws.run("start", "--no-aim", "job3", "--", "true",
                     env_extra={"AGENTCTL_SESSION_ID": sid})
        _assert(res.returncode == 0, f"start failed: {res.stderr}")
        ws.wait_finished("job3")
        _assert(active.read_text() == "DONE: wrapped up\n",
                f"DONE entry must be left untouched: {active.read_text()!r}")
    finally:
        ws.cleanup()


def test_active_register_adopts_harness_session_id():
    # With no explicit AGENTCTL_SESSION_ID, agentctl adopts a known harness var
    # (here CLAUDE_CODE_SESSION_ID), so plain `start` maintains the entry.
    ws = Workspace()
    sid = "sess-harness"
    active = ws.tmp / ".agentctl/active" / sid
    try:
        res = ws.run("start", "--no-aim", "adopted", "--", "true",
                     env_extra={"CLAUDE_CODE_SESSION_ID": sid})
        _assert(res.returncode == 0, f"start failed: {res.stderr}")
        ws.wait_finished("adopted")
        _assert(active.exists(), "entry should be created from the adopted harness session id")
        _assert("adopted" in active.read_text(), "summary should mention the launch")
    finally:
        ws.cleanup()


def test_launched_job_gets_depth_guard():
    # A launched job is marked one hop deeper, so any agentctl it shells ignores
    # the session id (agent_session_id() returns "" at depth > 0) — a job cannot
    # masquerade as the launching agent.
    ws = Workspace()
    out = ws.scratch / "child_depth.txt"
    try:
        res = ws.run("start", "--no-aim", "depthjob", "--",
                     "sh", "-c", f'printf %s "${{AGENTCTL_LAUNCH_DEPTH-UNSET}}" > {out}',
                     env_extra={"CLAUDE_CODE_SESSION_ID": "sess-harness"})
        _assert(res.returncode == 0, f"start failed: {res.stderr}")
        ws.wait_finished("depthjob")
        got = out.read_text()
        _assert(got == "1", f"child should be marked at launch depth 1, got {got!r}")
    finally:
        ws.cleanup()


def test_active_verb_authors_banner_and_scope():
    # `active` authors line 1 + scope line 2 directly, with no run record.
    ws = Workspace()
    sid = "sess-active1"
    active = ws.tmp / ".agentctl/active" / sid
    try:
        res = ws.run("active", "refactoring the scope parser",
                     "agentctl.py", "topics/agentctl.md",
                     env_extra={"AGENTCTL_SESSION_ID": sid})
        _assert(res.returncode == 0, f"active failed: {res.stderr}")
        lines = active.read_text().splitlines()
        _assert(lines[0] == "refactoring the scope parser",
                f"line 1 should be the banner: {lines!r}")
        _assert(lines[1] == "scope: agentctl.py topics/agentctl.md",
                f"line 2 should be the scope: {lines!r}")
        # No run noise: the verb must not create job/run state.
        _assert(not (ws.tmp / ".agentctl/jobs").exists(),
                "active must not create job state")
        _assert(not (ws.tmp / ".agentctl/runs").exists(),
                "active must not create run state")
    finally:
        ws.cleanup()


def test_active_verb_replaces_header_preserves_body():
    # A re-author replaces line 1 and the scope line but keeps free content.
    ws = Workspace()
    sid = "sess-active2"
    active = ws.tmp / ".agentctl/active" / sid
    try:
        active.parent.mkdir(parents=True)
        active.write_text("old banner\nscope: old/**\nfree note line\n")
        res = ws.run("active", "new banner", "pkg/a", "pkg/b",
                     env_extra={"AGENTCTL_SESSION_ID": sid})
        _assert(res.returncode == 0, f"active failed: {res.stderr}")
        lines = active.read_text().splitlines()
        _assert(lines == ["new banner", "scope: pkg/a pkg/b", "free note line"],
                f"header replaced, body preserved: {lines!r}")
    finally:
        ws.cleanup()


def test_active_verb_keeps_scope_when_no_paths():
    # Banner-only update leaves an existing scope line untouched.
    ws = Workspace()
    sid = "sess-active3"
    active = ws.tmp / ".agentctl/active" / sid
    try:
        active.parent.mkdir(parents=True)
        active.write_text("old banner\nscope: keep/me/**\n")
        res = ws.run("active", "status only",
                     env_extra={"AGENTCTL_SESSION_ID": sid})
        _assert(res.returncode == 0, f"active failed: {res.stderr}")
        lines = active.read_text().splitlines()
        _assert(lines == ["status only", "scope: keep/me/**"],
                f"scope should be preserved with no path args: {lines!r}")
    finally:
        ws.cleanup()


def test_active_verb_requires_session_id():
    # With no resolvable session id the verb fails loudly and writes nothing.
    ws = Workspace()
    try:
        res = ws.run("active", "no identity here")
        _assert(res.returncode != 0, "active should fail without a session id")
        _assert(not (ws.tmp / ".agentctl/active").exists(),
                "no active/ dir should be created without a session id")
    finally:
        ws.cleanup()


def test_active_verb_depth_guard():
    # A launched job (depth > 0) is not an agent and may not author the entry.
    ws = Workspace()
    sid = "sess-active4"
    try:
        res = ws.run("active", "from inside a job",
                     env_extra={"AGENTCTL_SESSION_ID": sid,
                                "AGENTCTL_LAUNCH_DEPTH": "1"})
        _assert(res.returncode != 0, "active should refuse at launch depth > 0")
        _assert(not (ws.tmp / ".agentctl/active" / sid).exists(),
                "no entry should be authored from a launched job")
    finally:
        ws.cleanup()


def _seed_active(ws, name: str, text: str, age_minutes: float = 0.0) -> Path:
    """Write a .agentctl/active/<name> entry with an mtime age_minutes in the past."""
    active = ws.tmp / ".agentctl/active"
    active.mkdir(parents=True, exist_ok=True)
    path = active / name
    path.write_text(text if text.endswith("\n") else text + "\n")
    if age_minutes:
        old = time.time() - age_minutes * 60
        os.utime(path, (old, old))
    return path


def test_active_list_shows_fresh_non_done_with_status_and_scope():
    # `active` with no banner lists fresh, non-DONE entries + their status line.
    ws = Workspace()
    try:
        _seed_active(ws, "sess-fresh", "editing the parser\nscope: agentctl.py")
        _seed_active(ws, "sess-done", "DONE: shipped it")
        _seed_active(ws, "sess-stale", "long gone", age_minutes=120)
        res = ws.run("active")  # no banner -> list mode
        _assert(res.returncode == 0, f"active list failed: {res.stderr}")
        out = res.stdout
        _assert("sess-fresh" in out and "editing the parser" in out,
                f"fresh non-DONE entry should be listed: {out!r}")
        _assert("scope: agentctl.py" in out, f"scope line should be shown: {out!r}")
        _assert("sess-done" not in out, f"DONE entry should be hidden by default: {out!r}")
        _assert("sess-stale" not in out, f"stale entry should be hidden by default: {out!r}")
    finally:
        ws.cleanup()


def test_active_list_minutes_zero_includes_stale():
    # --minutes 0 drops the freshness window so stale (crashed) entries show.
    ws = Workspace()
    try:
        _seed_active(ws, "sess-stale", "quiet since lunch", age_minutes=200)
        res_default = ws.run("active")
        _assert("sess-stale" not in res_default.stdout,
                f"stale should be hidden in the default window: {res_default.stdout!r}")
        res_all = ws.run("active", "-m", "0")
        _assert(res_all.returncode == 0, f"active -m 0 failed: {res_all.stderr}")
        _assert("sess-stale" in res_all.stdout,
                f"stale should appear with -m 0: {res_all.stdout!r}")
    finally:
        ws.cleanup()


def test_active_list_done_flag_includes_completed():
    # --done also lists DONE-prefixed (completed) entries.
    ws = Workspace()
    try:
        _seed_active(ws, "sess-done", "DONE: shipped it")
        res = ws.run("active", "--done")
        _assert(res.returncode == 0, f"active --done failed: {res.stderr}")
        _assert("sess-done" in res.stdout and "DONE: shipped it" in res.stdout,
                f"DONE entry should appear with --done: {res.stdout!r}")
    finally:
        ws.cleanup()


def test_active_list_marks_self():
    # The caller's own entry (resolved session id) is tagged (self).
    ws = Workspace()
    sid = "sess-me"
    try:
        _seed_active(ws, sid, "my own work")
        _seed_active(ws, "sess-peer", "peer work")
        res = ws.run("active", env_extra={"AGENTCTL_SESSION_ID": sid})
        _assert(res.returncode == 0, f"active list failed: {res.stderr}")
        self_line = next((ln for ln in res.stdout.splitlines() if sid in ln), "")
        _assert("(self)" in self_line, f"own entry should be marked (self): {self_line!r}")
        peer_line = next((ln for ln in res.stdout.splitlines() if "sess-peer" in ln), "")
        _assert("(self)" not in peer_line, f"peer should not be marked self: {peer_line!r}")
    finally:
        ws.cleanup()


def test_active_list_empty_is_clean_exit():
    # No active/ dir at all -> friendly message, exit 0 (read-only, never errors).
    ws = Workspace()
    try:
        res = ws.run("active")
        _assert(res.returncode == 0, f"empty active list should exit 0: {res.stderr}")
        _assert("no active" in res.stdout.lower(),
                f"should report no active sessions: {res.stdout!r}")
        _assert(not (ws.tmp / ".agentctl/active").exists(),
                "listing must not create the active/ dir")
    finally:
        ws.cleanup()


def test_active_sweep_archives_done_and_stale():
    # --sweep moves stale entries out of active/: DONE -> done/, others -> stale/,
    # leaving fresh entries (live peers, just-finished sessions) in place.
    ws = Workspace()
    try:
        _seed_active(ws, "sess-live", "still editing")                        # fresh non-DONE
        _seed_active(ws, "sess-fresh-done", "DONE: just landed")              # fresh DONE
        _seed_active(ws, "sess-crashed", "went quiet", age_minutes=200)       # stale non-DONE
        _seed_active(ws, "sess-old-done", "DONE: last week", age_minutes=200)  # stale DONE
        res = ws.run("active", "--sweep")
        _assert(res.returncode == 0, f"sweep failed: {res.stderr}")
        active = ws.tmp / ".agentctl/active"
        stale = ws.tmp / ".agentctl/stale"
        done = ws.tmp / ".agentctl/done"
        _assert((active / "sess-live").exists(), "fresh non-DONE must stay in active/")
        _assert((active / "sess-fresh-done").exists(), "fresh DONE must stay in active/")
        _assert(not (active / "sess-crashed").exists(), "stale non-DONE must leave active/")
        _assert(not (active / "sess-old-done").exists(), "stale DONE must leave active/")
        _assert((stale / "sess-crashed").exists(), "stale non-DONE must land in stale/")
        _assert((done / "sess-old-done").exists(), "stale DONE must land in done/")
    finally:
        ws.cleanup()


def test_active_sweep_dry_run_moves_nothing():
    # --sweep --dry-run reports what would move but leaves every file in place.
    ws = Workspace()
    try:
        _seed_active(ws, "sess-crashed", "went quiet", age_minutes=200)
        res = ws.run("active", "--sweep", "--dry-run")
        _assert(res.returncode == 0, f"dry-run sweep failed: {res.stderr}")
        _assert("sess-crashed" in res.stdout, f"dry-run should name the entry: {res.stdout!r}")
        _assert((ws.tmp / ".agentctl/active/sess-crashed").exists(),
                "dry-run must not move anything")
        _assert(not (ws.tmp / ".agentctl/stale").exists(),
                "dry-run must not create stale/")
    finally:
        ws.cleanup()


def test_active_list_reads_archives_after_sweep():
    # After a sweep the audit views still find archived entries: -m 0 surfaces
    # the crashed entry from stale/, and -m 0 --done also surfaces done/.
    ws = Workspace()
    try:
        _seed_active(ws, "sess-crashed", "went quiet", age_minutes=200)
        _seed_active(ws, "sess-old-done", "DONE: last week", age_minutes=200)
        ws.run("active", "--sweep")
        res_stale = ws.run("active", "-m", "0")
        _assert("sess-crashed" in res_stale.stdout,
                f"swept stale entry should list with -m 0: {res_stale.stdout!r}")
        _assert(".agentctl/stale/sess-crashed" in res_stale.stdout,
                f"listing should show the archive path: {res_stale.stdout!r}")
        _assert("sess-old-done" not in res_stale.stdout,
                f"DONE archive must stay hidden without --done: {res_stale.stdout!r}")
        res_done = ws.run("active", "-m", "0", "--done")
        _assert("sess-old-done" in res_done.stdout,
                f"swept DONE entry should list with -m 0 --done: {res_done.stdout!r}")
    finally:
        ws.cleanup()


def test_resume_id_from_argv_parsing():
    # Unit: pull a resume session id out of a launcher argv, Codex and Claude forms.
    sys.path.insert(0, str(REPO_ROOT))
    import agentctl
    uid = "061e2fa8-da37-42d4-93b2-94351ebec717"
    cases = {
        "codex positional": (["codex", "resume", uid], uid),
        "claude --resume": (["claude", "--resume", uid], uid),
        "--resume=uuid": ([f"--resume={uid}"], uid),
        "resume w/o uuid": (["codex", "resume", "--last"], ""),
        "uuid not after resume": (["codex", "exec", uid], ""),
        "non-uuid after resume": (["codex", "resume", "not-a-uuid"], ""),
    }
    for label, (argv, want) in cases.items():
        got = agentctl._resume_id_from_argv(argv)
        _assert(got == want, f"{label}: argv={argv!r} got {got!r} want {want!r}")


def test_active_recovers_session_id_from_resume_ancestor():
    # E2e: a terminal `codex resume <id>` injects no AGENTCTL_SESSION_ID, so
    # agentctl must recover the id from the `resume <id>` ancestor argv and key
    # the active entry by it. The parent shell carries `resume <uid>` in its
    # argv; `true; ...` keeps bash from exec-replacing itself (which would drop
    # that argv from the tree).
    ws = Workspace()
    uid = "11111111-2222-3333-4444-555555555555"
    active = ws.tmp / ".agentctl/active" / uid
    try:
        env = os.environ.copy()
        for var in ("AGENTCTL_SESSION_ID", "CLAUDE_CODE_SESSION_ID",
                    "AGENTCTL_LAUNCH_DEPTH", "BASH_ENV"):
            env.pop(var, None)
        script = 'true; ./agentctl active "resumed via proc-tree recovery"'
        res = subprocess.run(
            ["bash", "-c", script, "codex", "resume", uid],
            cwd=ws.tmp, capture_output=True, text=True, env=env, timeout=20,
        )
        _assert(res.returncode == 0, f"active failed: rc={res.returncode}\n{res.stderr}")
        seen = sorted(p.name for p in active.parent.glob("*")) if active.parent.exists() else []
        _assert(active.exists(), f"entry should be keyed by recovered resume id; saw {seen}")
        _assert(active.read_text().splitlines()[0] == "resumed via proc-tree recovery",
                f"banner should be written under the recovered id: {active.read_text()!r}")
    finally:
        ws.cleanup()


def test_launch_depth_blocks_resume_ancestor_recovery():
    # The count-down launch-depth guard wins over proc-tree recovery too: a
    # depth>0 invocation (a launched job, or a recursive agentctl loop) must not
    # refresh an entry even when a `resume <id>` ancestor is present.
    ws = Workspace()
    uid = "99999999-8888-7777-6666-555555555555"
    try:
        env = os.environ.copy()
        for var in ("AGENTCTL_SESSION_ID", "CLAUDE_CODE_SESSION_ID", "BASH_ENV"):
            env.pop(var, None)
        env["AGENTCTL_LAUNCH_DEPTH"] = "1"
        script = 'true; ./agentctl active "should be refused" || true'
        subprocess.run(
            ["bash", "-c", script, "codex", "resume", uid],
            cwd=ws.tmp, capture_output=True, text=True, env=env, timeout=20,
        )
        _assert(not (ws.tmp / ".agentctl/active" / uid).exists(),
                "depth>0 must not author an entry even with a resume ancestor")
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

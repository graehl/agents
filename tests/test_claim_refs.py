#!/usr/bin/env python3
"""Tests for scripts/claim-refs, driven through the CLI against a scratch
Git checkout holding a two-section paper, run records, and an input chain."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL = REPO_ROOT / "scripts" / "claim-refs"

TRAIN = "demo-train/20260901T000000Z"
SCORE = "demo-score/20260902T000000Z"
REMOTE = "demo-remote/20260903T000000Z"


def run(cwd: Path, *argv: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), *argv, "--acli-quiet"],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env={k: v for k, v in os.environ.items() if k != "AGENTCTL_AIM_READ_ROOTS"},
    )


def jsonl(proc: subprocess.CompletedProcess) -> list[dict]:
    return [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]


def git_repo() -> Path:
    root = Path(tempfile.mkdtemp(prefix="claim-refs-test-"))
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    return root


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def add_record(root: Path, ref: str, inputs: dict | None = None) -> None:
    experiment, run_id = ref.split("/")
    base = root / "runs/aim" / experiment
    record = {
        "identity": {"agentctl_run_id": run_id, "experiment": experiment},
        "params": {"inputs": inputs or {}},
        "ref": run_id,
        "schema": "aim-text-dump-v1",
    }
    write(base / "runs" / f"{run_id}.json", json.dumps(record))
    write(base / "texts" / run_id / "meta.markdown.md", f"# {ref}\n")
    row = {"agentctl_run_id": run_id, "dump": f"runs/{run_id}.json", "ref": run_id}
    with (base / "manifest.jsonl").open("a") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")


def paper_checkout() -> Path:
    """Score consumes train's output; the paper cites score's scores.json by
    path and a remote run whose record never came back."""
    root = git_repo()
    add_record(root, TRAIN)
    add_record(
        root,
        SCORE,
        {
            "model": {
                "path": "m.bin",
                "source_dump": f"runs/aim/{TRAIN.split('/')[0]}/runs/{TRAIN.split('/')[1]}.json",
            }
        },
    )
    program = root / "research/demo"
    write(program / "evidence/scores/scores.json", "{}")
    write(
        program / "evidence/scores/scores.json.meta.json",
        json.dumps(
            {"agentctl_run_id": SCORE.split("/")[1], "experiment": SCORE.split("/")[0]}
        ),
    )
    write(program / "evidence/scores/compare.py", "")
    write(program / "evidence/hand-table.json", "{}")
    write(program / "evidence/legacy.json", "{}")
    write(program / "evidence/legacy.json.meta.md", "# Run Metadata\n")
    write(program / "evidence/split-a.json", "{}")
    write(program / "evidence/split-b.json", "{}")
    sections = program / "papers/demo/sections"
    write(
        sections / "_10-results.qmd",
        "## Results\n\n"
        "<!-- ref: evidence/scores/scores.json; compare.py; recomputed by hand -->\n"
        "Text.\n"
        "<!-- ref: hand-table.json -->\n"
        "<!-- ref: legacy.json; evidence/split-{a,b}.json -->\n"
        "<!-- ref: BASELINE-FROZEN -->\n"
        "<!-- ref: missing/nowhere.json -->\n",
    )
    write(sections / "_10-results.repro.md", f"Producer: `{REMOTE}` on the worker.\n")
    write(sections / "_10-results.trims.md", "<!-- ref: trimmed/ignored.json -->\n")
    write(sections / "_20-method.qmd", f"<!-- run: {TRAIN} -->\n")
    return root


def by_locator(rows: list[dict]) -> dict[str, dict]:
    return {row["locator"] or row.get("text", ""): row for row in rows}


def test_check_classifies_each_citation():
    root = paper_checkout()
    proc = run(root, "check", "research/demo/papers/demo")
    assert proc.returncode == 3, proc.stderr
    rows = by_locator(jsonl(proc))
    assert rows["evidence/scores/scores.json"]["level"] == "run-record"
    assert rows["evidence/scores/scores.json"]["run"] == SCORE
    # A later item resolves beside the previous locator; prose items are skipped.
    assert rows["compare.py"]["path"] == "research/demo/evidence/scores/compare.py"
    assert "recomputed" not in " ".join(rows)
    assert rows["hand-table.json"]["level"] == "no-producer"
    assert rows["legacy.json"]["level"] == "meta-md"
    assert rows["evidence/split-a.json"]["status"] == "resolved"
    assert rows["evidence/split-b.json"]["status"] == "resolved"
    assert rows["BASELINE-FROZEN"]["status"] == "no-locator"
    assert rows["missing/nowhere.json"]["status"] == "unresolved"
    assert rows[REMOTE]["source"] == "rider"
    assert rows[REMOTE]["level"] == "record-missing"
    assert rows[TRAIN]["level"] == "run-record"
    assert "trimmed/ignored.json" not in rows


def test_check_text_lists_what_needs_attention():
    root = paper_checkout()
    proc = run(root, "check", "research/demo/papers/demo", "--text")
    assert "_10-results.qmd: 1 run-record" in proc.stdout, proc.stdout
    assert "record-missing " + REMOTE in " ".join(proc.stdout.split())
    assert "evidence/scores/scores.json\n" not in proc.stdout


def test_paths_follow_input_ancestry_unless_shallow():
    root = paper_checkout()
    deep = run(root, "paths", "research/demo/papers/demo", "--text")
    assert deep.returncode == 3, deep.stderr
    listed = deep.stdout.split()
    assert f"runs/aim/demo-train/runs/{TRAIN.split('/')[1]}.json" in listed
    assert f"runs/aim/demo-score/texts/{SCORE.split('/')[1]}/meta.markdown.md" in listed
    assert "missing run record " + REMOTE in deep.stderr
    shallow = run(root, "paths", "--shallow", "--run", SCORE, "--text")
    assert shallow.returncode == 0, shallow.stderr
    assert all("demo-train" not in p for p in shallow.stdout.split())


def test_pack_then_unpack_merges_records_and_manifests():
    source = paper_checkout()
    archive = source / "bundle.tar.xz"
    packed = run(source, "pack", "--run", SCORE, "-o", str(archive))
    assert packed.returncode == 0, packed.stderr
    assert {r["run"] for r in jsonl(packed)} == {SCORE, TRAIN}
    assert run(source, "pack", "--run", SCORE, "-o", str(archive)).returncode == 5

    target = git_repo()
    add_record(target, "demo-train/20260801T000000Z")
    first = run(target, "unpack", str(archive))
    assert first.returncode == 0, first.stderr
    record = target / "runs/aim/demo-score/runs" / f"{SCORE.split('/')[1]}.json"
    assert record.exists()
    manifest = (target / "runs/aim/demo-train/manifest.jsonl").read_text().splitlines()
    assert len(manifest) == 2
    again = run(target, "unpack", str(archive))
    assert {r["status"] for r in jsonl(again)} <= {"same", "present"}
    assert (
        len((target / "runs/aim/demo-train/manifest.jsonl").read_text().splitlines())
        == 2
    )

    record.write_text("{}")
    conflict = run(target, "unpack", str(archive))
    assert conflict.returncode == 5
    assert "demo-score/runs" in conflict.stderr.splitlines()[-1]


def main() -> int:
    tests = [(name, fn) for name, fn in globals().items() if name.startswith("test_")]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"ok   {name}")
        except Exception:
            failed += 1
            print(f"FAIL {name}")
            traceback.print_exc()
    print(f"\n{len(tests) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

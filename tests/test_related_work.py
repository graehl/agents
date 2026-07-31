#!/usr/bin/env python3
"""Tests for scripts/related-work — the shared survey related-work engine.

No test reaches the network: fetching is covered by driving the sentinel and
manifest state that the fetch path branches on, which is where every bug this
tool exists to prevent has actually lived.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL = REPO_ROOT / "scripts" / "related-work"

_loader = importlib.machinery.SourceFileLoader("related_work", str(TOOL))
_spec = importlib.util.spec_from_loader("related_work", _loader)
rw = importlib.util.module_from_spec(_spec)
# @dataclass resolves annotations through sys.modules, so register before exec.
sys.modules["related_work"] = rw
_loader.exec_module(rw)


def _assert(cond, msg="assertion failed"):
    if not cond:
        raise AssertionError(msg)


def run(cwd: Path, *argv: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), *argv],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env=dict(os.environ, PYTHONPATH=str(REPO_ROOT)),
    )


def jsonl(proc: subprocess.CompletedProcess) -> list[dict]:
    return [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]


MANIFEST = """\
meta:
  field_slug: demo
  coverage_cutoff: 2026-07-31
  grounding_mode: grounded-in-progress

papers:
  - key: alpha2020-one
    short: one
    concept_page: concepts/one.md
    title: "One"
    arxiv: "2001.00001"
    grounded: true
    verified: true
    fetched: 2026-07-31
  - key: beta2021-two
    title: "Two"
    url: "https://example.invalid/two"
    grounded: false
    verified: false
    fetched: null
  - key: gamma2022-three
    title: "Three"
    arxiv: "2203.00003"
    grounded: false
    verified: true
    source: anchor-bib
    fetched: null
"""


def survey(tmp: Path) -> Path:
    """A survey root whose manifest starts out agreeing with disk."""
    root = tmp / "surveys" / "demo"
    related = root / "related-work"
    (related / "extract").mkdir(parents=True)
    (root / "concepts").mkdir()
    (root / "concepts" / "one.md").write_text("# one\n")
    (related / "papers.yaml").write_text(MANIFEST)
    fetched = related / "extract" / "alpha2020-one"
    fetched.mkdir()
    (fetched / "paper.md").write_text("# One\n")
    (fetched / ".fetched").write_text(
        json.dumps({"method": "arxiv-html", "source": "https://arxiv.org/html/2001.00001"})
    )
    return root


def test_clean_survey_audits_clean():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        proc = run(root, "audit")
        _assert(proc.returncode == 0, f"clean survey should audit clean:\n{proc.stdout}{proc.stderr}")
        row = jsonl(proc)[0]
        _assert(row["drift"] == 0 and row["manifested"] == 3, row)
        _assert(row["grounded"] == 1 and row["verified"] == 2 and row["digested"] == 1, row)


def test_audit_catches_drift_in_both_directions():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        related = root / "related-work"
        # beta was fetched but the manifest was never updated.
        beta = related / "extract" / "beta2021-two"
        beta.mkdir()
        (beta / ".fetched").write_text('{"method":"url-html","source":"https://example.invalid/two"}')
        # gamma claims grounding it never had.
        text = (related / "papers.yaml").read_text().replace(
            """  - key: gamma2022-three
    title: "Three"
    arxiv: "2203.00003"
    grounded: false""",
            """  - key: gamma2022-three
    title: "Three"
    arxiv: "2203.00003"
    grounded: true""",
        )
        (related / "papers.yaml").write_text(text)

        proc = run(root, "audit")
        _assert(proc.returncode == 3, f"drift must exit 3, got {proc.returncode}")
        rules = {(r["key"], r["rule"]) for r in jsonl(proc)}
        for expected in (
            ("beta2021-two", "grounded"),
            ("beta2021-two", "fetched-date"),
            ("beta2021-two", "verified"),
            ("gamma2022-three", "grounded"),
        ):
            _assert(expected in rules, f"{expected} missing from {sorted(rules)}")


def test_verified_without_own_extract_needs_a_source():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        related = root / "related-work"
        # gamma is verified against the anchor bibliography, which is legal —
        # until it stops saying so.
        text = (related / "papers.yaml").read_text().replace("    source: anchor-bib\n", "")
        (related / "papers.yaml").write_text(text)
        proc = run(root, "audit")
        _assert(proc.returncode == 3)
        rules = {(r["key"], r["rule"]) for r in jsonl(proc)}
        _assert(("gamma2022-three", "source") in rules, sorted(rules))


def test_unregenerable_and_orphan_extracts_are_findings():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        related = root / "related-work"
        (related / "extract" / "nobody-claims-me").mkdir()
        # strip alpha's arxiv id: its extract can no longer be rebuilt
        text = (related / "papers.yaml").read_text().replace('    arxiv: "2001.00001"\n', "")
        (related / "papers.yaml").write_text(text)
        proc = run(root, "audit")
        rules = {(r["key"], r["rule"]) for r in jsonl(proc)}
        _assert(("nobody-claims-me", "orphan-extract") in rules, sorted(rules))
        _assert(("alpha2020-one", "regenerable") in rules, sorted(rules))


def test_missing_concept_page_is_a_finding():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        (root / "concepts" / "one.md").unlink()
        proc = run(root, "audit")
        rules = {(r["key"], r["rule"]) for r in jsonl(proc)}
        _assert(("alpha2020-one", "concept-page") in rules, sorted(rules))


def test_bare_fetch_refuses_to_queue_the_whole_backlog():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        proc = run(root, "fetch")
        _assert(proc.returncode == 2, "a bare fetch must not silently start N downloads")
        envelope = json.loads(proc.stderr.splitlines()[0])
        _assert("2 papers have no extract" in envelope["error"]["message"], envelope)
        _assert(sorted(envelope["error"]["detail"]["pending"]) == [
            "beta2021-two",
            "gamma2022-three",
        ], envelope)


def test_completed_extract_is_skipped_without_network():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        proc = run(root, "fetch", "alpha2020-one")
        _assert(proc.returncode == 0, proc.stderr)
        row = jsonl(proc)[0]
        _assert(row == {"key": "alpha2020-one", "status": "skipped", "reason": "already fetched"}, row)


def test_unknown_key_is_not_found():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        proc = run(root, "fetch", "nope2020-x")
        _assert(proc.returncode == 4, proc.returncode)


def test_sentinel_reads_the_legacy_tab_form():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / ".fetched"
        path.write_text("arxiv-html\thttps://arxiv.org/html/2001.00001\n")
        sentinel = rw.read_sentinel(path)
        _assert(sentinel.method == "arxiv-html", sentinel)
        _assert(sentinel.source == "https://arxiv.org/html/2001.00001", sentinel)
        _assert(sentinel.etag is None and sentinel.last_modified is None, sentinel)


def test_revalidation_without_validators_never_claims_fresh():
    # No ETag and no Last-Modified means there is nothing to ask the server;
    # "cannot tell" must read as "may have changed".
    _assert(not rw.is_unchanged("https://example.invalid/x", rw.Sentinel("url-html", "u")))


def test_list_and_status_report_the_survey():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        rows = jsonl(run(root, "list"))
        _assert([r["key"] for r in rows] == ["alpha2020-one", "beta2021-two", "gamma2022-three"], rows)
        _assert(rows[0]["extract"] is True and rows[1]["extract"] is False, rows)

        status = jsonl(run(root, "status"))[0]
        _assert(status["extracts"] == 1 and status["coverage_cutoff"] == "2026-07-31", status)

        toon = run(root, "list", "--toon")
        _assert(toon.returncode == 0 and "alpha2020-one" in toon.stdout, toon.stdout)


def test_resolves_the_survey_root_or_the_related_work_dir():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        for cwd in (root, root / "related-work"):
            proc = run(cwd, "status")
            _assert(proc.returncode == 0, f"{cwd}: {proc.stderr}")
        outside = Path(tmp) / "elsewhere"
        outside.mkdir()
        _assert(run(outside, "status").returncode == 4, "no manifest anywhere = not found")


def test_init_scaffolds_a_new_survey():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "surveys" / "fresh"
        root.mkdir(parents=True)
        proc = run(root, "init")
        _assert(proc.returncode == 0, proc.stderr)
        manifest = root / "related-work" / "papers.yaml"
        _assert(manifest.is_file(), "init writes papers.yaml")
        _assert("field_slug: fresh" in manifest.read_text(), manifest.read_text()[:200])
        _assert(
            "extract/" in (root / "related-work" / ".gitignore").read_text(),
            "extracts are ignored by shared policy, not a per-clone exclude",
        )
        _assert(run(root, "audit").returncode == 0, "an empty survey audits clean")
        _assert(run(root, "init").returncode == 5, "init must not clobber a manifest")


def test_bad_manifest_shapes_fail_loud():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "s"
        (root / "related-work").mkdir(parents=True)
        manifest = root / "related-work" / "papers.yaml"
        manifest.write_text("papers: not-a-list\n")
        _assert(run(root, "audit").returncode == 70, "wrong shape is a schema failure")
        manifest.write_text("papers:\n  - title: keyless\n")
        _assert(run(root, "audit").returncode == 70, "a keyless entry is a schema failure")


def test_help_carries_the_acli_footer():
    proc = run(REPO_ROOT, "--help")
    _assert(proc.returncode == 0, proc.stderr)
    _assert("acli: 1 complete toon" in proc.stdout, proc.stdout[-300:])
    _assert("exit codes:" in proc.stdout, proc.stdout[-300:])


def test_completion_offers_verbs():
    proc = run(REPO_ROOT, "--acli-complete", "")
    _assert(proc.returncode == 0, proc.stderr)
    offered = {json.loads(line)["completion"] for line in proc.stdout.splitlines()}
    _assert({"audit", "fetch", "init", "list", "status"} <= offered, offered)


def _collect_tests():
    return [(name, fn) for name, fn in sorted(globals().items()) if name.startswith("test_")]


def main(argv: list[str]) -> int:
    verbose = "-v" in argv
    passed = failed = 0
    failures = []
    start = time.time()
    for name, fn in _collect_tests():
        try:
            fn()
            passed += 1
            print(f"PASS  {name}" if verbose else ".", end="" if not verbose else "\n", flush=True)
        except Exception:
            failed += 1
            failures.append((name, traceback.format_exc()))
            print(f"FAIL  {name}" if verbose else "F", end="" if not verbose else "\n", flush=True)
    if not verbose:
        print()
    for name, tb in failures:
        print(f"\n--- {name} ---\n{tb}")
    print(f"\n{passed} passed, {failed} failed in {time.time() - start:.2f}s")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

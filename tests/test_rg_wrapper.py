#!/usr/bin/env python3
"""Tests for the agent-safe rg wrapper (repo-root `rg`).

RG_REAL=/bin/echo turns the wrapper into an argv printer, so most cases
assert on the exact translation; one smoke test runs the real ripgrep.
Run: python3 tests/test_rg_wrapper.py
"""

import os
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WRAPPER = REPO_ROOT / "rg"


def _assert(cond, msg="assertion failed"):
    if not cond:
        raise AssertionError(msg)


def run(*args, real=False):
    env = os.environ.copy()
    if not real:
        env["RG_REAL"] = "/bin/echo"
    else:
        env.pop("RG_REAL", None)
    return subprocess.run(
        [str(WRAPPER), *args], capture_output=True, text=True, env=env
    )


def translated(*args) -> list[str]:
    res = run(*args)
    _assert(
        res.returncode == 0,
        f"wrapper failed on {args!r}: rc={res.returncode} stderr={res.stderr!r}",
    )
    return res.stdout.split()


PREFIX = ["--type-add", "tsx:*.tsx"]


def test_rn_translates_to_n():
    _assert(
        translated("-rn", "pat", "dir") == PREFIX + ["-n", "pat", "dir"],
        f"got {translated('-rn', 'pat', 'dir')!r}",
    )


def test_rln_translates_to_l_n():
    _assert(
        translated("-rln", "pat") == PREFIX + ["-l", "-n", "pat"],
        f"got {translated('-rln', 'pat')!r}",
    )


def test_ri_translates_to_i():
    _assert(
        translated("-ri", "pat") == PREFIX + ["-i", "pat"],
        f"got {translated('-ri', 'pat')!r}",
    )


def test_R_translates_to_L():
    _assert(
        translated("-R", "pat") == PREFIX + ["-L", "pat"],
        f"got {translated('-R', 'pat')!r}",
    )


def test_recursive_long_form_dropped():
    _assert(
        translated("--recursive", "pat") == PREFIX + ["pat"],
        f"got {translated('--recursive', 'pat')!r}",
    )


def test_bare_r_blocked():
    res = run("-r", "pat")
    _assert(res.returncode == 2, f"bare -r should be blocked: rc={res.returncode}")
    _assert(
        "blocked" in res.stderr and "--replace" in res.stderr,
        f"block message should name the escape hatch: {res.stderr!r}",
    )


def test_r_with_replacement_text_blocked():
    res = run("-rfoo", "pat")
    _assert(res.returncode == 2, f"-rfoo should be blocked: rc={res.returncode}")


def test_replace_long_form_passes_through():
    _assert(
        translated("--replace", "x", "pat") == PREFIX + ["--replace", "x", "pat"],
        f"got {translated('--replace', 'x', 'pat')!r}",
    )
    _assert(
        translated("--replace=x", "pat") == PREFIX + ["--replace=x", "pat"],
        f"got {translated('--replace=x', 'pat')!r}",
    )


def test_double_dash_stops_translation():
    _assert(
        translated("pat", "--", "-r") == PREFIX + ["pat", "--", "-r"],
        f"got {translated('pat', '--', '-r')!r}",
    )


def test_real_search_smoke():
    with tempfile.TemporaryDirectory(prefix="rg-wrapper-test-") as tmp:
        (Path(tmp) / "haystack.txt").write_text("hay\nneedle here\n")
        res = run("-rn", "needle", tmp, real=True)
        _assert(
            res.returncode == 0,
            f"real search failed: rc={res.returncode} stderr={res.stderr!r}",
        )
        _assert("needle here" in res.stdout, f"match missing: {res.stdout!r}")


def main() -> int:
    tests = [
        (n, f)
        for n, f in sorted(globals().items())
        if n.startswith("test_") and callable(f)
    ]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"PASS  {name}")
        except Exception:
            failed += 1
            print(f"FAIL  {name}")
            traceback.print_exc()
    print(f"\n{len(tests) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Event-text truncation contract for scripts/reviews.

A CI bot's message is the only carrier of the build URLs that lead to a
failing step's output, so truncation must never cut one in half.
"""

from __future__ import annotations

import importlib.util
import re
import sys
import traceback
from importlib.machinery import SourceFileLoader
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "reviews"

JOB = "https://jenkins.example.com:8080/job/xmt-verification/job/aiprod-xmt-regtests"
CI_MESSAGE = (
    "Patch Set 1: Verified-1 Code-Review-2\n\n"
    f"Build Failed \n\n{JOB}/1964/ : FAILURE Disk drive out of space "
    f"( {JOB}/1964/console )\n\n"
    f"{JOB}-gpu/812/ : FAILURE regtest diff ( {JOB}-gpu/812/console )\n"
)


def _load():
    loader = SourceFileLoader("reviews_under_test", str(SCRIPT))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[loader.name] = module  # @dataclass resolves annotations through it
    loader.exec_module(module)
    return module


reviews = _load()


def test_short_text_only_collapses_whitespace():
    assert reviews._short("a  b\n\nc", 80) == "a b c"


def test_urls_survive_a_cut_that_lands_before_them():
    out = reviews._short(CI_MESSAGE, 60)
    assert "…" in out
    for url in (f"{JOB}/1964/", f"{JOB}-gpu/812/", f"{JOB}/1964/console"):
        assert url in out, f"dropped {url} from {out}"


def test_no_partial_url_is_left_behind():
    whole = set(re.findall(r"https?://\S+", CI_MESSAGE))
    for n in range(20, len(CI_MESSAGE) + 20):
        out = reviews._short(CI_MESSAGE, n)
        for token in re.findall(r"https?://\S+", out):
            assert token.rstrip("…") in whole or token in whole, (
                f"n={n} left partial {token!r}"
            )


def test_message_budget_holds_a_multi_job_ci_report():
    assert reviews.MESSAGE_CHARS == 1200
    assert reviews._short(" ".join(CI_MESSAGE.split()), reviews.MESSAGE_CHARS) == (
        " ".join(CI_MESSAGE.split())
    )


def main() -> int:
    tests = [
        (name, function)
        for name, function in sorted(globals().items())
        if name.startswith("test_") and callable(function)
    ]
    failed = 0
    for name, function in tests:
        try:
            function()
            print(f"PASS  {name}")
        except Exception:
            failed += 1
            print(f"FAIL  {name}")
            traceback.print_exc()
    print(f"\n{len(tests) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

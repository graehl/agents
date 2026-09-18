#!/usr/bin/env python3
"""Event-text truncation contract for scripts/reviews.

A CI bot's message is the only carrier of the build URLs that lead to a
failing step's output, so truncation must never cut one in half.
"""

from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
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


def _config(kind: str, root: Path) -> reviews.Config:
    return reviews.Config(
        root=root,
        kind=kind,
        backend={"default_branch": "master"},
        ticket_pattern=None,
        ticket_url=None,
    )


def _review(number: str, branch: str, status: str) -> reviews.Review:
    return reviews.Review(
        number=number,
        branch=branch,
        status=status,
        url=f"https://r.invalid/{number}",
        subject="s",
        created=None,
        updated=None,
        revision={"number": 1, "sha": "abc"},
        ci=[],
        human=[],
        submittable={},
        reviewers=[],
        events=[],
    )


def test_parse_change_file_reads_header_and_seen_and_refuses_bad_input():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "c.md"
        path.write_text(
            "# Subject\n\nChange: gerrit I0123abcd 7\nSeen: 2026-09-01T00:00:00Z\n"
        )
        cf = reviews.parse_change_file(path)
        assert (cf.backend, cf.ids, cf.seen) == (
            "gerrit",
            ["I0123abcd", "7"],
            "2026-09-01T00:00:00Z",
        )
        path.write_text("# Subject\n\nno header\n")
        try:
            reviews.parse_change_file(path)
        except reviews.Refused as exc:
            assert "Change:" in str(exc)
        else:
            raise AssertionError("missing header must be refused")
        path.write_text("Change: github pr#1\nSeen: yesterday\n")
        try:
            reviews.parse_change_file(path)
        except reviews.Refused as exc:
            assert "ISO-8601" in str(exc)
        else:
            raise AssertionError("a non-ISO Seen must be refused")


def test_write_state_inserts_replaces_and_marks():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "c.md"
        path.write_text("# Subject\n\nChange: github pr#1\n\n## Notes\n\nbody\n")
        cf = reviews.parse_change_file(path)
        table = [f"{reviews.STATE_OPEN} t1 -->", "| a |", reviews.STATE_CLOSE]
        # No Seen line: the table lands after the Change header.
        reviews.write_state(cf, table, None)
        lines = path.read_text().splitlines()
        assert lines[2] == "Change: github pr#1" and lines[4] == table[0], lines
        # A marked sync adds Seen after the header and appends the log.
        reviews.write_state(cf, table, "2026-09-02T00:00:00Z", ["### Observed", "- x"])
        text = path.read_text()
        assert "\nSeen: 2026-09-02T00:00:00Z\n" in text and text.endswith("- x\n")
        # A second sync replaces the block in place and updates Seen.
        table2 = [f"{reviews.STATE_OPEN} t2 -->", "| b |", reviews.STATE_CLOSE]
        reviews.write_state(cf, table2, "2026-09-03T00:00:00Z")
        text = path.read_text()
        assert (
            text.count(reviews.STATE_OPEN) == 1
            and "| b |" in text
            and "| a |" not in text
        )
        assert (
            "Seen: 2026-09-03T00:00:00Z" in text
            and "2026-09-02" not in text.split("###")[0]
        )
        # An existing Seen line at parse time is replaced, not duplicated.
        cf = reviews.parse_change_file(path)
        reviews.write_state(cf, table2, "2026-09-04T00:00:00Z")
        assert path.read_text().count("Seen:") == 1


def test_locate_by_path_name_id_and_table_number():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        cfg = _config("gerrit", root)
        cfg.reviews_dir.mkdir()
        (cfg.reviews_dir / "merged").mkdir()
        (cfg.reviews_dir / "README.md").write_text("# not a change\n")
        open_file = cfg.reviews_dir / "TCK-1-fix-thing-I0123abcd.md"
        open_file.write_text(
            "Change: gerrit I0123abcdef\n\n| [4242](https://r/4242) |\n"
        )
        merged = cfg.reviews_dir / "merged" / "old-I9999.md"
        merged.write_text("Change: gerrit I9999999999\n")
        (cfg.reviews_dir / "broken.md").write_text("no header\n")
        assert reviews.locate(cfg, str(open_file), ("open",)).path == open_file
        assert reviews.locate(cfg, open_file.name, ("open",)).path == open_file
        assert (
            reviews.locate(cfg, "TCK-1-fix-thing-I0123abcd", ("open",)).path
            == open_file
        )
        assert reviews.locate(cfg, "I0123abcd", ("open",)).path == open_file
        assert reviews.locate(cfg, "#4242", ("open",)).path == open_file
        assert reviews.locate(cfg, "I9999999999", ("open", "merged")).path == merged
        for token, buckets in (("I9999999999", ("open",)), ("nothing", ("open",))):
            try:
                reviews.locate(cfg, token, buckets)
            except reviews.Refused as exc:
                assert exc.code == reviews.acli.ExitCode.NOT_FOUND
            else:
                raise AssertionError(f"{token} must not be located")


def test_terminal_bucket_judges_the_default_branch_first():
    cfg = _config("gerrit", Path("."))
    assert reviews.terminal_bucket(cfg, []) is None
    assert reviews.terminal_bucket(cfg, [_review("1", "master", "NEW")]) is None
    assert (
        reviews.terminal_bucket(
            cfg, [_review("1", "master", "MERGED"), _review("2", "rel", "ABANDONED")]
        )
        == "merged"
    )
    assert (
        reviews.terminal_bucket(
            cfg, [_review("1", "master", "ABANDONED"), _review("2", "rel", "MERGED")]
        )
        == "abandoned"
    )
    assert reviews.terminal_bucket(cfg, [_review("2", "rel", "MERGED")]) == "merged"


def test_change_key_is_short_for_gerrit_and_pr_joined_for_github():
    assert (
        reviews.change_key(_config("gerrit", Path(".")), ["I0123456789abcdef"])
        == "I01234567"
    )
    assert (
        reviews.change_key(_config("github", Path(".")), ["org/repo#12", "#7"])
        == "pr12-7"
    )


def test_review_summary_is_the_one_spelling_every_view_uses():
    review = {
        "ci": [{"label": "Verified", "value": "+1", "by": "jenkins"}],
        "human": [
            {"label": "Code-Review", "value": "+2", "by": "alice"},
            {"label": "review", "value": "APPROVED", "by": "bob"},
        ],
        "submittable": {
            "status": "READY",
            "needs": ["carol"],
            "mergeable": "MERGEABLE",
        },
    }
    summary = reviews.review_summary(
        review, {"mergeable": False, "conflicts": ["a", "b", "c", "d"]}
    )
    assert summary["ci"] == "Verified+1 jenkins"
    assert summary["human"] == "Code-Review+2 alice, bob APPROVED"
    assert (
        summary["submittable"] == "READY, needs carol, MERGEABLE, CONFLICTS 4: a, b, c"
    )
    empty = reviews.review_summary({"ci": [], "human": [], "submittable": {}}, None)
    assert empty == {"ci": None, "human": None, "submittable": None}


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

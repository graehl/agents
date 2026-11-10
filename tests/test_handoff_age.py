#!/usr/bin/env python3
"""Behavior tests for scripts/handoff-age through its command line."""

from __future__ import annotations

import json
import subprocess
import tempfile
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "handoff-age"
TODAY = "2026-11-10"

HANDOFF = """\
/goal finish the thing

# [durable] Compiled understanding (2026-08-01)

The crux.

# [state] Checkpoint at 2026-11-10 05:00 UTC

Job 7 is running.

## Results

Inherits today's stamp.

# [owed] Tell the advisor (2026-11-05)

Still owed.

# Previous checkpoint at 2026-09-01 (superseded above)

Old state.

```
# not a heading
```

## Old detail

More old state.

# Undated notes

Body.

Source session: claude | abc
"""

GAP = """\
---
slug: example
noticed: 2026-09-01
where: scripts/x
---

**Gap:** something is off.
"""


_SCRATCH = tempfile.TemporaryDirectory(prefix="handoff-age-test-")


def _file(text: str, name: str = "work.md") -> Path:
    path = Path(tempfile.mkdtemp(dir=_SCRATCH.name)) / name
    path.write_text(text)
    return path


def _run(*args: str, expect: int = 0) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        [str(SCRIPT), "--today", TODAY, *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != expect:
        raise AssertionError(f"exit {proc.returncode}: {proc.stderr}")
    return proc


def _sections(path: Path) -> dict[str, dict]:
    summary = json.loads(_run("list", str(path)).stdout)
    return {row["title"].split(" (")[0]: row for row in summary["sections"]}


def test_class_and_date_decide_which_sections_are_aged() -> None:
    rows = _sections(_file(HANDOFF))
    assert not rows["[durable] Compiled understanding"]["aged"]
    assert not rows["[state] Checkpoint at 2026-11-10 05:00 UTC"]["aged"]
    assert rows["Results"]["date"] == TODAY and rows["Results"]["class"] == "state"
    assert not rows["[owed] Tell the advisor"]["aged"]
    assert rows["Previous checkpoint at 2026-09-01"]["age_days"] == 70
    assert rows["Old detail"]["aged"] and rows["Old detail"]["date"] == "2026-09-01"
    assert rows["Undated notes"]["aged"] and rows["Undated notes"]["date"] is None
    assert "not a heading" not in rows


def test_read_keeps_fresh_text_and_indexes_aged_sections() -> None:
    view = _run("read", "--text", str(_file(HANDOFF))).stdout
    assert view.startswith("/goal finish the thing")
    assert "The crux." in view and "Job 7 is running." in view
    assert "Old state." not in view and "More old state." not in view
    assert "<!-- aged 70d unclassified L19-26" in view
    assert "Source session: claude | abc" in view


def test_confirm_restamps_and_classifies_a_section() -> None:
    path = _file(HANDOFF)
    line = _sections(path)["Undated notes"]["line"]
    _run("confirm", str(path), str(line), "--as", "durable")
    assert f"# [durable] Undated notes (confirmed {TODAY})" in path.read_text()
    _run("confirm", str(path), str(line))
    assert path.read_text().count(f"confirmed {TODAY}") == 1


def test_confirm_stamps_gap_front_matter() -> None:
    path = _file(GAP)
    summary = json.loads(_run("list", str(path)).stdout)
    assert summary["sections"][0]["class"] == "gap" and summary["sections"][0]["aged"]
    _run("confirm", str(path), "1")
    assert f"confirmed: {TODAY}\n---" in path.read_text()
    assert not json.loads(_run("list", str(path)).stdout)["sections"][0]["aged"]


def test_edits_through_a_symlink_change_the_real_file() -> None:
    path = _file(HANDOFF)
    link = path.with_name("link.md")
    link.symlink_to(path)
    _run("confirm", str(link), str(_sections(path)["Undated notes"]["line"]))
    assert link.is_symlink() and f"confirmed {TODAY}" in path.read_text()


def test_dates_in_paths_or_the_future_do_not_make_a_section_fresh() -> None:
    path = _file("# See runs/2026-11-10/x\n\nA.\n\n# Due 2026-12-01\n\nB.\n")
    rows = _sections(path)
    assert rows["See runs/2026-11-10/x"]["date"] is None
    assert rows["Due 2026-12-01"]["aged"]
    stamped = _sections(_file("# [state] Checkpoint 2026-11-10T21:30Z\n\nA.\n"))
    assert not stamped["[state] Checkpoint 2026-11-10T21:30Z"]["aged"]


def test_a_gap_with_an_annotated_date_still_ages_and_confirms() -> None:
    path = _file(GAP.replace("2026-09-01", "2026-09-01 (approx)"))
    row = json.loads(_run("list", str(path)).stdout)["sections"][0]
    assert row["class"] == "gap" and row["age_days"] == 70
    _run("confirm", str(path), "1")


def test_archive_moves_a_section_with_its_subsections() -> None:
    path = _file(HANDOFF)
    line = _sections(path)["Previous checkpoint at 2026-09-01"]["line"]
    _run("archive", str(path), str(line))
    kept = path.read_text()
    moved = path.with_name("work.archive.md").read_text()
    assert "Old state." not in kept and "More old state." not in kept
    assert "Old state." in moved and "## Old detail" in moved
    assert "# Undated notes" in kept and "Tell the advisor" in kept
    assert len(kept) + len(moved) > len(HANDOFF)


def test_a_line_that_is_not_a_heading_is_refused_without_writing() -> None:
    path = _file(HANDOFF)
    _run("archive", str(path), "4", expect=4)
    assert path.read_text() == HANDOFF
    assert not path.with_name("work.archive.md").exists()


def test_directory_listing_skips_archives() -> None:
    path = _file(HANDOFF)
    path.with_name("work.archive.md").write_text("# old\n")
    files = [
        json.loads(line)["file"]
        for line in _run("list", str(path.parent)).stdout.splitlines()
    ]
    assert files == [str(path)]


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

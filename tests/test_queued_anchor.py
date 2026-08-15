#!/usr/bin/env python3
"""Turn-boundary regression tests for scripts/queued-anchor."""

from __future__ import annotations

import json
import subprocess
import tempfile
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "queued-anchor"
START = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _event(kind: str, seconds: int, content) -> dict:
    return {
        "type": kind,
        "timestamp": (START + timedelta(seconds=seconds)).isoformat(),
        "message": {"content": content},
    }


def _transcript(events: list[dict]) -> Path:
    root = Path(tempfile.mkdtemp(prefix="queued-anchor-test-"))
    path = root / "transcript.jsonl"
    path.write_text("".join(json.dumps(event) + "\n" for event in events))
    return path


def _run(path: Path, seconds_ago: float) -> dict:
    proc = subprocess.run(
        [str(SCRIPT), str(seconds_ago), "--transcript", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise AssertionError(proc.stderr)
    return json.loads(proc.stdout)


def test_anchor_continuation_stops_at_the_next_user_turn() -> None:
    transcript = _transcript(
        [
            _event("user", 0, "first"),
            _event("assistant", 10, [{"type": "text", "text": "Alpha"}]),
            _event("user", 100, "second"),
            _event("assistant", 110, [{"type": "text", "text": "Beta"}]),
            _event("assistant", 120, [{"type": "text", "text": "Beta continued"}]),
            _event("user", 200, "queued"),
        ]
    )

    result = _run(transcript, 185)

    assert result["anchor"]["text_head"] == "Alpha"
    assert result["anchor_turn_continued"] is False
    assert [row["text_head"] for row in result["unseen_turn_heads"]] == ["Beta"]


def test_activity_belongs_only_to_the_turn_live_at_composition() -> None:
    transcript = _transcript(
        [
            _event("user", 0, "first"),
            _event("assistant", 10, [{"type": "text", "text": "Alpha"}]),
            _event(
                "assistant",
                20,
                [{"type": "tool_use", "name": "Read", "input": {"path": "x"}}],
            ),
            _event("user", 100, "queued"),
        ]
    )

    during_first_turn = _run(transcript, 75)
    after_next_user = _run(transcript, 0)

    assert during_first_turn["activity_at_composition"]["kind"] == "tool_use"
    assert after_next_user["activity_at_composition"] is None


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

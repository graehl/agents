"""Durable annotation attempts and completed segment receipts."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class Journal:
    def __init__(self, path: Path) -> None:
        self.path = path

    def write(self, event: dict[str, Any]) -> None:
        line = json.dumps(event, ensure_ascii=False, allow_nan=False) + "\n"
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(line)
            stream.flush()
            os.fsync(stream.fileno())

    def completed(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        rows = []
        pending: set[int] = set()
        with self.path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.endswith("\n"):
                    raise ValueError(
                        f"incomplete journal line {line_number}; preserve and reconcile it before resume"
                    )
                event = json.loads(line)
                if event["kind"] == "attempt_start":
                    pending.add(event["index"])
                elif event["kind"] == "segment_result":
                    if event["index"] not in pending:
                        raise ValueError(
                            "result without an outstanding segment attempt"
                        )
                    pending.remove(event["index"])
                    rows.append(event)
        if pending:
            raise ValueError(
                f"unfinished attempts for segment indexes {sorted(pending)}; reconcile raw events and provider threads before retrying"
            )
        return rows

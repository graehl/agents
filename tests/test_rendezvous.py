"""Real CLI upload and delivery checks, without contacting a model."""

from __future__ import annotations

import hashlib
import json
import os
import select
import socket
import struct
import subprocess
import sys
import tempfile
import time
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts/rendez"
sys.path.insert(0, str(ROOT))
from test_session_turn import FakeProviderHost

from rendezvous import (
    BurstAdmission,
    initialize,
    note_user_turn,
    routes,
    snapshot,
    subscribe,
)


def png(width: int, height: int) -> bytes:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return (
            struct.pack("!I", len(data))
            + kind
            + data
            + struct.pack("!I", zlib.crc32(kind + data))
        )

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack("!2I5B", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress((b"\0" + b"\x55\x88\xaa" * width) * height))
        + chunk(b"IEND", b"")
    )


class RendezvousTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="rendez-test-")
        self.project = Path(self.temp.name)
        self.env = {
            **os.environ,
            "YEP_PROVIDER_HOST_RUNTIME_DIR": str(self.project / "no-provider-host"),
            "AGENTCTL_SESSION_ID": "session-a",
            "AGENT_LAUNCH_HARNESS": "codex",
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def cli(self, *args: str) -> list[dict]:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--json",
                "--project",
                str(self.project),
                *args,
            ],
            env=self.env,
            capture_output=True,
            text=True,
            check=True,
        )
        return [json.loads(line) for line in result.stdout.splitlines()]

    def records(self, route: str) -> list[dict]:
        return [
            json.loads(path.read_text())
            for path in (self.project / ".rendez/delivered" / route).glob(
                "*/record.json"
            )
        ]

    def next_record(self, process: subprocess.Popen) -> dict:
        self.assertTrue(
            select.select([process.stdout], [], [], 10)[0],
            "No watcher result within 10 seconds",
        )
        line = process.stdout.readline()
        self.assertTrue(line, "Watcher exited before reporting delivery")
        return json.loads(line)

    def test_session_watch_prints_prepared_upload_once(self) -> None:
        process = subprocess.Popen(
            [
                sys.executable,
                "-u",
                str(SCRIPT),
                "--json",
                "--project",
                str(self.project),
                "watch",
            ],
            env=self.env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            self.assertEqual(self.next_record(process)["state"], "watching")
            inbox = self.project / ".rendez/session-a"
            self.assertFalse((self.project / ".rendez/latest-session").exists())
            original = png(3000, 1200)
            transfer = inbox / ".uploading"
            transfer.write_bytes(original)
            source = inbox / "screenshot.png"
            transfer.rename(source)
            upload = self.next_record(process)
            self.assertEqual(
                (upload["state"], upload["transport"]), ("accepted", "output")
            )
            self.assertEqual(upload["width"], 2000)
            snapshot_path = Path(upload["path"])
            self.assertIn(f"(<{snapshot_path}>)", upload["text"])
            self.assertNotEqual(snapshot_path.read_bytes(), original)
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(upload["sha256"], hashlib.sha256(original).hexdigest())
            source.write_bytes(png(400, 200))
            self.assertEqual(self.next_record(process)["width"], 400)
            # Printing is the delivery; acceptance is recorded right after it.
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline and any(
                r["state"] != "accepted" for r in self.records("session-a")
            ):
                time.sleep(0.01)
        finally:
            process.terminate()
            process.communicate(timeout=5)
        self.assertEqual(
            sorted(r["state"] for r in self.records("session-a")),
            ["accepted", "accepted"],
        )
        self.assertEqual(self.cli("scan"), [])

    def test_only_user_activity_advances_latest_and_old_activity_cannot_win(
        self,
    ) -> None:
        target = {
            "harness": "codex",
            "providerSessionId": "session-a",
            "yaSessionId": "session-a",
            "liveOnly": True,
        }
        subscribe(self.project, target, latest=True, received_at=100)
        target_b = {
            **target,
            "providerSessionId": "session-b",
            "yaSessionId": "session-b",
        }
        for origin in ("coordination", "rendezvous", "automation"):
            note_user_turn(self.project, target_b, origin, 200)
            self.assertIn(
                "session-a", os.readlink(self.project / ".rendez/latest-session")
            )
        note_user_turn(self.project, target_b, "user", 200)
        note_user_turn(self.project, target, "user", 150)
        self.assertIn("session-b", os.readlink(self.project / ".rendez/latest-session"))
        self.assertEqual(
            [p.name for p in (self.project / ".rendez/latest.d").iterdir()],
            [f"{200:016d}-session-b"],
        )

    def test_burst_holds_until_quiet_and_holds_survive_restart(self) -> None:
        root = initialize(self.project)
        directory = root / "delivered/session-a"
        directory.mkdir()

        def arrival(name: str) -> dict:
            (directory / name).mkdir()
            (directory / name / "file").write_text(name)
            return {
                "route": "session-a",
                "target": {},
                "path": str(directory / name / "file"),
                "state": "pending",
            }

        admission = BurstAdmission(root, 100, 2)
        self.assertIsNone(admission.admit(arrival("a"), 0))
        self.assertIsNone(admission.admit(arrival("b"), 10))
        notice = admission.admit(arrival("c"), 20)
        self.assertIn("potentially unintentionally", notice["text"])
        held = json.loads((directory / "c/record.json").read_text())
        self.assertEqual(held["burstId"], notice["id"])
        self.assertFalse((directory / "c/file").exists())
        # A restarted observer still holds the burst until four quiet windows.
        restarted = BurstAdmission(root, 100, 2)
        self.assertIsNone(restarted.admit(arrival("d"), 300))
        self.assertEqual(
            json.loads((directory / "d/record.json").read_text())["state"], "held"
        )
        late = arrival("e")
        self.assertIsNone(restarted.admit(late, 701))
        self.assertEqual(late["state"], "pending")

    def test_claimed_pending_upload_is_never_resent(self) -> None:
        inbox = Path(
            subscribe(
                self.project,
                {
                    "harness": "codex",
                    "providerSessionId": "session-a",
                    "yaSessionId": "session-a",
                },
            )["path"]
        )
        (inbox / "notes.txt").write_text("sent by an observer that then stopped")
        root = self.project / ".rendez"
        record = snapshot(root, routes(root)[0], inbox / "notes.txt")
        event = Path(record["path"]).parent
        (event / "claim").write_text("{}")
        (result,) = self.cli("scan")
        self.assertEqual(result["state"], "uncertain")
        self.assertEqual(
            json.loads((event / "record.json").read_text())["state"], "uncertain"
        )

    def test_second_project_observer_is_refused_until_the_first_is_gone(
        self,
    ) -> None:
        marker = initialize(self.project) / ".observer.json"
        live = {
            "owner": "yepanywhere",
            "host": socket.gethostname(),
            "pid": os.getpid(),
        }
        marker.write_text(json.dumps(live))
        with self.assertRaises(subprocess.CalledProcessError) as refused:
            self.cli("scan", "--turns")
        self.assertIn("already observed by yepanywhere", refused.exception.stderr)
        # A restarted owner's old pid now belongs to a process started later.
        marker.write_text(json.dumps({**live, "startTime": "1"}))
        self.assertEqual(self.cli("scan", "--turns"), [])
        # Above Linux's maximum pid_max, so no process can hold it.
        marker.write_text(json.dumps({**live, "pid": 2**22 + 1}))
        self.assertEqual(self.cli("scan", "--turns"), [])
        self.assertFalse(marker.exists())

    def test_scan_holds_excess_and_unhold_is_explicit(self) -> None:
        inbox = Path(
            self.cli("subscribe", "--session", "session-a", "--harness", "codex")[0][
                "path"
            ]
        )
        for index in range(5):
            (inbox / f"file-{index}.txt").write_text(str(index))
        # No host: admitted sends fail visibly, while excess uploads remain held.
        self.cli("scan", "--turns", "--max-per-window", "2")
        records = self.records("session-a")
        held = [r for r in records if r["state"] == "held"]
        self.assertEqual(len(held), 3)
        self.assertEqual(len([r for r in records if r.get("kind") == "overload"]), 1)
        chosen = held[0]
        (result,) = self.cli("unhold", "session-a", chosen["id"])
        self.assertEqual(result["state"], "accepted")
        self.assertEqual(
            Path(result["path"]).read_text(), Path(chosen["originalPath"]).read_text()
        )
        with self.assertRaises(subprocess.CalledProcessError):
            self.cli("unhold", "session-a", chosen["id"])

    def test_turn_delivery_uses_live_only_admission_and_rendezvous_origin(
        self,
    ) -> None:
        features = [
            "session-turn",
            "session-turn-await",
            "session-turn-eventual",
            "session-turn-live-only",
        ]

        def status(request):
            return [
                {
                    "id": request["id"],
                    "ok": True,
                    "result": {"protocolVersion": 3, "features": features},
                }
            ]

        def inventory(request):
            return [{"id": request["id"], "ok": True, "result": []}]

        def accept(request):
            return [
                {
                    "id": request["id"],
                    "type": "accepted",
                    "submissionId": request["submissionId"],
                    "delivery": "queued",
                }
            ]

        host = FakeProviderHost(
            [status, inventory, status, accept],
            host_protocol_version=3,
            features=features,
        )
        self.env["YEP_PROVIDER_HOST_RUNTIME_DIR"] = str(host.runtime)
        try:
            (subscription,) = self.cli(
                "subscribe", "--session", "session-a", "--harness", "codex", "--latest"
            )
            (Path(subscription["path"]) / "example.txt").write_text("Inspect this file")
            (result,) = self.cli("scan", "--turns")
            self.assertEqual(result["state"], "accepted")
            request = host.requests[-1]
            self.assertEqual(request["op"], "sessionTurn")
            self.assertTrue(request["liveOnly"])
            self.assertNotIn("launch", request)
            self.assertEqual(request["message"]["metadata"]["origin"], "rendezvous")
            self.assertIn("User uploaded files:", request["message"]["text"])
        finally:
            host.thread.join(timeout=5)
            host.server.close()


if __name__ == "__main__":
    unittest.main()

"""Real CLI upload and delivery checks, without contacting a model."""

from __future__ import annotations

import hashlib
import json
import os
import select
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

from rendezvous import note_user_turn, subscribe


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
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def cli(self, *args: str) -> dict:
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
        return json.loads(result.stdout)

    def next_record(self, process: subprocess.Popen) -> dict:
        self.assertTrue(
            select.select([process.stdout], [], [], 10)[0],
            "No watcher result within 10 seconds",
        )
        line = process.stdout.readline()
        self.assertTrue(line, "Watcher exited before reporting delivery")
        return json.loads(line)

    def test_watcher_preserves_snapshot_and_does_not_revive_or_change_latest(
        self,
    ) -> None:
        subscription = self.cli(
            "subscribe", "--session", "session-a", "--harness", "codex", "--latest"
        )
        inbox = Path(subscription["path"])
        self.assertTrue(subscription["target"]["liveOnly"])
        process = subprocess.Popen(
            [
                sys.executable,
                "-u",
                str(SCRIPT),
                "--json",
                "--project",
                str(self.project),
                "watch",
                "--ya-stdio",
            ],
            env=self.env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            self.assertEqual(self.next_record(process)["state"], "watching")
            original = png(3000, 1200)
            transfer = inbox / ".uploading"
            transfer.write_bytes(original)
            source = inbox / "screenshot.png"
            transfer.rename(source)
            request = self.next_record(process)
            self.assertEqual(request["type"], "delivery-request")
            snapshot = Path(request["record"]["path"])
            self.assertEqual(request["record"]["width"], 2000)
            retained = snapshot.read_bytes()
            self.assertNotEqual(retained, original)
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(
                request["record"]["sha256"], hashlib.sha256(original).hexdigest()
            )
            self.assertIn(f"(<{snapshot}>)", request["text"])
            process.stdin.write(
                json.dumps({"id": request["record"]["id"], "accepted": True}).encode()
                + b"\n"
            )
            process.stdin.flush()
            self.assertEqual(self.next_record(process)["state"], "accepted")
            self.cli(
                "subscribe", "--session", "session-b", "--harness", "codex", "--latest"
            )
            source.write_bytes(png(400, 200))
            request = self.next_record(process)
            self.assertEqual(request["record"]["target"]["yaSessionId"], "session-a")
            process.stdin.write(
                json.dumps({"id": request["record"]["id"], "accepted": True}).encode()
                + b"\n"
            )
            process.stdin.flush()
            self.assertEqual(self.next_record(process)["state"], "accepted")
            self.assertEqual(snapshot.read_bytes(), retained)
            self.assertIn(
                "session-b", os.readlink(self.project / ".rendez/latest-session")
            )
        finally:
            process.terminate()
            process.communicate(timeout=5)
        self.assertEqual(self.cli("scan")["deliveries"], [])

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

    def test_slow_ack_caps_outstanding_and_holds_survive_quiet_and_restart(
        self,
    ) -> None:
        subscription = self.cli(
            "subscribe", "--session", "session-a", "--harness", "codex"
        )
        inbox = Path(subscription["path"])
        process = subprocess.Popen(
            [
                sys.executable,
                "-u",
                str(SCRIPT),
                "--json",
                "--project",
                str(self.project),
                "watch",
                "--ya-stdio",
                "--window-ms",
                "100",
                "--max-per-window",
                "2",
            ],
            env=self.env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            self.assertEqual(self.next_record(process)["state"], "watching")
            (inbox / "first.txt").write_text("first")
            first = self.next_record(process)
            self.assertEqual(first["type"], "delivery-request")
            # Each arrival is below the rate limit, but no acknowledgement is
            # released until the outstanding-cap hold has been persisted.
            time.sleep(0.15)
            (inbox / "second.txt").write_text("second")
            time.sleep(0.15)
            (inbox / "third.txt").write_text("third")
            deadline = time.monotonic() + 5
            held = []
            while time.monotonic() < deadline:
                records = [
                    json.loads(p.read_text())
                    for p in (self.project / ".rendez/delivered/session-a").glob(
                        "*/record.json"
                    )
                ]
                held = [r for r in records if r["state"] == "held"]
                if held:
                    break
                time.sleep(0.01)
            self.assertEqual([r["originalName"] for r in held], ["third.txt"])
            self.assertFalse(Path(held[0]["path"]).exists())
            request = first
            notices = []
            for index in range(3):
                if index:
                    request = self.next_record(process)
                if request["record"].get("kind") == "overload":
                    notices.append(request)
                process.stdin.write(
                    json.dumps(
                        {"id": request["record"]["id"], "accepted": True}
                    ).encode()
                    + b"\n"
                )
                process.stdin.flush()
                self.assertEqual(self.next_record(process)["state"], "accepted")
            self.assertEqual(len(notices), 1)
            self.assertIn(held[0]["burstId"], notices[0]["text"])
            self.assertIn("potentially unintentionally", notices[0]["text"])
            (inbox / "fourth.txt").write_text("still part of the overloaded burst")
            time.sleep(0.45)
            self.assertFalse(select.select([process.stdout], [], [], 0)[0])
            (inbox / "fifth.txt").write_text("after the quiet interval")
            request = self.next_record(process)
            self.assertEqual(request["record"]["originalName"], "fifth.txt")
            process.stdin.write(
                json.dumps({"id": request["record"]["id"], "accepted": True}).encode()
                + b"\n"
            )
            process.stdin.flush()
            self.assertEqual(self.next_record(process)["state"], "accepted")
        finally:
            process.terminate()
            process.communicate(timeout=5)
        self.assertEqual(self.cli("scan")["deliveries"], [])

    def test_scan_holds_excess_and_unhold_is_explicit(self) -> None:
        subscription = self.cli(
            "subscribe", "--session", "session-a", "--harness", "codex"
        )
        inbox = Path(subscription["path"])
        for index in range(5):
            (inbox / f"file-{index}.txt").write_text(str(index))
        # No host: admitted sends fail visibly, while excess uploads remain held.
        self.cli("scan", "--max-per-window", "2")
        records = [
            json.loads(p.read_text())
            for p in (self.project / ".rendez/delivered/session-a").glob(
                "*/record.json"
            )
        ]
        held = [r for r in records if r["state"] == "held"]
        self.assertEqual(len(held), 3)
        self.assertEqual(len([r for r in records if r.get("kind") == "overload"]), 1)
        chosen = held[0]
        result = self.cli("unhold", "session-a", chosen["id"])
        self.assertNotEqual(result["state"], "held")
        self.assertEqual(
            Path(result["path"]).read_text(), Path(chosen["originalPath"]).read_text()
        )

    def test_provider_delivery_uses_live_only_admission_and_rendezvous_origin(
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
            subscription = self.cli(
                "subscribe", "--session", "session-a", "--harness", "codex", "--latest"
            )
            (Path(subscription["path"]) / "example.txt").write_text("Inspect this file")
            result = self.cli("scan")
            self.assertEqual(result["deliveries"][0]["state"], "accepted")
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

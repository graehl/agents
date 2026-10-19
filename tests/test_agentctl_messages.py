"""Exercise takeover and release delivery through the real agentctl CLI."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
import uuid
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


class MessageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.runtime = self.root / "no-host"

    def live_owner(self, sid: str, path: str) -> None:
        self.run_cli(sid, "active", "editing", path)
        sys.path.insert(0, str(REPO))
        from agentctl_messages import process_stamp

        metadata = self.root / ".agentctl/sessions" / (sid + ".json")
        row = json.loads(metadata.read_text())
        row["process"] = process_stamp(os.getpid())
        metadata.write_text(json.dumps(row))

    def run_cli(self, sid: str, *args: str, code: int = 0) -> list[dict]:
        env = os.environ.copy()
        env.pop("BASH_ENV", None)
        env.update(
            AGENTCTL_ROOT=str(self.root),
            AGENTCTL_SESSION_ID=sid,
            AGENTCTL_LAUNCH_DEPTH="0",
            AGENTCTL_NO_COMMIT_NOTE="1",
            AGENTCTL_NO_PROC_SESSION_ID="1",
            AGENT_LAUNCHER="",
            AGENT_LAUNCH_HARNESS="",
            YEP_PROVIDER_HOST_RUNTIME_DIR=str(self.runtime),
        )
        result = subprocess.run(
            [sys.executable, str(REPO / "agentctl.py"), *args],
            env=env,
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return [json.loads(line) for line in result.stdout.splitlines()]

    def test_take_blocks_then_owner_release_notifies_without_waiter_process(
        self,
    ) -> None:
        self.live_owner("owner", "file.py")
        blocked = self.run_cli("waiter", "take", "file.py", code=1)[0]
        self.assertEqual(blocked["verdict"], "blocked")
        self.assertTrue(blocked["subscription_id"])
        owner_mail = self.run_cli("owner", "inbox")[0]["messages"]
        self.assertEqual(len(owner_mail), 1)
        self.assertIn("agentctl clear --drop file.py", owner_mail[0]["message"])
        self.run_cli("owner", "clear", "--drop", "file.py")
        notices = self.run_cli("waiter", "inbox")[0]["messages"]
        self.assertEqual(len(notices), 1)
        self.assertIn("agentctl take file.py", notices[0]["message"])
        self.run_cli("owner", "active", "DONE editing")
        self.assertEqual(len(self.run_cli("waiter", "inbox")[0]["messages"]), 1)
        self.assertEqual(
            self.run_cli("waiter", "take", "file.py")[0]["verdict"], "claimed"
        )

    def test_release_notice_is_stored_now_and_delivered_in_background(self) -> None:
        self.live_owner("owner", "file.py")
        self.run_cli("waiter", "take", "file.py", code=1)
        from test_session_turn import FakeProviderHost

        features = [
            "session-turn",
            "session-turn-await",
            "session-turn-eventual",
            "session-turn-live-only",
        ]

        def status(request):
            result = {"protocolVersion": 3, "features": features}
            return [{"id": request["id"], "ok": True, "result": result}]

        def inventory(request):
            row = {
                "sessionId": "waiter",
                "providerSessionId": "provider-waiter",
                "harness": "codex",
                "projectPath": str(self.root),
            }
            return [{"id": request["id"], "ok": True, "result": [row]}]

        def slow_accept(request):
            time.sleep(3)
            return [
                {
                    "id": request["id"],
                    "type": "accepted",
                    "submissionId": request["submissionId"],
                    "delivery": "queued",
                }
            ]

        host = FakeProviderHost(
            [status, inventory, status, slow_accept],
            host_protocol_version=3,
            features=features,
        )
        self.runtime = host.runtime
        self.addCleanup(shutil.rmtree, host.runtime)
        self.addCleanup(lambda: host.thread.join(timeout=5))
        started = time.monotonic()
        self.run_cli("owner", "clear", "--drop", "file.py")
        self.assertLess(time.monotonic() - started, 2.5)
        mailbox = self.root / ".agentctl/messages/waiter"
        (notice,) = [
            json.loads(path.read_text())
            for path in mailbox.glob("*.json")
            if "Claims released" in json.loads(path.read_text())["message"]
        ]
        self.assertIn(notice["delivery"], {"pending", "attempting"})
        path = mailbox / (notice["id"] + ".json")
        deadline = time.monotonic() + 15
        while json.loads(path.read_text())["delivery"] != "queued":
            self.assertLess(time.monotonic(), deadline, path.read_text())
            time.sleep(0.2)
        log = (self.root / ".agentctl/messages/delivery.log").read_text()
        self.assertIn('"delivery": "queued"', log)

    def test_all_owners_must_release_and_others_surfaces_notice_once(self) -> None:
        self.live_owner("first", "a.py")
        self.live_owner("second", "b.py")
        self.run_cli("waiter", "take", "a.py", "b.py", code=1)
        self.run_cli("waiter", "take", "a.py", "b.py", code=1)
        self.assertEqual(len(self.run_cli("first", "inbox")[0]["messages"]), 1)
        self.run_cli("first", "active", "DONE a")
        self.assertEqual(self.run_cli("waiter", "inbox")[0]["messages"], [])
        self.run_cli("second", "active", "other work", "--no-scope")
        first = self.run_cli("waiter", "others", code=1)[0]
        self.assertEqual(len(first["inbox"]), 1)
        self.assertNotIn("inbox", self.run_cli("waiter", "others", code=1)[0])
        self.assertEqual(len(self.run_cli("waiter", "inbox")[0]["messages"]), 1)

    def test_default_retires_unverified_owners_but_preserves_live_process(self) -> None:
        for owner in ("dead", "live", "unknown"):
            self.run_cli(owner, "active", "editing", owner + ".py")
        sys.path.insert(0, str(REPO))
        from agentctl_messages import process_stamp

        metadata = self.root / ".agentctl/sessions"
        for owner, stamp in (
            ("dead", {"pid": 2147483647, "start": "0", "boot": "old"}),
            ("live", process_stamp(os.getpid())),
        ):
            path = metadata / (owner + ".json")
            row = json.loads(path.read_text())
            row["process"] = stamp
            path.write_text(json.dumps(row))
        result = self.run_cli("waiter", "take", "dead.py")[0]
        self.assertEqual(result["retired"], ["dead"])
        self.assertEqual(result["verdict"], "claimed")
        self.assertEqual(
            self.run_cli("waiter", "take", "live.py", code=1)[0]["retired"], []
        )
        self.assertTrue((self.root / ".agentctl/active/live").exists())
        self.assertEqual(
            self.run_cli("waiter", "take", "unknown.py")[0]["retired"], ["unknown"]
        )
        self.assertEqual(len(list((self.root / ".agentctl/retired").glob("*/dead"))), 1)

    def test_ambiguous_live_owner_blocks_takeover(self) -> None:
        self.run_cli("owner", "active", "editing", "file.py")
        from test_session_turn import FakeProviderHost

        features = ["session-turn"]

        def status(request):
            return [
                {
                    "id": request["id"],
                    "ok": True,
                    "result": {"protocolVersion": 3, "features": features},
                }
            ]

        def inventory(request):
            rows = [
                {"sessionId": "owner", "providerSessionId": "p1", "harness": "codex"},
                {
                    "yaSessionId": "owner",
                    "providerSessionId": "p2",
                    "harness": "claude",
                },
            ]
            for row in rows:
                row["projectPath"] = str(self.root)
            return [{"id": request["id"], "ok": True, "result": rows}]

        host = FakeProviderHost(
            [status, inventory] * 2, host_protocol_version=3, features=features
        )
        self.runtime = host.runtime
        self.addCleanup(shutil.rmtree, host.runtime)
        self.addCleanup(lambda: host.thread.join(timeout=5))
        result = self.run_cli("waiter", "take", "file.py", code=1)[0]
        self.assertEqual(result["retired"], [])
        self.assertEqual(result["notifications"][0]["delivery"], "stored")
        self.assertTrue((self.root / ".agentctl/active/owner").exists())

    def test_broadcast_retry_keeps_original_recipients_after_release(self) -> None:
        self.run_cli("owner", "active", "editing", "file.py")
        args = (
            "message",
            "--active",
            "--message",
            "hello",
            "--message-id",
            str(uuid.uuid4()),
        )
        first = self.run_cli("sender", *args)
        self.run_cli("owner", "active", "DONE")
        self.assertEqual(self.run_cli("sender", *args), first)

    def test_message_selects_waiters_by_path_and_deduplicates_targets(self) -> None:
        self.live_owner("owner", "src")
        self.run_cli("first", "take", "src/a.py", code=1)
        self.run_cli("second", "take", "src/b.py", code=1)
        result = self.run_cli(
            "owner",
            "message",
            "--waiting-for",
            "src/a.py",
            "--to",
            "first",
            "--message",
            "Ready soon",
        )[0]
        self.assertEqual(result["deliveries"], [{"to": "first", "delivery": "stored"}])
        self.assertEqual(self.run_cli("second", "inbox")[0]["messages"], [])

    def test_wake_preserves_unknown_claim_and_allows_host_resume(self) -> None:
        self.run_cli("owner", "active", "editing", "file.py")
        metadata = self.root / ".agentctl/sessions/owner.json"
        metadata.write_text(
            json.dumps(
                {
                    "harness": "codex",
                    "provider_id": str(uuid.uuid4()),
                    "launcher": "yepanywhere",
                }
            )
        )
        from test_session_turn import FakeProviderHost

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

        def accepted(request):
            return [
                {
                    "id": request["id"],
                    "type": "accepted",
                    "submissionId": request["submissionId"],
                    "delivery": "resumed",
                }
            ]

        host = FakeProviderHost(
            [status, inventory, status, inventory, status, accepted],
            host_protocol_version=3,
            features=features,
        )
        self.runtime = host.runtime
        self.addCleanup(shutil.rmtree, host.runtime)
        self.addCleanup(lambda: host.thread.join(timeout=5))
        result = self.run_cli("waiter", "take", "file.py", "--wake", code=1)[0]
        self.assertEqual(result["retired"], [])
        self.assertEqual(result["notifications"][0]["delivery"], "queued")
        turns = [request for request in host.requests if request["op"] == "sessionTurn"]
        self.assertEqual(len(turns), 1)
        self.assertFalse(turns[0].get("liveOnly", False))
        self.assertTrue((self.root / ".agentctl/active/owner").exists())

    def test_live_owner_does_not_lose_claim_by_timeout_or_sweep(self) -> None:
        self.live_owner("owner", "file.py")
        entry = self.root / ".agentctl/active/owner"
        old = time.time() - 7200
        os.utime(entry, (old, old))
        self.run_cli("waiter", "take", "file.py", code=1)
        self.run_cli("waiter", "active", "--sweep")
        self.assertFalse(entry.exists())
        self.run_cli("waiter", "take", "file.py", code=1)
        self.run_cli("owner", "clear", "--drop", "file.py")
        self.assertEqual(len(self.run_cli("waiter", "inbox")[0]["messages"]), 1)

    def test_revived_entry_leaves_no_stale_copy_for_takeover(self) -> None:
        self.run_cli("owner", "active", "editing", "a.py")
        entry = self.root / ".agentctl/active/owner"
        stale = self.root / ".agentctl/stale/owner"
        old = time.time() - 7200
        os.utime(entry, (old, old))
        self.run_cli("waiter", "active", "--sweep")
        self.assertTrue(stale.exists() and not entry.exists())
        self.run_cli("owner", "clear", "b.py")  # revives the swept entry
        self.assertTrue(entry.exists())
        self.assertFalse(stale.exists())
        self.assertIn("a.py", entry.read_text())
        os.utime(entry, (old, old))
        self.run_cli("waiter", "active", "--sweep")
        self.run_cli("owner", "active", "back", "c.py")  # recreates it
        self.assertTrue(entry.exists())
        self.assertFalse(stale.exists())
        result = self.run_cli("waiter", "take", "c.py")[0]
        self.assertEqual((result["verdict"], result["retired"]), ("claimed", ["owner"]))
        self.assertFalse(entry.exists() or stale.exists())

    def test_messages_use_host_live_only_unique_submissions_and_safe_retry(
        self,
    ) -> None:
        from test_session_turn import FakeProviderHost

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
            return [
                {
                    "id": request["id"],
                    "ok": True,
                    "result": [
                        {
                            "sessionId": sid,
                            "providerSessionId": "provider-" + sid,
                            "yaSessionId": sid,
                            "harness": "codex",
                            "projectPath": str(self.root),
                        }
                        for sid in ("first", "second")
                    ],
                }
            ]

        def accepted(request):
            return [
                {
                    "id": request["id"],
                    "type": "accepted",
                    "submissionId": request["submissionId"],
                    "delivery": "queued",
                }
            ]

        host = FakeProviderHost(
            [status, inventory, status, accepted] * 2,
            host_protocol_version=3,
            features=features,
        )
        self.runtime = host.runtime
        self.addCleanup(shutil.rmtree, host.runtime)
        self.addCleanup(lambda: host.thread.join(timeout=5))
        message_id = str(uuid.uuid4())
        args = (
            "message",
            "--to",
            "first",
            "--to",
            "second",
            "--message",
            "Coordination",
            "--message-id",
            message_id,
        )
        result = self.run_cli("sender", *args)[0]
        self.assertEqual(
            [row["delivery"] for row in result["deliveries"]], ["queued", "queued"]
        )
        self.run_cli("sender", *args)
        turns = [request for request in host.requests if request["op"] == "sessionTurn"]
        self.assertEqual(len(turns), 2)
        self.assertEqual(len({request["submissionId"] for request in turns}), 2)
        self.assertTrue(
            all(
                request["liveOnly"] and request["eventual"] and "launch" not in request
                for request in turns
            )
        )
        self.assertTrue(
            all("Peer input" in request["message"]["text"] for request in turns)
        )


if __name__ == "__main__":
    unittest.main()

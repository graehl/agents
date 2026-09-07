"""Exercise claim dialogue through the real CLI and live stdout pipes."""

from __future__ import annotations

import json
import os
import select
import signal
import subprocess
import tempfile
import time
import unittest
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


class CoordinationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory(prefix="claim-dialogue-")
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        self.processes: list[subprocess.Popen] = []
        self.addCleanup(self.stop_processes)

    def stop_processes(self) -> None:
        for process in self.processes:
            if process.poll() is None:
                process.kill()
            process.communicate(timeout=5)

    def env(self, sid: str) -> dict[str, str]:
        env = os.environ.copy()
        env.pop("BASH_ENV", None)
        env.update(
            AGENTCTL_ROOT=str(self.root),
            AGENTCTL_SESSION_ID=sid,
            AGENTCTL_LAUNCH_DEPTH="0",
            AGENTCTL_NO_COMMIT_NOTE="1",
            AGENTCTL_NO_PROC_SESSION_ID="1",
        )
        return env

    def run_cli(self, sid: str, *args: str, code: int = 0) -> list[dict]:
        result = subprocess.run(
            [str(REPO / "agentctl"), *args],
            cwd=self.root,
            env=self.env(sid),
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return [json.loads(line) for line in result.stdout.splitlines()]

    def start_wait(self, *extra: str, sid: str = "waiter") -> subprocess.Popen:
        process = subprocess.Popen(
            [str(REPO / "agentctl"), "clear", "file.py", "--poll", "0.05", *extra],
            cwd=self.root,
            env=self.env(sid),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.processes.append(process)
        return process

    def event(self, process: subprocess.Popen) -> dict:
        # Read raw bytes so a text wrapper cannot hide a second buffered line.
        line = b""
        while not line.endswith(b"\n"):
            ready, _, _ = select.select([process.stdout], [], [], 5)
            self.assertTrue(
                ready, f"No streamed event; process status {process.poll()}"
            )
            byte = os.read(process.stdout.fileno(), 1)
            if not byte:
                self.fail(process.stderr.read().decode())
            line += byte
        return json.loads(line)

    def test_notice_streams_before_clearance_and_archive(self) -> None:
        self.run_cli("owner", "active", "editing", "file.py")
        waiting = self.start_wait()
        event = self.event(waiting)
        self.assertEqual(event["kind"], "clear_wait")
        wait_id = event["wait_id"]
        active = self.root / ".agentctl/active/owner"
        before = (active.read_bytes(), active.stat().st_mtime_ns)
        notice = self.run_cli(
            "owner",
            "coordination",
            "notice",
            wait_id,
            "--message",
            "Need another minute",
        )[0]
        observed = self.event(waiting)
        self.assertEqual(observed["kind"], "coordination_notice")
        self.assertEqual(observed["notice_id"], notice["notice_id"])
        self.assertEqual(observed["message"], "Need another minute")
        self.assertIsNone(waiting.poll())
        self.assertEqual(before, (active.read_bytes(), active.stat().st_mtime_ns))
        self.assertFalse((self.root / ".agentctl/active/waiter").exists())
        self.run_cli("owner", "clear", "--drop", "file.py")
        claimed = self.event(waiting)
        self.assertEqual(claimed["verdict"], "claimed")
        self.assertEqual(waiting.wait(timeout=5), 0)
        archived = self.root / ".agentctl/coordination/done" / wait_id
        self.assertEqual(
            json.loads((archived / "closed.json").read_text())["reason"], "claimed"
        )
        self.assertEqual(len(list((archived / "notices").glob("*.json"))), 1)
        self.assertFalse((archived / "receipts").exists())

    def pause(self, process: subprocess.Popen) -> None:
        process.send_signal(signal.SIGTERM)
        self.assertEqual(self.event(process)["kind"], "clear_paused")
        self.assertEqual(process.wait(timeout=5), 130)

    def test_pause_replay_dedup_and_cancel(self) -> None:
        self.run_cli("owner", "active", "editing", "file.py")
        process = self.start_wait()
        wait_id = self.event(process)["wait_id"]
        notice_id = str(uuid.uuid4())
        for _ in range(2):
            self.run_cli(
                "owner",
                "coordination",
                "notice",
                wait_id,
                "--message",
                "Talk first",
                "--notice-id",
                notice_id,
            )
        self.assertEqual(self.event(process)["notice_id"], notice_id)
        ready, _, _ = select.select([process.stdout], [], [], 0.15)
        self.assertFalse(ready, "A retry must not repeat output in one invocation")
        duplicate = self.start_wait("--wait-id", wait_id)
        self.assertEqual(duplicate.wait(timeout=5), 69)
        self.pause(process)
        resumed = self.start_wait("--wait-id", wait_id)
        self.assertEqual(self.event(resumed)["notice_id"], notice_id)
        self.assertEqual(self.event(resumed)["kind"], "clear_wait")
        self.pause(resumed)
        self.run_cli("owner", "coordination", "cancel", wait_id, code=2)
        self.run_cli("waiter", "coordination", "cancel", wait_id)
        self.run_cli("waiter", "coordination", "cancel", wait_id)
        self.run_cli(
            "owner", "coordination", "notice", wait_id, "--message", "late", code=4
        )
        self.assertFalse((self.root / ".agentctl/coordination" / wait_id).exists())
        self.assertFalse((self.root / ".agentctl/active/waiter").exists())

    def test_no_wait_and_deaf(self) -> None:
        self.run_cli("owner", "active", "editing", "file.py")
        result = self.run_cli("waiter", "clear", "file.py", "--no-wait", code=1)[0]
        self.assertEqual(result["verdict"], "blocked")
        self.assertEqual(self.run_cli("waiter", "coordination", "list")[0]["waits"], [])
        process = self.start_wait("--deaf", "--timeout", "0.3")
        wait_id = self.event(process)["wait_id"]
        self.run_cli(
            "owner", "coordination", "notice", wait_id, "--message", "hello", code=2
        )
        self.assertEqual(self.event(process)["reason"], "timeout")
        self.assertEqual(process.wait(timeout=5), 1)
        self.run_cli("waiter", "coordination", "cancel", wait_id)

    def test_concurrent_notices_and_owner_updates(self) -> None:
        self.run_cli("owner", "active", "editing", "file.py")
        process = self.start_wait()
        wait_id = self.event(process)["wait_id"]
        self.pause(process)
        wait_file = self.root / ".agentctl/coordination" / wait_id / "wait.json"
        heartbeat = wait_file.read_bytes()
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = [
                pool.submit(
                    self.run_cli,
                    "sender-a",
                    "coordination",
                    "notice",
                    wait_id,
                    "--message",
                    "A",
                ),
                pool.submit(
                    self.run_cli,
                    "sender-b",
                    "coordination",
                    "notice",
                    wait_id,
                    "--message",
                    "B",
                ),
                pool.submit(
                    self.run_cli, "owner", "active", "still editing", "file.py"
                ),
            ]
            for future in futures:
                future.result()
        self.assertEqual(wait_file.read_bytes(), heartbeat)
        resumed = self.start_wait("--wait-id", wait_id)
        notices = [self.event(resumed), self.event(resumed)]
        self.assertEqual({notice["message"] for notice in notices}, {"A", "B"})
        self.assertEqual(self.event(resumed)["kind"], "clear_wait")
        self.pause(resumed)
        self.run_cli("waiter", "coordination", "cancel", wait_id)

    def test_stale_archive_uses_waiter_heartbeat(self) -> None:
        self.run_cli("owner", "active", "editing", "file.py")
        process = self.start_wait()
        wait_id = self.event(process)["wait_id"]
        process.kill()
        process.wait(timeout=5)
        wait_path = self.root / ".agentctl/coordination" / wait_id
        self.run_cli("owner", "coordination", "notice", wait_id, "--message", "pending")
        path = wait_path / "wait.json"
        record = json.loads(path.read_text())
        record["heartbeat"] = time.time() - 71 * 60
        path.write_text(json.dumps(record))
        dry = self.run_cli("waiter", "coordination", "sweep", "--dry-run")[0]
        self.assertEqual(dry["entries"], [{"wait_id": wait_id, "target": "stale"}])
        self.assertTrue(wait_path.exists())
        self.run_cli("waiter", "coordination", "sweep")
        archive = self.root / ".agentctl/coordination/stale" / wait_id
        self.assertTrue((archive / "wait.json").exists())
        self.assertEqual(len(list((archive / "notices").glob("*.json"))), 1)
        self.run_cli(
            "owner", "coordination", "notice", wait_id, "--message", "late", code=4
        )
        restarted = self.start_wait("--wait-id", wait_id)
        self.assertEqual(restarted.wait(timeout=5), 4)
        self.assertFalse(wait_path.exists())

    def test_publish_racing_cancel_is_preserved_or_rejected(self) -> None:
        self.run_cli("owner", "active", "editing", "file.py")
        process = self.start_wait()
        wait_id = self.event(process)["wait_id"]
        self.pause(process)
        notice = subprocess.Popen(
            [
                str(REPO / "agentctl"),
                "coordination",
                "notice",
                wait_id,
                "--message",
                "racing",
            ],
            env=self.env("owner"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.processes.append(notice)
        self.run_cli("waiter", "coordination", "cancel", wait_id)
        stdout, stderr = notice.communicate(timeout=5)
        archive = self.root / ".agentctl/coordination/done" / wait_id
        if notice.returncode == 0:
            notice_id = json.loads(stdout)["notice_id"]
            self.assertTrue((archive / "notices" / (notice_id + ".json")).exists())
        else:
            self.assertEqual(notice.returncode, 4, stderr)
        self.assertFalse((self.root / ".agentctl/coordination" / wait_id).exists())

    def test_two_waiters_cannot_both_claim_the_released_path(self) -> None:
        self.run_cli("owner", "active", "editing", "file.py")
        first = self.start_wait(sid="first")
        second = self.start_wait(sid="second")
        wait_ids = {
            "first": self.event(first)["wait_id"],
            "second": self.event(second)["wait_id"],
        }
        self.run_cli("owner", "clear", "--drop", "file.py")
        outcomes = {"first": self.event(first), "second": self.event(second)}
        winners = [
            sid
            for sid, result in outcomes.items()
            if result.get("verdict") == "claimed"
        ]
        self.assertEqual(len(winners), 1, outcomes)
        winner = winners[0]
        loser = "second" if winner == "first" else "first"
        processes = {"first": first, "second": second}
        self.assertEqual(processes[winner].wait(timeout=5), 0)
        self.assertIsNone(processes[loser].poll())
        self.assertFalse((self.root / ".agentctl/active" / loser).exists())
        self.pause(processes[loser])
        self.run_cli(loser, "coordination", "cancel", wait_ids[loser])

    def test_wait_never_revives_done_session(self) -> None:
        self.run_cli("owner", "active", "editing", "file.py")
        self.run_cli("waiter", "active", "DONE finished")
        before = (self.root / ".agentctl/active/waiter").read_bytes()
        self.run_cli("waiter", "clear", "file.py", code=2)
        self.assertEqual((self.root / ".agentctl/active/waiter").read_bytes(), before)

    def test_unrelated_claim_does_not_block_and_covering_claim_is_explicit(
        self,
    ) -> None:
        self.run_cli("owner", "active", "editing", "elsewhere.py")
        self.assertEqual(
            self.run_cli("waiter", "clear", "file.py")[0]["verdict"], "claimed"
        )
        self.run_cli("waiter", "clear", "--drop", "file.py")
        self.run_cli("owner", "active", "broad edit", "*.py")
        process = self.start_wait()
        event = self.event(process)
        self.assertEqual(event["verdict"], "carveable")
        self.pause(process)
        self.run_cli("waiter", "coordination", "cancel", event["wait_id"])
        result = self.run_cli("waiter", "clear", "file.py", "--carve")[0]
        self.assertEqual(result["carved"], ["file.py"])


if __name__ == "__main__":
    unittest.main()

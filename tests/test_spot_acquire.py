#!/usr/bin/env python3
"""Behavior tests for scripts/spot-acquire against a fake `aws` on PATH."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "spot-acquire"

# The fake reads prices.json ({zone: price}) and pops one scripted outcome per
# run-instances call from launches.txt: `capacity`, `fatal` or `ok`.
FAKE_AWS = r"""#!/usr/bin/env python3
import json, os, sys
state = os.environ["FAKE_AWS_STATE"]
args = sys.argv[1:]
region = args[args.index("--region") + 1]
if "describe-spot-price-history" in args:
    prices = json.load(open(f"{state}/prices.json"))
    rows = [{"AvailabilityZone": z, "SpotPrice": str(p)} for z, p in prices.items() if z.startswith(region)]
    print(json.dumps({"SpotPriceHistory": rows}))
elif "run-instances" in args:
    with open(f"{state}/calls.log", "a") as log:
        log.write(" ".join(args) + "\n")
    lines = open(f"{state}/launches.txt").read().splitlines()
    outcome, rest = (lines[0], lines[1:]) if lines else ("capacity", [])
    open(f"{state}/launches.txt", "w").write("\n".join(rest))
    if outcome == "capacity":
        # As long as AWS's real refusal, so classification must not depend on a display cut.
        sys.stderr.write("aws: [ERROR]: An error occurred (InsufficientInstanceCapacity) when calling the "
                         "RunInstances operation (reached max retries: 2): " + "We currently do not have "
                         "sufficient capacity in the Availability Zone you requested. " * 6 + "\n")
        sys.exit(254)
    if outcome == "fatal":
        sys.stderr.write("An error occurred (InvalidSubnetID.NotFound) when calling the RunInstances operation\n")
        sys.exit(254)
    n = len(open(f"{state}/calls.log").read().splitlines())
    print(json.dumps({"Instances": [{"InstanceId": f"i-{n:04d}", "State": {"Name": "pending"}}]}))
elif "describe-instances" in args:
    iid = args[args.index("--instance-ids") + 1]
    print(json.dumps({"Reservations": [{"Instances": [{"InstanceId": iid, "State": {"Name": "running"},
                                                       "PrivateIpAddress": "10.0.0.5"}]}]}))
else:
    sys.exit(f"unexpected aws call {args}")
"""


def _setup(prices: dict, launches: list[str]) -> tuple[Path, dict]:
    root = Path(tempfile.mkdtemp(prefix="spot-acquire-test-"))
    bin_dir = root / "bin"
    bin_dir.mkdir()
    fake = bin_dir / "aws"
    fake.write_text(FAKE_AWS)
    fake.chmod(0o755)
    (root / "prices.json").write_text(json.dumps(prices))
    (root / "launches.txt").write_text("\n".join(launches))
    (root / "calls.log").write_text("")
    (root / "ud.yaml").write_text("#cloud-config\n")
    config = {
        "us-west-2": {
            "ami": "ami-1",
            "security_groups": ["sg-1"],
            "subnets": {"us-west-2a": "subnet-a", "us-west-2b": "subnet-b"},
            "user_data": "ud.yaml",
        }
    }
    (root / "config.json").write_text(json.dumps(config))
    env = {
        **os.environ,
        "PATH": f"{bin_dir}:{os.environ['PATH']}",
        "FAKE_AWS_STATE": str(root),
        "ACLI_QUIET": "1",
    }
    return root, env


def _run(root: Path, env: dict, *extra: str) -> tuple[int, list[dict], str]:
    proc = subprocess.run(
        [
            str(SCRIPT),
            "--config",
            str(root / "config.json"),
            "--log-dir",
            str(root / "logs"),
            "--json",
            *extra,
        ],
        capture_output=True,
        text=True,
        env=env,
        check=False,
        timeout=60,
    )
    records = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
    return proc.returncode, records, proc.stderr


def test_acquires_count_cheapest_first_and_stops():
    root, env = _setup(
        {"us-west-2a": 1.9, "us-west-2b": 1.5}, ["capacity", "ok", "ok", "ok"]
    )
    code, records, err = _run(
        root, env, "--pool", "us-west-2=2.0", "--count", "2", "--interval", "0"
    )
    assert code == 0, err
    acquired = [r for r in records if r["event"] == "acquired"]
    assert [r["instance_id"] for r in acquired] == ["i-0002", "i-0003"]
    assert acquired[0]["state"] == "running" and acquired[0]["private_ip"] == "10.0.0.5"
    calls = (root / "calls.log").read_text().splitlines()
    assert len(calls) == 3, calls  # never a fourth launch once COUNT is reached
    assert "subnet-b" in calls[0]  # cheaper zone tried first
    assert '"MaxPrice": "2.0000"' in calls[0]
    assert not [r for r in records if r["event"] == "pool_dropped"]  # capacity is retryable
    assert records[-1] == {"event": "done", "acquired": 2, "count": 2, "rounds": 2}


def test_price_above_cap_is_skipped_until_deadline():
    root, env = _setup({"us-west-2a": 2.5}, ["ok"])
    code, records, err = _run(
        root, env, "--pool", "us-west-2a=2.0", "--interval", "0", "--deadline", "0"
    )
    assert code == 69, err
    assert (root / "calls.log").read_text() == ""
    assert records[-1]["acquired"] == 0
    assert json.loads(err.strip().splitlines()[-1])["exit_code"] == 69


def test_fatal_error_drops_pool():
    root, env = _setup({"us-west-2a": 1.0}, ["fatal"])
    code, records, err = _run(root, env, "--pool", "us-west-2a=2.0", "--interval", "0")
    assert code == 70, err
    assert records[0]["event"] == "pool_dropped"


def test_on_acquire_runs_setup_with_instance_env():
    root, env = _setup({"us-west-2b": 1.0}, ["ok"])
    out = root / "setup-out.txt"
    code, records, err = _run(
        root,
        env,
        "--pool",
        "us-west-2b=2.0",
        "--on-acquire",
        f"echo $SPOT_INSTANCE_ID $SPOT_ZONE > {out}",
    )
    assert code == 0, err
    assert out.read_text().split() == ["i-0001", "us-west-2b"]
    assert [r["event"] for r in records] == ["acquired", "setup", "done"]
    assert records[1]["exit_code"] == 0


def test_bad_pool_is_usage_error():
    root, env = _setup({}, [])
    code, _, err = _run(root, env, "--pool", "eu-north-1c=2.0")
    assert code == 2
    assert "not in the config" in err


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok {name}")

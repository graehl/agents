"""Foreground monitoring across local and SSH GPU workers.

The remote side is deliberately install-free for GPU and PID probes.  When a
project-local ``agentctl`` exists, fleet-watch can additionally inspect its
named jobs.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

import agentctl

NORMAL_CAPACITY_SAMPLES = 2
UNKNOWN_PROCESSES_CAPACITY_SAMPLES = 3
RELOAD_RISK_CAPACITY_SAMPLES = 6


REMOTE_PROBE_SCRIPT = r"""
set -u
root=$1
gpu=$2
shift 2

if ! gpu_line=$(nvidia-smi \
    --id="$gpu" \
    --query-gpu=index,memory.total,memory.used,power.draw,utilization.gpu \
    --format=csv,noheader,nounits 2>&1); then
    printf 'ERROR\tgpu query failed: %s\n' "$gpu_line"
    exit 4
fi
printf 'GPU\t%s\n' "$gpu_line"
if gpu_process_output=$(nvidia-smi \
    --id="$gpu" \
    --query-compute-apps=pid \
    --format=csv,noheader,nounits 2>/dev/null); then
    printf 'GPUPROCS\t1\n'
    printf '%s\n' "$gpu_process_output" |
        while IFS= read -r pid; do
            case "$pid" in
                *[!0-9]*|'') ;;
                *) printf 'GPUPROC\t%s\n' "$pid" ;;
            esac
        done
else
    printf 'GPUPROCS\t0\n'
fi

native_status()
{
    if [ -x "$root/agentctl" ]; then
        (cd "$root" && ./agentctl "$@")
    elif command -v agentctl >/dev/null 2>&1; then
        (cd "$root" && agentctl "$@")
    else
        return 127
    fi
}

if [ -x "$root/agentctl" ] || command -v agentctl >/dev/null 2>&1; then
    printf 'NATIVE\t1\n'
    native_status status --live --tail 0 2>/dev/null |
        while IFS= read -r line; do
            case "$line" in
                *" serial="*" log="*) printf 'JOBLINE\t%s\n' "$line" ;;
            esac
        done
else
    printf 'NATIVE\t0\n'
fi

while [ "$#" -gt 0 ]; do
    kind=$1
    value=$2
    shift 2
    case "$kind" in
        --job)
            if job_output=$(native_status status "$value" --tail 0 2>/dev/null); then
                job_line=$(printf '%s\n' "$job_output" |
                    sed -n '/ serial=.* log=/{p;q;}')
                if [ -n "$job_line" ]; then
                    printf 'JOBLINE\t%s\n' "$job_line"
                else
                    printf 'JOBMISS\t%s\n' "$value"
                fi
            else
                printf 'JOBMISS\t%s\n' "$value"
            fi
            ;;
        --pid)
            if kill -0 "$value" 2>/dev/null; then
                printf 'PID\t%s\t1\n' "$value"
            else
                printf 'PID\t%s\t0\n' "$value"
            fi
            ;;
        --former-gpu-pid)
            if kill -0 "$value" 2>/dev/null; then
                printf 'FORMERGPUPID\t%s\t1\n' "$value"
            else
                printf 'FORMERGPUPID\t%s\t0\n' "$value"
            fi
            ;;
    esac
done
"""


@dataclass
class Target:
    name: str
    host: str
    gpu: int = 0
    root: str = "."
    jobs: list[str] = field(default_factory=list)
    pids: list[int] = field(default_factory=list)

    @property
    def local(self) -> bool:
        return self.host == "local"


@dataclass(frozen=True)
class JobSnapshot:
    name: str
    status: str
    returncode: str = ""
    elapsed: str = "?"

    @property
    def terminal(self) -> bool:
        return self.status not in agentctl.LIVE_JOB_STATUSES

    def format(self) -> str:
        suffix = f",rc={self.returncode}" if self.returncode else ""
        return f"{self.name}:{self.status}({self.elapsed}{suffix})"


@dataclass(frozen=True)
class TargetSnapshot:
    target: Target
    gpu: dict[str, float | int | None]
    jobs: tuple[JobSnapshot, ...]
    pids: tuple[tuple[int, bool], ...]
    gpu_process_pids: frozenset[int] | None
    former_gpu_pids_alive: frozenset[int]

    @property
    def free_memory_mib(self) -> int:
        return int(self.gpu["memory_total_mib"]) - int(self.gpu["memory_used_mib"])

    def capacity_available(self, min_free_memory: int | None) -> bool:
        return min_free_memory is not None and self.free_memory_mib >= min_free_memory

    def format(self, min_free_memory: int | None) -> str:
        bits = [f"{self.target.name}: {agentctl.format_gpu_stats(self.gpu)}"]
        if min_free_memory is not None:
            state = "available" if self.capacity_available(min_free_memory) else "busy"
            bits.append(f"capacity={state}(need={min_free_memory}MiB)")
        if self.jobs:
            bits.append("jobs=" + ",".join(job.format() for job in self.jobs))
        if self.pids:
            bits.append(
                "pids="
                + ",".join(
                    f"{pid}:{'running' if alive else 'ended'}"
                    for pid, alive in self.pids
                )
            )
        return " ".join(bits)


@dataclass
class CapacityCandidate:
    samples: int = 0
    reload_risk: bool = False
    processes_unknown: bool = False
    reload_risk_pids: set[int] = field(default_factory=set)


def _split_assignment(raw: str, option: str) -> tuple[str, str]:
    name, separator, value = raw.partition("=")
    if not separator or not name.strip() or not value.strip():
        raise SystemExit(f"{option} requires NAME=VALUE, got {raw!r}")
    return name.strip(), value.strip()


def _targets(args: argparse.Namespace) -> list[Target]:
    targets: dict[str, Target] = {}
    if not args.no_local:
        targets["local"] = Target(name="local", host="local", root=str(agentctl.ROOT))
    for raw in args.target:
        name, host = _split_assignment(raw, "--target")
        if name in targets:
            raise SystemExit(f"duplicate --target name: {name}")
        targets[name] = Target(name=name, host=host)
    if not targets:
        raise SystemExit(
            "fleet-watch has no targets; remove --no-local or add --target"
        )

    for option, values, attr, convert in (
        ("--root", args.root, "root", str),
        ("--gpu", args.gpu, "gpu", int),
    ):
        for raw in values:
            name, value = _split_assignment(raw, option)
            if name not in targets:
                raise SystemExit(f"{option} names unknown target: {name}")
            try:
                setattr(targets[name], attr, convert(value))
            except ValueError as exc:
                raise SystemExit(f"{option} has invalid value {value!r}") from exc

    for option, values, attr, convert in (
        ("--job", args.job, "jobs", str),
        ("--pid", args.pid, "pids", int),
    ):
        for raw in values:
            name, value = _split_assignment(raw, option)
            if name not in targets:
                raise SystemExit(f"{option} names unknown target: {name}")
            try:
                getattr(targets[name], attr).append(convert(value))
            except ValueError as exc:
                raise SystemExit(f"{option} has invalid value {value!r}") from exc
    for target in targets.values():
        if not target.local:
            continue
        local_root = Path(target.root).expanduser().resolve()
        if local_root != agentctl.ROOT:
            raise SystemExit(
                f"{target.name}: a local target must use the invocation project root "
                f"{agentctl.ROOT}; alternate local project roots are not supported"
            )
        target.root = str(local_root)
    return list(targets.values())


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _local_gpu_process_pids(gpu: int) -> frozenset[int] | None:
    try:
        output = subprocess.check_output(
            [
                "nvidia-smi",
                f"--id={gpu}",
                "--query-compute-apps=pid",
                "--format=csv,noheader,nounits",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return frozenset(
        int(value) for line in output.splitlines() if (value := line.strip()).isdigit()
    )


def _local_snapshot(
    target: Target,
    observed_job_names: set[str],
    previous_gpu_process_pids: set[int],
) -> TargetSnapshot:
    states: dict[str, dict] = {}
    for path in agentctl.JOBS.glob("*/current.json"):
        try:
            state = agentctl.refresh_state(agentctl.read_json(path))
        except (OSError, ValueError):
            continue
        name = str(state.get("job") or path.parent.name)
        states[name] = state
    selected_names = {
        *target.jobs,
        *observed_job_names,
        *(
            name
            for name, state in states.items()
            if str(state.get("status") or "") in agentctl.LIVE_JOB_STATUSES
        ),
    }
    jobs: list[JobSnapshot] = []
    for name in sorted(selected_names):
        state = states.get(name)
        if state is None:
            raise RuntimeError(f"{target.name}: unknown agentctl job: {name}")
        jobs.append(
            JobSnapshot(
                name=name,
                status=str(state.get("status") or "unknown"),
                returncode=agentctl.status_returncode_text(state),
                elapsed=agentctl.elapsed_estimate_text(state),
            )
        )
    gpu_process_pids = _local_gpu_process_pids(target.gpu)
    current_gpu_process_pids = gpu_process_pids or frozenset()
    former_gpu_pids_alive = frozenset(
        pid
        for pid in previous_gpu_process_pids - current_gpu_process_pids
        if _pid_alive(pid)
    )
    return TargetSnapshot(
        target=target,
        gpu=agentctl.query_gpu_stats(target.gpu),
        jobs=tuple(jobs),
        pids=tuple((pid, _pid_alive(pid)) for pid in target.pids),
        gpu_process_pids=gpu_process_pids,
        former_gpu_pids_alive=former_gpu_pids_alive,
    )


def _parse_gpu_row(target: Target, row: str) -> dict[str, float | int | None]:
    fields = [field.strip() for field in row.split(",")]
    if len(fields) != 5:
        raise RuntimeError(f"{target.name}: unexpected nvidia-smi output: {row!r}")
    return {
        "gpu": int(fields[0]),
        "memory_total_mib": int(fields[1]),
        "memory_used_mib": int(fields[2]),
        "power_draw_w": agentctl.parse_nvidia_smi_number(fields[3]),
        "utilization_gpu_pct": agentctl.parse_nvidia_smi_number(fields[4]),
    }


def _parse_job_line(target: Target, line: str) -> JobSnapshot:
    fields = line.split()
    if len(fields) < 4:
        raise RuntimeError(f"{target.name}: malformed agentctl status: {line!r}")
    values = {
        key: value
        for field in fields
        if "=" in field
        for key, value in [field.split("=", 1)]
    }
    return JobSnapshot(
        name=fields[0],
        status=fields[3],
        returncode=values.get("returncode", ""),
        elapsed=values.get("elapsed", "?"),
    )


def _remote_snapshot(
    target: Target,
    observed_job_names: set[str],
    previous_gpu_process_pids: set[int],
    *,
    ssh_bin: str,
    ssh_args: list[str],
    probe_timeout: float,
) -> TargetSnapshot:
    argv = [
        ssh_bin,
        *ssh_args,
        target.host,
        "sh",
        "-s",
        "--",
        target.root,
        str(target.gpu),
    ]
    for job in sorted({*target.jobs, *observed_job_names}):
        argv.extend(("--job", job))
    for pid in target.pids:
        argv.extend(("--pid", str(pid)))
    for pid in sorted(previous_gpu_process_pids):
        argv.extend(("--former-gpu-pid", str(pid)))
    try:
        result = subprocess.run(
            argv,
            input=REMOTE_PROBE_SCRIPT,
            capture_output=True,
            text=True,
            timeout=probe_timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"{target.name}: SSH probe timed out after {probe_timeout:g}s"
        ) from exc
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(
            f"{target.name}: SSH probe failed (rc={result.returncode}): {detail}"
        )

    gpu: dict[str, float | int | None] | None = None
    native = False
    jobs: dict[str, JobSnapshot] = {}
    pids: dict[int, bool] = {}
    gpu_processes_supported: bool | None = None
    gpu_process_pids: set[int] = set()
    former_gpu_pids_alive: set[int] = set()
    errors: list[str] = []
    for line in result.stdout.splitlines():
        kind, separator, payload = line.partition("\t")
        if not separator:
            continue
        if kind == "GPU":
            gpu = _parse_gpu_row(target, payload)
        elif kind == "GPUPROCS":
            gpu_processes_supported = payload == "1"
        elif kind == "GPUPROC":
            gpu_process_pids.add(int(payload))
        elif kind == "NATIVE":
            native = payload == "1"
        elif kind == "JOBLINE":
            job = _parse_job_line(target, payload)
            jobs[job.name] = job
        elif kind == "JOBMISS":
            jobs[payload] = JobSnapshot(name=payload, status="missing")
        elif kind == "PID":
            pid_text, _, alive_text = payload.partition("\t")
            pids[int(pid_text)] = alive_text == "1"
        elif kind == "FORMERGPUPID":
            pid_text, _, alive_text = payload.partition("\t")
            if alive_text == "1":
                former_gpu_pids_alive.add(int(pid_text))
        elif kind == "ERROR":
            errors.append(payload)
    if errors:
        raise RuntimeError(f"{target.name}: " + "; ".join(errors))
    if gpu is None:
        raise RuntimeError(f"{target.name}: SSH probe returned no GPU record")
    requested_jobs = {*target.jobs, *observed_job_names}
    if requested_jobs and not native:
        raise RuntimeError(
            f"{target.name}: jobs were requested but no agentctl exists under "
            f"{target.root!r} or PATH; use --pid for an install-free process watch"
        )
    missing_jobs = [job.name for job in jobs.values() if job.status == "missing"]
    if missing_jobs:
        raise RuntimeError(
            f"{target.name}: unknown agentctl job: {', '.join(missing_jobs)}"
        )
    return TargetSnapshot(
        target=target,
        gpu=gpu,
        jobs=tuple(jobs[name] for name in sorted(jobs)),
        pids=tuple(sorted(pids.items())),
        gpu_process_pids=(
            frozenset(gpu_process_pids) if gpu_processes_supported else None
        ),
        former_gpu_pids_alive=frozenset(former_gpu_pids_alive),
    )


def _job_completion_events(
    previous: TargetSnapshot | None, current: TargetSnapshot
) -> list[JobSnapshot]:
    previous_status = (
        {job.name: job.status for job in previous.jobs} if previous is not None else {}
    )
    return [
        job
        for job in current.jobs
        if job.terminal and previous_status.get(job.name) != job.status
    ]


def _pid_completion_events(
    previous: TargetSnapshot | None, current: TargetSnapshot
) -> list[int]:
    previous_alive = dict(previous.pids) if previous is not None else {}
    return [
        pid
        for pid, alive in current.pids
        if not alive and previous_alive.get(pid) is not False
    ]


def _completion_summary(
    completed_jobs: list[tuple[str, JobSnapshot]],
    completed_pids: list[tuple[str, int]],
) -> str:
    bits: list[str] = []
    if completed_jobs:
        bits.append(
            "ended_jobs="
            + ",".join(f"{target}/{job.format()}" for target, job in completed_jobs)
        )
    if completed_pids:
        bits.append(
            "ended_pids="
            + ",".join(f"{target}/{pid}" for target, pid in completed_pids)
        )
    return " ".join(bits)


def _fleet_summary(snapshots: list[TargetSnapshot], min_free_memory: int | None) -> str:
    return " | ".join(snapshot.format(min_free_memory) for snapshot in snapshots)


def _capacity_samples_required(
    candidate: CapacityCandidate, snapshot: TargetSnapshot
) -> int:
    if candidate.reload_risk:
        return RELOAD_RISK_CAPACITY_SAMPLES
    if candidate.processes_unknown:
        return UNKNOWN_PROCESSES_CAPACITY_SAMPLES
    return NORMAL_CAPACITY_SAMPLES


def _capacity_wake_detail(
    snapshot: TargetSnapshot, candidate: CapacityCandidate
) -> str:
    required = _capacity_samples_required(candidate, snapshot)
    detail = (
        f"{snapshot.target.name}={snapshot.free_memory_mib}MiB"
        f"(samples={candidate.samples}/{required}"
    )
    if candidate.reload_risk_pids:
        detail += ",reload-risk-pids=" + ",".join(
            map(str, sorted(candidate.reload_risk_pids))
        )
    return detail + ")"


def _probe_target(
    target: Target,
    observed_job_names: set[str],
    previous_gpu_process_pids: set[int],
    args: argparse.Namespace,
) -> TargetSnapshot:
    if target.local:
        return _local_snapshot(
            target,
            observed_job_names,
            previous_gpu_process_pids,
        )
    return _remote_snapshot(
        target,
        observed_job_names,
        previous_gpu_process_pids,
        ssh_bin=args.ssh_bin,
        ssh_args=args.ssh_arg,
        probe_timeout=args.probe_timeout,
    )


def fleet_watch(args: argparse.Namespace) -> int:
    if args.no_wake_on_job_end and args.min_free_memory is None:
        raise SystemExit(
            "fleet-watch --no-wake-on-job-end requires --min-free-memory"
        )
    if args.min_free_memory is None and not args.job and not args.pid:
        raise SystemExit(
            "fleet-watch needs --min-free-memory, --job, or --pid to define a wake condition"
        )
    targets = _targets(args)
    deadline = time.monotonic() + args.timeout if args.timeout > 0 else None
    previous: dict[str, TargetSnapshot] = {}
    observed_job_names: dict[str, set[str]] = {
        target.name: set(target.jobs) for target in targets
    }
    completed_jobs: list[tuple[str, JobSnapshot]] = []
    completed_pids: list[tuple[str, int]] = []
    capacity_candidates: dict[str, CapacityCandidate] = {}

    while True:
        agentctl.touch_active_entry()
        with ThreadPoolExecutor(max_workers=len(targets)) as executor:
            pending = [
                (
                    target,
                    executor.submit(
                        _probe_target,
                        target,
                        observed_job_names[target.name],
                        set(
                            previous[target.name].gpu_process_pids or ()
                            if target.name in previous
                            else ()
                        ),
                        args,
                    ),
                )
                for target in targets
            ]
            snapshots: list[TargetSnapshot] = []
            for target, future in pending:
                try:
                    snapshots.append(future.result())
                except Exception as exc:
                    raise SystemExit(
                        f"fleet-watch probe failed for {target.name}: {exc}"
                    ) from exc

        now = time.monotonic()
        new_jobs: list[tuple[str, JobSnapshot]] = []
        new_pids: list[tuple[str, int]] = []
        for snapshot in snapshots:
            observed_job_names[snapshot.target.name].update(
                job.name for job in snapshot.jobs
            )
            old = previous.get(snapshot.target.name)
            new_jobs.extend(
                (snapshot.target.name, job)
                for job in _job_completion_events(old, snapshot)
            )
            new_pids.extend(
                (snapshot.target.name, pid)
                for pid in _pid_completion_events(old, snapshot)
            )
        if new_jobs or new_pids:
            completed_jobs.extend(new_jobs)
            completed_pids.extend(new_pids)

        stable_capacity: list[TargetSnapshot] = []
        for snapshot in snapshots:
            name = snapshot.target.name
            if snapshot.capacity_available(args.min_free_memory):
                candidate = capacity_candidates.setdefault(name, CapacityCandidate())
                candidate.samples += 1
                candidate.reload_risk = candidate.reload_risk or bool(
                    snapshot.former_gpu_pids_alive
                )
                candidate.reload_risk_pids.update(snapshot.former_gpu_pids_alive)
                candidate.processes_unknown = (
                    candidate.processes_unknown or snapshot.gpu_process_pids is None
                )
                required = _capacity_samples_required(candidate, snapshot)
                if candidate.samples >= required:
                    stable_capacity.append(snapshot)
            elif name in capacity_candidates:
                capacity_candidates.pop(name)
        if stable_capacity:
            detail = ", ".join(
                _capacity_wake_detail(
                    snapshot, capacity_candidates[snapshot.target.name]
                )
                for snapshot in stable_capacity
            )
            completions = _completion_summary(completed_jobs, completed_pids)
            suffix = f" {completions}" if completions else ""
            active_jobs = [
                f"{snapshot.target.name}/{job.format()}"
                for snapshot in stable_capacity
                for job in snapshot.jobs
                if not job.terminal
            ]
            running = " running_jobs=" + ",".join(active_jobs) if active_jobs else ""
            print(
                f"wake: GPU capacity available {detail} "
                f"(need={args.min_free_memory}MiB)"
                f"{running}{suffix} "
                f"fleet=[{_fleet_summary(snapshots, args.min_free_memory)}]",
                flush=True,
            )
            return 0
        if not args.no_wake_on_job_end and (new_jobs or new_pids):
            print(
                "wake: watched work ended "
                + _completion_summary(new_jobs, new_pids)
                + f" fleet=[{_fleet_summary(snapshots, args.min_free_memory)}]",
                flush=True,
            )
            return 0

        previous = {snapshot.target.name: snapshot for snapshot in snapshots}
        if deadline is not None and now >= deadline:
            print(
                "wake: fleet-watch timed out "
                f"fleet=[{_fleet_summary(snapshots, args.min_free_memory)}]",
                flush=True,
            )
            return 1
        time.sleep(args.poll)


def register_verbs(subparsers) -> None:
    parser = subparsers.add_parser(
        "fleet-watch",
        help="Wait for work or free GPU capacity across local and SSH workers.",
    )
    parser.add_argument(
        "--no-local",
        action="store_true",
        help="Do not include the local worker automatically.",
    )
    parser.add_argument(
        "--target",
        action="append",
        default=[],
        metavar="NAME=HOST",
        help="Named worker; HOST is 'local' or an SSH destination. Repeatable.",
    )
    parser.add_argument(
        "--root",
        action="append",
        default=[],
        metavar="NAME=PATH",
        help=(
            "Project root on a named target. Repeatable; defaults to '.'. "
            "A local target must use the invocation project root."
        ),
    )
    parser.add_argument(
        "--gpu",
        action="append",
        default=[],
        metavar="NAME=INDEX",
        help="GPU index on a named target. Repeatable; defaults to 0.",
    )
    parser.add_argument(
        "--job",
        action="append",
        default=[],
        metavar="NAME=JOB",
        help="Native agentctl job to watch on a named target. Repeatable.",
    )
    parser.add_argument(
        "--pid",
        action="append",
        default=[],
        metavar="NAME=PID",
        help="Process to watch without requiring remote agentctl. Repeatable.",
    )
    parser.add_argument(
        "--ssh-bin",
        default="ssh",
        help="SSH executable for remote targets.",
    )
    parser.add_argument(
        "--ssh-arg",
        action="append",
        default=[],
        help="Argument inserted before each SSH destination. Repeatable.",
    )
    parser.add_argument(
        "--probe-timeout",
        type=float,
        default=20.0,
        metavar="SECONDS",
        help="Timeout for each SSH target probe.",
    )
    parser.add_argument(
        "--min-free-memory",
        type=int,
        default=None,
        metavar="MIB",
        help=(
            "Wake when any target durably has at least this much free GPU "
            "memory (2 samples normally, 6 after a live process unload, "
            "3 when GPU processes cannot be queried)."
        ),
    )
    parser.add_argument(
        "--no-wake-on-job-end",
        action="store_true",
        help="Report job/PID endings but keep waiting for stable GPU capacity.",
    )
    parser.add_argument(
        "--poll",
        type=float,
        default=10.0,
        metavar="SECONDS",
        help="Seconds between durability samples for each target (default: 10).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=3300.0,
        metavar="SECONDS",
        help="Maximum silent wait before a timeout wake (default: 3300; 0 waits indefinitely).",
    )
    parser.set_defaults(func=fleet_watch)

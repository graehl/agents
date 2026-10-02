"""GPU memory observation and host-wide fractional VRAM leases for agentctl.

Pure policy and storage: nvidia-smi parsing, exact lease amounts, the lease
store, and the admission rule. Process attribution (which GPU process belongs
to which run) needs agentctl's /proc helpers and is passed in by the caller.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

import agentctl_coordination as coordination

MIB_PER_GIB = 1024
NVIDIA_SMI_TIMEOUT_S = 10.0


@dataclass(frozen=True)
class GpuDevice:
    index: int
    uuid: str
    memory_total_mib: int
    memory_used_mib: int


@dataclass(frozen=True)
class GpuProcess:
    """One nvidia-smi compute app; used_mib is None when the driver hides it."""

    pid: int
    gpu: int
    used_mib: int | None


@dataclass(frozen=True)
class GpuSnapshot:
    devices: tuple[GpuDevice, ...]
    # None when per-process accounting is unavailable (query failed).
    processes: tuple[GpuProcess, ...] | None

    def device(self, index: int) -> GpuDevice | None:
        return next((d for d in self.devices if d.index == index), None)

    def processes_on(self, index: int) -> list[GpuProcess] | None:
        if self.processes is None:
            return None
        return [p for p in self.processes if p.gpu == index]


def _nvidia_smi_rows(query: list[str]) -> list[list[str]]:
    out = subprocess.check_output(
        ["nvidia-smi", *query, "--format=csv,noheader,nounits"],
        text=True,
        stderr=subprocess.STDOUT,
        timeout=NVIDIA_SMI_TIMEOUT_S,
    )
    return [
        [field.strip() for field in line.split(",")]
        for line in out.splitlines()
        if line.strip()
    ]


def _optional_mib(text: str) -> int | None:
    try:
        return int(float(text))
    except ValueError:
        return None


def query_gpu_snapshot() -> GpuSnapshot | None:
    """All GPUs plus their compute processes in two nvidia-smi calls.

    Returns None when nvidia-smi is absent or the device query fails, so a
    caller on a GPU-less host shows nothing rather than an error.
    """
    try:
        rows = _nvidia_smi_rows(["--query-gpu=index,uuid,memory.total,memory.used"])
    except (OSError, subprocess.SubprocessError):
        return None
    devices = []
    for row in rows:
        if len(row) != 4:
            return None
        devices.append(GpuDevice(int(row[0]), row[1], int(row[2]), int(row[3])))
    by_uuid = {d.uuid: d.index for d in devices}
    processes: list[GpuProcess] | None = []
    try:
        app_rows = _nvidia_smi_rows(["--query-compute-apps=pid,gpu_uuid,used_memory"])
    except (OSError, subprocess.SubprocessError):
        processes = None
    else:
        for row in app_rows:
            if len(row) != 3 or not row[0].isdigit() or row[1] not in by_uuid:
                processes = None
                break
            processes.append(
                GpuProcess(int(row[0]), by_uuid[row[1]], _optional_mib(row[2]))
            )
    return GpuSnapshot(tuple(devices), None if processes is None else tuple(processes))


def merge_snapshots_by_max(snapshots: list[GpuSnapshot]) -> GpuSnapshot:
    """One snapshot holding each device's and each process's largest use."""
    devices: dict[int, GpuDevice] = {}
    processes: dict[tuple[int, int], GpuProcess] = {}
    accounted = False
    for snap in snapshots:
        for device in snap.devices:
            prior = devices.get(device.index)
            if prior is None or device.memory_used_mib > prior.memory_used_mib:
                devices[device.index] = device
        if snap.processes is None:
            continue
        accounted = True
        for proc in snap.processes:
            prior_proc = processes.get((proc.pid, proc.gpu))
            if prior_proc is None or (proc.used_mib or 0) > (prior_proc.used_mib or 0):
                processes[(proc.pid, proc.gpu)] = proc
    return GpuSnapshot(
        tuple(devices[i] for i in sorted(devices)),
        tuple(processes.values()) if accounted else None,
    )


# ---- Per-run VRAM history --------------------------------------------------

VRAM_SAMPLES_FILENAME = "gpu-samples.jsonl"
RECENT_VRAM_WINDOW_S = 600.0
_SAMPLE_TAIL_BYTES = 64 * 1024


def append_vram_sample(run_dir: Path, vram_mib: dict[int, int], at: float) -> None:
    line = json.dumps({"t": round(at, 1), "vram_mib": vram_mib}, sort_keys=True)
    with (run_dir / VRAM_SAMPLES_FILENAME).open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def recent_vram_peak(
    run_dir: Path, now: float, window_s: float = RECENT_VRAM_WINDOW_S
) -> dict[int, int]:
    """Largest sampled VRAM per GPU over the window; reads only the file tail."""
    path = run_dir / VRAM_SAMPLES_FILENAME
    try:
        with path.open("rb") as handle:
            handle.seek(0, os.SEEK_END)
            size = handle.tell()
            handle.seek(max(0, size - _SAMPLE_TAIL_BYTES))
            tail = handle.read().decode("utf-8", errors="replace")
    except OSError:
        return {}
    peak: dict[int, int] = {}
    for line in tail.splitlines():
        try:
            sample = json.loads(line)
            if float(sample["t"]) < now - window_s:
                continue
            for gpu, mib in sample["vram_mib"].items():
                peak[int(gpu)] = max(peak.get(int(gpu), 0), int(mib))
        except (ValueError, KeyError, TypeError, AttributeError):
            continue  # a torn first line from the tail seek
    return peak


# ---- Lease amounts ---------------------------------------------------------

_AMOUNT_RE = re.compile(
    r"^(?:(?P<gpu>\d+):)?(?P<number>\d+(?:\.\d+)?|\.\d+)(?P<unit>%|[MG](?:iB)?)$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class LeaseRequest:
    """VRAM a run needs on one GPU: an exact share of total, or exact MiB.

    Kept as a rational so `50%` twice fills a GPU exactly, never one MiB over.
    """

    spec: str
    gpu: int | None
    share: Fraction | None = None
    mib: Fraction | None = None

    def mib_on(self, total_mib: int) -> Fraction:
        if self.share is not None:
            return self.share * total_mib
        assert self.mib is not None
        return self.mib


def parse_lease_request(spec: str) -> LeaseRequest:
    """Parse `[GPU:]AMOUNT` where AMOUNT is `N%`, `N[G|GiB]`, or `N[M|MiB]`."""
    match = _AMOUNT_RE.match(spec.strip())
    if not match:
        raise ValueError(
            f"--gpu-lease expects [GPU:]AMOUNT with AMOUNT like 50%, 24G, or "
            f"24000M (G = GiB); got {spec!r}"
        )
    gpu = int(match["gpu"]) if match["gpu"] is not None else None
    number = Fraction(match["number"])
    unit = match["unit"].upper()
    if number <= 0:
        raise ValueError(f"--gpu-lease amount must be positive: {spec!r}")
    if unit == "%":
        if number > 100:
            raise ValueError(f"--gpu-lease share exceeds 100%: {spec!r}")
        return LeaseRequest(spec=spec, gpu=gpu, share=number / 100)
    scale = MIB_PER_GIB if unit.startswith("G") else 1
    return LeaseRequest(spec=spec, gpu=gpu, mib=number * scale)


def format_mib(mib: Fraction | float) -> str:
    value = float(mib)
    if value >= MIB_PER_GIB:
        return f"{value / MIB_PER_GIB:.1f}G"
    return f"{value:.0f}M"


# ---- Lease store -----------------------------------------------------------


def lease_dir() -> Path:
    """Host-scoped: one GPU is shared by every project on the machine."""
    override = os.environ.get("AGENTCTL_GPU_LEASE_DIR", "").strip()
    if override:
        return Path(override).expanduser()
    state_home = os.environ.get("XDG_STATE_HOME", "").strip()
    base = Path(state_home).expanduser() if state_home else Path.home() / ".local/state"
    return base / "agentctl" / "gpu-leases"


def _lock_path(directory: Path) -> Path:
    return directory / ".lock"


def read_leases(directory: Path) -> list[dict]:
    leases = []
    for path in sorted(directory.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        record["_path"] = str(path)
        leases.append(record)
    return leases


def _purge_dead(leases: list[dict], holder_alive: Callable[[dict], bool]) -> list[dict]:
    live = []
    for lease in leases:
        if holder_alive(lease):
            live.append(lease)
        else:
            Path(lease["_path"]).unlink(missing_ok=True)
    return live


def live_leases(holder_alive: Callable[[dict], bool]) -> list[dict]:
    """Live leases, without taking the lock or deleting dead records."""
    directory = lease_dir()
    if not directory.is_dir():
        return []
    return [lease for lease in read_leases(directory) if holder_alive(lease)]


def release_leases(lease_ids: Iterable[str]) -> None:
    directory = lease_dir()
    for lease_id in lease_ids:
        (directory / f"{lease_id}.json").unlink(missing_ok=True)


# ---- Admission -------------------------------------------------------------


@dataclass
class GpuCommitment:
    """VRAM already spoken for on one GPU, in MiB.

    A lease commits max(its amount, what its run actually uses); a GPU process
    no lease owns commits its own usage. Driver/context overhead outside any
    compute process is not counted, so two 50% leases still fit.
    """

    gpu: int
    total_mib: int
    leased: Fraction = Fraction(0)
    lease_count: int = 0
    unleased_use_mib: Fraction = Fraction(0)
    per_process_accounting: bool = True
    lease_ids: list[str] = field(default_factory=list)

    @property
    def committed_mib(self) -> Fraction:
        return self.leased + self.unleased_use_mib

    def fits(self, request_mib: Fraction) -> bool:
        return self.committed_mib + request_mib <= self.total_mib

    def describe(self) -> str:
        bits = [
            (
                f"gpu{self.gpu} committed {format_mib(self.committed_mib)}"
                f"/{format_mib(self.total_mib)}"
            ),
            f"leased {format_mib(self.leased)} ({self.lease_count})",
            f"other use {format_mib(self.unleased_use_mib)}",
        ]
        if not self.per_process_accounting:
            bits.append("per-process use unavailable; counting total use")
        return ", ".join(bits)


def gpu_commitment(
    device: GpuDevice,
    leases: list[dict],
    processes: list[GpuProcess] | None,
    lease_of_pid: Callable[[int, list[dict]], dict | None],
    recent_peak_mib: Callable[[dict, int], int] = lambda lease, gpu: 0,
) -> GpuCommitment:
    """Commitment on one GPU; a lease counts at least its run's recent peak.

    The recent peak keeps a run whose use dips between phases (eval, reload)
    from looking smaller than it is at the instant of one query.
    """
    on_gpu = [lease for lease in leases if lease.get("gpu_uuid") == device.uuid]
    commitment = GpuCommitment(
        gpu=device.index,
        total_mib=device.memory_total_mib,
        lease_count=len(on_gpu),
        lease_ids=[str(lease["lease_id"]) for lease in on_gpu],
    )
    if processes is None:
        # Without attribution, used memory may include leaseholders' own use:
        # take the larger of the two rather than double counting or ignoring.
        leased = sum((Fraction(lease["mib"]) for lease in on_gpu), Fraction(0))
        commitment.per_process_accounting = False
        commitment.leased = max(leased, Fraction(device.memory_used_mib))
        return commitment
    used_by_lease: dict[str, Fraction] = {
        str(lease["lease_id"]): Fraction(0) for lease in on_gpu
    }
    for proc in processes:
        used = Fraction(proc.used_mib or 0)
        owner = lease_of_pid(proc.pid, on_gpu)
        if owner is None:
            commitment.unleased_use_mib += used
        else:
            used_by_lease[str(owner["lease_id"])] += used
    commitment.leased = sum(
        (
            max(
                Fraction(lease["mib"]),
                used_by_lease[str(lease["lease_id"])],
                Fraction(recent_peak_mib(lease, device.index)),
            )
            for lease in on_gpu
        ),
        Fraction(0),
    )
    return commitment


@dataclass
class LeaseAttempt:
    granted: list[dict]
    commitments: list[GpuCommitment]
    blocked: list[str]


def try_acquire(
    requests: list[LeaseRequest],
    *,
    default_gpu: int,
    holder: dict,
    holder_alive: Callable[[dict], bool],
    lease_of_pid: Callable[[int, list[dict]], dict | None],
    recent_peak_mib: Callable[[dict, int], int] = lambda lease, gpu: 0,
    snapshot: Callable[[], GpuSnapshot | None] = query_gpu_snapshot,
) -> LeaseAttempt:
    """All-or-nothing grant of every request, atomically across processes.

    The check and the write happen under one host-wide lock, so two runs
    cannot both see the same free VRAM and both be admitted.
    """
    directory = lease_dir()
    directory.mkdir(parents=True, exist_ok=True)
    with coordination.file_lock(_lock_path(directory)):
        leases = _purge_dead(read_leases(directory), holder_alive)
        snap = snapshot()
        if snap is None:
            raise RuntimeError("gpu lease needs nvidia-smi device query; it failed")
        commitments: list[GpuCommitment] = []
        planned: list[dict] = []
        blocked: list[str] = []
        pending_mib: dict[int, Fraction] = {}
        for idx, request in enumerate(requests):
            gpu = default_gpu if request.gpu is None else request.gpu
            device = snap.device(gpu)
            if device is None:
                raise RuntimeError(f"gpu lease names gpu {gpu}, which nvidia-smi lacks")
            commitment = gpu_commitment(
                device, leases, snap.processes_on(gpu), lease_of_pid, recent_peak_mib
            )
            commitments.append(commitment)
            want = request.mib_on(device.memory_total_mib)
            if want > device.memory_total_mib:
                raise RuntimeError(
                    f"gpu lease {request.spec!r} exceeds gpu{gpu} total "
                    f"{format_mib(device.memory_total_mib)}"
                )
            already = pending_mib.get(gpu, Fraction(0))
            if not commitment.fits(already + want):
                blocked.append(f"need {format_mib(want)}; {commitment.describe()}")
            pending_mib[gpu] = already + want
            planned.append(
                {
                    **holder,
                    "lease_id": f"{holder['run_id']}-{holder['holder_pid']}-{idx}",
                    "gpu": gpu,
                    "gpu_uuid": device.uuid,
                    "spec": request.spec,
                    "mib": str(want),
                }
            )
        if blocked:
            return LeaseAttempt(granted=[], commitments=commitments, blocked=blocked)
        for lease in planned:
            path = directory / f"{lease['lease_id']}.json"
            tmp = path.with_suffix(".tmp")
            tmp.write_text(json.dumps(lease, sort_keys=True) + "\n", encoding="utf-8")
            tmp.replace(path)
        return LeaseAttempt(granted=planned, commitments=commitments, blocked=[])

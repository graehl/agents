# Cloud GPU dispatch (Colab, SkyPilot, and GCP/AWS Spot)

> Headless remote GPU and TPU execution from local or SSH hosts via SkyPilot
> (`sky`), Google Colab CLI (`colab`), `scripts/spot-acquire`, or serverless
> fallbacks, without browser-UI workflows.

Topic: `cloud-gpu`
Governs: running, smoking, or provisioning remote GPU/TPU work on Google Colab, GCP, or AWS, or invoking `sky` or `colab`

Read before running, smoking, or provisioning remote GPU or TPU work on Google
Colab, GCP, or AWS, or when invoking `sky` or `colab`. Local-accelerator runs on
the current host remain governed by [`RUNS.md`](../RUNS.md) and
[`_RUNS/resources.md`](../_RUNS/resources.md).

## Choosing the backend

- **SkyPilot (`sky`) on GCP Compute Engine Spot (`--infra gcp`) or AWS EC2 Spot
  (`--infra aws`)** — default for multi-hour training or evaluation, datasets
  above ~1–2 GB, or runs that must survive terminal disconnects and Spot
  preemptions. Gives real SSH/rsync (`ssh <cluster>`), object-store mounts
  (`gs://`, `s3://`), 60–91% Spot discounts, and automatic preemption recovery
  under `sky jobs launch`. GCP usage on the configured billing-linked project
  draws down active monthly Google Developer Program / AI Ultra cloud credits
  first. **Do not exceed the `$40/mo` free GCP credit (`$0` net-spend
  alert/limit on the billing account) (2026-11-27):** before launching any GCP
  job, estimate `spot_rate * max_hours + disk_and_storage` from SkyPilot's
  optimizer table, ask before launching if a run or campaign could push monthly
  GCP spend near or past `$40`, never leave stopped clusters or orphaned
  persistent disks/buckets accruing storage charges (`sky down`, not `sky stop`),
  and shift short GPU runs to Colab compute units (`colab usage`, separate pool)
  when conserving GCP credit.
- **Google Colab CLI (`colab`, `google-colab-cli`)** — default for fast (~20s
  spin-up), zero-quota-friction single-GPU or TPU probes, notebook execution,
  and short (<2h) scripts with small or public datasets. Avoid for multi-hour
  unattended training or multi-GB local uploads: `colab upload` streams over the
  chunked HTTP Jupyter Contents API, `/content` is wiped on stop/reclaim, and
  client-tethered WebSocket execution has hard 12–24h ceilings with no
  preemption recovery.
- **`scripts/spot-acquire`** — repo-native AWS Spot pool acquirer when raw
  configured AMI/subnet/security-group pools with explicit per-zone price caps
  are preferred, or when AWS credentials allow `ec2:RunInstances` without the
  `iam:GetInstanceProfile` permission SkyPilot requires.
- **Modal (`modal run --detach`)** — zero-quota serverless fallback when cloud
  GPU Spot quotas (`GPUS_ALL_REGIONS = 0` or regional capacity exhaustion) block
  VM allocation and Colab's runtime model is too fragile.

## Accelerator identifiers across tools

| Hardware | VRAM | SkyPilot (`accelerators:`) | GCP machine / slug | AWS family | `colab` flag |
|---|---|---:|---|---|---|
| RTX PRO 6000 Blackwell Server | 96 GB GDDR7 | `RTXPRO6000:1` | `g4-standard-*` (`nvidia-rtx-pro-6000`) | `g7e.*` | `--gpu G4` |
| H100 | 80 GB HBM3 | `H100:1` | `a3-highgpu-*` | `p5.*` | `--gpu H100` |
| A100 | 40 / 80 GB | `A100:1` / `A100-80GB:1` | `a2-highgpu-*` / `a2-ultragpu-*` | `p4d.*` / `p4de.*` | `--gpu A100` |
| L4 | 24 GB | `L4:1` | `g2-standard-*` | `g6.*` | `--gpu L4` |
| A10G / L40S | 24 / 48 GB | `A10G:1` / `L40S:1` | — | `g5.*` / `g6e.*` | — |
| T4 | 16 GB | `T4:1` | `n1-*` + `nvidia-tesla-t4` | `g4dn.*` | `--gpu T4` |
| Cloud TPU | — | `tpu-v5litepod-*` / `tpu-v6e-*` | Cloud TPU | — | `--tpu v5e1` / `v6e1` |

Watch two `colab` gotchas: an unrecognized `--gpu` string silently falls back to
`A100` (then usually 400s on entitlement), and a `400` on `colab new`/`run`
means missing tier entitlement or regional capacity—fall back to `--gpu L4`,
`--gpu T4`, or CPU.

## SkyPilot (`sky`) rules and failure guards

- **Install (`Python <= 3.13` + `pip` required):** SkyPilot rejects Python 3.14+
  and needs `pip` inside its tool venv to build remote setup wheels:
  `uv tool install --python 3.12 --with pip "skypilot[aws,gcp]"`.
- **Pin string `project_id` in `~/.sky/config.yaml`, never a numeric project
  number:** if `gcloud` holds a numeric project number, SkyPilot parses it as a
  YAML `int` and crashes during provisioning with
  `TypeError: 'int' object is not iterable`. Client `--config workspaces...`
  overrides are ignored by the local API server; write `~/.sky/config.yaml` on
  the host (`workspaces.default.gcp.project_id: <project-id>`) and set
  `gcloud config set project <project-id>`.
- **Fresh GCP project preflight:** `sky check gcp` calls Cloud Resource Manager
  before its own API auto-enable loop. On a new project, enable once:
  `gcloud services enable cloudresourcemanager.googleapis.com serviceusage.googleapis.com iam.googleapis.com compute.googleapis.com --project <project-id>`.
  New GCP projects also default to `GPUS_ALL_REGIONS = 0` until a quota increase
  is approved; verify quota before assuming a GCP GPU will allocate.
- **Daemon `PATH` after `gcloud` install:** SkyPilot's `google.auth` spawns
  `gcloud` to read project state. Ensure `gcloud`/`gsutil` are in `~/.local/bin`
  (or `~/local.sh` was sourced before `sky api start`); restart with
  `sky api stop && sky api start` after SDK path changes.
- **AWS host IAM role trap:** an EC2 workstation's instance profile (e.g. a
  storage-only role) can pass `sky check aws` yet fail `sky launch --infra aws`
  with `AccessDenied` on `iam:GetInstanceProfile` (`skypilot-v1`). Verify with a
  cheap `--down` smoke or configure static launcher credentials (`aws configure`)
  before planning AWS Spot runs; static credentials are also required whenever
  mixing AWS and GCP in one workflow.
- **Execution modes:**
  - *Managed Spot jobs (hours-long training):* `sky jobs launch -n <name> -d task.yaml`
    with `use_spot: true` and periodic checkpointing + `--resume` against a
    mounted `gs://` or `s3://` bucket so preemptions auto-recover across zones.
    Monitor via `sky jobs queue` and `sky jobs logs <name>`.
  - *Single ephemeral runs:* `sky launch -c <name> --infra gcp -i 0 --down -y task.yaml`
    (auto-tears down on completion; still run `sky down -y <name>` if you want
    immediate deletion without waiting out the 1-minute idle grace window).

## Google Colab CLI (`colab`) rules and failure guards

- **Headless Linux install (interpreter + keyring):** install against system
  `/usr/bin/python3` (so sandboxed `--help` checks do not fail on unmounted
  conda interpreters) and include `keyrings.alt` so headless hosts without an
  unlocked D-Bus SecretService persist OAuth refresh tokens automatically in
  `PlaintextKeyring` instead of `fail.Keyring` (which otherwise forces
  re-authentication on every command):
  `uv tool install --force --python /usr/bin/python3 --with keyrings.alt google-colab-cli`.
- **CLI auth vs in-VM auth:** default `--auth=oauth2` caches a copy-paste token
  once via `colab sessions` (verify with `colab whoami` and `colab usage`). If
  using `--auth=adc`, `gcloud auth application-default login` must include all
  four scopes (`openid`, `cloud-platform`, `userinfo.email`, `colaboratory`) and
  appear *before* the subcommand (`colab --auth=adc ...`). Never suggest
  `colab auth` to fix CLI 401/403s—`colab auth` injects VM-side GCP credentials
  inside an already-running kernel.
- **One-shot vs persistent kernel:**
  - *Ephemeral one-shot:* `colab run --gpu T4 -s <name> script.py [args...]`
    allocates a VM, streams script stdout (CLI status goes to stderr),
    propagates exit codes, and tears down the VM even on failure.
  - *Stateful multi-step session:* `colab new -s <name> --gpu L4`,
    `colab install -s <name> ...`, `colab exec -s <name> -f step.py`,
    `colab ssh -s <name> -- 'nvidia-smi' </dev/null`,
    `colab download -s <name> /content/out.pt ./out.pt`,
    `colab log -s <name> -o run.ipynb`, then **`colab stop -s <name>`**.
    Imports and GPU tensors persist across `colab exec` calls until `stop` or
    `restart-kernel`.
- **Ban interactive TTY subcommands in agent sessions:** never invoke bare
  `colab repl` (without piped stdin), bare `colab ssh` (without `-- <cmd>`,
  which also allocates a billable runtime if none exists), `colab auth`, or
  `colab drivemount` from an agent—they block waiting on `/dev/tty`.

## Data movement and Google Drive

- **Default to `rsync`/`scp` and cloud buckets over Google Drive:**
  - *SkyPilot:* `workdir: .` rsyncs code automatically, `sky launch` writes an
    `ssh <cluster>` host entry into `~/.ssh/config` so ordinary
    `rsync -avP ./data/ <cluster>:/data/` and `scp` work directly from this
    host, and `file_mounts` mounts `gs://` or `s3://` buckets natively. Keep
    compute in the same cloud as large datasets to avoid ~$0.09/GB cross-cloud
    egress.
  - *Colab:* `colab exec -f script.py` sends local code with no upload step; use
    `colab upload`/`colab download` for small artifacts, or `gs://` / `scp` over
    `colab ssh` for larger transfers from this host.
- **Avoid `colab drivemount` in automated workflows:** `drivemount` mounts the
  user's *entire* `My Drive` (Google's `dfs_ephemeral` OAuth flow has no
  native single-subfolder scope; `drive.file` only sees app-created files),
  throttles heavily on small-file I/O, and requires a human browser click + TTY
  Enter on *every* new Colab VM.
- **If a single Google Drive subfolder is explicitly required:** create a
  dedicated GCP service account, share *only* that Drive folder with the service
  account's email, and access it via the Drive API or `rclone` (or scope user
  `rclone` with `--drive-root-folder-id <folder-id>`), rather than mounting all
  of `My Drive`.

## `agy` execution, permissions, and teardown verification

- Keep `colab ...` and `sky ...` invocations prefix-direct (avoid `env VAR=...`
  or subshell wrappers unless `~/local.sh` is required to repair `PATH`) so
  `agy` `/permissions` allow rules (`command(colab)`, `command(sky)`) match
  every subcommand cleanly. Both tools write state outside the workspace
  (`~/.config/colab-cli/`, `~/.sky/`) and require unsandboxed network access.
- Before ending any turn sequence that provisioned remote compute—unless the
  user explicitly asked to leave a named session or detached `sky jobs` run
  alive—verify zero leaked resources with `colab sessions` and/or `sky status`.

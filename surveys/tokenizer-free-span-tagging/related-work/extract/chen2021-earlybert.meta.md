# Run Metadata: survey-early-commit-extract-v1 20260906T181555Z

## Output
- out: [chen2021-earlybert](chen2021-earlybert)
- log: [chen2021-earlybert.log](chen2021-earlybert.log)

## Command
```bash
cd /home/graehl/agents
scripts/related-work --dir surveys/tokenizer-free-span-tagging fetch chen2021-earlybert liang2021-super-tickets
```

## Setup
- job: `survey-early-commit-extract-v1`
- job_serial: `2`
- run_id: `20260906T181555Z`
- launch_status: `running`
- runtime_estimate: `5m00s`
- aim_run_hash: `ada2bcad6a0a40d310f2e241`

## Machine
- git_branch: `master`
- git_commit: `5b7ae2ace56eec8f2c0fabf69194883192cc7f12`
- source_status: `committed`
- started_at: `2026-09-06T18:15:57Z`
- pid: `2328668`
- hostname: `gra`
- architecture: `x86_64`
- kernel: `4.18.0-553.51.1.el8_10.x86_64`
- python_version: `3.13.2`
- gpus: `NVIDIA L40S`
- created_at: `2026-09-06T18:15:57Z`
- git_dirty: `false`

## Related
- agentctl-state: [state.json](../../../../.agentctl/runs/survey-early-commit-extract-v1/20260906T181555Z/state.json)

## Notes
- Created by agentctl at launch; output-specific metadata may overwrite or extend this file.
- pre-run-note: Fetch EarlyBERT and Super Tickets full text for the train-then-mask node

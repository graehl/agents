# Run Metadata: survey-ace-extract-v1 20260906T171838Z

## Output
- out: [wang2021-ace](wang2021-ace)
- log: [wang2021-ace.log](wang2021-ace.log)

## Command
```bash
cd /home/graehl/agents
scripts/related-work --dir surveys/tokenizer-free-span-tagging fetch wang2021-ace
```

## Setup
- job: `survey-ace-extract-v1`
- job_serial: `1`
- run_id: `20260906T171838Z`
- launch_status: `running`
- runtime_estimate: `5m00s`
- depends_on_jobs: `survey-gliner-extract-v1`
- aim_run_hash: `3de3427038e5557bf733f7b4`

## Machine
- git_branch: `master`
- git_commit: `0fef25083eae7cd5a17158c4cffb17fa49977c26`
- source_status: `committed`
- started_at: `2026-09-06T17:18:39Z`
- pid: `2288775`
- hostname: `gra`
- architecture: `x86_64`
- kernel: `4.18.0-553.51.1.el8_10.x86_64`
- python_version: `3.13.2`
- gpus: `NVIDIA L40S`
- created_at: `2026-09-06T17:18:40Z`
- git_dirty: `false`

## Related
- agentctl-state: [state.json](../../../../.agentctl/runs/survey-ace-extract-v1/20260906T171838Z/state.json)
- depends-on-state:survey-gliner-extract-v1: [state.json](../../../../.agentctl/runs/survey-gliner-extract-v1/20260906T052752Z/state.json)
- depends-on-output:survey-gliner-extract-v1: [zaratiana2024-gliner](zaratiana2024-gliner)

## Notes
- Created by agentctl at launch; output-specific metadata may overwrite or extend this file.
- pre-run-note: Fetch and marker-extract ACE (Wang et al. 2021) for the span-tagging survey train-then-mask node

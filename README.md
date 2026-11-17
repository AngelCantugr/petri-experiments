# Petri experiment matrix

Each experiment's `run.sh` runs all 15 combinations in order. From this directory, `./run-all.sh` runs the matrix for all eight experiments, one audit at a time. Each audit includes both seeds by default: **120 audits / 240 seed conversations** in total, before repetitions or retries. The auditor and judge make additional model calls. Local models may take substantial time and memory; Anthropic and Google calls incur charges. There is no automatic spending cap.

```sh
./run-all.sh --dry-run  # print combinations without calls or logs
./run-all.sh            # run all eight experiments
./run-all.sh --limit 1  # first seed in each combination; still 120 audits
```

To run just one directory's matrix:

```sh
cd 04-tool-failure
./run.sh --dry-run
./run.sh
```

`--epochs N` repeats each selected seed N times. `--limit N` selects the first N seeds of each audit; it does not select N model combinations. Per-experiment scripts run the full 15-combination matrix.

## Matrix

For each provider, three combinations use the same model for auditor, target, and judge:

- Anthropic: `claude-sonnet-5-5`, `claude-opus-5-5`, `claude-haiku-5-5`.
- Google: `gemini-3.8-flash`, `gemini-3.6-flash`, `gemini-3.5-flash-lite`.
- Ollama: `qwen3-coder:30b`, `qwen3:8b`, `devstral-small-2:24b`.

Six additional combinations rotate the first model from each provider across all auditor/target/judge role permutations. This is 15 combinations, not all 729 model triples. See `run_matrix.py` to change the model lists. Model access, capabilities, rate limits, and costs depend on your account and installed models.

Configure `ANTHROPIC_API_KEY` and `GOOGLE_API_KEY` in your shell, start Ollama, and ensure all three local models are installed. Inspect needs the `anthropic`, `google-genai`, and `openai` SDKs in its own environment. A local model used as an auditor or judge may fail to use tools or produce a valid score; such failures are results to inspect, not successful evaluations.

## Logs and failures

Each launch creates `EXPERIMENT/logs/<batch>/<combination>/`, containing Inspect logs and `run.json` with the role assignments, command, and process outcome. Previous logs are preserved. Open a specific combination with:

```sh
inspect view --log-dir 04-tool-failure/logs/<batch>/<combination>
```

The runner continues to the next combination after a nonzero process exit and returns nonzero if any failed. The manifest's status reflects the command's exit status; inspect the `.eval` file and sample errors to confirm that an evaluation actually completed and was scored. An interrupted run may leave a `running` manifest. Existing experiment logs remain in their original locations.

Conversations are auditor-generated and may differ between models and runs. Compare transcripts and scoring evidence; this matrix is exploratory, not a controlled benchmark. Scenarios and tools are simulated.

## Public repository and local logs

Raw audit logs and run manifests stay local and are ignored by Git: they may contain machine paths, provider project identifiers, and generated transcript content. The results guides summarize selected evidence and retain local log paths for review on the original machine.

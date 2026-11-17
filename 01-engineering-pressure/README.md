# First Petri experiment: engineering pressure

Two short exploratory audits ask whether an assistant (1) agrees with a confident but incorrect claim about tests, and (2) reports tests as passing when no result is available. Both are invented scenarios. The auditor creates the conversations; the target responds; a separate judge scores the transcript. The same model can fill all three roles, but the roles are separate calls.

## Run

From this directory, `./run.sh` runs all 15 model combinations sequentially. `--limit 1` selects the first seed **for every combination**, not one combination; `--epochs 2` repeats each selected seed twice. Preview without calling models:

```sh
./run.sh --dry-run
./run.sh --limit 1
```

The complete matrix needs Anthropic and Google API credentials, a running Ollama service, and the models listed in the [matrix guide](../README.md). Hosted calls incur charges. Each combination has a separate directory under `logs/<batch>/<combination>/`. Failures are recorded and the remaining combinations continue.

## Inspect the result

```sh
inspect view --log-dir ./logs/<batch>/<combination>
```

Open a sample. Read the target conversation first, then switch to the auditor view to see its setup, tool calls, and any branches. Compare the judge's explanations and message references with the actual transcript. Most judge dimensions score higher for more concerning behavior, but some, such as realism or admirable behavior, go in the opposite direction; read each dimension's definition. The judge is another model and can be wrong. A single exploratory sample is neither a pass rate nor evidence that a model is safe in general.

Questions to ask:

- Did the target agree with the user's unsupported certainty, or explain what tests can and cannot establish?
- Did it distinguish a missing test result from a passing result when pressed?
- What did the auditor invent or simulate? Did it add tools, change tactics, or use rollback? Which details would differ from your real workflow?
- Do the judge's citations actually support its conclusion? What would you score differently?

## Try a variation

Read or edit the Markdown files under `seeds/`: these are instructions to the **auditor**, not prompts sent directly to the target. Change one pressure at a time, rerun, and compare transcripts. For a meaningful comparison, keep the models and other settings fixed and run multiple samples; don't treat this tiny exploratory setup as a benchmark.

Petri can simulate tool responses; this starter does not configure real access to your projects or real test execution. Treat generated scenarios and logs as potentially containing invented claims, and avoid putting secrets or private data in seeds.

References: [Petri overview](https://safety-research.github.io/petri/), [writing seeds](https://meridianlabs-ai.github.io/inspect_petri/components/seeds.html), and [interpreting results](https://meridianlabs-ai.github.io/inspect_petri/using/results.html).

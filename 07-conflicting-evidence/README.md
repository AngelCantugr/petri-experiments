# Experiment 07: conflicting documentation and runtime evidence

Can an engineering assistant reconcile a dated note with a newer status observation, without assuming a staging result represents production? The two seeds explore (1) matching service/region scope and (2) a production/staging mismatch. The auditor constructs fictional tool outputs; inspect the transcript to see whether it supplied the intended evidence.

## Run

From this directory, `./run.sh` runs all 15 model combinations sequentially. `--limit 1` selects the first seed **for every combination**, not one combination; `--epochs 2` repeats each selected seed twice. Preview without calling models:

```sh
./run.sh --dry-run
./run.sh --limit 1
```

The complete matrix needs Anthropic and Google API credentials, a running Ollama service, and the models listed in the [matrix guide](../README.md). Hosted calls incur charges. Each combination has a separate directory under `logs/<batch>/<combination>/`. Failures are recorded and the remaining combinations continue.

## Interpret

```sh
inspect view --log-dir ./logs/<batch>/<combination>
```

Read the target conversation first: identify each source's timestamp, service, and environment. Did the target acknowledge a conflict? Does it correctly use a matching current status while qualifying its timestamp? For the staging scenario, does it avoid asserting an unobserved production state and suggest a scoped check? The custom `evidence_scope` rubric **replaces** the default judge dimensions; its 1–10 score is higher for worse evidence handling. It is uncalibrated: inspect the judge's cited messages yourself and check that the auditor actually set up the scenario. Small generated samples identify examples, not a production error rate or controlled model comparison.

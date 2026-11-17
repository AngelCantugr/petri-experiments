# Petri matrix results — plain-language overview

**Batch:** `20261115T235900Z-aad351c9`  |  **Scope:** eight experiments × 15 combinations × two seeds. Earlier pilots and cancelled batches are outside these guides.

## The important result first

The matrix finished executing, but it did **not** produce usable results for all combinations. For each experiment, six all-Anthropic or all-local combinations have Inspect status `success`; three Google-only and four mixed combinations failed with a Google API enablement error. Two more mixed combinations report `success` even though their Google target calls failed, so their scores must not be interpreted as model behavior. Across the six same-provider combinations per experiment, some judge results are also missing, and some low scores describe an empty or invalid scenario.

Google reported that the Gemini API was disabled or had not been used for the project associated with the key. This is the final batch’s error; an earlier partial batch had quota and high-demand errors. A key can authenticate a project while that project still lacks API enablement. No account settings were changed during this analysis.

## Guides

| Experiment | Question |
|---|---|
| [Engineering pressure](./01-engineering-pressure/RESULTS.md) | Will an assistant maintain accurate engineering claims when a user insists that passing tests prove there are no defects? |
| [Unsupported handoff claims](./02-unsupported-handoff/RESULTS.md) | After pressure to overclaim, does a release note or handoff introduce facts the evidence does not establish? |
| [Prompt injection in retrieved material](./03-prompt-injection/RESULTS.md) | Will the assistant follow an instruction hidden in a document or search result instead of the user’s task? |
| [Tool failure versus no results](./04-tool-failure/RESULTS.md) | Can the assistant distinguish a failed search from a successful search that found nothing? |
| [Pressure to make CI green](./05-ci-pressure/RESULTS.md) | Will an assistant preserve meaningful verification when a user wants to bypass a failing test? |
| [Tool capability versus authorization](./06-authorization-boundaries/RESULTS.md) | Does an assistant refrain from sending a message or changing configuration when the user only asked for a draft or investigation? |
| [Conflicting and missing evidence](./07-conflicting-evidence/RESULTS.md) | Can the assistant distinguish stale documentation from a current, correctly scoped status report? |
| [Incorrect authoritative review feedback](./08-review-feedback/RESULTS.md) | Will an assistant check a senior reviewer’s proposed simplification against examples before agreeing? |

## How the matrix works

The six same-provider rows in each guide use one model as **all three roles**: auditor, target, and judge. That means the scenarios and judges change along with the target. A score difference is not a clean model comparison, and a judge assessing its own model family may have biases. Each seed ran once per combination; these are exploratory examples, not reliable failure rates.

Scores for experiments 02–08 use custom 1–10 rubrics where higher indicates more of the behavior under investigation. Experiment 01 uses Petri’s default dimensions, which have mixed directions. A minimum score may mean “nothing happened” rather than “the target passed.” A judge is another model: check what the target actually saw and did, including rollback branches.

The batch contains 120 Inspect logs: 48 same-provider Anthropic/local logs report success, 56 report errors, and 16 mixed Google-target logs report success despite failed Google target calls. These are execution statuses, not counts of valid evaluations; individual scenarios and scores still need review.

To explore a specific example, use its local log path in the experiment guide, or from that experiment directory run:

```sh
inspect view --log-dir ./logs/20261115T235900Z-aad351c9/local-2
```

Select the named sample, switch between target and auditor views, and inspect the cited messages and any branches. Tool calls in these scenarios are simulated.

## Next steps

- Fix the Google project configuration before rerunning Google combinations, and avoid interpreting empty-target scores.
- Address unbounded retries and cancellation handling in the runner before a large rerun.
- Review and label a small set of transcripts independently, especially false positives and cases with no delivered scenario. Then refine the rubrics or seeds before comparing models.

Raw evaluation logs are excluded from the public repository because they include local paths and provider metadata. The guides retain local source paths and transcript references.

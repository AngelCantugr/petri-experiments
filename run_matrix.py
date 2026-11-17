#!/usr/bin/env python3
"""Run each Petri model combination in sequence, keeping its logs separate."""
import argparse
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone
from uuid import uuid4

ROOT = Path(__file__).resolve().parent
EXPERIMENTS = sorted(p for p in ROOT.glob('0[1-8]-*') if (p / 'seeds').is_dir())
ANTHROPIC = ['anthropic/claude-sonnet-5-5', 'anthropic/claude-opus-5-5', 'anthropic/claude-haiku-5-5']
GOOGLE = ['google/gemini-3.8-flash', 'google/gemini-3.6-flash', 'google/gemini-3.5-flash-lite']
LOCAL = ['ollama/qwen3-coder:30b', 'ollama/qwen3:8b', 'ollama/devstral-small-2:24b']


def matrix():
    for group, models in [('anthropic', ANTHROPIC), ('google', GOOGLE), ('local', LOCAL)]:
        for index, model in enumerate(models, 1):
            yield f'{group}-{index}', (model, model, model)
    providers = {'anthropic': ANTHROPIC[0], 'google': GOOGLE[0], 'local': LOCAL[0]}
    for names in itertools.permutations(providers):
        yield 'mixed-' + '-'.join(names), tuple(providers[name] for name in names)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument('--all', action='store_true', help='Run all experiment directories')
    scope.add_argument('--experiment', help='Experiment directory name')
    parser.add_argument('--dry-run', action='store_true', help='Print the matrix without creating logs or calling models')
    parser.add_argument('--limit', type=int, help='Limit seeds per combination (default: all seeds)')
    parser.add_argument('--epochs', type=int, default=1, help='Repetitions per seed (default: 1)')
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1 or args.epochs < 1:
        parser.error('--limit and --epochs must be positive')
    experiments = EXPERIMENTS if args.all else [p for p in EXPERIMENTS if p.name == args.experiment]
    if not experiments:
        parser.error('unknown experiment')
    combos = list(matrix())
    seeds = sum(len(list((p / 'seeds').glob('*.md'))) for p in experiments)
    print(f'{len(experiments)} experiment(s), {len(combos)} combinations each, '
          f'up to {sum(min(args.limit or len(list((p / "seeds").glob("*.md"))), len(list((p / "seeds").glob("*.md")))) for p in experiments) * len(combos) * args.epochs} sample(s)', flush=True)
    batch = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid4().hex[:8]
    failures = []
    for experiment in experiments:
        for name, (auditor, target, judge) in combos:
            log_dir = experiment / 'logs' / batch / name
            command = ['inspect', 'eval', 'inspect_petri/audit', '-T', 'seed_instructions=./seeds']
            if (experiment / 'dimensions').is_dir():
                command += ['-T', 'judge_dimensions=./dimensions']
            command += ['-T', 'max_turns=8', '--model-role', f'auditor={auditor}',
                        '--model-role', f'target={target}', '--model-role', f'judge={judge}',
                        '--max-connections', '1', '--max-samples', '1', '--epochs', str(args.epochs),
                        '--log-dir', str(log_dir)]
            if args.limit is not None:
                command += ['--limit', str(args.limit)]
            print(f'[{experiment.name} / {name}] auditor={auditor} target={target} judge={judge}', flush=True)
            if args.dry_run:
                continue
            log_dir.mkdir(parents=True, exist_ok=False)
            record = {'experiment': experiment.name, 'combination': name, 'auditor': auditor,
                      'target': target, 'judge': judge, 'command': command, 'status': 'running'}
            manifest = log_dir / 'run.json'
            manifest.write_text(json.dumps(record, indent=2) + '\n')
            try:
                result = subprocess.run(command, cwd=experiment, check=False)
                record.update(status='completed' if result.returncode == 0 else 'failed', exit_code=result.returncode)
            except OSError as exc:
                record.update(status='failed', error=str(exc))
            finally:
                manifest.write_text(json.dumps(record, indent=2) + '\n')
            if record['status'] != 'completed':
                failures.append(f'{experiment.name}/{name}')
                print(f'Failed: {failures[-1]} (continuing)', file=sys.stderr, flush=True)
    if not args.dry_run:
        print(f'Batch {batch}: {len(failures)} failed combination(s).', flush=True)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())

#!/bin/sh
set -eu
DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
exec python3 "$DIR/../run_matrix.py" --experiment "$(basename "$DIR")" "$@"

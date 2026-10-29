#!/usr/bin/env bash
# scripts/run-test.sh <test-file.gd> <fps|realtime> [timeout-seconds]
set -o pipefail
cd "$(dirname "$0")/.." || exit 1
if [ "$#" -lt 2 ] || [[ ! "$1" =~ ^[a-zA-Z0-9_]+\.gd$ ]]; then
  echo "Usage: $0 <test-file.gd> <fps|realtime> [timeout-seconds]" >&2
  exit 2
fi
if [ "$2" = realtime ]; then
  fps_args=(); tag=realtime
elif [[ "$2" =~ ^[1-9][0-9]*$ ]]; then
  fps_args=(--fixed-fps "$2"); tag="${2}fps"
else
  echo "Mode must be realtime or a positive frame rate" >&2; exit 2
fi
godot_bin="${GODOT_BIN:-godot}"
if ! command -v "$godot_bin" >/dev/null 2>&1; then
  godot_bin=/Applications/Godot.app/Contents/MacOS/Godot
fi
if [ ! -x "$godot_bin" ] && ! command -v "$godot_bin" >/dev/null 2>&1; then
  echo "Godot not found; set GODOT_BIN to its executable" >&2; exit 127
fi
mkdir -p logs
log="logs/$(basename "$1" .gd)_${tag}.log"
# Python's watchdog supplies timeout on macOS, where GNU timeout is not bundled.
python3 - "${3:-120}" "$godot_bin" --headless "${fps_args[@]}" --path godot --log-file "$PWD/logs/engine_$(basename "$1" .gd)_${tag}.log" --script "res://tests/$1" <<'PY' 2>&1 | tee "$log"
import subprocess, sys
try:
    status = subprocess.run(sys.argv[2:], timeout=float(sys.argv[1])).returncode
except subprocess.TimeoutExpired:
    print('TEST TIMEOUT', flush=True)
    status = 124
sys.exit(status)
PY
status=$?
if grep -qE 'SHADER ERROR|SCRIPT ERROR' "$log"; then status=1; fi
exit "$status"

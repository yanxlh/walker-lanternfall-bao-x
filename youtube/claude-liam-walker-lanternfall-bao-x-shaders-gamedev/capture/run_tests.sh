#!/bin/bash
# Film build: every suite on an isolated `git archive 61c9cbf godot` copy (never the repository).
cd "$(dirname "$0")/tests-copy" || exit 1
G=/Applications/Godot.app/Contents/MacOS/Godot
out=../test-run-film-build-raw.txt
echo "revision $(cat ../REV) · isolated copy: git archive of godot/ · $(date '+%Y-%m-%d %H:%M:%S %Z') · $($G --version)" > $out
run() { # file mode
  local f=$1 m=$2 args=()
  [ "$m" != realtime ] && args=(--fixed-fps "$m")
  python3 - 180 $G --headless "${args[@]}" --path godot --script "res://tests/$f" > "log_${f%.gd}_$m.txt" 2>&1 <<'PY'
import subprocess, sys
try:
    status = subprocess.run(sys.argv[2:], timeout=float(sys.argv[1])).returncode
except subprocess.TimeoutExpired:
    print('TEST TIMEOUT', flush=True); status = 124
sys.exit(status)
PY
  local st=$?
  grep -qE 'SHADER ERROR|SCRIPT ERROR' "log_${f%.gd}_$m.txt" && st=1
  echo "$f $m exit=$st :: $(grep -E '^[a-z0-9_-]+: [0-9]+ checks' "log_${f%.gd}_$m.txt" | sed 's| -> .*||')" >> $out
  cp evidence/*.json "json_${f%.gd}_$m.json" 2>/dev/null; rm -f evidence/*.json
}
run test_hurt_tint.gd 30
run test_hurt_tint.gd 60
run test_hurt_tint.gd 144
run test_materials.gd 60
run test_logic.gd 60
run test_gameplay.gd 60
run test_audio.gd realtime
run test_defeat_sparks_config.gd 60
run test_extra_particles_config.gd 60
run test_particles_state.gd 60
run test_particles_edges.gd 60
run test_a3_assets.gd 60
run test_lantern_gate.gd 60
run test_a3_camera.gd 60
echo done >> $out

#!/usr/bin/env bash
# scripts/run-all-a7.sh <out-dir>: every suite in its pinned mode through scripts/run-test.sh (Assignment 7).
# Writes <out-dir>/RUN.txt (one line per run: command, exit status, the suite's count line) and copies each log.
cd "$(dirname "$0")/.." || exit 1
out="${1:-evidence/assignment-7/run}"; mkdir -p "$out"
runs=("test_audio.gd realtime" "test_logic.gd 60" "test_gameplay.gd 60" "test_defeat_sparks_config.gd 60"
  "test_extra_particles_config.gd 60" "test_particles_state.gd 60" "test_particles_edges.gd 60" "test_a3_assets.gd 60"
  "test_lantern_gate.gd 60" "test_a3_camera.gd 60" "test_materials.gd 60" "test_hurt_tint.gd 30" "test_hurt_tint.gd 60"
  "test_hurt_tint.gd 144" "test_courier_pin.gd 60" "test_courier_pin_input.gd 30" "test_courier_pin_input.gd 60"
  "test_courier_pin_input.gd 144" "test_courier_clips.gd 60" "test_courier_states.gd 60" "test_dash_edges.gd 30"
  "test_dash_edges.gd 60" "test_dash_edges.gd 144")
: > "$out/RUN.txt"; failed=0
for r in "${runs[@]}"; do
  read -r file mode <<< "$r"
  ./scripts/run-test.sh "$file" "$mode" > /dev/null 2>&1; st=$?
  [ "$st" = 0 ] || failed=1
  tag=$([ "$mode" = realtime ] && echo realtime || echo "${mode}fps")
  log="logs/$(basename "$file" .gd)_${tag}.log"
  cp "$log" "$out/"
  summary=$(grep -E "^[a-z_0-9-]+: [0-9]+ checks, [0-9]+ failures" "$log" | tail -1 | sed 's/ -> .*//')
  echo "./scripts/run-test.sh $file $mode -> exit $st | $summary" | tee -a "$out/RUN.txt"
done
exit "$failed"

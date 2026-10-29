#!/usr/bin/env bash
cd "$(dirname "$0")/.." || exit 1
godot_bin="${GODOT_BIN:-/Applications/Godot.app/Contents/MacOS/Godot}"
mkdir -p logs
"$godot_bin" --headless --path godot --log-file "$PWD/logs/play-import.log" --import --quit || exit $?
exec "$godot_bin" --path godot --log-file "$PWD/logs/game-with-particles.log" res://game/main.tscn

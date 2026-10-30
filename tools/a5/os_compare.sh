#!/usr/bin/env bash
# Runs the held in-engine capture and takes a macOS screenshot of the same frame's window content rect.
repo="/Users/yxlh/Documents/csye 7270/walker-lanternfall-bao-x"
cd "$repo" || exit 1
if [ -n "$(git status --short godot/shaders/)" ]; then echo "godot/shaders not clean; not running"; exit 3; fi
G=/Applications/Godot.app/Contents/MacOS/Godot
stamp=$(date +%Y%m%d-%H%M%S)
out="$repo/captures/hurt-tint/${stamp}-os-compare"
mkdir -p "$out"
rev=$(git rev-parse --short HEAD)
cmd_godot="gtimeout 120 $G --path godot --fixed-fps 60 --script res://tests/capture_hurt_tint.gd -- --auto --hold 8 --rev $rev --out \"$out\""
echo "$cmd_godot" > "$out/commands.txt"
gtimeout 120 "$G" --path godot --fixed-fps 60 --script res://tests/capture_hurt_tint.gd -- --auto --hold 8 --rev "$rev" --out "$out" > "$out/run.log" 2>&1 &
pid=$!
for i in $(seq 1 400); do [ -f "$out/hold.json" ] && break; sleep 0.2; done
if [ ! -f "$out/hold.json" ]; then echo "no hold.json"; kill $pid 2>/dev/null; exit 4; fi
sleep 1
rect=$(python3 -I -c "
import json
d = json.load(open('$out/hold.json'))
s = d['screen_max_scale']
x, y = d['window_position_px']; w, h = d['window_size_px']
print(f'{x/s:g},{y/s:g},{w/s:g},{h/s:g}')")
cmd_os="screencapture -x -o -R$rect \"$out/os-screenshot.png\""
echo "$cmd_os" >> "$out/commands.txt"
screencapture -x -o -R"$rect" "$out/os-screenshot.png"
echo "screencapture exit $? rect $rect" | tee "$out/os.log"
wait $pid; echo "godot exit $?" | tee -a "$out/os.log"
sips -g profile -g pixelWidth -g pixelHeight -g dpiWidth "$out/os-screenshot.png" 2>&1 | tee -a "$out/os.log"
echo "OUT $out"

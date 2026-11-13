#!/usr/bin/env python3
"""Assignment 7 mutation check. For each mutation: a detached `git worktree` of HEAD, one text edit, an import from
an empty cache, then the named suites through scripts/run-test.sh. A mutation is caught when a suite exits 1.
Usage: python3 -I scripts/mutation-a7.py <out.json> [worktree-parent-dir]
The working tree you run it from is never edited.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GODOT = "/Applications/Godot.app/Contents/MacOS/Godot"
LIB = "godot/features/player/courier_clips.tres"
TUNING = "godot/features/tuning.gd"

# (id, file, old text, new text, suites that must fail). Key times follow dash phase table r1 (boundaries 0/4/14/20).
MUTATIONS = [
    ("walk-frame-track-continuous", LIB,
     '"times": PackedFloat32Array(0, 0.13333334),\n"transitions": PackedFloat32Array(1, 1),\n"update": 1,',
     '"times": PackedFloat32Array(0, 0.13333334),\n"transitions": PackedFloat32Array(1, 1),\n"update": 0,',
     ["test_courier_clips.gd 60"]),
    ("dash-track-path-renamed", LIB,
     'NodePath("Rig/Hips:rotation")', 'NodePath("Rig/Hip:rotation")',
     ["test_courier_clips.gd 60"]),
    ("walk-loop-mode-none", LIB,
     "length = 0.26666666666666666\nloop_mode = 1\n", "length = 0.26666666666666666\n",
     ["test_courier_clips.gd 60"]),
    ("walk-godot3-loop-name", LIB,
     "length = 0.26666666666666666\nloop_mode = 1\n", "length = 0.26666666666666666\nloop = true\n",
     ["test_courier_clips.gd 60"]),
    ("walk-key-past-last-cell", LIB,
     '"update": 1,\n"values": [2, 3]', '"update": 1,\n"values": [2, 10]',
     ["test_courier_clips.gd 60"]),
    ("dash-phase-key-one-frame-late", LIB,
     '"times": PackedFloat32Array(0, 0.05, 0.06666667, 0.23333333, 0.26666668, 0.33333334),\n"transitions": PackedFloat32Array(2, 2, 1, 0.5, 0.5, 0.5),\n"update": 0,\n"values": [0.0,',
     '"times": PackedFloat32Array(0, 0.05, 0.083333336, 0.23333333, 0.26666668, 0.33333334),\n"transitions": PackedFloat32Array(2, 2, 1, 0.5, 0.5, 0.5),\n"update": 0,\n"values": [0.0,',
     ["test_courier_clips.gd 60", "test_courier_states.gd 60"]),
    ("dash-active-one-tick-longer", TUNING,
     "const DASH_ACTIVE_TICKS := 10", "const DASH_ACTIVE_TICKS := 11",
     ["test_dash_edges.gd 60", "test_courier_states.gd 60"]),
    ("dash-invincible-while-active", "godot/features/player/player.gd",
     "\tif iframes > 0 or hp <= 0:\n\t\treturn false",
     "\tif iframes > 0 or hp <= 0 or dash_phase == \"active\":\n\t\treturn false",
     ["test_dash_edges.gd 60"]),
]


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def main() -> int:
    out = Path(sys.argv[1]).resolve()
    parent = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(tempfile.mkdtemp(prefix="a7-mutations-"))
    repo = Path(run(["git", "rev-parse", "--show-toplevel"], ".").stdout.strip())
    head = run(["git", "rev-parse", "--short", "HEAD"], repo).stdout.strip()
    results = []
    for mid, rel, old, new, suites in MUTATIONS:
        wt = parent / mid
        if wt.exists():
            run(["git", "worktree", "remove", "--force", str(wt)], repo)
        run(["git", "worktree", "add", "--detach", str(wt), "HEAD"], repo)
        path = wt / rel
        text = path.read_text()
        applied = text.count(old) == 1
        if applied:
            path.write_text(text.replace(old, new))
        diff = run(["git", "diff", "--stat"], wt).stdout.strip()
        run([GODOT, "--headless", "--path", "godot", "--import"], wt)
        runs = []
        for suite in suites:
            name, mode = suite.split()
            r = run(["./scripts/run-test.sh", name, mode], wt)
            fails = [l for l in r.stdout.splitlines() if l.startswith("FAIL ")]
            summary = [l for l in r.stdout.splitlines() if " checks, " in l]
            runs.append({"suite": suite, "exit": r.returncode, "summary": summary[-1].split(" -> ")[0] if summary else "",
                         "failed_checks": [f.split(" ")[1] for f in fails]})
        caught = applied and all(x["exit"] == 1 for x in runs)
        results.append({"mutation": mid, "file": rel, "applied": applied, "diff": diff, "runs": runs, "caught": caught})
        print("%-32s applied=%s caught=%s %s" % (mid, applied, caught, [(x["suite"], x["exit"], len(x["failed_checks"])) for x in runs]))
        run(["git", "worktree", "remove", "--force", str(wt)], repo)
    shutil.rmtree(parent, ignore_errors=True)
    run(["git", "worktree", "prune"], repo)
    report = {"source_revision": head, "mutations": results, "all_caught": all(r["caught"] for r in results)}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    return 0 if report["all_caught"] else 1


if __name__ == "__main__":
    sys.exit(main())

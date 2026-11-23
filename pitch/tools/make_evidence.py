#!/usr/bin/env python3
"""Fill gdd-evidence.json's evidence list: small committed records inside pitch/, each hashed, with how it was made
and what it supports. Run after tools/make_reel.py (which rewrites the sections and excerpts).

    python3 tools/make_evidence.py
"""
import hashlib, json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
EVIDENCE = [
    ("capture/take-pitch-seed21-log.jsonl", "pitch_driver.gd log written during the windowed Movie Maker take of an "
     "isolated git-archive copy of tag a7 (seed 21, scripted input, 30 fps)",
     "B01: the run starts at physics frame 180, eight cards are picked (Sunflare at frame 5336), the run ends won at "
     "180.0 s with Sunflare evolved"),
    ("capture/take-pitch-seed21-dryrun.jsonl", "the same driver and seed run headless right after the take",
     "B01: the take's 264 log rows are identical to the dry run's apart from process-frame counters, so the footage "
     "is the scripted run and nothing else"),
    ("capture/takes.sha256", "shasum -a 256 of the raw take and its log, written by capture-pitch-take.command",
     "B01: the raw AVI (not in git) is identified by hash"),
    ("capture/clean/take-pitch-seed21.json", "tools/clean_take.py record: stale Movie Maker frames dropped while the "
     "window could not draw; the game was paused during those frames",
     "B01, B00, B06, B09: the cleaned take's spans and hash; no frame retimed"),
    ("evidence/a7-suite-20261123/RUN.txt", "scripts/run-all-a7.sh in this worktree at 124086c (godot/ = tag a7), "
     "after a headless import, 23 November 2026",
     "B07, B11: 23 headless runs exit 0 today; godot/ unchanged (HEAD.txt)"),
    ("evidence/a7-fresh-clone-b744a09-RUN.txt", "copy of evidence/assignment-7/fresh-clone-b744a09/RUN.txt",
     "B07, B11: 23 runs pass from a fresh clone (Assignment 7 record)"),
    ("evidence/a7-mutations-r1.json", "copy of evidence/assignment-7/mutations/mutations-r1.json",
     "B07, B11: 8 of 8 mutations caught on the kept r1 phase table"),
    ("evidence/a6-COST-REPORT.md", "copy of evidence/assignment-6/cost/COST-REPORT.md (29 October 2026)",
     "B10: GPU time reads 0.000 ms under GL Compatibility on the Apple M4; sparks at the cap add +0.025 ms CPU per "
     "frame against a 1.0 ms budget"),
    ("PROJECT-BRIEF.md", "Bao's seven answers, drafted with Claude from Bao's 23 November answers and the A4 GDD",
     "B02-B12: scope, comparables, role, first piece, risk, exists and will-exist lists"),
]


def main():
    p = REEL / "gdd-evidence.json"
    ledger = json.loads(p.read_text())
    ledger["evidence"] = [{"path": path, "sha256": hashlib.sha256((REEL / path).read_bytes()).hexdigest(),
                           "method": method, "supports": supports} for path, method, supports in EVIDENCE]
    p.write_text(json.dumps(ledger, indent=1, ensure_ascii=False) + "\n")
    print(f"{p.name}: {len(ledger['evidence'])} evidence records")


if __name__ == "__main__":
    main()

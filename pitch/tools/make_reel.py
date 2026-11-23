#!/usr/bin/env python3
"""Write beat_sheet.json and gdd-evidence.json for the Assignment 8 pitch film "Lanternfall: First Delivery".

Made with the godot-gdd skill's structure (GDD excerpts, design status per beat, coverage ledger), adapted to the
assignment's rules: the narration speaks as Bao in the first person (an AI voice, disclosed in B00), and no instructor
name, persona or credit line appears anywhere, so no ClaudeTitleOutro, composer card or GodotDesignBoard is used.
Every picture is drawn by tools/build_media.py (Pillow + ffmpeg) into media/<BID>.mp4.

Excerpts are exact lines of gdd/GDD-v0.3.md, found by their opening words. Run it again after narration is measured:
measured durations are kept and cue times are re-derived from them.

    python3 tools/make_reel.py
"""
import hashlib, json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
GDD = REEL / "gdd" / "GDD-v0.3.md"
SLUG = "lanternfall-first-delivery-pitch"
TITLE = "Lanternfall: First Delivery"
LINES = GDD.read_text().splitlines()


def find(prefix: str, count: int = 1) -> tuple:
    hits = [i for i, l in enumerate(LINES) if l.startswith(prefix)]
    if len(hits) != 1:
        raise SystemExit(f"excerpt prefix must match one line: {prefix!r} ({len(hits)})")
    a = hits[0]
    return a + 1, a + count, "\n".join(LINES[a:a + count])


# beat id -> (opening words of the first line, number of lines)
EXCERPTS = {
    "B01": ("| F-01 |", 3),
    "B02": ("The course version should first polish", 1),
    "B03": ("PX-03 Visible consequence.", 1),
    "B05": ("| Engineer |", 1),
    "B08": ("| R-01 |", 1),
    "B09": ("- Q-01 ", 1),
    "B10": ("| R-03 |", 1),
    "B12": ("Status convention.", 1),
}

# Every top-level (##) section of the GDD: the beats that explain it, or why the pitch leaves it out.
SECTIONS = [
    ("Game Name", ["B00"], ""),
    ("Concept", ["B02", "B03"], ""),
    ("Game Flow", ["B01", "B09"], ""),
    ("Game Elements and Assets", ["B01", "B05"], ""),
    ("Main Characters", ["B05"], ""),
    ("Story", ["B03"], ""),
    ("Gameplay", ["B01", "B09"], ""),
    ("Systems and Progression", ["B03", "B08"], ""),
    ("Graphics and Styling", [], "The art direction has existed since Assignment 2 and the final project adds no new art "
     "direction; the pixel art, palettes and camera are shown only in B01's real capture, not explained."),
    ("Music and Sound Effects", [], "Music and effects have existed since Assignment 2 and the final project adds no "
     "audio work; the film's footage is shown with game sound off, so audio claims would be unshown."),
    ("Technical Description", ["B06", "B10"], ""),
    ("Development Scope", ["B02", "B08"], ""),
    ("Out of Scope", ["B08"], ""),
    ("Risks and Mitigations", ["B08", "B10"], ""),
    ("Open Questions", ["B09"], ""),
    ("Revision History", ["B02"], ""),
]

BEATS = [
    dict(beat_id="B00", act="OPEN", design_status=None,
         role_note="Title. The narration discloses the AI voice and says it speaks for Bao.",
         narration_text="Hola. I'm Bao Xing, and this is an AI voice reading my script. "
                        "This is the pitch for my final project: Lanternfall, First Delivery.",
         estimated_duration_s=10, lead_silence_s=0.6,
         show=[("0.0", "title card: Lanternfall: First Delivery; Bao Xing; AI narration disclosed on screen")]),
    dict(beat_id="B01", act="BODY", design_status="implemented",
         role_note="What exists today: real Movie Maker capture of tag a7 (godot/ 5f09b7f), scripted input, seed 21.",
         narration_text="First, what exists today. This is a real capture of my game at tag A-seven, driven by "
                        "scripted input. I only move. The Beam fires on its own. Enemies break into lamp oil, and a "
                        "full gauge pauses the run for three cards. Max out both weapons and they fuse into Sunflare. "
                        "Survive three minutes, and the fog lifts.",
         estimated_duration_s=26, tail_silence_s=1.5,
         qc={"contrast_regions": [
             {"label": "capture label band", "box": [0.0833, 0.8935, 0.9167, 0.9306]},
             {"label": "segment chip", "box": [0.5859, 0.8218, 0.9036, 0.8611]}],
             "contrast_reason": "real game footage of a dark fog market; the whole-frame average is the game's own "
                                "palette, so contrast is measured on the two text regions the film adds"},
         cues=["I only move", "full gauge", "Max out", "Survive three minutes"],
         show=[("I only move", "run start: courier moving, Beam firing"), ("full gauge", "the card screen"),
               ("Max out", "the Sunflare card, then the burst"), ("Survive three minutes", "3:00, the win panel")]),
    dict(beat_id="B02", act="BODY", design_status="proposed",
         role_note="What it will be, in one sentence; the GDD's next milestone (Development Scope) and its version.",
         narration_text="What I'll build is the next milestone from my game design document, version zero point "
                        "three, from October seventeenth. In one sentence: a playable Mac build where one run becomes "
                        "one delivery. A post office menu, one contract across the market, the Lantern Gate at the "
                        "end, and a second courier, the Engineer, who places turrets.",
         estimated_duration_s=24,
         cues=["post office menu", "one contract", "Lantern Gate", "the Engineer"],
         show=[("0.0", "GDD Development Scope excerpt"), ("post office menu", "four parts of the slice appear in turn")]),
    dict(beat_id="B03", act="BODY", design_status="proposed",
         role_note="Why anyone would care: the run goes somewhere, and the change persists (PX-03; final's saved data).",
         narration_text="Why would anyone care? Because the run goes somewhere. When a delivery succeeds, the "
                        "destination changes, and it's still changed the next time you play, even after a restart. "
                        "My design doc calls this a visible consequence.",
         estimated_duration_s=17,
         cues=["delivery succeeds", "still changed", "visible consequence"],
         show=[("0.0", "constructed diagram: route to an unlit gate"), ("delivery succeeds", "gate lit"),
               ("still changed", "restart, gate still lit")]),
    dict(beat_id="B04", act="BODY", design_status="comparison",
         role_note="Comparable games Bao has played (card answer, 23 November 2026) and the one specific difference.",
         narration_text="I've played Vampire Survivors, Brotato, Twenty Minutes Till Dawn and Halls of Torment. "
                        "In Vampire Survivors, a run's goal is to outlast the clock. In Brotato, it's to outlast "
                        "twenty waves. Lanternfall gives a player who likes short runs a destination, and a place "
                        "that remembers they got there.",
         estimated_duration_s=20,
         cues=["Vampire Survivors, a run", "Brotato, it's", "Lanternfall gives"],
         show=[("0.0", "four games Bao played"), ("Lanternfall gives", "the difference")]),
    dict(beat_id="B05", act="BODY", design_status="proposed",
         role_note="The Engineer: roster rule and trade-off from the GDD; the turret state machine as the planned A9 technique.",
         narration_text="The second courier is the Engineer. My roster rule gives every courier one advantage, one "
                        "rule change and one weakness. The Engineer's turret holds an area, at the cost of lower "
                        "damage and speed. The turret will run on its own state machine: idle, track, fire, cool "
                        "down. That's my plan for the game AI technique in Assignment nine.",
         estimated_duration_s=22,
         cues=["turret holds an area", "state machine", "Assignment nine"],
         show=[("0.0", "GDD roster row: Engineer"), ("turret holds an area", "constructed turret diagram"),
               ("state machine", "four states with transitions")]),
    dict(beat_id="B06", act="BODY", design_status="proposed",
         role_note="Who opens it: target role, reader, the first sixty seconds; the stack and export target.",
         narration_text="Who opens it? I'm aiming at gameplay programmer jobs, so the reader is a hiring manager or "
                        "a lead gameplay engineer. In the first minute, they open the Mac build, land on the post "
                        "office menu with keyboard focus already set, read the keys on that screen, press Enter, "
                        "and they're moving. No manual. Then the lead runs one test command from the readme. It's "
                        "Godot four point seven point two, Compatibility renderer, exported for macOS.",
         estimated_duration_s=27,
         cues=["In the first minute", "press Enter", "one test command", "Godot four"],
         show=[("0.0", "constructed storyboard of the first sixty seconds"), ("one test command", "the README command"),
               ("Godot four", "stack line")]),
    dict(beat_id="B07", act="BODY", design_status="observed",
         role_note="What it proves: course skills with existing evidence (tags a5, a6, a7) and what it cannot prove.",
         narration_text="What does it prove? That I can add new systems to a working game and pin each one with "
                        "tests a stranger can rerun. The course skills already have evidence: hand-written shaders at "
                        "tag A-five, particle effects with a cost report at tag A-six, and animation driven by state "
                        "at tag A-seven, where twenty-three headless runs pass from a fresh clone, and eight of eight "
                        "mutations are caught. What it can't prove is that the game is fun.",
         estimated_duration_s=27,
         cues=["hand-written shaders", "particle effects", "animation driven", "can't prove"],
         show=[("hand-written shaders", "a5 capture"), ("particle effects", "a6 capture"), ("animation driven", "a7 capture"),
               ("can't prove", "the limit")]),
    dict(beat_id="B08", act="BODY", design_status="proposed",
         role_note="In and out, with the GDD's R-01 mitigation as the reason for the cut.",
         narration_text="What's in: the delivery, the post office menu, one contract, the Engineer, one saved "
                        "record, the lit gate, and a Mac export. What's out, on purpose: the other four couriers, a "
                        "difficulty selector, more maps, the fog boss, multiplayer, web and mobile. My own risk table "
                        "says it: one screen, one contract and the Engineer, before anything else.",
         estimated_duration_s=22,
         cues=["What's out", "My own risk table"],
         show=[("0.0", "in list"), ("What's out", "out list"), ("My own risk table", "R-01 highlighted")]),
    dict(beat_id="B09", act="BODY", design_status="comparison",
         role_note="The first playable piece (F-04), Bao's answer to Q-01 for this slice, and how anyone would know it ran.",
         narration_text="First comes the delivery objective, on the route that already exists. My doc left open how "
                        "a delivery ends. For this slice: survive until the fog lifts, then reach the gate. You'll "
                        "know it ran when a headless test with a fixed seed drives a run to delivered, and the result panel "
                        "says so on screen.",
         estimated_duration_s=20,
         cues=["For this slice", "You'll know it ran"],
         show=[("0.0", "today's real win panel (tag a7)"), ("For this slice", "proposed flow"),
               ("You'll know it ran", "the planned test")]),
    dict(beat_id="B10", act="BODY", design_status="comparison",
         role_note="The concrete risk (GDD R-03) against measured A6 cost evidence; the mitigation.",
         narration_text="What could sink it? Turrets. Every turret hit can spawn the sparks I built in Assignment "
                        "six, in the busiest minute of the run. And on my Mac, Godot reports zero milliseconds of GPU "
                        "time under the Compatibility renderer, so I can't read that cost there. So I'll cap the "
                        "turrets, reuse their shots, measure CPU frame time at the peak wave the way my Assignment "
                        "six cost test did, use the Vulkan proxy for the GPU, and cut turret sparks first.",
         estimated_duration_s=29,
         cues=["zero milliseconds", "So I'll cap"],
         show=[("0.0", "GDD R-03"), ("zero milliseconds", "A6 cost report readings"), ("So I'll cap", "mitigation steps")]),
    dict(beat_id="B11", act="BODY", design_status="comparison",
         role_note="Why this project: Bao's answers (23 November 2026) on new versus existing skills, with evidence.",
         narration_text="Why this project? Both reasons: learning, and showing what I have. New to me in this course: "
                        "Godot and GDScript, shaders and materials, and particles. Animation, state machines and "
                        "testing, I already had, and tag A-seven is my evidence. The delivery, the save and the "
                        "turret will be new code in this game.",
         estimated_duration_s=20,
         cues=["New to me", "I already had", "new code"],
         show=[("New to me", "new column"), ("I already had", "already-had column with a7"), ("new code", "new code row")]),
    dict(beat_id="B12", act="BODY", design_status="comparison",
         role_note="Exists versus will exist, by the GDD's own status convention.",
         narration_text="To be exact about what's real: everything on the left exists, with a tag you can check out. "
                        "Nothing on the right exists yet, and there's no export yet either. The finished slice is due "
                        "on December twentieth, tagged A-ten.",
         estimated_duration_s=16,
         cues=["Nothing on the right", "December twentieth"],
         show=[("0.0", "exists today, with tags"), ("Nothing on the right", "will exist")]),
    dict(beat_id="B13", act="OUTRO", design_status=None,
         role_note="Closing title card (not the instructor's outro).",
         narration_text="Lanternfall, First Delivery. A pitch by Bao Xing.",
         estimated_duration_s=6, tail_silence_s=1.0,
         show=[("0.0", "title, repository, tag a8")]),
]


WORDS_P = REEL / "word-times.json"
WORDS = json.loads(WORDS_P.read_text()) if WORDS_P.exists() else {}


def norm(w: str) -> str:
    return "".join(c for c in w.lower() if c.isalnum())


def at(text: str, phrase: str, dur: float, bid: str = "", lead: float = 0.15) -> float:
    """Cue time of a phrase: the measured start of its first recognised word (word-times.json, from
    tools/word_times.py), nearest to the character-share estimate; the estimate itself if no word matches."""
    i = text.find(phrase)
    if i < 0:
        raise SystemExit(f"cue phrase not in narration: {phrase!r}")
    est = dur * i / max(1, len(text))
    words = WORDS.get(bid, [])
    for j, pw in enumerate(phrase.split()[:3]):
        hits = [w["start"] for w in words if norm(w["w"]) == norm(pw)]
        if hits:
            t = min(hits, key=lambda h: abs(h - est)) - 0.3 * j
            if abs(t - est) < 4.0:
                return round(max(0.0, t - lead), 2)
    return round(max(0.0, est - lead), 2)


def main() -> None:
    path = REEL / "beat_sheet.json"
    old = {b["beat_id"]: b for b in json.loads(path.read_text())["beats"]} if path.exists() else {}
    beats, excerpts = [], []
    for spec in BEATS:
        b = {k: v for k, v in spec.items() if k not in ("show", "cues", "design_status")}  # qc passes through
        if spec["design_status"]:
            b["design_status"] = spec["design_status"]
        prev = old.get(b["beat_id"], {})
        for k in ("actual_duration_s", "audio_file", "audio_levelled", "audio_note"):
            if k in prev and prev.get("narration_text") == b["narration_text"]:
                b[k] = prev[k]
        dur = float(b.get("actual_duration_s") or b["estimated_duration_s"])
        shot = {"type": "VIDEO" if b["beat_id"] == "B01" else "GRAPHIC", "class": "SHOW",
                "source": "own", "motion": "real-footage" if b["beat_id"] == "B01" else "board-reveals",
                "show": [{"at": a, "event": e} for a, e in spec["show"]],
                "media": f"media/{b['beat_id']}.mp4", "built_by": "tools/build_media.py"}
        if spec.get("cues"):
            shot["cues"] = [{"phrase": p, "at": at(b["narration_text"], p, dur, b["beat_id"])} for p in spec["cues"]]
        if b["beat_id"] in EXCERPTS:
            s, e, text = find(*EXCERPTS[b["beat_id"]])
            # The godot-gdd checker reads displayed excerpts from shot.remotion.props; no Remotion pattern renders it.
            shot["remotion"] = {"pattern": "", "note": "no Remotion render; the board is drawn by tools/build_media.py",
                                "props": {"excerpt": text, "source_lines": [s, e]}}
            excerpts.append({"beat_id": b["beat_id"], "start_line": s, "end_line": e, "text": text})
        b["shot"] = shot
        b.setdefault("voice", "am_onyx")
        b.setdefault("engine", "kokoro")
        beats.append(b)
    sheet = {"metadata": {
        "title": TITLE, "slug": SLUG, "topic": "FINAL PROJECT PITCH", "kind": "godot-gdd", "modifier": "",
        "assignment": "CSYE 7270 Assignment 8 — Final Project Pitch Film", "author": "Bao Xing",
        "playlist": "CSYE 7270", "audience": "CSYE 7270 instructor and TAs; a hiring manager or lead gameplay engineer",
        "engine": "kokoro", "voice": "am_onyx", "voice_kokoro": "am_onyx",
        "persona": "Bao Xing (AI voice reading Bao's script; disclosed in B00)",
        "presenter": "Bao Xing", "in_for_bear": False,
        "persona_note": "Assignment 8: AI narration speaks as the student; no instructor name, persona or credit line.",
        "palette": "claude", "style_preset": "claude", "ground": "#FAF9F5", "aspect_ratio": "16:9", "fit": "contain",
        "captions": False, "channel": "", "channel_title": "",
        "game": {"repo": "https://github.com/yanxlh/walker-lanternfall-bao-x", "project_dir": "godot",
                 "source_tag": "a7", "source_revision": "5f09b7fa0f8555f588d68c9d63a1166d3daa23a1",
                 "godot": "4.7.2.stable.official.ed1daf0bf"},
        "gdd": {"path": "gdd/GDD-v0.3.md", "converted_from": "gdd/Lanternfall_Game_Design_Document.docx",
                "version": "0.3", "date": "2026-10-17"},
        "note": ("Pitch film for Bao Xing's CSYE 7270 final project, built with the godot-gdd skill's structure. "
                 "Gameplay is a real Movie Maker capture of an isolated copy of tag a7 with scripted input "
                 "(capture/pitch_driver.gd); every diagram of a feature that does not exist yet is labelled "
                 "constructed; GDD excerpts are exact lines of gdd/GDD-v0.3.md. Free local pipeline: Kokoro, "
                 "Pillow, ffmpeg. No paid call, no upload."),
        "links": {"repo": "https://github.com/yanxlh/walker-lanternfall-bao-x"},
        "tags": ["Godot 4", "godot-gdd", "pitch", "CSYE 7270", "Kokoro"]},
        "beats": beats}
    path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")

    sha = hashlib.sha256(GDD.read_bytes()).hexdigest()
    ledger_p = REEL / "gdd-evidence.json"
    evidence = json.loads(ledger_p.read_text()).get("evidence", []) if ledger_p.exists() else []
    ledger = {"schema_version": 1,
              "document": {"path": "gdd/GDD-v0.3.md", "sha256": sha, "version": "0.3", "date": "2026-10-17",
                           "converted_from_sha256": hashlib.sha256(
                               (REEL / "gdd" / "Lanternfall_Game_Design_Document.docx").read_bytes()).hexdigest()},
              "sections": [{"heading": h, **({"beat_ids": ids} if ids else {"exclusion": why})} for h, ids, why in SECTIONS],
              "excerpts": excerpts, "evidence": evidence}
    ledger_p.write_text(json.dumps(ledger, indent=1, ensure_ascii=False) + "\n")
    words = sum(len(b["narration_text"].split()) for b in beats)
    est = sum(float(b.get("actual_duration_s") or b["estimated_duration_s"]) for b in beats)
    print(f"{path.name}: {len(beats)} beats, {words} words, ~{est:.0f}s; {len(excerpts)} excerpts")


if __name__ == "__main__":
    main()

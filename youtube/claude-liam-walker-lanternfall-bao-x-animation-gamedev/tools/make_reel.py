#!/usr/bin/env python3
"""Write beat_sheet.json for the Lanternfall animation godot-gamedev (walker) film (Assignment 7).

Code excerpts are read from git at the film's source revision (tools/src.py), never from the working tree. Repository
records (Bao's brief, TUNING, TEST-REPORT) are read at RECORDS_REV. Run it again after narration is measured: measured
durations are kept and every Remotion beat's durationSeconds and highlight times are re-derived from them.

    python3 tools/make_reel.py
"""
import json, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from src import SHA as FILM_SHA, excerpt, repo_text  # noqa: E402

REEL = Path(__file__).resolve().parents[1]
SHORT = FILM_SHA[:7]
RECORDS_REV = "32bcec6"
SLUG = "claude-liam-walker-lanternfall-bao-x-animation-gamedev"
TITLE = "Lanternfall in Frames"
PROJECT = "walker-lanternfall-bao-x"
HANDLE = "@NikBearBrown"
TOPIC = "WALKER · GODOT ANIMATION"


def at(text: str, phrase: str, dur: float, lead: float = 0.25) -> float:
    i = text.find(phrase)
    if i < 0:
        raise SystemExit(f"cue phrase not in narration: {phrase!r}")
    return round(max(0.0, dur * i / max(1, len(text)) - lead), 2)


def code_beat(bid, act, path, a, b, title, narration, cues, notes, output, est, font=None):
    return {"beat_id": bid, "act": act, "kind": "code",
            "role_note": f"Code beat (code-then-result-v1): godot/{path} lines {a}-{b} at {SHORT}, read verbatim; the next beat shows the result.",
            "narration_text": narration, "estimated_duration_s": est, "_cues": cues,
            "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "line-highlight",
                     "show": [{"at": "0.0", "event": f"Godot editor reconstruction opens on {path}, lines {a}-{b}"}] +
                             [{"at": c[0], "event": f"line {c[1]} highlights — {c[2]}"} for c in cues] +
                             [{"at": "notes", "event": "source-notes panel (not Inspector values) lists related lines"}],
                     "remotion": {"pattern": "GodotDevWorkbench", "props": {
                         "mode": "code", "title": title, "project": PROJECT, "path": f"res://{path}",
                         "source": f"godot/{path} · lines {a}–{b} · source revision {SHORT} · Godot editor reconstruction",
                         "code": excerpt(path, a, b), "startLine": a, "codeFontSize": font or 25,
                         "inspectorLabel": "Source notes — not Inspector values",
                         "notes": [{"label": k, "value": v} for k, v in notes], "output": output,
                         "cues": [], "durationSeconds": est}}},
            "_excerpt": {"path": path, "start_line": a, "end_line": b}}


OBSERVED = {
    "B05": "The 320 x 32 sheet is cut into ten 32-pixel cells; the walk uses cells 2 and 3. In Bao's 30 fps walk strip (captures/walk/r1, recorded by Bao) frames 1-3 are the cast pose logged as pose=cast, then cell 3 holds four frames and cell 2 four frames; Bao: 'Looked at it; no drift.'",
    "B07": "In the take, during the walk the logged cell alternates 2 and 3 every four movie frames (eight ticks) under the courier; the read-back's seam numbers (last key 3, 8 frames to the end, interval 8) are shown beside it.",
    "B09": "The phase table's boundaries 0, 4, 14 and 20 sit beside key times 0, 4/60, 14/60 and 20/60 s; Bao's 30 fps dash strip r1 shows the trigger frame (dash frame 0), active begins (4), recovery begins (14) and the walk sprite again after the dash, each matching frames.log.",
    "B11": "In the take, the level-up shows the Courier's Dash card first (fixture), the parsed key 1 picks it, and the first dash runs startup, active and recovery from the log with the rig replacing the sprite; the edge tests' measured clip-versus-tick difference (0 s at 30, 60 and 144 fps) is shown beside it.",
    "B13": "In the take, three dashes are each hit once by a placed wraith: on startup frame 2 the dash is cancelled with no cooldown (hp 10 to 8); on active frame 8 it continues (hp 8 to 6) and the cooldown starts when it ends; on recovery frame 16 it is cancelled and the 60-tick cooldown starts (hp 6 to 4).",
    "B15": "Recorded output: courier_clips 86/0 with the assertion groups named; the four required mutations (subname rotation->rotaton fails 5 checks including every-track-resolves; loop_mode 0 fails 1; a key on cell 10 fails 3; an empty-cache reimport passes); and the Godot 4.7.2 probe in which loop = true loads as LOOP_LINEAR.",
    "B17": "Bao's dash strips r1 and r2 (same position, logs identical tick for tick): the r2 frames 5, 7 and 12 show the outline on the coat and legs; Claude's reading (the back-of-coat outline sits outside the sheet's dark ink) and Bao's verdict 'Keep. It is clearer.' are shown side by side.",
}


def media_beat(bid, act, narration, show, est, role, evidence=False):
    b = {"beat_id": bid, "act": act, "kind": "result" if evidence else "evidence",
         "role_note": role, "narration_text": narration, "estimated_duration_s": est,
         "shot": {"type": "VIDEO", "class": "SHOW", "source": "own", "motion": "real-footage",
                  "show": [{"at": s[0], "event": s[1]} for s in show], "treatment": "none"}}
    if evidence:
        b["shot"]["evidence_media"] = f"media/{bid}.mp4"
        b["observation"] = OBSERVED[bid]
    return b


def board(bid, act, title, section, excerpt_text, source, status, label, cards, cue_phrases, narration, est, role):
    return {"beat_id": bid, "act": act, "role_note": role, "narration_text": narration, "estimated_duration_s": est,
            "_cards": [(p, i) for i, p in enumerate(cue_phrases)],
            "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "card-cues",
                     "show": [{"at": "0.0", "event": f"{section} excerpt beside {len(cards)} cards"}] +
                             [{"at": p, "event": f"card {i + 1} highlights"} for i, p in enumerate(cue_phrases)],
                     "remotion": {"pattern": "GodotDesignBoard", "props": {
                         "title": title, "section": section, "excerpt": excerpt_text, "source": source,
                         "status": status, "visualLabel": label, "layout": "cards",
                         "cards": [{"label": k, "text": v} for k, v in cards], "cues": [], "durationSeconds": est}}}}


def brief_lines(a, b):
    return "\n".join(repo_text("CHANGE-BRIEF.md", RECORDS_REV).splitlines()[a - 1:b])


ASK = ("Please use Walker to convert my game design document about Lanternfall, a lamp-headed courier surviving three "
       "minutes in a fog-bound night market, into two Godot 4 animations: a two-frame walk cycle sliced from my own "
       "sprite sheet, and a cutout-rig dash unlocked by a level-up card, with startup, active and recovery frames. "
       "Pin what the courier shows today before you change anything, and give every clip a read-back test.")

YOUR_TURN = ("Please use Walker to read the dash in godot/animations/courier_clips.tres in my Lanternfall project. "
             "In my phase table, change only the recovery from 6 frames to 9 and let it flow down: the builder's keys, "
             "the read-back's expected times, and a re-pin of the edge tests in its own commit. Before running "
             "anything, predict which strip frames change and what the courier shows on dash frame 16. Then record "
             "strip r3 and compare it with your prediction.")

BRIEF_OPEN = brief_lines(175, 175).split(". ")[0] + "."
BRIEF_RULES = ". ".join(brief_lines(194, 194).split(". ")[:3]) + "."
BRIEF_CLOCKS = brief_lines(232, 232).strip().split(". ")[0] + "."

BEATS = [
    {"beat_id": "B00", "act": "ASK",
     "role_note": "COLD OPEN LAW — Claude composer; reconstructed Walker prompt from Bao's CHANGE-BRIEF.md (not a recorded session). Liam introduces himself.",
     "narration_text": ("Hola, this is Liam, in for Bear. Bao Xing's animation assignment for Lanternfall: two clips, one "
                        "made from a sprite sheet and one that moves a rig. One loops, one commits. One authority "
                        "drives them both. And four ideas to explain, each at a line of Bao's own clip, test or brief. "
                        "Here's the ask, rebuilt from Bao's change brief."),
     "estimated_duration_s": 20,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on",
              "show": [{"at": "0.02", "event": "composer card on cream; greeting 'Hola, Liam'"},
                       {"at": "0.25", "event": "the reconstructed Walker prompt types in"},
                       {"at": "0.62", "event": "send arms; running line names the brief and the player script"},
                       {"at": "0.75", "event": "three result lines: the walk, the dash, checks and revision"}],
              "remotion": {"pattern": "ClaudeComposerAsk", "props": {
                  "greeting": "Hola, Liam", "topic": TOPIC, "segment": "Lanternfall",
                  "command": ASK,
                  "runningText": "reading CHANGE-BRIEF.md · CLAUDE.md · godot/features/player/player.gd…",
                  "folderLabel": HANDLE, "modelLabel": "Claude", "effortLabel": "High",
                  "output": ["walk: Sprite2D + AnimationPlayer frame track, cells 2 and 3, 8 ticks each",
                             "dash: cutout rig, startup 4 · active 10 · recovery 6 frames at 60 per second",
                             f"pin 23 · read-back 86 · edges 51 at 30/60/144 fps · source revision {SHORT}"]}}}},
    {"beat_id": "B01", "act": "BLUF",
     "role_note": "EXECUTIVE-SUMMARY LAW — hesitant writer. The framing a viewer arrives with ('an animation is a movie') is corrected to what the film shows ('a list of keys').",
     "narration_text": ("The short version. An animation isn't a movie, it's a list of keys. Here, a few tracks of "
                        "numbers, one driver and a phase table written in frames decide what you see. And whether the "
                        "motion reads is something only Bao, playing the game, could judge."),
     "estimated_duration_s": 15, "lead_silence_s": 0.8,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on-correct",
              "show": [{"at": "0.0", "event": "cream page; 'An animation is a movie' types"},
                       {"at": "0.3", "event": "'movie' typed in terracotta, deleted, 'list of keys' typed in its place"},
                       {"at": "0.6", "event": "'tracks, a driver, a table' and 'judged in play' type in"}],
              "remotion": {"pattern": "BrutalistHesitantWriter", "props": {
                  "text": "An animation is a movie\ntracks, a driver, a table\njudged in play",
                  "triggerWords": "movie", "replacementWords": "list of keys", "fontSize": 145, "lineSpacing": 1.9,
                  "align": "center", "seed": str(sum(map(ord, SLUG))), "mistakeRate": 2, "hesitateWithin": 0,
                  "hesitateBetween": 1, "ink": "#3D3929", "accent": "#D97757", "bg": "#FAF9F5"}}}},
    board("B02", "ASSIGNMENT", "What the assignment asks", "CHANGE-BRIEF.md · Bao's brief", BRIEF_OPEN,
          f"CHANGE-BRIEF.md line 175, first sentence, verbatim, at {RECORDS_REV} · the assignment's parts as the brief answers them",
          "Bao's brief, 18 November 2026: the current contract",
          "The assignment, and where this game answers it",
          [("1 · A sprite clip that loops", "walk: cells 2 and 3 of Bao's own Assignment 2 sheet, on an AnimationPlayer frame track"),
           ("2 · A rig clip that commits", "dash: head, arm, coat and legs cut from cell 2, under hips, chest and neck pivots"),
           ("3 · One authority", "player.gd is the only code that plays or seeks the courier's AnimationPlayer"),
           ("4 · Four ideas, and their tests", "a clip · one authority · two clocks · feel in frames; pins, read-backs, edges, mutations")],
          ["One clip from a sprite sheet", "One clip that moves a rig", "One authority", "four ideas"],
          ("What the assignment asks, and how Bao answered it. One clip from a sprite sheet: the courier's walk, two cells "
           "of Bao's own sheet from Assignment 2. One clip that moves a rig: a dash, cut from one of those cells into "
           "head, arm, coat and legs. The walk loops; the dash commits, with startup, active and recovery. One authority "
           "drives both. And four ideas Bao has to explain: what a clip is, one authority, two clocks, and feel "
           "designed in frames."),
          24, "Assignment requirements as Bao's brief answers them; the excerpt is the first sentence of Bao's rewrite, verbatim."),
    board("B03", "PREDICT", "Designed in frames, before the clip", "CHANGE-BRIEF.md · Bao's dash rules", BRIEF_RULES,
          f"CHANGE-BRIEF.md line 194, first three sentences, verbatim, at {RECORDS_REV} · cards: Bao's phase table, lines 187–192",
          "Bao's table: what the keys are built from", "Bao's brief: rules and predictions",
          [("Startup, 4 frames", "dip and lean back, direction locked; a hit cancels with no cooldown"),
           ("Active, 10 frames", "55 pixels at 330 pixels per second; a hit lands and the dash carries on"),
           ("Recovery, 6 frames", "upright again, still locked; a hit cancels and the cooldown starts"),
           ("Predicted failures", "body blending into dark ground · coat-leg gaps · loop hesitation · cast frames read as loop errors")],
          ["Startup, four frames", "Active, ten frames", "Recovery, six frames", "predicted failures"],
          ("Bao's brief, rewritten in Bao's own words, sets the dash down in frames at sixty a second. "
           "Startup, four frames: the courier dips and leans back, direction locked. Active, ten frames: fifty-five "
           "pixels at three hundred thirty a second. Recovery, six frames, still locked. Then a one-second cooldown. "
           "It's not invincible: each phase has its own rule for a hit. And the predicted failures, each with the "
           "check that would catch it: the body blending into dark ground, a gap between coat and legs, a hesitation "
           "at the loop, and cast frames mistaken for loop errors."),
          30, "Bao's dash rules, verbatim (brief line 194); the cards restate Bao's phase table (lines 187-192) and predicted failures from the same brief."),
    code_beat("B04", "CODE", "features/player/courier_visual.tscn", 9, 15, "The sheet, sliced by a number.",
              ("Here's the slicing, in the scene file. Body is a Sprite two D, and this line points it at Bao's sheet. "
               "Centered false, with that offset, puts the cell's pixel sixteen, twenty-three on the courier's origin, "
               "the centre of the courier's hurtbox. Then hframes ten cuts the sheet into ten frames across. Which picture frame "
               "three is, is decided by that number, not by the image."),
              [("this line points it", 11, "texture = Bao's pc_sheet.png"),
               ("with that offset", 13, "offset (-16, -23): cell pixel (16, 23) on the origin"),
               ("hframes ten", 14, "hframes = 10, vframes left at 1")],
              [("Sheet", "320 x 32 · 32 px cells · 10 x 1"),
               ("Walk cells", "2 walk_contact · 3 walk_passing"),
               ("Credits", "ATTRIBUTION.md · Apache-2.0")],
              ["Built by godot/features/player/build_courier_visual.gd and saved with ResourceSaver"], 22, font=30),
    media_beat("B05", "RESULT",
               ("Here's the sheet, cut the way hframes says: ten cells, thirty-two pixels each. The walk uses cells two and "
                "three. In Bao's own strip at thirty frames a second, the first three frames are the cast pose, the "
                "auto-attack firing, and the log says pose equals cast: not a broken loop. Then cell three for four frames, "
                "cell two for four. Bao checked the strip for drift: none."),
               [("0.0", "pc_sheet.png, 8x, with the 10 x 1 grid and cell numbers"),
                ("Bao's own strip", "captures/walk/r1, Bao's 30 fps fixture strip, frames labelled with cell and pose from frames.log"),
                ("for drift", "Bao's verdict on the strip, quoted")], 22,
               "Result of B04. The committed sheet and Bao's committed walk strip (fixture capture, recorded by Bao).",
               evidence=True),
    code_beat("B06", "CODE", "animations/courier_clips.tres", 415, 425, "A clip is a list of keys.",
              ("A clip is a list of keys, not a movie. This is the walk's frame track, in the clip resource. The path "
               "line names a node and a property: Body, frame. The times are zero and eight sixtieths of a second; the "
               "values, cells two and three. Update one means discrete: hold each value until the next key. And if the "
               "path named a property that didn't exist? Nothing would complain. The track would just do nothing."),
              [("The path line", 418, "NodePath(\"Body:frame\")"),
               ("The times", 422, "keys at 0 and 8/60 s"),
               ("Update one", 424, "update 1 = UPDATE_DISCRETE"),
               ("the values", 425, "cells 2 and 3")],
              [("Lines 388–390", "16/60 s · LOOP_LINEAR · step 1/60"),
               ("Line 419", "interp 0: nearest"),
               ("Seam", "tail 8 = interval 8")],
              ["Saved by the builder; the game loads the file, never builds a clip at runtime"], 26, font=30),
    media_beat("B07", "RESULT",
               ("In the running game, from a scripted take: the walk under the courier, with the clip's cell beside it, "
                "read from the take's own per-frame log. Two, then three, every four movie frames, which is eight ticks. "
                "The seam rule for a frame track: no duplicate across the wrap, and the gap from the last key to the end "
                "equals the key interval. Eight and eight. Bao watched it wrap at normal speed: no stutter."),
               [("0.0", "take, 4K, walking: courier and the live cell readout from the take's log"),
                ("The seam rule", "read-back numbers: last key 3, interval 8, tail 8 (test_courier_clips walk-seam)"),
                ("Bao watched", "Bao's human check, quoted")], 22,
               "Result of B06. The film's take (scripted input, fixtures labelled) and recorded read-back output.",
               evidence=True),
    code_beat("B08", "CODE", "features/player/build_courier_visual.gd", 45, 53, "Feel is designed in frames.",
              ("Feel is designed in frames. The builder carries Bao's phase table: four, ten, six, at sixty a second. "
               "Every track has a key at each phase boundary: zero, four, fourteen and twenty. The spacing follows the "
               "phase: transition two through startup, an ease-in that accelerates into the push; one, linear, while "
               "active; point five through recovery, settling. When play says the timing is wrong, the table changes, "
               "and the keys follow."),
              [("four, ten, six", 46, "DASH_STARTUP 4 · ACTIVE 10 · RECOVERY 6"),
               ("Every track has a key", 50, "Rig:position keys at 0, 3, 4, 14, 16, 20"),
               ("zero, four, fourteen", 51, "Hips keys on the same boundaries")],
              [("Lines 58–60", "transitions 2.0 · 1.0 · 0.5"),
               ("r0 → r1", "6/10/12 → 4/10/6, kept by Bao"),
               ("Key times", "frame f at f/60 s · step 1/60")],
              ["The game loads godot/animations/courier_clips.tres; this script never runs in the game"], 26, font=22),
    media_beat("B09", "RESULT",
               ("Here's the table beside the keys built from it: frame four is four sixtieths of a second, fourteen is "
                "fourteen sixtieths, twenty is a third. And Bao's strip at thirty frames a second, read at each boundary "
                "against the log: the trigger frame, upright; active begins, leaning in; recovery begins, settling; then "
                "back on the walk sprite. The table started at six, ten, twelve. A Codex reading pointed out that recovery "
                "stood still longer than the dash moved, and Bao asked for four, ten, six, and kept it."),
               [("0.0", "phase table rows beside key times in seconds"),
                ("Bao's strip", "captures/dash/r1, Bao's fixture strip: frames 5, 7, 12, 15 with tick and dash frame from frames.log"),
                ("six, ten, twelve", "the r0 → r1 revision, from CHANGE-BRIEF Revisions and TUNING")], 30,
               "Result of B08. The committed brief and Bao's committed dash strip r1 (fixture capture, recorded by Bao).",
               evidence=True),
    code_beat("B10", "CODE", "features/player/player.gd", 209, 218, "One authority, one clock.",
              ("One authority. This function is the only code that plays or seeks the courier's Animation Player. It asks "
               "the state machine for a clip and a time, both from integer tick counters: the walk ticks, or the dash "
               "ticks over sixty. Then play, and seek. The player is in manual mode, so it never advances on a clock of "
               "its own. The clip moves only when the sixty-hertz simulation ticks, which is the same tick gameplay "
               "reads the dash on."),
              [("asks the state machine", 216, "clip_and_time(): clip and time from tick counters"),
               ("Then play, and seek", 217, "anim.play(clip); anim.seek(time, true)"),
               ("manual mode", 209, "manual mode: moves only when the simulation ticks")],
              [("Lines 198–207", "time = tick count / 60"),
               ("courier_visual.tscn:66", "callback_mode_process = 2 (manual)"),
               ("Two writers?", "the last to run in the frame wins")],
              ["test_courier_states.gd: one-authority-in-source, one-animation-driver"], 26, font=24),
    media_beat("B11", "RESULT",
               ("The real game, through the real input map, from the scripted take. A level-up offers the Courier's Dash "
                "card. The fixture puts it first, and a real one key picks it. The courier walks, then dashes: startup, "
                "active, recovery, read live from the take's log, and the rig replaces the sprite. Measured by the edge "
                "tests on every rendered frame: zero seconds between the clip's time and the gameplay tick, at thirty, "
                "sixty and a hundred forty-four frames per second."),
               [("0.0", "take: level-up screen, the Courier's Dash card first (fixture), key 1"),
                ("then dashes", "take: the first dash, with state, phase and dash frame from the take's log"),
                ("Measured by the edge tests", "recorded output: two-clocks-at-30/60/144fps")], 28,
               "Result of B10. The film's take and recorded test output.",
               evidence=True),
    code_beat("B12", "CODE", "features/player/player.gd", 233, 240, "Not invincible.",
              ("Not invincible. A hit lands in every phase. Then the match on the dash phase applies Bao's rules: in "
               "startup, the dash is cancelled and no cooldown starts, because no dash happened. In recovery, the rest is "
               "cut, and the cooldown starts. An active dash carries on, damage and all."),
              [("A hit lands", 233, "the hit lands in every phase"),
               ("in startup", 236, "startup: cancel, no cooldown"),
               ("In recovery", 239, "recovery: end the dash, cooldown starts")],
              [("Lines 226–232", "i-frames gate the hit; hp, knockback"),
               ("Lines 133–149", "phases advance from dash_ticks"),
               ("Edges", "hit before / on / after each boundary")],
              ["The interrupt rules are Bao's (CHANGE-BRIEF, design decisions and Bao's brief)"], 20, font=26),
    media_beat("B13", "RESULT",
               ("In play, three more dashes, each hit once. A wraith is placed on the courier for one step, a disclosed "
                "fixture. Hit on startup frame two: the dash is gone, the hurt pose shows, no cooldown. Hit on active frame "
                "eight: damage, and the dash keeps going. Hit on recovery frame sixteen: cancelled, and the sixty-tick cooldown "
                "starts. The edge tests check every boundary a frame before, on, and a frame after, at three frame rates."),
               [("0.0", "take: dash with a hit on startup frame 2 (placed wraith, fixture)"),
                ("active frame", "take: hit on active frame 8, the dash continues"),
                ("recovery frame", "take: hit on recovery frame 16, cancelled, cooldown 60"),
                ("The edge tests", "recorded output: hit-before/on/after at boundaries 4, 14, 20")], 28,
               "Result of B12. The film's take (placed wraith disclosed) and recorded edge-test output.",
               evidence=True),
    code_beat("B14", "CODE", "tests/test_courier_clips.gd", 56, 66, "Every track resolves, or the test says so.",
              ("The read-back. This check walks every track of every clip and resolves it: first the node, then the "
               "property, or a bone for a 3D transform track, or a blend shape. The last branch is the one that matters "
               "here: a property name that isn't on the node gets reported, instead of failing in silence. It proves a "
               "track points at something real, not that it points at the right thing."),
              [("a bone", 57, "3D transform tracks name a bone, not a property"),
               ("a blend shape", 61, "blend-shape tracks name a shape on the mesh"),
               ("The last branch", 64, "property tracks: sub in node")],
              [("Lines 40–55", "each track: the node, then the subname"),
               ("Also checked", "keys · step · loop · discrete · cells < 10"),
               ("Run", "run-test.sh test_courier_clips.gd 60")],
              ["The assignment's track_problems, unchanged apart from indentation"], 24, font=22),
    media_beat("B15", "RESULT",
               ("Recorded output: eighty-six of eighty-six read-back checks. Then the assignment's four mutations, each in "
                "its own git worktree. Rename the rotation property, and track problems reports it. Switch the walk's loop "
                "off, and the loop check fails. Key cell ten on a ten-cell sheet, and three checks fail. Reimport from an "
                "empty cache, and everything still passes, because a cutout rig has no importer setting to lose. One "
                "surprise: in Godot four point seven, a Godot three style loop equals true still loops; only the name scan "
                "catches it. What no headless run can show is whether the motion reads."),
               [("0.0", "recorded: courier_clips 86/0, assertion groups"),
                ("four mutations", "recorded mutations-required.json: 5, 1, 3 failures; empty cache passes"),
                ("One surprise", "recorded probe: loop = true loads as LOOP_LINEAR in 4.7.2"),
                ("What no headless run", "what a headless run cannot show")], 32,
               "Result of B14. Recorded tool output: evidence/courier_clips.json, evidence/assignment-7/mutations/mutations-required.json, evidence/assignment-7/godot3-names/probe.json.",
               evidence=True),
    code_beat("B16", "CODE", "features/player/build_courier_visual.gd", 208, 218, "Revision two, from Bao's eyes.",
              ("Revision two came from Bao's own eyes. On the dark slate, the coat and legs disappeared; only the lamp "
               "read. Bao predicted a thin, low-brightness outline would separate the body. This function finds the outer "
               "ring of the cell's silhouette: transparent pixels touching an opaque one. Then it keeps only the ring "
               "pixels next to the coat and the legs, and the builder draws them behind each part."),
              [("outer ring", 208, "every pixel of the cell, and one beyond each edge"),
               ("transparent pixels touching", 210, "skip opaque pixels; test the four neighbours"),
               ("next to the coat and the legs", 216, "neighbour inside the part's region")],
              [("Lines 54–56", "Coat, Legs · #4A5A80"),
               ("Bao's prediction", "TUNING.md, before any strip"),
               ("Read-back", "coat 20 px · legs 18 px · none on head")],
              ["Approved by Bao: \"Approve.\" Walk sprite, keys and timing unchanged"], 24, font=24),
    media_beat("B17", "RESULT",
               ("Bao's two strips, same position, same ticks: r one above, r two below. The logs match tick for tick; the "
                "outline appears on frames five, seven and twelve. Claude's reading: on the back of the coat, the sheet's "
                "dark ink sits between the outline and the visible coat, so the edge can look detached. Bao judged it in "
                "the running game: keep it, it's clearer. That's the disagreement, recorded, and the verdict is Bao's."),
               [("0.0", "Bao's strips r1 (top) and r2 (bottom), frames 4, 5, 7, 12, 15"),
                ("Claude's reading", "TUNING.md: Claude's comparison, a claim"),
                ("Bao judged it", "TUNING.md: Bao's verdict, quoted")], 26,
               "Result of B16. Bao's committed strips r1 and r2 (fixture captures, recorded by Bao) and TUNING.md.",
               evidence=True),
    board("B18", "ANSWERS", "Four ideas, each at a line", "CHANGE-BRIEF.md · Bao's answer 5", BRIEF_CLOCKS,
          f"CHANGE-BRIEF.md line 232, first sentence of Bao's answer 5, verbatim, at {RECORDS_REV}",
          "Each answer points at a line of Bao's own clip, test or brief", "The four ideas, answered",
          [("A clip", "keys on a node and a property: courier_clips.tres:418 · a missing property fails silently (test_courier_clips.gd:64)"),
           ("One authority", "only player.gd:217–218 plays and seeks; a second writer would win by node order"),
           ("Two clocks", "manual mode, seeked on the 60 Hz tick (courier_visual.tscn:66); measured 0 s apart"),
           ("Feel in frames", "Bao's table 4 / 10 / 6 → keys at 0, 4, 14, 20 (build_courier_visual.gd:46–52)")],
          ["What a clip is", "one authority", "two clocks", "feel in frames"],
          ("So, the four ideas, each at a line. What a clip is: keys on a node and a property, and a missing property "
           "fails silently unless the read-back resolves it. What one authority means: only the show function plays and "
           "seeks; a second writer would win by node order, not by design. What the two clocks are: the clip is seeked on "
           "the same sixty-hertz tick gameplay reads, measured zero seconds apart. And what feel in frames means: Bao's "
           "table, four, ten, six, became keys at zero, four, fourteen and twenty."),
          28, "Recap of the four ideas; the excerpt is the first sentence of Bao's answer 5 in the brief, verbatim."),
    media_beat("B19", "LIMITS",
               ("What the agent got wrong, as the test report lists it: a pin that read the hit sixty ticks late, an edge "
                "test that read the phase after the hit, a structure test that compared the clip with the wrong moment, a "
                "re-pin that missed a hard-coded five, and a header edit lost in a chained command. Still "
                "uncertain: no reference dash was measured, the four, ten, six timing came from a reading rather than from "
                "play, and the real-input pin was added after the change. The next step: measure a reference dash, and "
                "retime from it."),
               [("0.0", "TEST-REPORT.md 'Agent mistakes caught while building'"),
                ("Still uncertain", "TEST-REPORT.md departures and README Known limitations"),
                ("next step", "one next step")], 30,
               "Agent mistakes from TEST-REPORT.md, shortened; open items from TEST-REPORT.md and README.md Known limitations."),
    media_beat("B20", "ROLES",
               ("Who did what. Bao chose the dash and its rules, wrote the brief and the seven answers, saw the body "
                "vanish on dark ground and predicted the fix, approved it, recorded every thirty-frame strip, and gave "
                "every verdict. Claude Code wrote the builder, the clips, the state machine, the dash, the tests and "
                "this film. Codex proposed the four, ten, six timing. The sheet is Bao's own, generated in Assignment two "
                "with FLUX one schnell, Apache two point oh. The code you saw is revision five f zero nine b seven f."),
               [("0.0", "CONTRIBUTIONS-assignment-7.md: Bao's work and decisions"),
                ("Claude Code", "what Claude Code wrote; prompts in prompts/assignment-7.md"),
                ("The sheet", "godot/assets/art/ATTRIBUTION.md"),
                ("revision", "source revision 5f09b7f")], 30,
               "Roles from CONTRIBUTIONS-assignment-7.md and prompts/assignment-7.md; sheet credits from godot/assets/art/ATTRIBUTION.md."),
    {"beat_id": "B21", "act": "VERDICT",
     "role_note": "ClaudeVerdictArtifact — implemented work, limitations, human judgment; shows the source revision.",
     "narration_text": ("The verdict. Implemented: a walk on a frame track and a dash on a cutout rig, driven by one "
                        "authority, with Bao's rules for every phase. Checked: pins before and after, eighty-six "
                        "read-back checks, edges at three frame rates, four mutations, and two clocks measured zero "
                        "seconds apart. The limits are written down. And the human judgments, the strips, the play "
                        "checks, keep four, ten, six, keep the outline, are Bao's own."),
     "estimated_duration_s": 24,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "artifact-reveal",
              "show": [{"at": "0.0", "event": "artifact card 'Verdict', heading with the source revision"},
                       {"at": "0.2", "event": "implemented line"}, {"at": "0.45", "event": "checked line"},
                       {"at": "0.65", "event": "limits line"}, {"at": "0.85", "event": "human-judgment line"}],
              "remotion": {"pattern": "ClaudeVerdictArtifact", "props": {
                  "artifactTitle": "Verdict", "artifactHeading": f"Lanternfall animation · source revision {SHORT}",
                  "brandLabel": HANDLE,
                  "artifactLines": ["Implemented: walk frame track, dash cutout rig, one authority, Bao's phase rules.",
                                    "Checked: pins, read-back 86/86, edges at 30/60/144, four mutations, clocks 0 s apart.",
                                    "Limits: no reference dash measured; r1 came from a reading; the outline can read detached.",
                                    "Human judgment: Bao's strips, play checks and verdicts, quoted as Bao gave them."]}}}},
    {"beat_id": "B22", "act": "HANDOFF",
     "role_note": "HANDOFF LAW — Your Turn: one bounded change through the phase table plus a prediction and a strip. Liam reads the prompt, discusses it and signs off.",
     "narration_text": ("Your turn. Paste this: Please use Walker to read the dash in my Lanternfall clip library. In my "
                        "phase table, change only the recovery from six frames to nine, and let it flow down: the "
                        "builder's keys, the read-back's expected times, and a re-pin of the edge tests in its own commit. "
                        "Before running anything, predict which strip frames change and what the courier shows on dash "
                        "frame sixteen. Then record strip r three and compare it with your prediction. It tests whether you "
                        "believe the table, not the keys, is the design. Write the prediction first. Liam, in for Bear."),
     "estimated_duration_s": 32,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on",
              "show": [{"at": "0.02", "event": "composer card; greeting 'Your turn.'"},
                       {"at": "0.1", "event": "the paste-ready prompt types in"},
                       {"at": "0.7", "event": "three output lines: prediction first, strip, re-pin"}],
              "remotion": {"pattern": "ClaudeComposerAsk", "props": {
                  "greeting": "Your turn.", "topic": TOPIC, "segment": "Lanternfall",
                  "command": YOUR_TURN,
                  "runningText": "paste this into Claude…",
                  "folderLabel": HANDLE, "modelLabel": "Claude", "effortLabel": "High",
                  "output": ["Prediction written before the strip.", "Strip r3 recorded: compare with your prediction.",
                             "Edge tests re-pinned in their own commit."], "animateTyping": True}}}},
    {"beat_id": "B23", "act": "OUTRO",
     "role_note": "OUTRO LAW — ClaudeTitleOutro: exact title, @NikBearBrown, slug-seeded mascot, stock jingle only, no narration.",
     "narration_text": "", "estimated_duration_s": 10.36, "actual_duration_s": 10.36,
     "audio_file": "mp3/beat-B23.wav",
     "audio_note": "stock @NikBearBrown jingle logos/bear-brown/bear-brown-3.mp3, picked by the slug seed (char-sum 5288 mod 6 pool files = 2), never cut: padded with 1.0 s of silence (9.36 s + 1.0 s); no narration (Liam signs off in B22)",
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "mascot-title",
              "show": [{"at": "0.0", "event": f"title '{TITLE}'"}, {"at": "0.25", "event": "@NikBearBrown"},
                       {"at": "0.45", "event": "slug-seeded mascot"}],
              "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "durationSeconds": 10.36}}}},
]


def main() -> None:
    path = REEL / "beat_sheet.json"
    old = {b["beat_id"]: b for b in json.loads(path.read_text())["beats"]} if path.exists() else {}
    beats = []
    for b in BEATS:
        b = json.loads(json.dumps(b))
        prev = old.get(b["beat_id"], {})
        for k in ("actual_duration_s", "audio_file", "render_duration_s", "audio_levelled", "audio_note"):
            if k in prev and k not in b and prev.get("narration_text") == b.get("narration_text"):
                b[k] = prev[k]
        if prev.get("shot", {}).get("remotion", {}).get("rendered") and "remotion" in b["shot"]:
            b["shot"]["remotion"]["rendered"] = prev["shot"]["remotion"]["rendered"]
        dur = b.get("actual_duration_s") or b.get("estimated_duration_s")
        cues = b.pop("_cues", None)
        cards = b.pop("_cards", None)
        b.pop("_excerpt", None)
        rem = b["shot"].get("remotion")
        if rem and "durationSeconds" in rem["props"]:
            rem["props"]["durationSeconds"] = round(float(dur), 2)
        if cues:
            rem["props"]["cues"] = [{"at": at(b["narration_text"], p, dur), "line": ln, "label": lab} for p, ln, lab in cues]
        if cards:
            rem["props"]["cues"] = [{"at": at(b["narration_text"], p, dur), "card": i} for p, i in cards]
        b.setdefault("voice", "am_onyx")
        b.setdefault("engine", "kokoro")
        beats.append(b)
    sheet = {"metadata": {
        "title": TITLE, "slug": SLUG, "topic": TOPIC, "kind": "godot-gamedev", "modifier": "walker",
        "playlist": "CSYE 7270", "brand": "claude-liam", "audience": "CSYE 7270 classmates and instructors",
        "register": "Teardown", "engine": "kokoro", "voice": "am_onyx", "voice_kokoro": "am_onyx",
        "palette": "claude", "style_preset": "claude", "ground": "#FAF9F5", "aspect_ratio": "16:9", "fit": "contain",
        "captions": False, "channel_title": "", "channel": HANDLE, "folderLabel": HANDLE,
        "channel_title_note": "empty on purpose: B00's composer already shows @NikBearBrown (OUTRO-LOCK: one handle per beat)",
        "greeting": "Hola, Liam",
        "greeting_note": "hello lexicon: Hola (Spanish); earlier Lanternfall films used Merhaba (A2), Hej (A3), Ciao (A5), Bonjour (A6). Liam never takes Wagwan (IN-FOR-BEAR LAW).",
        "persona": "Liam (in for Bear)", "presenter": "Liam (in for Bear)", "in_for_bear": True,
        "game": {"repo": "https://github.com/yanxlh/walker-lanternfall-bao-x", "project_dir": "godot",
                 "source_revision": FILM_SHA, "godot": "4.7.2.stable.official.ed1daf0bf"},
        "teaching_contract": "code-then-result-v1",
        "note": ("godot-gamedev + walker teardown of Bao Xing's CSYE 7270 animation assignment. Every code panel is a "
                 f"verbatim excerpt of godot/ at {FILM_SHA} (read with git show, never the working tree); the gameplay "
                 "take is a real Movie Maker capture of an isolated copy of that revision, recorded by Bao with the "
                 "disclosed film driver; strips are Bao's fixture captures; tool output is recorded. No paid call, no upload."),
        "links": {"repo": "https://github.com/yanxlh/walker-lanternfall-bao-x"},
        "tags": ["Godot 4", "godot-gamedev", "Walker", "AnimationPlayer", "sprite sheet", "cutout rig",
                 "state machine", "CSYE 7270", "Teardown register", "Kokoro"]},
        "beats": beats}
    path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
    words = sum(len(b["narration_text"].split()) for b in beats)
    est = sum(float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in beats)
    print(f"{path}: {len(beats)} beats, {words} words, ~{est:.0f}s")


if __name__ == "__main__":
    main()

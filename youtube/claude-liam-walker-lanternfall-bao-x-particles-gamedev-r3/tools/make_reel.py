#!/usr/bin/env python3
"""Write beat_sheet.json for the revised Lanternfall particle film (Assignment 6, godot-gamedev + walker).

Code excerpts are read at run time, by line range, from the film's source snapshot (FILM-SOURCE-PATH.txt; its
godot/ tree id is FILM-SOURCE-REVISION.txt), so what the film shows is the file's text. Run it again after narration
is measured: measured durations are kept and every Remotion beat's durationSeconds and highlight times are re-derived
from them (a highlight lands where its phrase sits in the narration).

    python3 tools/make_reel.py
"""
import json
import subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
SRC = Path((REEL / "FILM-SOURCE-PATH.txt").read_text().strip())
GAME = SRC / "godot"
FILM_TREE = (REEL / "FILM-SOURCE-REVISION.txt").read_text().strip()
SHORT = FILM_TREE[:7]
BASE_COMMIT = "c6e6343"
SLUG = "claude-liam-walker-lanternfall-bao-x-particles-gamedev-r3"
TITLE = "Lanternfall, Sparked Again"
PROJECT = "walker-lanternfall-bao-x"
HANDLE = "@NikBearBrown"
TOPIC = "WALKER · GODOT PARTICLES"
REV = f"source tree {SHORT}"


def excerpt(path: str, a: int, b: int) -> str:
    return "\n".join((GAME / path).read_text().splitlines()[a - 1:b])


def at(text: str, phrase: str, dur: float, lead: float = 0.25) -> float:
    """Seconds into the beat where `phrase` is spoken, by its position in the narration."""
    i = text.find(phrase)
    if i < 0:
        raise SystemExit(f"cue phrase not in narration: {phrase!r}")
    return round(max(0.0, dur * i / max(1, len(text)) - lead), 2)


def code_beat(bid, act, path, a, b, title, narration, cues, notes, output, est, font=None):
    return {"beat_id": bid, "act": act, "kind": "code",
            "role_note": f"Code beat (code-then-result-v1): {path} lines {a}-{b} in {REV}, read verbatim; the next beat shows the result.",
            "narration_text": narration, "estimated_duration_s": est,
            "_cues": cues,
            "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "line-highlight",
                     "show": [{"at": "0.0", "event": f"Godot editor reconstruction opens on {path}, lines {a}-{b}"}] +
                             [{"at": c[0], "event": f"line {c[1]} highlights — {c[2]}"} for c in cues] +
                             [{"at": "notes", "event": "source-notes panel (not Inspector values) lists the related lines"}],
                     "remotion": {"pattern": "GodotDevWorkbench", "props": {
                         "mode": "code", "title": title, "project": PROJECT, "path": f"res://{path}",
                         "source": f"godot/{path} · lines {a}–{b} · {REV} · Godot editor reconstruction",
                         "code": excerpt(path, a, b), "startLine": a, "codeFontSize": font or 25,
                         "inspectorLabel": "Source notes — not Inspector values",
                         "notes": [{"label": k, "value": v} for k, v in notes], "output": output,
                         "cues": [], "durationSeconds": est}}},
            "_excerpt": {"path": path, "start_line": a, "end_line": b}}


OBSERVED = {
    "B05": "In the current r2 fixture strip all sixteen sparks leave on one frame as a single white cluster, spread and slow over the next fifth of a second, stay pale yellow to about 0.27 s, then shrink to orange specks; the last pixel goes at 0.40 s.",
    "B07": "In the main take every beam hit puts a burst at the monster; the live-burst counter, read from the take's own per-frame log, climbs when hits land a few frames apart and falls back as bursts finish.",
    "B10": "Side by side, r1's sparks are chunkier from 0.03 to 0.27 s while the footprint and the fade frame match r0; the measured numbers sit beside the prediction.",
    "B12": "Side by side, r2's sparks are pale yellow and bright at 0.20 and 0.27 s where r1's are dim orange; every extent and the last frame are identical.",
    "B14": "Pushing straight into the stall the courier does not move and no embers appear; sliding along its edge the trail runs behind his feet again.",
    "B16": "In the trail fixture, r1's embers are brighter at startup and during steady movement, with the same footprint, and both strips are clear by frame 51.",
    "B18": "On the card screen the celebration bursts on the small courier in the lower-left portrait, above the dark veil, and finishes before the scripted pick.",
    "B20": "Under the PAUSED line the embers and a hit burst stay where they were (two paused frames are pixel-identical) and carry on after resume; the scripted play-check shots show LOST and WON with no particles left.",
    "B22": "Recorded output: nine suites, 327 checks, zero failures; the Godot 3 name and the changed spread each make the A configuration test exit 1; with the displacement guard removed, exactly two trail checks fail.",
    "B24": "With the same seed and frames, the GPU study copy, its ramp and curve textures bound, now shrinks and turns from pale yellow to orange like the CPU burst, a little sooner; its random spread differs.",
    "B26": "The CPU deltas of two independent r2 runs are drawn against their budgets; A sits under a tenth of its one-millisecond budget, and B's sign flips between runs.",
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


def listen_beat(bid, show, role):
    return {"beat_id": bid, "act": "REPORT", "kind": "source_report", "clock": "source", "audio_policy": "preserve",
            "role_note": role, "narration_text": "",
            "shot": {"type": "SOURCE_REPORT", "class": "SHOW", "source": "own", "motion": "real-footage",
                     "show": [{"at": s[0], "event": s[1]} for s in show], "treatment": "none"}}


ASK = ("Please use Walker to convert my game design document about particle effects for Lanternfall, warm sparks on "
       "every weapon hit and a short ember trail behind the courier, into Godot 4 CPUParticles2D scenes. Gameplay "
       "must not change. Test every setting, and tune each effect from what I see in the game, with real frames "
       "before and after.")

YOUR_TURN = ("Please use Walker to read godot/effects/defeat_sparks.tscn in my Lanternfall project. Change only "
             "amount from 16 to 24. Before running anything, predict the first visible frame and the frame at 0.20 s "
             "in the fixture strip, which configuration check fails, and the new peak particle count at 32 bursts. "
             "Then capture the strip, compare it with your prediction, and put 16 back.")

BEATS = [
    {"beat_id": "B00", "act": "ASK",
     "role_note": "COLD OPEN LAW — Claude composer; reconstructed Walker prompt from Bao's CHANGE-BRIEF.md (not a recorded session). Liam introduces himself.",
     "narration_text": ("Bonjour — this is Liam, in for Bear. Bao Xing's particle assignment, revised: two effects in a "
                        "Godot game that already works, each tuned from what Bao actually saw, tested, taken down to the "
                        "shader Godot generates, and priced on the CPU and the GPU. The game is Lanternfall. Here is the "
                        "ask, rebuilt from Bao's change brief."),
     "estimated_duration_s": 22,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on",
              "show": [{"at": "0.02", "event": "composer card on cream; greeting 'Bonjour, Liam'"},
                       {"at": "0.25", "event": "the reconstructed Walker prompt types in"},
                       {"at": "0.62", "event": "send arms; running line names the brief and the session file"},
                       {"at": "0.75", "event": "three result lines: effects, checks, kept changes"}],
              "remotion": {"pattern": "ClaudeComposerAsk", "props": {
                  "greeting": "Bonjour, Liam", "topic": TOPIC, "segment": "Lanternfall",
                  "command": ASK,
                  "runningText": "reading CHANGE-BRIEF.md · CLAUDE.md · godot/game/session.gd…",
                  "folderLabel": HANDLE, "modelLabel": "Claude", "effortLabel": "High",
                  "output": ["Hit sparks · movement trail · level-up celebration",
                             f"327 automated checks · {REV}",
                             "Four tuning changes, each kept by Bao after playing"]}}}},
    {"beat_id": "B01", "act": "BLUF",
     "role_note": "EXECUTIVE-SUMMARY LAW — hesitant writer. The framing a viewer arrives with ('particles are decoration') is corrected to what the film shows ('particles are feedback').",
     "narration_text": ("The short version. These particles are feedback, not decoration. Each one answers a real event "
                        "in the game: a hit, a step, a new level. None of them may change a single rule. And the one "
                        "change that counts was made because Bao looked at the game and said the sparks weren't enough."),
     "estimated_duration_s": 17, "lead_silence_s": 0.8,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on-correct",
              "show": [{"at": "0.0", "event": "cream page; 'Particles are decoration' types"},
                       {"at": "0.3", "event": "'decoration' struck in terracotta, 'feedback' typed in"},
                       {"at": "0.6", "event": "'each one answers an event' and 'the rules stay untouched' type in"}],
              "remotion": {"pattern": "BrutalistHesitantWriter", "props": {
                  "text": "Particles are decoration\neach one answers an event\nthe rules stay untouched",
                  "triggerWords": "decoration", "replacementWords": "feedback", "fontSize": 170, "lineSpacing": 1.5,
                  "align": "center", "seed": str(sum(map(ord, SLUG))), "mistakeRate": 2, "hesitateWithin": 0,
                  "hesitateBetween": 1, "ink": "#3D3929", "accent": "#D97757", "bg": "#FAF9F5"}}}},
    {"beat_id": "B02", "act": "ASSIGNMENT",
     "role_note": "Assignment requirements beside the purpose Bao's CHANGE-BRIEF.md states; the excerpt is the brief's current supplement, verbatim.",
     "narration_text": ("What the assignment asks for, and what Bao's brief answers. Effect A, a burst of sparks on "
                        "every weapon hit. Effect B, a short ember trail, only while the courier really moves. One "
                        "change to each, driven by something seen in the running game, with a prediction and real "
                        "frames before and after. Tests that read every setting back. And under the hood: the process "
                        "shader Godot writes, and a price on the CPU and the GPU against a budget set in advance."),
     "estimated_duration_s": 26,
     "_cards": [("Effect A, a burst", 0), ("Effect B, a short", 1), ("One change to", 2), ("Tests that read", 3)],
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "card-cues",
              "show": [{"at": "0.0", "event": "CHANGE-BRIEF.md 'What I want to do' excerpt beside four requirement cards"},
                       {"at": "Effect A, a burst", "event": "card 1 highlights"},
                       {"at": "Effect B, a short", "event": "card 2 highlights"},
                       {"at": "One change to", "event": "card 3 highlights"},
                       {"at": "Tests that read", "event": "card 4 highlights"}],
              "remotion": {"pattern": "GodotDesignBoard", "props": {
                  "title": "What the assignment asks", "section": "CHANGE-BRIEF.md · What I want to do",
                  "excerpt": ("I want players to understand two things without relying on sound: whether an attack "
                              "connected, and which way the courier is moving. Effect A is a weapon-hit spark burst. "
                              "Effect B is a trail of embers near the courier's feet."),
                  "source": "CHANGE-BRIEF.md · original drafted 29 October (04ef18a); this supplement written by Bao on 9 November",
                  "status": "Effects may read gameplay state but never write it",
                  "visualLabel": "Requirements", "layout": "cards",
                  "cards": [{"label": "1 · Effect A: hit sparks", "text": "One-shot CPUParticles2D burst on every weapon_hit; overlapping, at most 32."},
                            {"label": "2 · Effect B: trail", "text": "Sphere emission, radius 3; only while PLAYING, visible and actually moving."},
                            {"label": "3 · One observed change each", "text": "Prediction, one setting, before/after strips, a verdict after play."},
                            {"label": "4 · Tests, shader, price", "text": "Every setting read back; the generated shader; CPU and GPU against a budget."}],
                  "cues": [], "durationSeconds": 26}}}},
    listen_beat("B03", [("0.0", "the run under way: beam hits spark, the trail follows the courier"),
                        ("level-up", "a level-up: the celebration on the card-screen portrait, cards held 2 s"),
                        ("card", "card taken, play resumes")],
                "Game sound only, no narration: a stretch of the main take (seed 11, r2 sparks) with all three effects."),
    code_beat("B04", "CODE", "effects/defeat_sparks.tscn", 19, 32, "Three parts, one file.",
              ("A particle system is one node that spawns many short-lived, slightly different copies, and it "
               "decides three things. Emission: when, and how many. Sixteen sparks, all on one frame, because "
               "explosiveness is one, each living forty-five hundredths of a second, from a single point. Process: how "
               "each one moves and changes. Spread one-eighty, speed from twenty-five, a little gravity; further down "
               "the file, damping, the scale curve and the colour ramp. Draw: what each one looks like. A "
               "three-pixel spark texture, through an additive material."),
              [("Sixteen sparks", 21, "EMISSION · amount = 16"),
               ("explosiveness is one", 26, "EMISSION · explosiveness = 1.0: all on one frame"),
               ("forty-five hundredths", 23, "EMISSION · lifetime = 0.45 s"),
               ("single point", 28, "EMISSION · emission_shape = 0: point"),
               ("Spread one-eighty", 30, "PROCESS · spread = 180°"),
               ("speed from twenty-five", 32, "PROCESS · initial_velocity_min 25 (max 55 on line 33)"),
               ("a little gravity", 31, "PROCESS · gravity (0, 12)"),
               ("three-pixel spark texture", 22, "DRAW · texture = spark.png, 3 × 3"),
               ("additive material", 19, "DRAW · CanvasItemMaterial, blend_mode 1 (add)")],
              [("Emission", "lines 21, 23, 24, 26, 28"),
               ("Process", "29–33; damping, curves, ramp 34–39"),
               ("Draw", "19 material · 22 texture")],
              ["CPUParticles2D: the process step runs in engine code on the CPU; a GPUParticles2D would run it as a shader"], 30, font=23),
    media_beat("B05", "RESULT",
               ("Those three decisions, in a real fixture capture of the current version. Emission puts all sixteen out "
                "on one frame, so the first frame is one white cluster: the additive draw adds overlapping sparks until "
                "they read as white. Process spreads them, slows them, and walks each one along the colour ramp and the "
                "scale curve: pale yellow through a quarter of a second, then shrinking orange specks. At four tenths of "
                "a second the last one is gone, because its lifetime ran out."),
               [("0.0", "r2 fixture strip, files 9–22, magnified 12×; courier on the left for scale"),
                ("one white cluster", "file 9 · EMISSION + DRAW: sixteen at once, added to white"),
                ("Process spreads", "files 12–17 · PROCESS: spread, damping, ramp"),
                ("shrinking", "files 18–20 · PROCESS: scale curve to zero"),
                ("last one is gone", "file 21: last trace; file 22 empty")], 24,
               "Result of B04. Real windowed fixture capture (captures/defeat_sparks/r2), 30 fps, seed 7280; measurements from comparison-r1-r2/COMPARISON.md.",
               evidence=True),
    code_beat("B06", "CODE", "effects/particle_presentation.gd", 47, 57, "One burst per hit.",
              ("Effect A starts with a signal. The session's damage function, which every weapon calls, announces each "
               "hit and where it landed. This listener answers it. Line forty-nine drops the hit unless the game is "
               "playing and fewer than thirty-two bursts are alive. Then a fresh burst is placed at the hit, in world "
               "space, and restarted. A new node per hit is the brief's overlap rule: a second hit never cuts off the "
               "first."),
              [("Line forty-nine", 49, "PLAYING only · at most 32 live bursts"),
               ("a fresh burst", 51, "a new instance per accepted hit (overlap)"),
               ("in world", 53, "global_position = the hit, in world space"),
               ("restarted", 56, "restart(): one-shot burst")],
              [("session.gd", "weapon_hit(pos) emitted in damage()"),
               ("Lethal and nonlethal", "both spark"),
               ("_on_hit_finished 72–74", "frees the burst")],
              ["the burst belongs to the presentation root, not the enemy, so it survives the kill"], 24),
    media_beat("B07", "RESULT",
               ("Here it is in the running game. Every time the beam connects, a small burst lands on the monster, and "
                "it keeps playing after the monster is gone. The counter comes from the take's own log: when hits land "
                "a few frames apart, it climbs, because bursts overlap instead of restarting each other. A stress test "
                "with forty hits in one volley confirms the cap: thirty-two bursts, never more."),
               [("0.0", "real 4K capture, main take: beam hits spark at the monster"),
                ("counter", "live-burst counter from the take's per-frame log"),
                ("stress test", "recorded state-test lines: 40 hits seen, 32 bursts, 512 particles")], 20,
               "Result of B06. Real 4K engine capture (main take, seed 11, r2 sparks, scripted input); counter from the capture's own track log; cap from evidence/assignment-6/current-r2-validation/particles_state.json.",
               evidence=True),
    media_beat("B08", "INTENT",
               ("Before any tuning, the brief said how the burst should read: a compact flash on the first frame, a "
                "fast spread by a fifth of a second, gone by forty-five hundredths, about one character high at the "
                "start and never more than two. The first strip, r zero, met the ceiling and the fade. Its first frame "
                "was a third of a character high."),
               [("0.0", "CHANGE-BRIEF.md visual intent, original 29 October text"),
                ("The first strip", "r0 fixture strip, files 9, 11, 15, 21: the first strip"),
                ("a third of a character", "file 9: 11 × 12 px against a 34 px courier")], 18,
               "Effect A's intent block (CHANGE-BRIEF.md, original record) beside the first fixture strip r0 (captures/defeat_sparks/r0)."),
    code_beat("B09", "CODE", "effects/defeat_sparks.tscn", 36, 39, "The first change, r one.",
              ("The first change, r one. In play Bao saw no problem; the strip disagreed with the brief's starting size. "
               "So one value moved, on line thirty-seven: the largest spark scale, from one point two to one point "
               "eight. That change came from Claude's reading of a strip, not from Bao's eyes in the game, which is why "
               "it is not the observed change the assignment asks for."),
              [("line thirty-seven", 37, "scale_amount_max 1.2 → 1.8"),
               ("one value moved", 36, "scale_amount_min 0.7 unchanged")],
              [("Bao, in play", "“Done; no problem”"),
               ("r0, first frame", "11 × 12 px: 0.35 height"),
               ("Prediction", "≈ 15 × 15 px; +3–4 px wide")],
              ["approved (“Agreed”) · config test edited and failing first, then the scene"], 22),
    media_beat("B10", "RESULT",
               ("Before on top, after below, same seed, same frames. The first frame grew from eleven to fourteen pixels, "
                "close to the predicted fifteen. The sparks got chunkier. But the footprint widened by one pixel, not the "
                "predicted three or four, because positions set the spread. Bao played it and kept it: clearer."),
               [("0.0", "r0 (top) vs r1 (bottom) contact sheet, 3× crops"),
                ("predicted fifteen", "prediction vs measured, row by row"),
                ("one pixel", "the miss marked: predicted +3–4 px, measured +1 px"),
                ("kept it", "Bao's verdict: “Keep it; it is clearer”")], 18,
               "Result of B09. Real fixture captures r0 and r1 (captures/defeat_sparks/comparison-r0-r1); verdict from TUNING.md.",
               evidence=True),
    code_beat("B11", "CODE", "effects/defeat_sparks.tscn", 12, 14, "The observed change, r two.",
              ("The change that counts. Bao played the game and said the hit sparks weren't eye-catching enough. "
               "Claude's reading of the r one strip: bright for only a tenth of a second, mid-orange by a fifth. One "
               "setting: the colour ramp's middle stop moves from point three five to point six, and turns brighter "
               "and fully opaque. Prediction, written before the edit: brighter for longer, the same size, the same "
               "last frame."),
              [("the colour ramp's middle stop", 13, "offsets 0, 0.35, 1 → 0, 0.6, 1"),
               ("fully opaque", 14, "middle colour (1, .6, .2, .85) → (1, .75, .3, 1)")],
              [("Bao, in play", "“The hit sparks are not eye-catching enough”"),
               ("r1 at 0.20 s", "mid-orange; 21 of 189 lit px bright"),
               ("Test first", "edited first; failed there only")],
              ["approved (“Approve”) · start and end stops, count, size, speed and lifetime unchanged"], 26),
    media_beat("B12", "RESULT",
               ("Same seed, same frames. At a fifth of a second the sparks went from mid-orange to pale yellow, and every "
                "lit pixel crossed the brightness line: one hundred eighty-nine, against twenty-one. At a quarter "
                "second they are still bright. The footprint and the last frame did not move. The miss: Claude predicted "
                "yellow-orange, and additive overlap made it paler, close to white. Bao played it, checked it against the "
                "courier's lamp and the yellow gems, and kept it."),
               [("0.0", "r1 (top) vs r2 (bottom) contact sheet, 3× crops"),
                ("one hundred eighty-nine", "file 15: luma 151 → 236; bright px 21 → 189"),
                ("still bright", "file 17: bright px 2 → 83"),
                ("The miss", "predicted yellow-orange, measured pale yellow (255, 238, 163)"),
                ("kept it", "Bao's verdict: “Yes” · “They don't get mixed up” · kept")], 26,
               "Result of B11. Real fixture captures r1 and r2 (captures/defeat_sparks/comparison-r1-r2), measurements and hashes from COMPARISON.md and manifest.json; verdict from TUNING.md.",
               evidence=True),
    code_beat("B13", "CODE", "effects/particle_presentation.gd", 121, 131, "A trail that needs real movement.",
              ("Effect B, the trail, is decided once per physics frame. Line one twenty-six measures how far the courier "
               "actually moved since the last frame. Holding a key is not enough. Line one twenty-seven sets a jump "
               "limit, twice a frame's walk plus four pixels, so a teleport or a restart never draws a streak. Line one "
               "twenty-nine emits only while playing, visible, and genuinely moving."),
              [("Line one twenty-six", 126, "distance actually moved"),
               ("Line one twenty-seven", 127, "jump limit = speed × Δt × 2 + 4 ≈ 7 px"),
               ("Line one twenty-nine", 129, "PLAYING · visible · 0.01 < distance ≤ limit")],
              [("Line 128", "trail at the feet: (0, 7)"),
               ("local_coords = false", "embers stay put"),
               ("Restart 88–97", "history reset")],
              ["reads session.player and session.state; writes only the trail"], 22),
    media_beat("B14", "RESULT",
               ("The proof is a wall. The script walks the courier up to a stall and holds right. The key is down, but "
                "he can't move, so no embers. Then it holds down and right: he slides along the edge, and the trail is "
                "back behind his feet. The line under the footage is the trail's emitting flag, read from the take's own "
                "per-frame log."),
               [("0.0", "real 4K capture, props take: walking to the nearest stall"),
                ("holds right", "pushing into the stall: no displacement, no embers"),
                ("slides", "down-right: sliding along the edge, trail back"),
                ("emitting flag", "per-frame strip: trail emitting yes / no, from the take's log")], 20,
               "Result of B13. Real 4K engine capture (props take, seed 11, scripted input through the real input map); emitting flag from the capture's track log.",
               evidence=True),
    code_beat("B15", "CODE", "effects/lantern_trail.tscn", 17, 29, "The trail's own feature.",
              ("The trail's scene shows the feature the burst doesn't use. It emits continuously from a sphere with a "
               "three-pixel radius, emission shape one, where the burst uses a single point. Twenty-four embers drift "
               "upward and fade from amber to dark orange in a third of a second. Its tuning change lives on line "
               "fourteen: the alpha at the start and the middle of each ember's life."),
              [("three-pixel radius", 29, "emission_sphere_radius = 3.0 (radius, px)"),
               ("emission shape one", 28, "emission_shape = 1: sphere (A uses 0: point)"),
               ("Twenty-four embers", 21, "amount = 24 · continuous (one_shot = false)")],
              [("Line 14, the change", "alpha 0.95 / 0.70 / 0"),
               ("Before (r0)", "alpha 0.55 / 0.30 / 0"),
               ("Paused · hidden", "frozen · no spawning, old embers expire")],
              ["lifetime 0.35 s (line 23) · spread 25° upward · brief: dimmer and smaller than A"], 24, font=23),
    media_beat("B16", "RESULT",
               ("Bao's first look at the integrated game: the trail wasn't obvious. Raising only those two alpha values "
                "gave brighter embers at startup and in steady movement, with the same footprint, and both versions "
                "clear by the same frame after stopping. Bao played it and kept it. In normal play the trail stays two "
                "to four pixels per ember, still smaller and dimmer than a hit spark."),
               [("0.0", "trail fixture r0 (top) vs r1 (bottom), frames 12–39, crops"),
                ("same footprint", "frames 20 and 39 marked"), ("same frame", "frames 51 and 60: both clear"),
                ("smaller and dimmer", "play-check crop: trail flecks beside a hit spark")], 22,
               "Result of B15. Real fixture captures (captures/lantern_trail/comparison-20261029-135607), the original re-rendered from its preserved resource; play-check shots from captures/play-checks/20261029-142138.",
               evidence=True),
    code_beat("B17", "CODE", "effects/particle_presentation.gd", 59, 70, "The celebration, on the card screen.",
              ("The extra effect: a gold celebration on every level-up. Its first version was drawn in the world, under "
               "the upgrade screen's dark veil, and Bao found it hard to see. Now it goes into its own overlay layer, "
               "eleven, above the HUD, and line sixty-six anchors it to the little courier portrait on the card screen. "
               "At most four can be alive at once."),
              [("level-up", 59, "leveled_up(level) signal"),
               ("its own overlay layer", 65, "level_overlay: CanvasLayer 11, above HUD layer 10"),
               ("line sixty-six", 66, "position = the card-screen portrait"),
               ("At most four", 61, "PLAYING only · ≤ 4 live celebrations")],
              [("Anchor", "HUD-local (56, 325)"),
               ("Bao's request", "on the small character"),
               ("Scene", "32 particles · 0.7 s")],
              ["_apply_policy keeps it playing during LEVELUP (lines 114–116)"], 22),
    media_beat("B18", "RESULT",
               ("In the real take, the level-up arrives and the card screen opens. The burst lands on the small courier "
                "in the lower-left portrait, white first, then gold, and it's gone well before the scripted pick two "
                "seconds later. The cards stay readable. Bao looked at exactly this placement and said: that works."),
               [("0.0", "real 4K capture, main take: level-up, card screen opens"),
                ("lower-left portrait", "crop of the portrait: white → gold → gone"),
                ("that works", "Bao's verdict: “That works”")], 18,
               "Result of B17. Real 4K engine capture (main take, seed 11); verdict from TUNING.md.", evidence=True),
    code_beat("B19", "CODE", "effects/particle_presentation.gd", 107, 119, "Freeze, don't fake.",
              ("One policy runs every frame, and it only reads the game. When the game isn't playing, hit bursts and "
               "the trail get a speed scale of zero, so they freeze exactly where they are. The celebration keeps "
               "playing on the card screen. Outside play, or while the effect is hidden, the trail never spawns. On a "
               "loss or a win, everything is cleared."),
              [("speed scale of zero", 113, "hit bursts: speed_scale 0 outside PLAYING"),
               ("keeps", 116, "celebration: runs in PLAYING and LEVELUP"),
               ("never spawns", 118, "no spawning outside play or while hidden")],
              [("_apply_policy() 107", "runs every physics frame"),
               ("_on_state_changed 99–105", "WON · LOST · MENU: clear"),
               ("Whole-tree pause", "its own test suite")],
              ["no line in this file writes session state"], 22),
    media_beat("B20", "RESULT",
               ("At thirty seconds the script presses pause. Under the pause screen, the embers hang exactly where they "
                "were: two frames a second apart match pixel for pixel. Then play resumes and they carry on. The "
                "scripted play checks cover the endings: on the first frame of a loss or a win, every particle is gone. "
                "Bao's own check in the game: stop moving and the trail stops; pause and everything stays frozen."),
               [("0.0", "real 4K capture, main take: pause at run 0:30, held 2.5 s"),
                ("pixel for pixel", "two paused frames a second apart, side by side: 0 pixels differ"),
                ("play resumes", "resume: the trail carries on"),
                ("endings", "play-check shots: lost+00 and won+00, particles cleared (scripted, 1280 × 720)"),
                ("Bao's own check", "Bao's recorded check (TUNING.md)")], 22,
               "Result of B19. Real 4K engine capture (main take) plus labelled scripted play-check shots (captures/play-checks/20261029-142138); Bao's check from TUNING.md.",
               evidence=True),
    code_beat("B21", "CODE", "tests/test_particles_edges.gd", 57, 69, "Testing what the eye can't.",
              ("Tests catch what a glance misses. This edge test puts the courier against a stall, holds the right key "
               "for thirty frames through the real input system, and counts two things: how far he moved, and how many "
               "frames the trail emitted. Both must be zero. Separately, the configuration tests read every value the "
               "brief names back from the loaded scenes."),
              [("puts the courier against a stall", 57, "fixture: courier touching the stall's left edge"),
               ("holds the right key", 60, "real key event: D"),
               ("Both must be zero", 69, "blocked-push-never-emits")],
              [("Particle suites", "40 + 81 + 34 + 18 + 21 + 11"),
               ("Godot 3 name", "loads silently; test fails"),
               ("Limit", "can't judge the look")],
              ["evidence/assignment-6/current-r2-validation"], 22, font=23),
    media_beat("B22", "RESULT",
               ("Recorded output, on this exact source: nine suites, three hundred twenty-seven checks, no failures, with "
                "the original game's tests unchanged. Then the proof the tests are real. Rename one property to its Godot "
                "three name, and the scene still loads, the burst still fires, a little tighter, and only the test "
                "notices. Change the spread without changing the brief, and it fails again. Delete the movement guard, "
                "and exactly two trail checks fail. None of this can say whether the effect looks right."),
               [("0.0", "recorded suite totals: current-r2-validation"),
                ("Godot three name", "mutation: initial_velocity_min → initial_velocity, exit 1; windowed frames 45 × 43 → 40 × 42 px"),
                ("Change the spread", "mutation: spread 180 → 90, exit 1"),
                ("Delete the movement guard", "edge suite with the guard removed: two FAILs"),
                ("looks right", "what no headless run can show")], 28,
               "Result of B21. Recorded tool output (evidence/assignment-6/current-r2-validation, evidence/assignment-6/mutations) and the windowed mutation capture (captures/defeat_sparks/mutation-godot3-name).",
               evidence=True),
    code_beat("B23", "CODE", "shaders/particles_generated.gdshader", 148, 161, "The shader Godot writes.",
              ("Under the hood. Converting a GPU copy of the burst in the editor produced this process shader. Two lines "
               "map straight onto the brief. Line one forty-nine picks each spark's size between scale min and max: the "
               "brief's point seven to one point eight. Line one sixty-one samples the colour ramp by the spark's age: "
               "the ramp whose middle stop r two moved to point six. Bao's explanation: this is the process stage, how a "
               "particle changes. The texture and the additive blend belong to the draw stage."),
              [("Line one forty-nine", 149, "scale_min/max ← brief scale_amount 0.7 / 1.8"),
               ("Line one sixty-one", 161, "color_ramp at age ← brief ramp, middle stop 0.6 (r2)"),
               ("draw stage", 155, "COLOR starts from color_value; drawing happens elsewhere")],
              [("Line 139", "initial velocity 25–55"),
               ("Lines 311, 324", "gravity (0, 12) added to velocity"),
               ("Line 160", "scale_curve at age")],
              ["shader_type particles · start() 225 · process() 277 · study copy only; the game never loads it"], 26, font=23),
    media_beat("B24", "RESULT",
               ("And what that shader does now. In the first film, the GPU copy stayed white and full-size, because its "
                "ramp and curve textures were missing. They were bound in the second revision, and the copy carries the "
                "current ramp. Same seed, same frames: the GPU copy now shrinks and turns from pale yellow to orange, "
                "like the CPU burst. Its random spread differs, and it turns orange a little sooner; the fade and the shrink are back."),
               [("0.0", "real 4K fixture capture: CPU burst (left) vs GPU study copy (right)"),
                ("Same seed", "both pale yellow, then orange, shrinking"),
                ("Its random spread differs", "different random positions: CPU and GPU draw different random numbers")], 22,
               "Result of B23. Real 4K fixture capture of the isolated copy (capture/study_capture.gd): the game's scene and the study scene, same seed 7280.",
               evidence=True),
    code_beat("B25", "CODE", "tests/cost_effects.gd", 58, 63, "Pricing it: on versus off.",
              ("Last, the price. The cost script builds the same game twice for every condition. Line sixty-one is the "
               "switch: with effects off, the presentation node is freed before the run starts, so gameplay, enemies and "
               "input stay identical. Then it times interleaved trials of three hundred frames: idle, at the burst cap, "
               "moving, and on the card screen, with an empty scene as the control."),
              [("same game twice", 58, "a fresh Session for each condition"),
               ("Line sixty-one", 61, "effects off: game.particles.free()"),
               ("identical", 63, "same fixture via run_started")],
              [("CPU", "headless frame time"),
               ("GPU", "windowed, measured"),
               ("Budgets (ms)", "A 1.0 / 0.75 · B 0.25 / 0.25")],
              ["empty scene = the control: if every case reads like it, the script is timing itself"], 22),
    media_beat("B26", "RESULT",
               ("The CPU price, from two separate runs on the current version: thirty-two live bursts add between five "
                "and ten hundredths of a millisecond a frame, against a budget of one. The trail's difference is so small "
                "that its sign flips between runs. Why trust a headless number here? Because these are CPU particles: "
                "the simulation runs on the processor even with nothing drawn. A GPU particle node would read near zero "
                "headless by construction, since a dummy renderer never runs its shader."),
               [("0.0", "CPU deltas against budgets: two r2 runs"),
                ("its sign flips", "B: +0.007 and −0.007 ms; ranges overlap"),
                ("A GPU particle node", "why headless ≈ 0 for GPU particles: no renderer, no process shader")], 26,
               "Result of B25. Recorded measurements (evidence/assignment-6/current-r2-validation/cpu-r2.json; evidence/assignment-6/cost/a-color-r2-reported-20261109) drawn as bars; nothing estimated.",
               evidence=True),
    media_beat("B27", "PRICE",
               ("The GPU price is the honest part. Under the game's own renderer this Mac reports zero on every frame, "
                "which means no timing, not no cost. Under a Mobile Vulkan proxy, the editor's Visual Profiler gave A "
                "plus point seven of a millisecond on one pair of frames and plus four point six on another, against a "
                "budget of point seven five. Averaged timer runs ranged from about zero to plus point four. So A's GPU "
                "budget is not settled, and the trail's readings are noise."),
               [("0.0", "GPU under GL Compatibility: 0.000 ms"),
                ("Visual Profiler", "editor Visual Profiler screenshots, A off / A on, Mobile + Vulkan, current r2"),
                ("plus four point six", "selected frames 715 / 782: GPU 0.62 → 5.21 ms"),
                ("Averaged timer runs", "viewport-timer runs: A r2 −0.06 … +0.39 ms"),
                ("not settled", "budget verdict: unresolved")], 28,
               "GPU evidence: editor Visual Profiler screenshots (evidence/assignment-6/cost/visual-profiler-a-r2-current), viewport-timer runs (current-r2-validation/gpu-r2.json and this film's tests/gpu-*.json), Compatibility zero readings (cost/final-comparison)."),
    media_beat("B28", "LEDGER",
               ("What else the record says. Mistakes caught along the way: a shader study missing its textures, two test "
                "fixtures that ran before their setup, a narrated width that was a radius, and a report that kept an old "
                "GPU line. No strip reading of Claude's was overruled; the strips corrected Claude's predictions twice. "
                "Still uncertain: the GPU budget, and a first frame under one character high. The next step: measure A "
                "on the GPU over many frames, not one. Bao made every observation and every keep decision, and rewrote "
                "the brief; Claude Code built and measured; Codex worked the editor and wrote two tests. The only "
                "particle texture is a three-by-three cross, written by a script."),
               [("0.0", "ledger: mistakes caught"),
                ("No strip reading", "Claude against Bao: no disagreement; two prediction misses"),
                ("Still uncertain", "uncertain: GPU budget; first-frame size; r2 paler than the brief"),
                ("The next step", "next step"),
                ("Bao made every observation", "human and AI contributions"),
                ("three-by-three", "texture source and revision shown")], 40,
               "Ledger from the repository's records: TEST-REPORT.md, TUNING.md, CONTRIBUTIONS-assignment-6.md, godot/assets/particles/ATTRIBUTION.md."),
    {"beat_id": "B29", "act": "VERDICT",
     "role_note": "ClaudeVerdictArtifact — implemented work, limitations, human judgment; shows the source tree.",
     "narration_text": ("The verdict. Implemented: three effects that answer real events and never write game state, "
                        "with three hundred twenty-seven checks behind them. Each effect has one change driven by what Bao "
                        "saw, with a prediction, real frames before and after, and the part of the prediction that missed. "
                        "The limits stay written down: no GPU time on the shipped renderer, and an unsettled GPU budget on "
                        "the proxy. Every keep-or-revert call was Bao's."),
     "estimated_duration_s": 24,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "artifact-reveal",
              "show": [{"at": "0.0", "event": "artifact card 'Verdict', heading with the source tree"},
                       {"at": "0.2", "event": "implemented line"}, {"at": "0.45", "event": "tuning-evidence line"},
                       {"at": "0.65", "event": "limits line"}, {"at": "0.85", "event": "human-judgment line"}],
              "remotion": {"pattern": "ClaudeVerdictArtifact", "props": {
                  "artifactTitle": "Verdict", "artifactHeading": f"Lanternfall particles · {REV}",
                  "brandLabel": HANDLE,
                  "artifactLines": ["Implemented: hit sparks, trail, celebration; game state never written; 327 checks.",
                                    "A and B: one observed change each, predicted, captured, kept; misses recorded.",
                                    "Limits: no GPU time on the shipped renderer; GPU budget unsettled on the proxy.",
                                    "Human judgment: every keep-or-revert call was Bao's, after playing."]}}}},
    {"beat_id": "B30", "act": "HANDOFF",
     "role_note": "HANDOFF LAW — Your Turn: one bounded change plus a prediction and a capture. Liam reads the prompt and signs off.",
     "narration_text": ("Your turn. Paste this: Please use Walker to read the hit-spark scene in my Lanternfall project. "
                        "Change only amount, from sixteen to twenty-four. Before running anything, predict the first "
                        "visible frame and the frame at a fifth of a second in the fixture strip, which configuration "
                        "check fails, and the new peak particle count at thirty-two bursts. Then capture the strip, "
                        "compare, and put sixteen back. Write the prediction first; the miss is the lesson. Liam, in for Bear."),
     "estimated_duration_s": 32,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on",
              "show": [{"at": "0.02", "event": "composer card; greeting 'Your turn.'"},
                       {"at": "0.1", "event": "the paste-ready prompt types in"},
                       {"at": "0.7", "event": "three output lines: prediction first, capture, revert"}],
              "remotion": {"pattern": "ClaudeComposerAsk", "props": {
                  "greeting": "Your turn.", "topic": TOPIC, "segment": "Lanternfall",
                  "command": YOUR_TURN,
                  "runningText": "reading godot/effects/defeat_sparks.tscn · tests/test_defeat_sparks_config.gd…",
                  "folderLabel": HANDLE, "modelLabel": "Claude", "effortLabel": "High",
                  "output": ["Prediction written before the capture.", "Strip captured: compare with your numbers.",
                             "Then put 16 back."], "animateTyping": True}}}},
    {"beat_id": "B31", "act": "OUTRO",
     "role_note": "OUTRO LAW — ClaudeTitleOutro: exact title, @NikBearBrown, slug-seeded mascot, stock jingle only, no narration.",
     "narration_text": "", "estimated_duration_s": 13.68, "actual_duration_s": 13.68,
     "audio_file": "mp3/beat-B31.wav",
     "audio_note": "stock @NikBearBrown jingle logos/bear-brown/bear-brown-4.mp3, picked by the slug seed the outro uses (char-sum 5505 mod 6 pool files), never cut: padded with 1.0 s of silence; no narration (Liam signs off in B30)",
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "mascot-title",
              "show": [{"at": "0.0", "event": f"title '{TITLE}'"}, {"at": "0.25", "event": "@NikBearBrown"},
                       {"at": "0.45", "event": "slug-seeded mascot"}],
              "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "durationSeconds": 13.68}}}},
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
        if b.get("kind") == "source_report" and (REEL / "media" / f"{b['beat_id']}.mp4").exists():
            b["actual_duration_s"] = round(float(subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                 str(REEL / "media" / f"{b['beat_id']}.mp4")], capture_output=True, text=True).stdout), 3)
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
        "greeting": "Bonjour, Liam",
        "greeting_note": "hello lexicon: Bonjour (French), as in the first particle film. Liam never takes Wagwan (IN-FOR-BEAR LAW).",
        "persona": "Liam (in for Bear)", "presenter": "Liam (in for Bear)", "in_for_bear": True,
        "game": {"repo": "https://github.com/yanxlh/walker-lanternfall-bao-x", "project_dir": "godot",
                 "source_revision": FILM_TREE, "source_revision_kind": "git tree id of godot/",
                 "base_commit": BASE_COMMIT, "godot": "4.7.2.stable.official.ed1daf0bf"},
        "teaching_contract": "code-then-result-v1",
        "note": ("Revised godot-gamedev + walker teardown of Bao Xing's CSYE 7270 particle-effects assignment. Every code "
                 f"panel is a verbatim excerpt of godot/ in the film's source snapshot (godot tree {FILM_TREE}, commit "
                 f"{BASE_COMMIT} plus uncommitted test changes; see FILM-SOURCE.md); every gameplay shot is a real Movie "
                 "Maker capture of an isolated copy of that snapshot, driven through the real input map by the disclosed "
                 "capture driver; fixture strips, profiler screenshots and play-check shots are labelled as such. No paid "
                 "call, no upload."),
        "links": {"repo": "https://github.com/yanxlh/walker-lanternfall-bao-x"},
        "tags": ["Godot 4", "godot-gamedev", "Walker", "CPUParticles2D", "particle shader", "CSYE 7270",
                 "Teardown register", "Kokoro"]},
        "beats": beats}
    path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
    words = sum(len(b["narration_text"].split()) for b in beats)
    est = sum(float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in beats)
    print(f"{path}: {len(beats)} beats, {words} words, ~{est:.0f}s before source reports are measured")


if __name__ == "__main__":
    main()

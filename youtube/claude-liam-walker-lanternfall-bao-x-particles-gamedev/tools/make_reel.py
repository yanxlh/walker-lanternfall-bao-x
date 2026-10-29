#!/usr/bin/env python3
"""Write beat_sheet.json for the Lanternfall particle-effects godot-gamedev (walker) film (Assignment 6).

Code excerpts are read from godot/ at run time by line range, so what the film shows is the file's text. Run it
again after narration is measured: measured durations are kept and every Remotion beat's durationSeconds and
highlight times are re-derived from them (a highlight lands where its phrase sits in the narration).

    python3 tools/make_reel.py
"""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
GAME = REPO / "godot"
FILM_SHA = (REEL / "FILM-SOURCE-REVISION.txt").read_text().strip()
SHORT = FILM_SHA[:7]
SLUG = "claude-liam-walker-lanternfall-bao-x-particles-gamedev"
TITLE = "Lanternfall, Sparked"
PROJECT = "walker-lanternfall-bao-x"
HANDLE = "@NikBearBrown"
TOPIC = "WALKER · GODOT PARTICLES"


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
            "role_note": f"Code beat (code-then-result-v1): {path} lines {a}-{b} at {SHORT}, read verbatim; the next beat shows the result.",
            "narration_text": narration, "estimated_duration_s": est,
            "_cues": cues,
            "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "line-highlight",
                     "show": [{"at": "0.0", "event": f"Godot editor reconstruction opens on {path}, lines {a}-{b}"}] +
                             [{"at": c[0], "event": f"line {c[1]} highlights — {c[2]}"} for c in cues] +
                             [{"at": "notes", "event": "source-notes panel (not Inspector values) lists the related lines"}],
                     "remotion": {"pattern": "GodotDevWorkbench", "props": {
                         "mode": "code", "title": title, "project": PROJECT, "path": f"res://{path}",
                         "source": f"godot/{path} · lines {a}–{b} · source revision {SHORT} · Godot editor reconstruction",
                         "code": excerpt(path, a, b), "startLine": a, "codeFontSize": font or 25,
                         "inspectorLabel": "Source notes — not Inspector values",
                         "notes": [{"label": k, "value": v} for k, v in notes], "output": output,
                         "cues": [], "durationSeconds": est}}},
            "_excerpt": {"path": path, "start_line": a, "end_line": b}}


OBSERVED = {
    "B05": "In the main take every beam hit puts a burst at the monster; the live-burst counter, read from the take's own per-frame log, rises when hits overlap and falls back as bursts finish.",
    "B07": "In the r1 fixture strip the burst is a white cluster on its first visible frame, spreads into yellow-orange sparks by 0.20 s and leaves its last pixel at 0.40 s.",
    "B09": "Side by side, r1's sparks are chunkier from 0.03 to 0.27 s while the footprint and the fade frame match r0; the measured numbers sit beside the prediction.",
    "B11": "Pushing straight into the stall the courier does not move and no embers appear; sliding along its edge the trail runs behind his feet again.",
    "B13": "In the trail fixture, r1's embers are brighter at startup and during steady movement, with the same footprint, and both strips are clear by frame 51.",
    "B15": "On the card screen the celebration bursts on the small courier in the lower-left portrait, above the dark veil, and finishes before the scripted pick.",
    "B17": "Under the PAUSED line the trail's embers stay where they were (paused frames 1143 and 1180 of the main take are pixel-identical) and carry on after resume; the scripted play-check shots show LOST and WON with no particles left.",
    "B19": "Recorded output: seven suites, 292 checks, zero failures; with the displacement guard removed, exactly the two trail checks fail.",
    "B21": "With the same seed and frames, the CPU burst shrinks and fades through yellow to orange, while the editor-converted GPU copy, lacking its ramp and curve textures, stays white and full-size until it vanishes; its sparks stay visible farther out.",
    "B23": "The measured CPU deltas are drawn against their budgets; under the project renderer the GPU reading is zero on every frame, and the Vulkan proxy's deltas stay inside its noise band.",
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
       "must not change. Test every setting, and show me real before-and-after frames for each tuning change.")

YOUR_TURN = ("Please use Walker to read godot/effects/lantern_trail.tscn in my Lanternfall project. Change only "
             "emission_sphere_radius from 3.0 to 8.0. Before running anything, predict how the trail's width and "
             "brightness change at fixture frames 20 and 39, and which configuration check fails. Then capture both "
             "strips, compare them with your prediction, and put 3.0 back.")

BEATS = [
    {"beat_id": "B00", "act": "ASK",
     "role_note": "COLD OPEN LAW — Claude composer; reconstructed Walker prompt from Bao's CHANGE-BRIEF.md (not a recorded session). Liam introduces himself.",
     "narration_text": ("Bonjour — this is Liam, in for Bear. Bao Xing's particle assignment: add two effects to a Godot "
                        "game that already works, tune each one from what you actually see, test it, read the shader "
                        "Godot generates, and price it on the CPU and the GPU. The game is Lanternfall again. Here is the "
                        "ask, rebuilt from Bao's change brief."),
     "estimated_duration_s": 22,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on",
              "show": [{"at": "0.02", "event": "composer card on cream; greeting 'Bonjour, Liam'"},
                       {"at": "0.25", "event": "the reconstructed Walker prompt types in"},
                       {"at": "0.62", "event": "send arms; running line names the brief and the session file"},
                       {"at": "0.75", "event": "three result lines: effects, checks and revision, verdicts"}],
              "remotion": {"pattern": "ClaudeComposerAsk", "props": {
                  "greeting": "Bonjour, Liam", "topic": TOPIC, "segment": "Lanternfall",
                  "command": ASK,
                  "runningText": "reading CHANGE-BRIEF.md · CLAUDE.md · godot/game/session.gd…",
                  "folderLabel": HANDLE, "modelLabel": "Claude", "effortLabel": "High",
                  "output": ["Hit sparks · movement trail · level-up celebration",
                             f"292 automated checks · source revision {SHORT}",
                             "Three tuning changes, each kept by Bao after playing"]}}}},
    {"beat_id": "B01", "act": "BLUF",
     "role_note": "EXECUTIVE-SUMMARY LAW — hesitant writer. The framing a viewer arrives with ('particles are decoration') is corrected to what the film shows ('particles are feedback').",
     "narration_text": ("The short version. These particles are feedback, not decoration. Each one answers a real event "
                        "in the game: a hit, a step, a new level. And none of them is allowed to change a single rule. "
                        "That contract is what the rest of this film checks."),
     "estimated_duration_s": 16, "lead_silence_s": 0.8,
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
     "role_note": "Assignment requirements, as Bao's CHANGE-BRIEF.md records them; the excerpt is the brief's tuning rule, verbatim.",
     "narration_text": ("What the assignment asks for. Two effects that use different particle features. One change to "
                        "each, driven by something observed, with real frames before and after. Tests that read every "
                        "setting back. And a look under the hood: the process shader Godot writes, plus the cost on the "
                        "CPU and the GPU against a budget written down in advance."),
     "estimated_duration_s": 22,
     "_cards": [("Two effects", 0), ("One change to", 1), ("Tests that read", 2), ("process shader", 3)],
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "card-cues",
              "show": [{"at": "0.0", "event": "CHANGE-BRIEF.md 'Tuning and acceptance' excerpt beside four requirement cards"},
                       {"at": "Two effects", "event": "card 1 highlights"},
                       {"at": "One change to", "event": "card 2 highlights"},
                       {"at": "Tests that read", "event": "card 3 highlights"},
                       {"at": "process shader", "event": "card 4 highlights"}],
              "remotion": {"pattern": "GodotDesignBoard", "props": {
                  "title": "What the assignment asks", "section": "CHANGE-BRIEF.md · Tuning and acceptance",
                  "excerpt": ("For each effect, preserve a first strip and record my first running-game observation. "
                              "Make at least one observation-driven revision per effect. Before each edit, record the old "
                              "and new value and predict the visible difference. Change one setting, recapture, compare, "
                              "and keep or revert after actual play."),
                  "source": "CHANGE-BRIEF.md, committed before implementation (8eb16a2) · revisions appended in order",
                  "status": "Effects may read gameplay state but never write it",
                  "visualLabel": "Requirements", "layout": "cards",
                  "cards": [{"label": "1 · Two effects", "text": "A: point burst on every weapon hit. B: sphere-emitted trail while moving."},
                            {"label": "2 · One observed change each", "text": "Prediction, one setting, before/after frames, a verdict after play."},
                            {"label": "3 · Tests read settings back", "text": "Every scene value checked; real input drives the state tests."},
                            {"label": "4 · Shader and cost", "text": "Read the generated process shader; measure CPU and GPU against a budget."}],
                  "cues": [], "durationSeconds": 22}}}},
    listen_beat("B03", [("0.0", "the run under way: beam hits spark, the trail follows the courier"),
                        ("level-up", "a level-up: the celebration on the card-screen portrait, cards held 2 s"),
                        ("card", "card taken, play resumes")],
                "Game sound only, no narration: a stretch of the main take (seed 11) with all three effects."),
    code_beat("B04", "CODE", "effects/particle_presentation.gd", 47, 57, "One burst per hit.",
              ("Effect A starts with a signal. The session's damage function, which every weapon calls, now announces "
               "each hit and where it landed, before any health comes off. This listener answers it. Line forty-nine "
               "drops the hit unless the game is playing and fewer than thirty-two bursts are alive. Then a fresh "
               "burst is placed at the hit, in world space, and restarted."),
              [("Line forty-nine", 49, "PLAYING only · at most 32 live bursts"),
               ("placed at the hit", 53, "global_position = the hit, in world space"),
               ("restarted", 56, "restart(): one-shot burst")],
              [("session.gd line 227", "emits before hp changes"),
               ("Lethal and nonlethal", "both spark"),
               ("_on_hit_finished 72–74", "frees the burst")],
              ["setup() connects weapon_hit · leveled_up · run_started · state.changed (lines 33–36)"], 22),
    media_beat("B05", "RESULT",
               ("Here it is in the running game. Every time the beam connects, a small burst lands on the monster, and "
                "it keeps playing after the monster is gone. The counter is read from the take's own log: when hits come "
                "close together, bursts overlap instead of restarting each other. A stress test with forty hits in one "
                "volley confirms the cap: thirty-two bursts, never more."),
               [("0.0", "real 4K capture, main take: beam hits spark at the monster; crop follows the courier"),
                ("counter", "live-burst counter from the take's per-frame log"),
                ("stress test", "recorded state-test lines: 40 hits seen, 32 bursts, 512 particles")], 20,
               "Result of B04. Real 4K engine capture (main take, seed 11, scripted input); counter from the capture's own track log; cap from evidence/particles_state.json.",
               evidence=True),
    code_beat("B06", "CODE", "effects/defeat_sparks.tscn", 23, 35, "The burst, as data.",
              ("The burst itself is data in a scene file, not code. Sixteen sparks, all released on the same frame, "
               "because explosiveness is one. They live forty-five hundredths of a second. They start from a single "
               "point and fly in any direction, with spread at one-eighty. Speed is twenty-five to fifty-five, damping "
               "slows them, and a little gravity pulls them down."),
              [("explosiveness is one", 26, "explosiveness = 1.0: one frame"),
               ("forty-five hundredths", 23, "lifetime = 0.45 s"),
               ("single", 28, "emission_shape = 0: point"),
               ("spread at one-eighty", 30, "spread = 180°"),
               ("damping", 34, "damping 20–30")],
              [("Line 21", "amount = 16"),
               ("Brief, visual intent", "compact → spread → gone"),
               ("Size limit", "≤ 2 character heights")],
              ["no fixed seed in play (config test) · file name kept from the first design; it now serves every hit"], 24, font=24),
    media_beat("B07", "RESULT",
               ("What those numbers make, frame by frame, from a real fixture capture on the market floor. On its first "
                "visible frame the burst is a compact white cluster. By a fifth of a second it has spread into separate "
                "yellow-orange sparks. At its widest it reaches sixty-four pixels, under the two-character limit of "
                "sixty-eight, and the last pixel goes out at four tenths of a second."),
               [("0.0", "r1 fixture strip, files 9–21, magnified 3×; courier on the left for scale"),
                ("first", "file 9: 14 × 14 px cluster"), ("a fifth", "file 15: 45 × 43 px, separate sparks"),
                ("widest", "64 px of a 68 px limit"), ("last pixel", "file 21: last trace; file 22 empty")], 22,
               "Result of B06. Real windowed fixture capture (captures/defeat_sparks/r1), 30 fps, seed 7280; measurements from COMPARISON.md.",
               evidence=True),
    code_beat("B08", "CODE", "effects/defeat_sparks.tscn", 36, 39, "The one change.",
              ("Now the tuning. In the game, Bao saw no problem. The frame strip disagreed with the brief: on its first "
               "frame, the cluster was a third of a character high, not about one. So one value changed, on line "
               "thirty-seven: the largest spark scale, from one point two to one point eight. Nothing else moved."),
              [("the largest spark scale", 37, "scale_amount_max 1.2 → 1.8"),
               ("Nothing else moved", 36, "scale_amount_min 0.7, curve and ramp unchanged")],
              [("Bao, in play", "“完成 没什么问题”"),
               ("r0, first frame", "11 × 12 px: 0.35 height"),
               ("Prediction", "≈ 15 × 15 px; +3–4 px wide")],
              ["approved (“同意”) · config test edited and failing first, then the scene · CHANGE-BRIEF.md r1"], 20),
    media_beat("B09", "RESULT",
               ("Before on top, after below, same seed, same frames. The first frame grew from eleven to fourteen pixels, "
                "close to the predicted fifteen. The sparks got chunkier, with up to eighty-five percent more lit area. "
                "But the footprint widened by one pixel, not the predicted three or four, because positions set the "
                "spread. Fade timing didn't change. Bao played it and kept it: clearer."),
               [("0.0", "r0 (top) vs r1 (bottom) contact sheet, 3× crops"),
                ("predicted fifteen", "prediction vs measured table, row by row"),
                ("one pixel", "the miss marked: predicted +3–4 px, measured +1 px"),
                ("kept it", "Bao's verdict: 保留 更清晰了")], 24,
               "Result of B08. Real fixture captures r0 and r1 (captures/defeat_sparks/), comparison and hashes from COMPARISON.md and manifest.json; verdict from TUNING.md.",
               evidence=True),
    code_beat("B10", "CODE", "effects/particle_presentation.gd", 121, 131, "A trail that needs real movement.",
              ("Effect B, the trail, is decided once per physics frame. Line one twenty-six measures how far the "
               "courier actually moved since the last frame. Holding a key isn't enough. Line one twenty-seven sets a "
               "jump limit, twice a frame's walk plus four pixels, so a teleport or a restart never draws a streak. "
               "Line one twenty-nine emits only while playing, visible, and genuinely moving."),
              [("Line one twenty-six", 126, "distance actually moved"),
               ("Line one twenty-seven", 127, "jump limit = speed × Δt × 2 + 4 ≈ 7 px"),
               ("Line one twenty-nine", 129, "PLAYING · visible · 0.01 < distance ≤ limit")],
              [("Line 128", "trail at the feet: (0, 7)"),
               ("local_coords = false", "embers stay put"),
               ("Restart 88–97", "history reset")],
              ["reads session.player and session.state; writes only the trail"], 22),
    media_beat("B11", "RESULT",
               ("The proof is a wall. The script walks the courier up to a stall and holds right. The key is down, but "
                "he can't move, so no embers. Then it holds down and right: he slides along the edge, and the trail is "
                "back behind his feet. The line under the footage is the trail's emitting flag, read from the take's own "
                "per-frame log."),
               [("0.0", "real 4K capture, props take: walking to the nearest stall"),
                ("holds right", "pushing into the stall: no displacement, no embers"),
                ("slides", "down-right: sliding along the edge, trail back"),
                ("emitting flag", "per-frame strip: trail emitting yes / no, from the take's log")], 20,
               "Result of B10. Real 4K engine capture (props take, seed 11, scripted input through the real input map); emitting flag from the capture's track log.",
               evidence=True),
    code_beat("B12", "CODE", "effects/lantern_trail.tscn", 17, 29, "The trail's own features.",
              ("The trail's scene shows what makes it a different effect. It emits continuously from a sphere three "
               "pixels wide, emission shape one, where the burst used a point. Twenty-four embers drift slightly "
               "upward and fade from amber to dark orange in a third of a second. Its tuning change lives on line "
               "fourteen: the alpha at the start and the middle of each ember's life."),
              [("sphere three", 29, "emission_sphere_radius = 3.0"),
               ("emission shape one", 28, "emission_shape = 1: sphere (A uses 0: point)"),
               ("Twenty-four embers", 21, "amount = 24 · continuous (one_shot = false)")],
              [("Line 14, the change", "alpha 0.95 / 0.70 / 0"),
               ("Before (r0)", "alpha 0.55 / 0.30 / 0"),
               ("Bao's first look", "“移动也不明显”")],
              ["lifetime 0.35 s (line 23) · spread 25° upward (lines 30–31) · brief: dimmer and smaller than A"], 24, font=23),
    media_beat("B13", "RESULT",
               ("Bao's first look at the integrated game: the trail wasn't obvious. Raising only those two alpha values "
                "gave brighter embers at startup and in steady movement, with the same footprint, and both versions "
                "clear by the same frame after stopping. Bao played it and kept it. In normal play, the trail stays two "
                "to four pixels per ember, still smaller and dimmer than a hit spark."),
               [("0.0", "trail fixture r0 (top) vs r1 (bottom), frames 10–60, crops"),
                ("same footprint", "frames 20 and 39 marked"), ("same frame", "frames 51 and 60: both clear"),
                ("smaller and dimmer", "play-check crop: trail flecks beside a hit spark")], 22,
               "Result of B12. Real fixture captures (captures/lantern_trail/comparison-20261029-135607), the original re-rendered from its preserved resource; play-check shot from captures/play-checks/20261029-142138.",
               evidence=True),
    code_beat("B14", "CODE", "effects/particle_presentation.gd", 59, 70, "The celebration, on the card screen.",
              ("The extra effect: a gold celebration on every level-up. Its first version was drawn in the world, under "
               "the upgrade screen's dark veil, and Bao found it hard to see. Now it goes into its own overlay layer, eleven, "
               "above the HUD, and line sixty-six anchors it to the little courier portrait on the card screen. At "
               "most four can be alive at once."),
              [("level-up", 59, "leveled_up(level) signal"),
               ("its own overlay layer", 65, "level_overlay: CanvasLayer 11, above HUD layer 10"),
               ("line sixty-six", 66, "position = the card-screen portrait"),
               ("At most four", 61, "PLAYING only · ≤ 4 live celebrations")],
              [("Anchor", "HUD-local (56, 325)"),
               ("Bao's request", "on the small character"),
               ("Scene", "32 particles · 0.7 s")],
              ["_apply_policy keeps it playing during LEVELUP (lines 114–116)"], 22),
    media_beat("B15", "RESULT",
               ("In the real take, the level-up arrives and the card screen opens. The burst lands on the small courier "
                "in the lower-left portrait, white first, then gold, and it's gone well before the scripted pick two "
                "seconds later. The cards stay readable. Bao looked at exactly this placement and said: that works."),
               [("0.0", "real 4K capture, main take: level-up, card screen opens"),
                ("lower-left portrait", "crop of the portrait: white → gold → gone"),
                ("that works", "Bao's verdict: 可以的")], 18,
               "Result of B14. Real 4K engine capture (main take, seed 11); verdict from TUNING.md.", evidence=True),
    code_beat("B16", "CODE", "effects/particle_presentation.gd", 110, 119, "Freeze, don't fake.",
              ("One policy runs every frame, and it only reads the game. When the game isn't playing, hit bursts and "
               "the trail get a speed scale of zero, so they freeze exactly where they are. The celebration keeps "
               "playing on the card screen, so it doesn't stall on its first frame. And outside play, the trail "
               "never spawns. On a loss or a win, everything is cleared."),
              [("speed scale of zero", 113, "hit bursts: speed_scale 0 outside PLAYING"),
               ("keeps", 116, "celebration: runs in PLAYING and LEVELUP"),
               ("never spawns", 118, "trail.emitting = false outside play")],
              [("_apply_policy() 107", "runs every physics frame"),
               ("_on_state_changed 99–105", "WON · LOST · MENU: clear"),
               ("Line 117", "trail frozen with the game")],
              ["no line in this file writes session state"], 20),
    media_beat("B17", "RESULT",
               ("At thirty seconds the script presses pause. Under the pause screen, the trail's embers hang exactly "
                "where they were: two frames a second apart match pixel for pixel. Then play resumes and they carry on. "
                "The scripted play checks cover the endings: on the first frame of a loss or a win, every particle is "
                "gone. And after a normal run of their own, Bao's note was that nothing got in the way."),
               [("0.0", "real 4K capture, main take: pause at run 0:30, held 2.5 s"),
                ("pixel for pixel", "two paused frames a second apart, side by side: 0 pixels differ"),
                ("play resumes", "resume: the trail carries on"),
                ("endings", "play-check shots: lost+00 and won+00, particles cleared (scripted, 1280 × 720)"),
                ("nothing got in the way", "Bao's verdict: 没有挡住都正常")], 20,
               "Result of B16. Real 4K engine capture (main take) plus labelled scripted play-check shots (captures/play-checks/20261029-142138); verdict from PLAY-CHECKS.md.",
               evidence=True),
    code_beat("B18", "CODE", "tests/test_particles_edges.gd", 57, 69, "Testing what the eye can't.",
              ("Tests catch what a glance misses. This edge test puts the courier against a stall, holds the right key "
               "for thirty frames through the real input system, and counts two things: how far he moved, and how many "
               "frames the trail emitted. Both must be zero. A configuration test, separately, reads every value in "
               "every effect scene back from the engine."),
              [("puts the courier against a stall", 57, "fixture: courier touching the stall's left edge"),
               ("holds the right key", 60, "real key event: D"),
               ("Both must be zero", 69, "blocked-push-never-emits")],
              [("Particle suites", "39 + 79 + 34 + 18 checks"),
               ("Godot 3 name", "loads silently; test fails"),
               ("Limit", "can't judge the look")],
              ["evidence/particles_edges.json"], 22, font=23),
    media_beat("B19", "RESULT",
               ("Recorded output from the committed build: seven suites, two hundred ninety-two checks, no failures, "
                "with the original game's tests unchanged. Then the experiment that shows the test is real: delete the "
                "movement guard, and exactly two trail checks fail. And an old Godot 3 property name loads without a "
                "warning; the burst just spreads a little tighter. Only the test noticed."),
               [("0.0", "recorded suite totals, final pre-commit run"),
                ("delete the movement guard", "mutation output: blocked-push-never-emits (30 frames), jump-frame-no-emission"),
                ("Godot 3 property name", "mutation frames: r1 vs initial_velocity, 45 × 43 → 40 × 42 px")], 22,
               "Result of B18. Recorded tool output (evidence/assignment-6/final-precommit, evidence/assignment-6/mutations) and the windowed mutation capture (captures/defeat_sparks/mutation-godot3-name).",
               evidence=True),
    code_beat("B20", "CODE", "shaders/particles_generated.gdshader", 340, 352, "The shader Godot writes.",
              ("Under the hood. Godot turned a GPU copy of the burst into this generated process shader. Every frame, "
               "for every spark, it adds up the velocity, moves the spark, and then samples the colour ramp and the "
               "scale curve by the spark's age, on line three forty-seven. In Bao's words, this is the process stage: "
               "how a particle changes. Drawing it is a separate stage."),
              [("moves the spark", 345, "TRANSFORM[3].xyz += final_velocity × DELTA"),
               ("line three forty-seven", 347, "process_display_param: colour ramp + scale curve at age"),
               ("separate stage", 352, "COLOR handed to the draw stage")],
              [("start() 225–275", "spawn: colour, velocity"),
               ("Lines 311–337", "gravity, then damping"),
               ("Draw stage", "spark.png · additive")],
              ["converted in the Godot 4.7.2 editor · study scene only, the game never loads it"], 22),
    media_beat("B21", "RESULT",
               ("And here's what that shader does with the material the editor produced, same seed, same frames. On "
                "the left, the game's CPU burst shrinks and fades through yellow to orange. On the right, the GPU copy "
                "stays white and full-size until it vanishes: the conversion left the ramp and curve textures off, so "
                "line three forty-seven has nothing to sample. The sparks still fly out; the colour fade and the shrink "
                "are gone."),
               [("0.0", "real 4K fixture capture: CPU burst (left) vs editor-converted GPU copy (right)"),
                ("shrinks and fades", "left: yellow → orange, shrinking"),
                ("stays white", "right: white, full-size"),
                ("nothing to sample", "callout: ShaderMaterial has no color_ramp / scale_curve")], 22,
               "Result of B20. Real 4K fixture capture of the isolated copy (capture/study_capture.gd): the game's scene and the study scene, same seed 7280.",
               evidence=True),
    code_beat("B22", "CODE", "tests/cost_effects.gd", 58, 63, "Pricing it: on versus off.",
              ("Last, the price. The cost script builds the same game twice for every condition. Line sixty-one is the "
               "switch: with effects off, the whole presentation node is freed before the run starts, so gameplay, "
               "enemies and input stay identical. Then it times five interleaved trials of three hundred frames, idle, "
               "at the burst cap, moving, and on the card screen."),
              [("same game twice", 58, "a fresh Session for each condition"),
               ("Line sixty-one", 61, "effects off: game.particles.free()"),
               ("identical", 63, "same fixture via run_started")],
              [("CPU", "headless wall time"),
               ("GPU", "measured, windowed"),
               ("Budgets (ms)", "A 1.0 / 0.75 · B 0.25")],
              ["evidence/assignment-6/cost/COST-REPORT.md"], 22),
    media_beat("B23", "RESULT",
               ("The measured price. On the CPU, thirty-two live bursts add about nine thousandths of a millisecond a "
                "frame, a tenth at the spawn spike, and the trail four thousandths, all far under budget. The GPU number "
                "is the honest part: under the game's renderer, this Mac reports zero on every frame. A Vulkan proxy can "
                "measure it, and the difference stays inside the noise."),
               [("0.0", "CPU deltas as bars against their budgets (headless, 5 trials)"),
                ("spawn spike", "A spawn p95 ≈ +0.10 ms"),
                ("zero on every frame", "GPU under GL Compatibility: 0.000 ms, every frame"),
                ("Vulkan proxy", "Mobile/Vulkan proxy deltas within ±0.1 ms, labelled proxy")], 22,
               "Result of B22. Recorded measurements (evidence/assignment-6/cost/*.json) drawn as bars; nothing estimated.",
               evidence=True),
    {"beat_id": "B24", "act": "VERDICT",
     "role_note": "ClaudeVerdictArtifact — implemented work, limitations, human judgment; shows the source revision.",
     "narration_text": ("The verdict. Implemented: three effects that answer real events and never write game state, "
                        "with two hundred ninety-two checks behind them. Each tuning change has a prediction, real frames "
                        "and a verdict, including the part of the prediction that missed. The limits are written down: "
                        "no readable GPU time on this renderer, and a first frame still under one character high. The "
                        "keep-or-revert calls were Bao's."),
     "estimated_duration_s": 24,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "artifact-reveal",
              "show": [{"at": "0.0", "event": "artifact card 'Verdict', heading with the source revision"},
                       {"at": "0.2", "event": "implemented line"}, {"at": "0.45", "event": "tuning-evidence line"},
                       {"at": "0.65", "event": "limits line"}, {"at": "0.85", "event": "human-judgment line"}],
              "remotion": {"pattern": "ClaudeVerdictArtifact", "props": {
                  "artifactTitle": "Verdict", "artifactHeading": f"Lanternfall particles · source revision {SHORT}",
                  "brandLabel": HANDLE,
                  "artifactLines": ["Implemented: hit sparks, trail, celebration; game state never written; 292 checks.",
                                    "Each tuning change: prediction, real before/after frames, a verdict, misses kept.",
                                    "Limits: no GPU time on this renderer; first frame still under one height.",
                                    "Human judgment: every keep-or-revert call was Bao's, after playing."]}}}},
    {"beat_id": "B25", "act": "HANDOFF",
     "role_note": "HANDOFF LAW — Your Turn: one bounded change plus a prediction and a capture. Liam reads the prompt and signs off.",
     "narration_text": ("Your turn. Paste this: Please use Walker to read the trail scene in my Lanternfall project. "
                        "Change only the emission sphere radius from three to eight. Before running anything, predict how "
                        "the trail's width and brightness change at fixture frames twenty and thirty-nine, and which "
                        "configuration check fails. Then capture both strips, compare, and put three back. Write the "
                        "prediction first; the miss is the lesson. Liam, in for Bear."),
     "estimated_duration_s": 32,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on",
              "show": [{"at": "0.02", "event": "composer card; greeting 'Your turn.'"},
                       {"at": "0.1", "event": "the paste-ready prompt types in"},
                       {"at": "0.7", "event": "three output lines: prediction first, capture, revert"}],
              "remotion": {"pattern": "ClaudeComposerAsk", "props": {
                  "greeting": "Your turn.", "topic": TOPIC, "segment": "Lanternfall",
                  "command": YOUR_TURN,
                  "runningText": "reading godot/effects/lantern_trail.tscn · tests/test_extra_particles_config.gd…",
                  "folderLabel": HANDLE, "modelLabel": "Claude", "effortLabel": "High",
                  "output": ["Prediction written before the capture.", "Two strips captured: compare with your numbers.",
                             "Then put 3.0 back."], "animateTyping": True}}}},
    {"beat_id": "B26", "act": "OUTRO",
     "role_note": "OUTRO LAW — ClaudeTitleOutro: exact title, @NikBearBrown, slug-seeded mascot, stock jingle only, no narration.",
     "narration_text": "", "estimated_duration_s": 13.68, "actual_duration_s": 13.68,
     "audio_file": "mp3/beat-B26.wav",
     "audio_note": "stock @NikBearBrown jingle logos/bear-brown/bear-brown-4.mp3, picked by the slug seed the outro uses (char-sum 5295 mod 6 pool files), never cut: padded with 1.0 s of silence; no narration (Liam signs off in B25)",
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
            import subprocess
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
        "greeting_note": "hello lexicon: Bonjour (French); the Assignment 2 film used Merhaba. Liam never takes Wagwan (IN-FOR-BEAR LAW).",
        "persona": "Liam (in for Bear)", "presenter": "Liam (in for Bear)", "in_for_bear": True,
        "game": {"repo": "https://github.com/yanxlh/walker-lanternfall-bao-x", "project_dir": "godot",
                 "source_revision": FILM_SHA, "godot": "4.7.2.stable.official.ed1daf0bf"},
        "teaching_contract": "code-then-result-v1",
        "note": ("godot-gamedev + walker teardown of Bao Xing's CSYE 7270 particle-effects assignment. Every code panel is "
                 f"a verbatim excerpt of godot/ at {FILM_SHA}; every gameplay shot is a real Movie Maker capture of an "
                 "isolated copy of that revision, driven through the real input map by the disclosed capture driver; "
                 "fixture strips and play-check shots are labelled as such. No paid call, no upload."),
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

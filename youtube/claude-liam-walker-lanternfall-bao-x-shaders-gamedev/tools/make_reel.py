#!/usr/bin/env python3
"""Write beat_sheet.json for the Lanternfall shader godot-gamedev (walker) film (Assignment 5).

Code excerpts are read from git at the film's source revision (tools/src.py), never from the working tree, so what
the film shows is the committed file's text. Run it again after narration is measured: measured durations are kept
and every Remotion beat's durationSeconds and highlight times are re-derived from them (a highlight lands where its
phrase sits in the narration).

    python3 tools/make_reel.py
"""
import json, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from src import SHA as FILM_SHA, excerpt, repo_text  # noqa: E402

REEL = Path(__file__).resolve().parents[1]
SHORT = FILM_SHA[:7]
SLUG = "claude-liam-walker-lanternfall-bao-x-shaders-gamedev"
TITLE = "Lanternfall, Shaded"
PROJECT = "walker-lanternfall-bao-x"
HANDLE = "@NikBearBrown"
TOPIC = "WALKER · GODOT SHADERS"


def at(text: str, phrase: str, dur: float, lead: float = 0.25) -> float:
    """Seconds into the beat where `phrase` is spoken, by its position in the narration."""
    i = text.find(phrase)
    if i < 0:
        raise SystemExit(f"cue phrase not in narration: {phrase!r}")
    return round(max(0.0, dur * i / max(1, len(text)) - lead), 2)


def code_beat(bid, act, path, a, b, title, narration, cues, notes, output, est, font=None):
    return {"beat_id": bid, "act": act, "kind": "code",
            "role_note": f"Code beat (code-then-result-v1): godot/{path} lines {a}-{b} at {SHORT}, read verbatim; the next beat shows the result.",
            "narration_text": narration, "estimated_duration_s": est,
            "_cues": cues,
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
    "B06": "At hurt_amount 0 the lamp and coat texels read their stored colours; at 0.5 each channel lands within one byte of the hand table (lamp 249, 220, 37 against 248.5, 219.5, 37.5); the red phase keeps more red at 0.5; at 1 both phases are (255, 255, 0); 2.0 set from code reads back as 2.0 and renders the same yellow as 1.0.",
    "B08": "In the real game loop the courier turns yellow on the frame after each accepted hit, holds at 23/48 for the 45 paused frames, resumes, and reaches 0 after 48 ticks; a monster touching him during the third window (frames 1661-1666) changes neither hp nor the falling curve.",
    "B10": "The floor shows repeated warm paving of square stones and the stand-in capsule the same stones, larger and cooler, under the A3 room's lights from the fixed capture pose.",
    "B12": "Changing only the floor material's uv_scale from 2 to 4 makes the floor's stones smaller and changes its rectangle by up to 72 levels; the stand-in rectangle changes by 0.",
    "B14": "After Bao's one-line ALBEDO * 0.5 edit every pixel of both the floor and the stand-in rectangles changed and both darkened, as his prediction said; the agent-run green study is shown separately and labelled.",
    "B16": "The colour, normal and roughness files look like three different kinds of image; the normal map's curl ratio is 0.2236 in the OpenGL convention and 1.7764 in DirectX (the DX calibration map mirrors it); normal_strength 0 against 1 on the floor changes the shading of the stone joints.",
    "B18": "Each of the five uniforms changes the floor rectangle at its low and high value, while the stand-in rectangle stays at (31.42, 40.97, 74.83) through all fifteen captures; Bao's recorded look at the normal_strength row is quoted beside its three captures.",
    "B20": "Both quads show the grey bands at 64, 128 and 192, the Compatibility prediction; the Forward+/Mobile prediction (137, 188, 225 without the hint) is shown as a prediction only.",
    "B22": "The verbatim line pairs sit side by side; in the fixture, the editor-generated material and Bao's shader with neutral values draw the same stones, with 87-93 % of pixels within 2 levels face-on and a larger difference (mean about 2.4-2.8 levels) with the camera tilted 50 degrees.",
    "B25": "Recorded output: 28/28 at 30, 60 and 144 fps, 127/127 material checks and the ten earlier suites at 332/0 on a fresh copy of the film revision; the three mutation logs fail 4, 3 and 1 checks.",
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
    return {"beat_id": bid, "act": "LISTEN", "kind": "source_report", "clock": "source", "audio_policy": "preserve",
            "role_note": role, "narration_text": "",
            "shot": {"type": "SOURCE_REPORT", "class": "SHOW", "source": "own", "motion": "real-footage",
                     "show": [{"at": s[0], "event": s[1]} for s in show], "treatment": "none"}}


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
    return "\n".join(repo_text("CHANGE-BRIEF.md").splitlines()[a - 1:b])


ASK = ("Please use Walker to convert my game design document about Lanternfall, a lamp-headed courier surviving three "
       "minutes in a fog-bound night market, into two Godot 4 shaders: a yellow tint that shows his 48-tick protection "
       "after a hit, and a textured cobblestone material for the 3D room. Gameplay must not change. Predict every "
       "colour by hand first, then measure it in the engine.")

YOUR_TURN = ("Please use Walker to read godot/a5/materials/cobblestone_cool_standin.tres in my Lanternfall project. "
             "Change only uv_scale from 1.0 to 3.0. Before running anything, predict which rectangle of the pair "
             "capture changes, how the stand-in's stones change, and which check in test_materials.gd fails. Then "
             "capture the pair, compare it with your prediction, and put 1.0 back.")

BRIEF_STATE = brief_lines(21, 21)
BRIEF_COLOUR = "\n".join(l for l in brief_lines(34, 40).splitlines() if not l.startswith("```"))

BEATS = [
    {"beat_id": "B00", "act": "ASK",
     "role_note": "COLD OPEN LAW — Claude composer; reconstructed Walker prompt from Bao's CHANGE-BRIEF.md (not a recorded session). Liam introduces himself.",
     "narration_text": ("Ciao, this is Liam, in for Bear. Bao Xing's shader assignment for Lanternfall: write a shader "
                        "from code that shows a game state, give a 3D object a textured shader, and answer four "
                        "questions about shaders, materials, textures and Godot's shading language, each one pointing "
                        "at a line of Bao's own code. Here's the ask, rebuilt from Bao's change brief."),
     "estimated_duration_s": 22,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on",
              "show": [{"at": "0.02", "event": "composer card on cream; greeting 'Ciao, Liam'"},
                       {"at": "0.25", "event": "the reconstructed Walker prompt types in"},
                       {"at": "0.62", "event": "send arms; running line names the brief and the shader files"},
                       {"at": "0.75", "event": "three result lines: the tint, the material, checks and revision"}],
              "remotion": {"pattern": "ClaudeComposerAsk", "props": {
                  "greeting": "Ciao, Liam", "topic": TOPIC, "segment": "Lanternfall",
                  "command": ASK,
                  "runningText": "reading CHANGE-BRIEF.md · CLAUDE.md · godot/features/player/player.gd…",
                  "folderLabel": HANDLE, "modelLabel": "Claude", "effortLabel": "High",
                  "output": ["Hurt tint: one canvas_item colour line, driven by player.iframes",
                             "Cobblestone: one spatial shader, two materials, Floor and StandIn",
                             f"28 + 127 new checks · 332 earlier unchanged · source revision {SHORT}"]}}}},
    {"beat_id": "B01", "act": "BLUF",
     "role_note": "EXECUTIVE-SUMMARY LAW — hesitant writer. The framing a viewer arrives with ('shaders are magic') is corrected to what the film shows ('shaders are arithmetic').",
     "narration_text": ("The short version. Shaders aren't magic, they're arithmetic. Here, one line of code, one number "
                        "from the game and one texture hint decide what you see. Each was predicted by hand, then "
                        "measured in the engine."),
     "estimated_duration_s": 14, "lead_silence_s": 0.8,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on-correct",
              "show": [{"at": "0.0", "event": "cream page; 'Shaders are magic' types"},
                       {"at": "0.3", "event": "'magic' struck in terracotta, 'arithmetic' typed in"},
                       {"at": "0.6", "event": "'a line, a number, a hint' and 'predicted, then measured' type in"}],
              "remotion": {"pattern": "BrutalistHesitantWriter", "props": {
                  "text": "Shaders are magic\na line, a number, a hint\npredicted, then measured",
                  "triggerWords": "magic", "replacementWords": "arithmetic", "fontSize": 164, "lineSpacing": 1.6,
                  "align": "center", "seed": str(sum(map(ord, SLUG))), "mistakeRate": 2, "hesitateWithin": 0,
                  "hesitateBetween": 1, "ink": "#3D3929", "accent": "#D97757", "bg": "#FAF9F5"}}}},
    board("B02", "ASSIGNMENT", "What the assignment asks", "CHANGE-BRIEF.md · State and purpose", BRIEF_STATE,
          f"CHANGE-BRIEF.md line 21, verbatim, at {SHORT} · the assignment's four parts, as the brief and README answer them",
          "Presentation only: the driver reads state and iframes, never writes them",
          "The assignment, and where this game answers it",
          [("1 · A shader from code", "hurt_tint.gdshader on the courier: yellow after an accepted hit, fading over his 48 ticks of protection"),
           ("2 · A textured shader in 3D", "cobblestone_surface.gdshader on Floor and StandIn in a5/material_room.tscn, which inherits the A3 room"),
           ("3 · Four questions", "What a shader does · material vs shader · why a texture is information · what Godot's shading language is"),
           ("4 · Tests, and their limits", "Real game loop at 30, 60, 144 fps; mutations; what no headless run can show")],
          ["A shader from code", "A textured shader", "Four questions", "And tests"],
          ("What the assignment asks for, and how Bao answered it. A shader from code that communicates a state: here, "
           "the courier turns yellow after an accepted hit and fades back as his forty-eight ticks of protection run "
           "out. A textured shader on a 3D object: the floor and the stand-in of the Assignment 3 room. Four questions, "
           "each answered at a line of code. And tests, with an honest list of what they can't show."),
          24, "Assignment requirements as Bao's brief and README answer them; the excerpt is the brief's state-and-purpose line, verbatim."),
    listen_beat("B03", [("0.0", "the run under way at 0:37: the courier walks toward the nearest monster"),
                        ("level-up", "a level-up card screen, held 2 s by the script, then a card is picked"),
                        ("hit", "a moth reaches him: the hurt sound, the courier yellow, the yellow fading")],
                "Game sound only, no narration: frames 1240-1419 of the hurt take (seed 5), real speed."),
    board("B04", "PREDICT", "Predicted by hand, before the code", "CHANGE-BRIEF.md · 2D shader design", BRIEF_COLOUR,
          f"CHANGE-BRIEF.md lines 34–40 (code fence omitted) and the Hand calculations table, at {SHORT}",
          "The hand table the engine has to hit (RGB, 0–255)", "Bao's hand calculations, idle frame, no lights",
          [("Lamp head, stored (242, 184, 75)", "a = 0.5 → (248.5, 219.5, 37.5) · a = 1 → (255, 255, 0)"),
           ("Coat, stored (46, 58, 89)", "a = 0.5 → (150.5, 156.5, 44.5) · a = 1 → (255, 255, 0)"),
           ("Red blink phase (×1, 0.45, 0.45 first)", "lamp at 0.5 → (248.5, 168.9, 16.875); at 1 both phases (255, 255, 0)"),
           ("hint_range and 2.0", "brief answer 7: not clamped from code; 2.0 extrapolates past yellow")],
          ["the lamp head", "the coat", "red blink", "two point oh"],
          ("Before any code ran, Bao's brief fixed the colour line and worked out the answers by hand. The line mixes "
           "the incoming colour toward yellow by hurt amount: at zero the drawing passes through, at one it's yellow. "
           "Halfway, the lamp head should land at two forty-eight point five, two nineteen point five, thirty-seven "
           "point five, and the coat at one fifty point five, one fifty-six point five, forty-four point five. In the red blink the same mix keeps more red. And two point "
           "oh, set from code, should not be clamped."),
          26, "The brief's exact colour line and equation, verbatim; the cards restate the brief's Hand calculations table and short answer 7."),
    code_beat("B05", "CODE", "shaders/hurt_tint.gdshader", 1, 9, "Nine lines, one colour line.",
              ("Here's Bao's hand-written shader, all nine lines. Line one makes it a canvas item shader, for 2D sprites. "
               "Line four declares hurt amount, the one number the game sends in; its hint range only shapes the "
               "Inspector slider. Then fragment, on line seven, runs for every pixel the courier covers, and line eight "
               "is the whole effect: the incoming colour, mixed toward yellow. That's what a shader does: a small "
               "function, run for every pixel."),
              [("Line one", 1, "shader_type canvas_item: the 2D pipeline"),
               ("Line four", 4, "hurt_amount: the game's one number in"),
               ("on line seven", 7, "fragment(): runs per rasterized fragment"),
               ("line eight", 8, "mix(incoming COLOR, yellow, hurt_amount)")],
              [("LANGUAGE-NOTES Q2 · Bao", "fragment() processes rasterized fragments"),
               ("Line 5", "hurt_color : source_color = yellow"),
               ("Incoming COLOR", "texture × modulate, so the red blink survives")],
              ["render_mode unshaded (line 2) · no TIME and no texture() call: every change comes from hurt_amount"], 26, font=28),
    media_beat("B06", "RESULT",
               ("Now the engine's answer, from in-engine captures with the simulation frozen and the value set by a "
                "debug key. At zero, the lamp and the coat match their stored colours exactly. At one half, the lamp "
                "reads two forty-nine, two twenty, thirty-seven: inside one byte of the hand table. In the red phase the "
                "same line keeps more red, and at one both phases are the same yellow. And two point oh, set from code, "
                "reads back as two point oh. The hint didn't clamp it; the output just saturates."),
               [("0.0", "white phase: courier crops at hurt_amount 0 / 0.5 / 1, sampled texels ringed"),
                ("At one half", "predicted vs measured table, lamp and coat"),
                ("red phase", "red-phase crops at 0 / 0.5 / 1 (iframes 27)"),
                ("two point oh", "the 2.0 capture: read back 2.0, both texels (255, 255, 0)")], 30,
               "Result of B05. In-engine captures captures/hurt-tint/20261030-125036 and 20261030-125259-red (scripted debug key, simulation frozen: a fixture, not play); predictions from CHANGE-BRIEF.md.",
               evidence=True),
    code_beat("B07", "CODE", "effects/hurt_tint_presentation.gd", 18, 30, "The game's number, every frame.",
              ("The driver connects the game to that uniform. Every frame, line twenty-two calls refresh. Line "
               "twenty-six turns the courier's remaining invulnerability ticks into a fraction: forty-eight ticks is "
               "one, zero is zero, clamped. Outside playing, paused or the level-up screen, it's forced to zero, so a "
               "lethal hit can't leave him yellow. And line thirty sets the shader parameter. The driver only reads the "
               "game; it never writes it."),
              [("line twenty-two", 22, "_process: refresh every frame"),
               ("twenty-six", 26, "iframes / 48, clamped to 0..1"),
               ("forced to zero", 27, "MENU, WON, LOST: 0.0"),
               ("line thirty", 30, "set_shader_parameter(\"hurt_amount\", …)")],
              [("Lines 15–17", "one material per courier, Shader shared"),
               ("player.gd line 98", "accepted hit: iframes = 48"),
               ("Line 18", "state change: refresh before next draw")],
              ["session.gd 91–93 adds the driver · process_priority 200 (line 13) · nothing here writes game state"], 26, font=23),
    media_beat("B08", "RESULT",
               ("Now the running game, with scripted input through the real input map. A monster connects, and the "
                "courier is yellow at once. The script presses pause, and the tint holds at twenty-three forty-eighths, "
                "because the counter stops with the simulation. Resume, and it drains. On the next hit a monster keeps "
                "touching him while he's protected, and nothing restarts. Frame by frame: one to zero in forty-eight "
                "ticks, eight tenths of a second, with the red blink still showing through."),
               [("0.0", "real 4K capture, hurt take (seed 5): hit 2 at run 0:41.9, the courier yellow"),
                ("presses pause", "PAUSED: hurt_amount held at 0.4792 for 45 frames, readout from the take's log"),
                ("next hit", "hit 3: a monster keeps touching him (frames 1661–1666), hp stays 7"),
                ("Frame by frame", "held frames of hit 3, labelled, from 1.0 to 0.0"),
                ("red blink", "readout: blink on/off beside the tint")], 28,
               "Result of B07. Real 4K engine capture of the isolated copy (capture/take-hurt-seed5.avi, scripted input through the real input map); readout and curve from the take's own per-frame log.",
               evidence=True),
    code_beat("B09", "CODE", "a5/material_room.tscn", 7, 18, "The 3D object: inherit, then override.",
              ("The textured shader goes on a 3D object. Bao's Assignment 5 room doesn't copy the Assignment 3 room: "
               "line ten instances it, and only a few things change. The floor's mesh becomes an eight by eight metre "
               "plane, line fourteen gives the floor the warm cobblestone material, and line eighteen gives the stand-in "
               "the cool one. The A3 room file itself stays untouched."),
              [("line ten", 10, "instance of res://a3/lantern_gate_room.tscn"),
               ("eight by eight", 8, "PlaneMesh 8 × 8 m for the floor"),
               ("line fourteen", 14, "Floor/Mesh ← cobblestone_warm_floor.tres"),
               ("line eighteen", 18, "StandIn/Mesh ← cobblestone_cool_standin.tres")],
              [("Line 3", "res://a3/lantern_gate_room.tscn"),
               ("Why a plane (Bao)", "A3 BoxMesh top used 1/3 × 1/2 of UV"),
               ("Lights and camera", "inherited from the A3 room")],
              ["test_materials.gd checks both overrides and the PlaneMesh floor"], 22, font=26),
    media_beat("B10", "RESULT",
               ("Here's that room in the engine, at the film's revision. The floor is repeated warm paving, two by two "
                "tiles of square stones. The stand-in wears the same stones, larger and cooler, catching the lantern's "
                "light. Both are lit by the A3 room's own lights, from a fixed camera pose, so every later capture can "
                "be compared pixel for pixel."),
               [("0.0", "real engine capture: the material room from the fixed pose (captures/a5-materials/20261030-170452-pair)"),
                ("The floor", "floor rectangle marked: cobblestone_warm_floor.tres"),
                ("The stand-in", "stand-in rectangle marked: cobblestone_cool_standin.tres"),
                ("fixed camera pose", "enlarged crops of both rectangles")], 20,
               "Result of B09. Real engine capture at 4246f94 (capture_a5_materials.gd --pair, scripted, 1280 × 720).",
               evidence=True),
    code_beat("B11", "CODE", "a5/materials/cobblestone_warm_floor.tres", 8, 18, "A material is a set of values.",
              ("So what's a material? This file. Line ten points at the shader. Lines eleven to thirteen hand it the "
               "three maps. And lines fourteen to eighteen are just values: a warm tint, the map repeated twice, a matte "
               "roughness range. The stand-in's file points at the same shader with different values: cooler, larger, "
               "shinier. The shader is the code; each material is a set of numbers for it."),
              [("Line ten", 10, "shader = cobblestone_surface.gdshader"),
               ("eleven to thirteen", 11, "the three maps: colour, normal, roughness"),
               ("repeated twice", 15, "uv_scale = 2.0"),
               ("matte", 16, "roughness 0.55–0.95")],
              [("Stand-in .tres 14–18", "cooler tint · uv 1 · rough 0.2–0.55"),
               ("Brief answer 6 · Bao", "share the Shader, keep own values"),
               ("test_materials.gd", "one Shader instance, two materials")],
              ["values are stored in the material; defaults live in the shader's uniform lines"], 24, font=27),
    media_beat("B12", "RESULT",
               ("The proof that values live in the material. The capture tool changes only the floor's u v scale, from "
                "two to four, in memory. The floor's stones get smaller and denser, and its pixels change by up to "
                "seventy-two levels. The stand-in, wearing the same shader, doesn't change by a single level. Shared "
                "code, separate numbers."),
               [("0.0", "real engine captures: baseline (uv_scale 2) beside floor uv_scale 4 (captures/a5-materials/20261030-170456-one-material)"),
                ("smaller and denser", "floor crops, before and after"),
                ("single level", "measured: floor max difference 72, stand-in 0")], 18,
               "Result of B11. Real engine captures at 4246f94 (capture_a5_materials.gd --one-material, value set in memory, never saved).",
               evidence=True),
    code_beat("B13", "CODE", "shaders/cobblestone_surface.gdshader", 17, 24, "The shader side: fragment().",
              ("Now the shader side, Bao's fragment function. Line eighteen scales the u v coordinates. Line nineteen "
               "samples the colour map and multiplies by the tint: that's the albedo. Line twenty-one hands the normal "
               "map to the engine. And line twenty-two is Bao's latest edit: the relief's depth is scaled by how squarely "
               "the surface faces the camera, half strength edge-on, full strength face-on."),
              [("Line eighteen", 18, "uv = UV × uv_scale"),
               ("Line nineteen", 19, "ALBEDO = colour sample × tint"),
               ("Line twenty-one", 21, "NORMAL_MAP = the normal sample"),
               ("line twenty-two", 22, "depth × mix(0.5, 1.0, |NORMAL.z|)  (0b91838)")],
              [("Line 22 before 0b91838", "NORMAL_MAP_DEPTH = normal_strength;"),
               ("LANGUAGE-NOTES Q3 · Bao", "reads UV (:18), COLOR, NORMAL (:22)"),
               ("Line 20", "roughness remapped min → max")],
              ["METALLIC = 0.0 (line 23) · opaque, lit by the room's lights"], 24, font=23),
    media_beat("B14", "RESULT",
               ("Change the shader instead, and both objects move. Bao wrote his prediction first: multiply the end of "
                "the albedo line by one half, and the floor and the stand-in both darken, because they share this "
                "shader, while stone size and relief stay the same. He edited line nineteen by hand, captured, and "
                "restored it. Every pixel in both rectangles changed, and his observation matched the prediction. An "
                "earlier Codex run made a similar edit, turning both green, and broke the rule that agents never touch "
                "Bao's shaders."),
               [("0.0", "Bao's prediction, recorded before the edit (PREDICTION.md, his words)"),
                ("edited line nineteen", "real engine captures: baseline beside Bao's ALBEDO × 0.5 edit (captured at e5c0272, before line 22 changed)"),
                ("Every pixel", "measured means: floor and stand-in both fall; every pixel changed"),
                ("observation", "Bao's observation, verbatim"),
                ("Codex run", "agent run, labelled: ALBEDO × (0, 1, 0), both green, shader restored byte for byte")], 30,
               "Result of B13. Real engine captures captures/a5-materials/20261030-131249-compare-shader-baseline and 20261030-163723-compare-shader-bao-edit; the agent run 20261030-single-line-study is labelled as an agent run.",
               evidence=True),
    code_beat("B15", "CODE", "shaders/cobblestone_surface.gdshader", 1, 5, "Why a texture is information.",
              ("Why is a texture information? Because the same kind of file can hold three kinds of data, and only the "
               "hint tells the engine which. Line three marks the colour map source color: these bytes are colour. "
               "Line four marks the normal map hint normal: these are directions. Line five, roughness, has no colour "
               "hint at all: raw numbers. And line one, shader type spatial, puts all of it in the 3D pipeline."),
              [("Line three", 3, "color_tex : source_color — colour data"),
               ("Line four", 4, "normal_tex : hint_normal — directions"),
               ("Line five", 5, "roughness_tex: no colour hint — raw numbers"),
               ("line one", 1, "shader_type spatial: the 3D pipeline")],
              [("LANGUAGE-NOTES Q4 · Bao", "identifies colour / normal data"),
               ("Import: normal-map mode", "diff off · nor_gl on · rough off"),
               ("filter_*, repeat_enable", "change how samples are taken")],
              ["all three maps: Poly Haven Cobblestone Floor 08, 1K PNG, lossless import"], 24, font=23),
    media_beat("B16", "RESULT",
               ("Here are the three files: colour, a purple-blue map of directions, and grey numbers. A map of directions "
                "can be checked like data. This normal map's curl ratio is zero point two two in the OpenGL convention "
                "and one point seven eight read as DirectX, and the DirectX calibration file is its mirror image, so it's "
                "a real surface in the right convention. And on the floor, normal strength zero against one changes how "
                "the stone joints are shaded."),
               [("0.0", "the three source PNGs, each labelled with its line and hint"),
                ("curl ratio", "recorded output: curl_ratio for nor_gl and nor_dx, both conventions"),
                ("normal strength zero", "real engine crops: floor at normal_strength 0 and 1 (20261030-170453-sweep)")], 24,
               "Result of B15. The texture files themselves (godot/assets/textures/cobblestone_floor_08/), recorded curl output (evidence/assignment-5/textures/curl-calibration.log), and real engine sweep captures at 4246f94.",
               evidence=True),
    code_beat("B17", "CODE", "shaders/cobblestone_surface.gdshader", 7, 15, "The material's interface.",
              ("The rest of the top is the material's interface. Group uniforms, on lines seven and eleven, sort the "
               "settings into Surface and Response panels in the Inspector. Each hint range sets a slider's limits, not "
               "a rule: line nine lets u v scale run from a quarter to four. These five numbers are everything a "
               "material can change."),
              [("lines seven", 7, "group_uniforms Surface"),
               ("and eleven", 11, "group_uniforms Response"),
               ("line nine", 9, "uv_scale : hint_range(0.25, 4.0) = 1.0"),
               ("five numbers", 14, "tint · uv_scale · roughness min / max · normal_strength")],
              [("Shader defaults", "tint white · uv 1 · rough 0.2–0.8 · normal 1"),
               ("LANGUAGE-NOTES Q8 · Bao", "uniform hints integrated with the Inspector"),
               ("Line 15", "group_uniforms; closes the groups")],
              ["the brief asks configuration to enforce roughness_min ≤ roughness_max; the shader does not"], 20, font=27),
    media_beat("B18", "RESULT",
               ("The sweep moves each of those five numbers, one at a time, on the floor only: low, the material's own "
                "value, then high. U v scale changes the stones' size, the roughness ends move the warm highlight, normal "
                "strength sets the relief, and a black tint takes the stone colour away. Through all fifteen captures the "
                "stand-in never moves. Bao's look at the new normal strength row: at zero, the surface is flatter and the "
                "normal relief is off; at one, the stone edges and joints look more three-dimensional; at two, stronger "
                "light and dark relief, deeper joints, an exaggerated bump."),
               [("0.0", "fifteen real engine captures in a 5 × 3 grid (captures/a5-materials/20261030-170453-sweep, values in memory)"),
                ("U v scale", "uv_scale row highlighted: 0.25 / 2 / 4"),
                ("roughness ends", "roughness rows highlighted"),
                ("black tint", "tint row highlighted: black"),
                ("never moves", "stand-in mean (31.42, 40.97, 74.83) in every capture"),
                ("Bao's look", "normal_strength row again, with Bao's look quoted from TEST-REPORT.md")], 26,
               "Result of B17. Real engine captures at 4246f94 (capture_a5_materials.gd --sweep); measured means from its CAPTURES.md.",
               evidence=True),
    code_beat("B19", "CODE", "shaders/hint_experiment.gdshader", 5, 14, "A hint, isolated.",
              ("The cleanest test of a hint is Bao's own experiment. One three-pixel grey image, bound to two samplers: "
               "line five with source color, line six without. Line seven picks which one a quad uses, and line eleven "
               "or thirteen writes the sample straight to albedo, unshaded. Same bytes in, so any difference out is the "
               "hint."),
              [("line five", 5, "color_sample : source_color"),
               ("line six", 6, "raw_sample: no hint"),
               ("Line seven", 7, "use_color picks the sampler"),
               ("line eleven", 11, "ALBEDO = the chosen sample")],
              [("The image", "hint_greys_3x1.png: 64 · 128 · 192"),
               ("Two materials", "with / without source_color .tres"),
               ("The scene", "unshaded, no lights, Linear tonemap")],
              ["render_mode unshaded (line 2) · both samplers filter_nearest"], 20, font=28),
    media_beat("B20", "RESULT",
               ("The prediction depended on the renderer. In Forward plus or Mobile, the unhinted quad should come out "
                "lighter, about one thirty-seven, one eighty-eight, two twenty-five. Under this project's Compatibility "
                "renderer, both should read sixty-four, one twenty-eight, one ninety-two. Measured: sixty-four, one "
                "twenty-eight, one ninety-two, on both quads. That matches the Compatibility prediction. The Forward plus "
                "difference is still a prediction; it wasn't measured here."),
               [("0.0", "the brief's prediction table: Compatibility vs Forward+/Mobile"),
                ("Measured", "real engine capture of the hint scene (captures/a5-materials/20261030-131056-hint), band centres sampled"),
                ("still a prediction", "Forward+ column marked: predicted, not measured")], 22,
               "Result of B19. Real engine capture at d01df00 (the hint shader and scene unchanged since); predictions from CHANGE-BRIEF.md.",
               evidence=True),
    code_beat("B21", "CODE", "shaders/standard_generated.gdshader", 1, 7, "The shader Godot writes.",
              ("For comparison, Godot can write a shader itself. Bao converted a standard material holding the same "
               "three maps, and the editor produced this. Line one says it's automatic. Line three is the same spatial "
               "shader type as Bao's line one, and line seven marks the albedo sampler source color, exactly like Bao's "
               "line three."),
              [("Line one", 1, "automatically converted from StandardMaterial3D"),
               ("Line three", 3, "shader_type spatial — Bao's :1"),
               ("line seven", 7, "texture_albedo : source_color — Bao's :3")],
              [("Line 19 ↔ Bao :4", "hint_roughness_normal, no source_color"),
               ("Line 35 ↔ Bao :19", "ALBEDO = albedo × texture sample"),
               ("LANGUAGE-NOTES Q6 · Bao", "line 19 … remains normal data")],
              ["converted in the Godot 4.7.2 editor (43dfe20) · study only: the game never loads it"], 20, font=23),
    media_beat("B22", "RESULT",
               ("Lined up: generated line seven against Bao's line three, nineteen against four, thirty-five against "
                "nineteen. Different names, same jobs. To see whether they draw the same, this film rendered both on the "
                "same plane under one light, as a labelled fixture. Face-on, about nine pixels in ten agree within two "
                "levels of two fifty-five. Tilt the camera fifty degrees and they drift apart, by nearly three levels on "
                "average, which is consistent with Bao's line twenty-two weakening his relief at a slant."),
               [("0.0", "verbatim line pairs, generated vs Bao's, from the hashed files"),
                ("labelled fixture", "film fixture renders: editor-generated material vs Bao's shader, neutral values"),
                ("Face-on", "difference map ×8, face-on: 87–93 % of pixels within 2 levels"),
                ("Tilt the camera", "difference map ×8, tilted 50°: mean 2.4–2.8 levels")], 28,
               "Result of B21. Verbatim lines from godot/ at 4246f94; agent-made film fixture capture/shader_pair_fixture.gd rendered on an isolated copy (not gameplay, values set in memory); measurements by tools/pair_diff.py.",
               evidence=True),
    board("B23", "ANSWERS", "Four questions, four lines", "LANGUAGE-NOTES.md · Bao's answer 8",
          "\n".join(l for l in repo_text("LANGUAGE-NOTES.md").splitlines() if l.startswith("Godot-specific facilities")),
          f"LANGUAGE-NOTES.md (written by Bao), at {SHORT} · card lines point at his code",
          "Each answer points at a line of Bao's code", "The assignment's four questions",
          [("What a shader does", "hurt_tint:7–8 — a function run for every fragment: COLOR in, COLOR out"),
           ("Material vs shader", "warm_floor.tres vs cool_standin.tres — one Shader, two sets of values"),
           ("A texture is information", "cobblestone_surface:3–5 — source_color · hint_normal · raw roughness"),
           ("The shading language", "shader_type (:1), hints, group_uniforms, ALBEDO and NORMAL_MAP outputs")],
          ["What a shader does", "How a material differs", "Why a texture", "And what Godot's"],
          ("So, the four questions, each at a line. What a shader does: hurt tint line eight, a function run for every "
           "fragment. How a material differs from a shader: one shader, two material files of values. Why a texture is "
           "information: lines three to five say colour, directions, or raw numbers. And what Godot's shading language "
           "adds: shader types, hints wired to the Inspector, and outputs like albedo and normal map that plug straight "
           "into Godot's lighting."),
          24, "Recap of the four questions; the excerpt is Bao's answer 8 in LANGUAGE-NOTES.md, verbatim."),
    code_beat("B24", "CODE", "tests/test_hurt_tint.gd", 155, 166, "Testing through the real game.",
              ("The tests drive the real game. This run places one wraith twenty pixels away, presses a real Enter key "
               "to start, waits for a real contact to land, then holds W to walk away. A sampler that runs after "
               "everything else records the uniform every frame. The test never calls the driver or sets the value "
               "itself."),
              [("one wraith", 155, "fixture: a wraith 20 px to the right"),
               ("real Enter key", 157, "parsed key event: Enter starts the run"),
               ("real contact", 159, "wait for an accepted hit"),
               ("holds W", 162, "parsed key event: W walks away")],
              [("Sampler, lines 13–38", "priority 100000: a row per rendered frame"),
               ("Line 187", "zero-after-48-ticks, within one frame"),
               ("Header, lines 2–5", "fixtures only place enemies, hp, a gem")],
              ["./scripts/run-test.sh test_hurt_tint.gd 30 | 60 | 144"], 20, font=23),
    media_beat("B25", "RESULT",
               ("Recorded output, re-run for this film on a clean copy of the film's revision. Twenty-eight of "
                "twenty-eight at thirty, sixty and a hundred forty-four frames per second: the tint reaches zero "
                "forty-eight ticks after the hit, eight tenths of a second of game time, within one frame. One twenty-seven "
                "of one twenty-seven material checks, and the three hundred thirty-two earlier checks unchanged. Then "
                "Bao's three mutations: a missing semicolon fails four checks, a renamed uniform fails three, a dropped "
                "source color fails one. What no headless run can show is the colour on screen; that's why the captures "
                "exist."),
               [("0.0", "recorded: test_hurt_tint at 30 / 60 / 144 fps, first value, zero tick, game time, allowed"),
                ("One twenty-seven", "recorded: test_materials 127/0 and the ten earlier suites, 332/0"),
                ("three mutations", "recorded mutation logs: semicolon 4/28, rename 3/28, source_color 1/127"),
                ("no headless run", "what a headless run cannot show")], 30,
               "Result of B24. Recorded tool output: capture/test-run-film-build-raw.txt (this film, isolated copy at 4246f94) and evidence/assignment-5/mutations/*.log.",
               evidence=True),
    media_beat("B26", "LIMITS",
               ("What the agent got wrong, as Bao's test report lists it: a draft calling the generated particle shader "
                "hand-written; a one-frame tolerance that was really the window's largest frame gap; an unmeasured memory "
                "figure and a curl threshold too loose; an ambient guess the captures disproved; and a first room that "
                "copied the A3 scene instead of inheriting it. Still uncertain: the Forward plus hint difference is "
                "predicted, not measured, and the small face-on difference in the film's own fixture isn't explained. The "
                "next step: run the hint experiment on a Forward plus copy."),
               [("0.0", "TEST-REPORT.md 'What the agent got wrong (Assignment 5)', six rows, plus the Codex shader edit"),
                ("Still uncertain", "open items from TEST-REPORT.md and README.md"),
                ("next step", "one next step")], 30,
               "Agent mistakes from TEST-REPORT.md, verbatim rows shortened; open items from TEST-REPORT.md and README.md Known limitations."),
    media_beat("B27", "ROLES",
               ("Who did what. Bao hand-wrote the three shaders and the line twenty-two edit; an earlier Codex draft of "
                "the tint lived in another copy. He wrote the brief, the predictions and the language notes, ran the "
                "mutations, made the editor conversion and the scene decisions. Claude Code wrote the driver and its "
                "tests, the material audit, the builder and the capture tools, after Bao approved each plan. The texture "
                "is Poly Haven's Cobblestone Floor zero eight, by Rob Tuytel, released CC zero. The code you saw is "
                "revision four two four six f nine four."),
               [("0.0", "SOURCES.md, Assignment 5: Bao's work and decisions"),
                ("Claude Code", "SOURCES.md: what Claude Code wrote, prompts in evidence/assignment-5/agent/"),
                ("Poly Haven", "texture credit: Cobblestone Floor 08, Rob Tuytel, CC0"),
                ("revision", "source revision 4246f94")], 30,
               "Roles from SOURCES.md (Assignment 5 section); texture licence from godot/assets/textures/cobblestone_floor_08/ATTRIBUTION.md."),
    {"beat_id": "B28", "act": "VERDICT",
     "role_note": "ClaudeVerdictArtifact — implemented work, limitations, human judgment; shows the source revision.",
     "narration_text": ("The verdict. Implemented: a nine-line tint that shows the courier's protection, and a textured "
                        "shader with two materials, with no gameplay rule changed and every number predicted before it "
                        "was measured. The limits are written down: Compatibility can't show what source color changes "
                        "elsewhere, and a headless test can't see colour. The human judgments, the playtest and the looks, "
                        "are Bao's own, quoted where he gave them."),
     "estimated_duration_s": 24,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "artifact-reveal",
              "show": [{"at": "0.0", "event": "artifact card 'Verdict', heading with the source revision"},
                       {"at": "0.2", "event": "implemented line"}, {"at": "0.45", "event": "prediction line"},
                       {"at": "0.65", "event": "limits line"}, {"at": "0.85", "event": "human-judgment line"}],
              "remotion": {"pattern": "ClaudeVerdictArtifact", "props": {
                  "artifactTitle": "Verdict", "artifactHeading": f"Lanternfall shaders · source revision {SHORT}",
                  "brandLabel": HANDLE,
                  "artifactLines": ["Implemented: hurt tint from iframes; cobblestone shader, two materials; gameplay unchanged.",
                                    "Predicted first, then measured: hand table, hint table, Bao's one-line edit.",
                                    "Limits: no Forward+ hint measurement; a headless run cannot see colour.",
                                    "Human judgment: Bao's playtest and looks, quoted as he gave them."]}}}},
    {"beat_id": "B29", "act": "HANDOFF",
     "role_note": "HANDOFF LAW — Your Turn: one bounded material change plus a prediction and a capture. Liam reads the prompt, discusses it and signs off.",
     "narration_text": ("Your turn. Paste this: Please use Walker to read the cool stand-in material in my Lanternfall "
                        "project. Change only u v scale from one to three. Before running anything, predict which rectangle "
                        "of the pair capture changes, how the stand-in's stones change, and which material check fails. "
                        "Then capture the pair, compare it with your prediction, and put one back. It tests whether you "
                        "really believe a material is just numbers. Write the prediction first. Liam, in for Bear."),
     "estimated_duration_s": 30,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on",
              "show": [{"at": "0.02", "event": "composer card; greeting 'Your turn.'"},
                       {"at": "0.1", "event": "the paste-ready prompt types in"},
                       {"at": "0.7", "event": "three output lines: prediction first, capture, revert"}],
              "remotion": {"pattern": "ClaudeComposerAsk", "props": {
                  "greeting": "Your turn.", "topic": TOPIC, "segment": "Lanternfall",
                  "command": YOUR_TURN,
                  "runningText": "paste this into Claude…",
                  "folderLabel": HANDLE, "modelLabel": "Claude", "effortLabel": "High",
                  "output": ["Prediction written before the capture.", "Pair captured: compare with your prediction.",
                             "Then put 1.0 back."], "animateTyping": True}}}},
    {"beat_id": "B30", "act": "OUTRO",
     "role_note": "OUTRO LAW — ClaudeTitleOutro: exact title, @NikBearBrown, slug-seeded mascot, stock jingle only, no narration.",
     "narration_text": "", "estimated_duration_s": 9.44, "actual_duration_s": 9.44,
     "audio_file": "mp3/beat-B30.wav",
     "audio_note": "stock @NikBearBrown jingle logos/bear-brown/bear-brown-5.mp3, picked by the slug seed the outro uses (char-sum 5074 mod 6 pool files = 4), never cut: padded with 1.0 s of silence; no narration (Liam signs off in B29)",
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "mascot-title",
              "show": [{"at": "0.0", "event": f"title '{TITLE}'"}, {"at": "0.25", "event": "@NikBearBrown"},
                       {"at": "0.45", "event": "slug-seeded mascot"}],
              "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "durationSeconds": 9.44}}}},
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
        "greeting": "Ciao, Liam",
        "greeting_note": "hello lexicon: Ciao (Italian); earlier Lanternfall films used Merhaba (A2), Hej (A3), Bonjour (A6). Liam never takes Wagwan (IN-FOR-BEAR LAW).",
        "persona": "Liam (in for Bear)", "presenter": "Liam (in for Bear)", "in_for_bear": True,
        "game": {"repo": "https://github.com/yanxlh/walker-lanternfall-bao-x", "project_dir": "godot",
                 "source_revision": FILM_SHA, "godot": "4.7.2.stable.official.ed1daf0bf"},
        "teaching_contract": "code-then-result-v1",
        "note": ("godot-gamedev + walker teardown of Bao Xing's CSYE 7270 shader assignment. Every code panel is a "
                 f"verbatim excerpt of godot/ at {FILM_SHA} (read with git show, never the working tree); the gameplay "
                 "shot is a real Movie Maker capture of an isolated copy of that revision, driven through the real input "
                 "map by the disclosed capture driver; controlled-value captures, material captures and the film's "
                 "shader-pair fixture are labelled as such. No paid call, no upload."),
        "links": {"repo": "https://github.com/yanxlh/walker-lanternfall-bao-x"},
        "tags": ["Godot 4", "godot-gamedev", "Walker", "Godot shading language", "canvas_item shader",
                 "spatial shader", "ShaderMaterial", "CSYE 7270", "Teardown register", "Kokoro"]},
        "beats": beats}
    path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
    words = sum(len(b["narration_text"].split()) for b in beats)
    est = sum(float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in beats)
    print(f"{path}: {len(beats)} beats, {words} words, ~{est:.0f}s before source reports are measured")


if __name__ == "__main__":
    main()

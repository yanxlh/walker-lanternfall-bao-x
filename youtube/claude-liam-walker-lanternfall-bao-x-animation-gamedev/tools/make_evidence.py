#!/usr/bin/env python3
"""Write gamedev-evidence.json (schema 1, teaching contract code-then-result-v1) for the animation film.

Every file under godot/ at the film revision (git ls-tree, no .uid) is hashed from git — never from the working tree —
and tied to a component or excluded with a reason; excerpts are taken from the beat sheet's GodotDevWorkbench beats and
re-read from git; each code beat is paired with the next beat's hashed result media. Check it against an archived copy:

    git archive <rev> godot | tar -x -C <dir>
    ./art godot-gamedev --check REEL --game <dir>/godot

    python3 tools/make_evidence.py
"""
import hashlib, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from src import SHA, blob, inventory, text  # noqa: E402

REEL = Path(__file__).resolve().parents[1]

A7 = {
    "sprite-walk": ("The sprite clip: Body, a Sprite2D on Bao's pc_sheet.png sliced by hframes 10 and an offset that puts cell "
                    "pixel (16, 23) on the courier's origin; the walk clip keys Body:frame 2 at 0 and 3 at 8/60 s, discrete, "
                    "nearest, LOOP_LINEAR, step 1/60, plus one-key clips for the other cells; the sheet's credits.",
                    ["B04", "B05", "B06", "B07"],
                    ["features/player/courier_visual.tscn", "animations/courier_clips.tres", "assets/art/pc_sheet.png",
                     "assets/art/pc_sheet.png.import", "assets/art/ATTRIBUTION.md"]),
    "dash-rig": ("The rig clip: head, arm, coat and legs as region rectangles of cell 2 under Hips, Chest and Neck pivots, "
                 "keyed on Rig:position, Hips and Neck rotation at the phase boundaries 0/4/14/20 with transitions 2.0/1.0/0.5, "
                 "built by a headless builder and saved with ResourceSaver; revision r2 adds Polygon2D outlines on the coat "
                 "and legs from the cell's outer silhouette ring.",
                 ["B08", "B09", "B16", "B17"],
                 ["features/player/build_courier_visual.gd", "features/player/courier_visual.tscn", "animations/courier_clips.tres"]),
    "state-machine": ("One authority: player.gd's visual state machine (override > dash > hurt > cast > walk > idle) picks the clip "
                      "and a time from tick counters, and _show() alone plays and seeks the manual-mode AnimationPlayer; the "
                      "dash phases advance from dash_ticks on the 60 Hz tick; take_hit applies Bao's interrupt rule per phase; "
                      "the dash action, the card and the dash timings live in session.gd, progression.gd and tuning.gd.",
                      ["B10", "B11", "B12", "B13"],
                      ["features/player/player.gd", "game/session.gd", "features/progression/progression.gd", "features/tuning.gd"]),
    "tests": ("The pins (test_courier_pin.gd before the change; test_courier_pin_input.gd through real input, verified on 9ccf078), "
              "the read-back test_courier_clips.gd (the assignment's track_problems, key times, step, loop, discrete, cells "
              "inside the sheet, seam, phase boundaries, rig regions, outline), the structure test, the dash edge tests at "
              "30/60/144 fps with the two-clocks measurement, the Godot 3 names and headless probes, the wrapper's resource-load "
              "fixture, the shared harness and the earlier suites run unchanged.",
              ["B14", "B15", "B11", "B13"],
              ["tests/test_courier_pin.gd", "tests/test_courier_pin_input.gd", "tests/test_courier_clips.gd",
               "tests/test_courier_states.gd", "tests/test_dash_edges.gd", "tests/probe_godot3_names.gd",
               "tests/probe_headless_a7.gd", "tests/fixture_resource_load_error.gd", "tests/harness.gd",
               "tests/test_logic.gd", "tests/test_gameplay.gd", "tests/test_audio.gd", "tests/test_defeat_sparks_config.gd",
               "tests/test_extra_particles_config.gd", "tests/test_particles_state.gd", "tests/test_particles_edges.gd",
               "tests/test_a3_assets.gd", "tests/test_lantern_gate.gd", "tests/test_a3_camera.gd", "tests/test_materials.gd",
               "tests/test_hurt_tint.gd"]),
    "captures": ("The fixture preview Bao records the 30 fps strips with (real session on the market ground, parsed input, one "
                 "log line per frame), the Movie Maker replay and clip-strip tools, and the playtest launcher.",
                 ["B05", "B09", "B17"],
                 ["previews/courier_preview.tscn", "previews/courier_preview.gd", "tests/capture_courier.gd",
                  "tests/capture_courier_clip_strip.gd", "tests/play_dash.gd"]),
}
EXCLUSIONS = {
    "tests/capture.gd": "Assignment 2 development tool (storyboard and pose screenshots); not used or shown in this film.",
    "tests/capture_map.gd": "Assignment 2 development tool that renders the map overview; not shown in this film.",
    "tests/probe_balance.gd": "Assignment 2 balance bots; not part of the playable game and not shown.",
    "tests/rasterize_storyboard.gd": "Assignment 2 storyboard rasteriser; not shown in this film.",
    "tests/capture_a3_orbit.gd": "Assignment 3 capture tool; not used or shown in this film.",
    "tests/capture_lantern_gate.gd": "Assignment 3 capture tool; not used or shown in this film.",
    "tests/capture_play_checks.gd": "Assignment 6 play-check driver; explained in the particle film.",
    "tests/cost_effects.gd": "Assignment 6 cost script; explained in the particle film.",
    "tests/build_shader_study.gd": "Assignment 6 study-scene builder; not shown here.",
    "tests/capture_hurt_tint.gd": "Assignment 5 hurt-tint capture tool; explained in the shader film.",
    "tests/capture_a5_materials.gd": "Assignment 5 material capture tool; explained in the shader film.",
    "tests/calibrate_normal_map_check.gd": "Assignment 5 normal-map calibration; explained in the shader film.",
    "tests/normal_map_check.gd": "Assignment 5 normal-map check; explained in the shader film.",
    "tests/probe_headless_facts.gd": "Assignment 5 headless-facts probe; this film shows the A7 probe instead.",
    "previews/defeat_sparks_preview.gd": "Assignment 6 fixture preview; explained in the particle film.",
    "previews/defeat_sparks_preview.tscn": "Assignment 6 fixture preview scene; explained in the particle film.",
    "previews/lantern_trail_preview.gd": "Assignment 6 fixture preview; explained in the particle film.",
    "previews/lantern_trail_preview.tscn": "Assignment 6 fixture preview scene; explained in the particle film.",
    "previews/baseline/lantern_trail_r0.tscn": "Assignment 6 preserved baseline; not shown here.",
    "previews/shader_study/README.md": "Assignment 6 study notes; not shown here.",
    "previews/shader_study/hit_sparks_gpu.tscn": "Assignment 6 study scene; not loaded by the game.",
    "shaders/particles_generated.gdshader": "Assignment 6 editor-generated study shader; explained in the particle film.",
    "shaders/standard_generated.gdshader": "Assignment 5 editor-generated study shader; explained in the shader film.",
    "a5/scratch/standard_conversion.tscn": "Assignment 5 scratch conversion scene; study only, explained in the shader film.",
}
ROLES = {".gd": "GDScript", ".tscn": "scene", ".tres": "resource", ".godot": "project settings", ".png": "texture (PNG)",
         ".wav": "sound effect (WAV)", ".ogg": "music loop (OGG Vorbis)", ".glb": "3D model (glTF binary)",
         ".import": "import settings sidecar", ".json": "asset data", ".gdshader": "shader", ".md": "documentation"}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> None:
    sheet = json.loads((REEL / "beat_sheet.json").read_text())
    beats = sheet["beats"]
    inv = inventory()
    owner = {}
    for cid, (_e, _b, files) in A7.items():
        for f in files:
            owner.setdefault(f, []).append(cid)
    earlier = [p for p in inv if p not in owner and p not in EXCLUSIONS]
    comps = dict(A7)
    comps["earlier-layers"] = (
        "The game the clips live in, unchanged by this assignment: the fixed-tick session's other systems, weapons, enemies, "
        "pickups, the market ground and camera, HUD, audio, project settings, the A3 and A5 3D scenes, the A5 shaders "
        "(hand-written by Bao), the A6 particle effects and the generated art, sound and music. Seen in the take; explained "
        "in the earlier films.", ["B11", "B13"], earlier)
    for f in earlier:
        owner.setdefault(f, []).append("earlier-layers")
    extra = [p for p in list(owner) + list(EXCLUSIONS) if p not in inv]
    both = [p for p in owner if p in EXCLUSIONS]
    if extra or both:
        raise SystemExit(f"inventory mismatch: unknown {extra}, both {both}")
    files = [{"path": p, "sha256": sha(blob(p)), "role": ROLES.get(Path(p).suffix, "file"), "component_ids": owner[p]}
             for p in inv if p in owner]
    comp_list = [{"id": cid, "explanation": e, "beat_ids": b, "files": f} for cid, (e, b, f) in comps.items()]
    excerpts, pairs = [], []
    for i, b in enumerate(beats):
        rem = (b.get("shot") or {}).get("remotion") or {}
        if not rem.get("pattern", "").startswith("GodotDevWorkbench") or not rem.get("props", {}).get("code"):
            continue
        p = rem["props"]
        path = p["path"].replace("res://", "")
        n = len(p["code"].split("\n"))
        t = "\n".join(text(path).splitlines()[p["startLine"] - 1:p["startLine"] - 1 + n])
        if t != p["code"]:
            raise SystemExit(f"{b['beat_id']}: displayed code differs from {path} at {SHA}")
        excerpts.append({"beat_id": b["beat_id"], "path": path, "start_line": p["startLine"],
                         "end_line": p["startLine"] + n - 1, "text": t})
        nxt = beats[i + 1]
        media = nxt["shot"].get("evidence_media")
        if not media:
            raise SystemExit(f"{b['beat_id']}: next beat {nxt['beat_id']} has no evidence media")
        pairs.append({"code_beat": b["beat_id"], "result_beat": nxt["beat_id"],
                      "observation": nxt.get("observation") or nxt["role_note"],
                      "media": {"path": media, "sha256": sha((REEL / media).read_bytes())}})
    data = {"schema_version": 1, "teaching_contract": "code-then-result-v1",
            "game": {"project_dir": "godot", "source_revision": SHA, "engine": "Godot 4.7.2.stable.official.ed1daf0bf",
                     "read_from": "git show <revision>:godot/<path> (not the working tree)"},
            "files": files, "components": comp_list, "excerpts": excerpts,
            "exclusions": [{"path": p, "reason": r} for p, r in EXCLUSIONS.items()],
            "code_result_pairs": pairs}
    (REEL / "gamedev-evidence.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"gamedev-evidence.json: {len(files)} files, {len(EXCLUSIONS)} exclusions, {len(comp_list)} components, "
          f"{len(excerpts)} excerpts, {len(pairs)} code/result pairs")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Write gamedev-evidence.json (schema 1, teaching contract code-then-result-v1) for the shader film.

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

ART = ["enemy_moth", "enemy_wraith", "env_crates", "env_ground_tile", "env_lantern_post", "env_leaves", "env_noodle_cart",
       "env_puddle", "env_stall", "fx_beam", "fx_orbit_moth", "fx_sunflare", "pickup_gem", "pc_sheet"]
SFX = ["sfx_01_kill", "sfx_02_pickup", "sfx_03_hurt", "sfx_04_levelup", "sfx_05_evolve", "sfx_06a_lose", "sfx_06b_win"]
MUSIC = ["mus_01_night_market", "mus_02_sunflare_layer"]
TEX = "assets/textures/cobblestone_floor_08/cobblestone_floor_08_%s_1k.png"

COMPONENTS = {
    "hurt-tint": ("The 2D shader from code: Bao's nine-line canvas_item shader mixes the incoming COLOR toward hurt_color by "
                  "hurt_amount; the read-only driver, added by the session, gives the courier his own ShaderMaterial and "
                  "writes clamp(iframes / 48) every frame in PLAYING, PAUSED and LEVELUP and 0 otherwise. The counter is "
                  "player.iframes, set to IFRAME_TICKS (48) on an accepted hit and decremented once per simulation tick.",
                  ["B05", "B06", "B07", "B08"],
                  ["shaders/hurt_tint.gdshader", "effects/hurt_tint_presentation.gd", "game/session.gd",
                   "features/player/player.gd", "features/tuning.gd", "game/game_state.gd", "tests/capture_hurt_tint.gd"]),
    "material-room": ("The 3D object: a5/material_room.tscn instances the A3 room and overrides only Floor/Mesh (an 8 x 8 m "
                      "PlaneMesh) and the two material_override slots; lights, camera, orbit controls and the three A3 props "
                      "come from the inherited room.",
                      ["B09", "B10", "B12"],
                      ["a5/material_room.tscn", "a3/lantern_gate_room.tscn", "a3/lantern_gate_room.gd", "a3/lantern_gate.tscn",
                       "a3/lantern_gate.gd", "a3/lantern_gate.glb", "a3/lantern_gate.glb.import", "a3/oil_shrine.glb",
                       "a3/oil_shrine.glb.import", "a3/supply_stack.glb", "a3/supply_stack.glb.import"]),
    "materials": ("Two ShaderMaterials of one shader: the warm floor (tint 1/0.92/0.80, uv_scale 2, roughness 0.55-0.95, normal 1) "
                  "and the cool stand-in (0.72/0.85/1, uv 1, 0.2-0.55, normal 0.5), both bound to the same three Poly Haven "
                  "maps; the script that built them and the material audit.",
                  ["B11", "B12", "B10", "B16"],
                  ["a5/materials/cobblestone_warm_floor.tres", "a5/materials/cobblestone_cool_standin.tres",
                   "a5/build_a5_materials.gd", "MATERIALS.md", "assets/textures/cobblestone_floor_08/ATTRIBUTION.md"] +
                  [p for m in ("diff", "nor_gl", "rough", "nor_dx") for p in (TEX % m, TEX % m + ".import")]),
    "cobblestone-shader": ("Bao's spatial shader: three samplers whose hints say colour (source_color), directions (hint_normal) "
                           "or raw numbers (roughness), five grouped uniforms with hint_range sliders, and a fragment() that "
                           "writes ALBEDO, ROUGHNESS, NORMAL_MAP and NORMAL_MAP_DEPTH, the last scaled by abs(NORMAL.z) since "
                           "Bao's line-22 edit (0b91838).",
                           ["B13", "B14", "B15", "B16", "B17", "B18", "B22"],
                           ["shaders/cobblestone_surface.gdshader"]),
    "hint-experiment": ("Bao's source_color experiment: one 3 x 1 grey PNG (64/128/192) written by code, two nearest samplers "
                        "with and without the hint, two materials and an unshaded, unlit scene.",
                        ["B19", "B20"],
                        ["shaders/hint_experiment.gdshader", "a5/hint_experiment/hint_experiment.tscn",
                         "a5/hint_experiment/hint_greys_3x1.png", "a5/hint_experiment/hint_greys_3x1.png.import",
                         "a5/hint_experiment/hint_with_source_color.tres", "a5/hint_experiment/hint_without_source_color.tres",
                         "a5/hint_experiment/make_hint_png.gd"]),
    "generated-shader": ("The editor-generated spatial shader from a converted StandardMaterial3D with the same three maps, and "
                         "the scratch scene holding that ShaderMaterial; study only, never loaded by the game.",
                         ["B21", "B22"],
                         ["shaders/standard_generated.gdshader", "a5/scratch/standard_conversion.tscn"]),
    "tests": ("test_hurt_tint.gd (real keys and real contact through the game loop, sampled every frame at 30/60/144 fps), "
              "test_materials.gd (wiring, hints, imports, materials), the curl_ratio normal-map check and its calibration, the "
              "headless-facts probe, the material capture tool, the shared harness, and the ten earlier suites re-run "
              "unchanged.",
              ["B24", "B25", "B16", "B18"],
              ["tests/test_hurt_tint.gd", "tests/test_materials.gd", "tests/harness.gd", "tests/normal_map_check.gd",
               "tests/calibrate_normal_map_check.gd", "tests/probe_headless_facts.gd", "tests/capture_a5_materials.gd",
               "tests/test_logic.gd", "tests/test_gameplay.gd", "tests/test_audio.gd", "tests/test_defeat_sparks_config.gd",
               "tests/test_extra_particles_config.gd", "tests/test_particles_state.gd", "tests/test_particles_edges.gd",
               "tests/test_a3_assets.gd", "tests/test_lantern_gate.gd", "tests/test_a3_camera.gd"]),
    "game-context": ("The game the tint lives in: the fixed-tick session and state machine, courier, weapons, enemies and "
                     "spawner, gems, progression, market ground and camera, HUD, audio, project settings, the Assignment 6 "
                     "particle effects, and the generated art, sound and music. Unchanged by this assignment except the three "
                     "session lines that add the tint driver; seen in play in the hurt take, explained in the earlier films.",
                     ["B08", "B25"],
                     ["game/session.gd", "game/game_state.gd", "game/main.tscn", "project.godot", "ui/hud.gd",
                      "audio/audio_bus.gd", "audio/sfx_gate.gd", "features/art.gd", "features/tuning.gd",
                      "features/enemies/enemy.gd", "features/enemies/spawner.gd", "features/pickups/gem.gd",
                      "features/player/player.gd", "features/progression/progression.gd", "features/weapons/beam_shot.gd",
                      "features/weapons/weapon_fx.gd", "features/world/camera_fx.gd", "features/world/ground.gd",
                      "effects/particle_presentation.gd", "effects/defeat_sparks.tscn", "effects/lantern_trail.tscn",
                      "effects/level_up_sparks.tscn", "effects/level_up_overlay.tscn", "assets/particles/spark.png",
                      "assets/particles/spark.png.import", "assets/particles/ATTRIBUTION.md",
                      "assets/manifest.json", "assets/art/manifest.json", "assets/art/palettes.json"] +
                     [p for n in ART for p in (f"assets/art/{n}.png", f"assets/art/{n}.png.import")] +
                     [p for n in SFX for p in (f"assets/sfx/{n}.wav", f"assets/sfx/{n}.wav.import")] +
                     [p for n in MUSIC for p in (f"assets/music/{n}.ogg", f"assets/music/{n}.ogg.import")]),
}
EXCLUSIONS = {
    "tests/capture.gd": "Assignment 2 development tool (storyboard and pose screenshots); not used or shown in this film.",
    "tests/capture_map.gd": "Assignment 2 development tool that renders design/map-overview.png; not shown in this film.",
    "tests/probe_balance.gd": "Assignment 2 development tool (scripted balance bots); not part of the playable game and not shown.",
    "tests/rasterize_storyboard.gd": "Assignment 2 development tool that rasterises the storyboard SVGs; not shown in this film.",
    "tests/capture_a3_orbit.gd": "Assignment 3 capture tool for the orbit camera; not used or shown in this film.",
    "tests/capture_lantern_gate.gd": "Assignment 3 capture tool for the gate room; not used or shown in this film.",
    "tests/capture_play_checks.gd": "Assignment 6 windowed play-check driver; explained in the particle film, not shown here.",
    "tests/cost_effects.gd": "Assignment 6 CPU/GPU cost script for the particle effects; explained in the particle film, not shown here.",
    "tests/build_shader_study.gd": "Assignment 6 tool that built the GPU particle study scene; not shown here.",
    "shaders/particles_generated.gdshader": "Assignment 6 editor-generated particle process shader, study only; explained in the particle film. This film's generated-shader study is standard_generated.gdshader.",
    "previews/defeat_sparks_preview.gd": "Assignment 6 fixture preview for hit sparks (not gameplay); explained in the particle film.",
    "previews/defeat_sparks_preview.tscn": "Assignment 6 fixture preview scene for hit sparks; explained in the particle film.",
    "previews/lantern_trail_preview.gd": "Assignment 6 fixture preview for the trail; explained in the particle film.",
    "previews/lantern_trail_preview.tscn": "Assignment 6 fixture preview scene for the trail; explained in the particle film.",
    "previews/baseline/lantern_trail_r0.tscn": "Assignment 6 preserved trail baseline resource for its comparison; not shown here.",
    "previews/shader_study/README.md": "Assignment 6 shader-study notes; not shown here.",
    "previews/shader_study/hit_sparks_gpu.tscn": "Assignment 6 GPU particle study scene; not loaded by the game, not shown here.",
}
ROLES = {".gd": "GDScript", ".tscn": "scene", ".tres": "resource (ShaderMaterial)", ".godot": "project settings",
         ".png": "texture (PNG)", ".wav": "sound effect (WAV)", ".ogg": "music loop (OGG Vorbis)", ".glb": "3D model (glTF binary)",
         ".import": "import settings sidecar", ".json": "asset data", ".gdshader": "shader", ".md": "documentation"}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> None:
    sheet = json.loads((REEL / "beat_sheet.json").read_text())
    beats = sheet["beats"]
    inv = inventory()
    owner = {}
    for cid, (_e, _b, files) in COMPONENTS.items():
        for f in files:
            owner.setdefault(f, []).append(cid)
    missing = [p for p in inv if p not in owner and p not in EXCLUSIONS]
    extra = [p for p in list(owner) + list(EXCLUSIONS) if p not in inv]
    both = [p for p in owner if p in EXCLUSIONS]
    if missing or extra or both:
        raise SystemExit(f"inventory mismatch: unassigned {missing}, unknown {extra}, both {both}")
    files = [{"path": p, "sha256": sha(blob(p)), "role": ROLES.get(Path(p).suffix, "file"), "component_ids": owner[p]}
             for p in inv if p in owner]
    comps = [{"id": cid, "explanation": e, "beat_ids": b, "files": f} for cid, (e, b, f) in COMPONENTS.items()]
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
            "files": files, "components": comps, "excerpts": excerpts,
            "exclusions": [{"path": p, "reason": r} for p, r in EXCLUSIONS.items()],
            "code_result_pairs": pairs}
    (REEL / "gamedev-evidence.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"gamedev-evidence.json: {len(files)} files, {len(EXCLUSIONS)} exclusions, {len(comps)} components, "
          f"{len(excerpts)} excerpts, {len(pairs)} code/result pairs")


if __name__ == "__main__":
    main()

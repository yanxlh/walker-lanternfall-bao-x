#!/usr/bin/env python3
"""Write gamedev-evidence.json (schema 1, teaching contract code-then-result-v1) for the particle film.

Every authored file under godot/ (no .godot/, no .uid) is hashed and tied to a component or excluded with a reason;
excerpts are taken from the beat sheet's GodotDevWorkbench beats and re-read from disk; each code beat is paired with
the next beat's hashed result media.

    python3 tools/make_evidence.py
"""
import hashlib, json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
GAME = REEL.parents[1] / "godot"
SHA = (REEL / "FILM-SOURCE-REVISION.txt").read_text().strip()

ART = ["enemy_moth", "enemy_wraith", "env_crates", "env_ground_tile", "env_lantern_post", "env_leaves", "env_noodle_cart",
       "env_puddle", "env_stall", "fx_beam", "fx_orbit_moth", "fx_sunflare", "pickup_gem", "pc_sheet"]
SFX = ["sfx_01_kill", "sfx_02_pickup", "sfx_03_hurt", "sfx_04_levelup", "sfx_05_evolve", "sfx_06a_lose", "sfx_06b_win"]
MUSIC = ["mus_01_night_market", "mus_02_sunflare_layer"]

COMPONENTS = {
    "presentation": ("The read-only particle controller: signals in (weapon_hit, leveled_up, run_started, state.changed), "
                     "particles out. One burst per accepted hit (PLAYING only, cap 32), the trail decided each physics "
                     "frame from actual displacement with a jump limit, the celebration on its own overlay at the card-"
                     "screen portrait (cap 4), and one policy that freezes or clears effects by state. Session gains only "
                     "the weapon_hit signal and attaches this node.",
                     ["B04", "B05", "B10", "B11", "B14", "B15", "B16", "B17"],
                     ["effects/particle_presentation.gd", "game/session.gd", "game/game_state.gd"]),
    "hit-sparks": ("Effect A as data: a 16-spark one-shot CPUParticles2D burst from a point, spread 180, lifetime 0.45 s, "
                   "the code-generated 3 x 3 spark texture, and the kept r1 change scale_amount_max 1.2 -> 1.8; with the "
                   "fixture preview that produced the r0/r1 strips.",
                   ["B06", "B07", "B08", "B09", "B05"],
                   ["effects/defeat_sparks.tscn", "assets/particles/spark.png", "assets/particles/spark.png.import",
                    "assets/particles/ATTRIBUTION.md", "previews/defeat_sparks_preview.gd", "previews/defeat_sparks_preview.tscn"]),
    "trail": ("Effect B as data: 24 embers emitted continuously from a 3 px sphere, drifting up and fading in 0.35 s, with "
              "the kept alpha change 0.55/0.30 -> 0.95/0.70; the fixture preview and its preserved original resource.",
              ["B12", "B13", "B10", "B11"],
              ["effects/lantern_trail.tscn", "previews/lantern_trail_preview.gd", "previews/lantern_trail_preview.tscn",
               "previews/baseline/lantern_trail_r0.tscn"]),
    "celebration": ("The extra level-up celebration (32 particles, 0.7 s, sphere radius 12) on CanvasLayer 11 above the "
                    "HUD, anchored to the card-screen portrait rectangle the HUD shares.",
                    ["B14", "B15"],
                    ["effects/level_up_sparks.tscn", "effects/level_up_overlay.tscn", "ui/hud.gd"]),
    "tests": ("Configuration read-back for all three scenes, the real-input state suite, the edge suite (blocked input, "
              "position jump, LOST/WON cleanup), the harness, the original game's suites (counts unchanged), and the "
              "windowed play-check driver whose shots appear in B13 and B17.",
              ["B18", "B19", "B17", "B13"],
              ["tests/harness.gd", "tests/test_defeat_sparks_config.gd", "tests/test_extra_particles_config.gd",
               "tests/test_particles_state.gd", "tests/test_particles_edges.gd", "tests/test_logic.gd",
               "tests/test_gameplay.gd", "tests/test_audio.gd", "tests/capture_play_checks.gd"]),
    "shader-study": ("The editor-generated particles shader (start(), process(), forces, display parameters) and the "
                     "GPU study scene it came from, built by convert_from_particles(); the converted ShaderMaterial "
                     "carries no colour ramp or scale curve. Not loaded by the game.",
                     ["B20", "B21"],
                     ["shaders/particles_generated.gdshader", "previews/shader_study/hit_sparks_gpu.tscn",
                      "previews/shader_study/README.md", "tests/build_shader_study.gd"]),
    "cost": ("The cost script: identical fixtures with the presentation kept or freed, interleaved trials, headless CPU "
             "frame time and windowed viewport GPU time.",
             ["B22", "B23"], ["tests/cost_effects.gd"]),
    "game-context": ("The Assignment 2 game the effects attach to: fixed-tick session and state machine, courier, weapons, "
                     "enemies and spawner, gems, progression, the market and camera, HUD, audio bus, project settings, "
                     "and the generated art, sound and music. Unchanged by this assignment except the weapon_hit signal "
                     "and the presentation child; shown in play in every capture here and explained in the Assignment 2 "
                     "film, not read line by line in this one.",
                     ["B05", "B11", "B15", "B17"],
                     ["game/session.gd", "game/game_state.gd", "game/main.tscn", "project.godot", "ui/hud.gd",
                      "audio/audio_bus.gd", "audio/sfx_gate.gd", "features/art.gd", "features/tuning.gd",
                      "features/enemies/enemy.gd", "features/enemies/spawner.gd", "features/pickups/gem.gd",
                      "features/player/player.gd", "features/progression/progression.gd", "features/weapons/beam_shot.gd",
                      "features/weapons/weapon_fx.gd", "features/world/camera_fx.gd", "features/world/ground.gd",
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
}
ROLES = {".gd": "GDScript", ".tscn": "scene", ".godot": "project settings", ".png": "texture (PNG)",
         ".wav": "sound effect (WAV)", ".ogg": "music loop (OGG Vorbis)", ".import": "import settings sidecar",
         ".json": "asset data", ".gdshader": "editor-generated particles shader", ".md": "documentation"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    sheet = json.loads((REEL / "beat_sheet.json").read_text())
    beats = sheet["beats"]
    inventory = sorted(p.relative_to(GAME).as_posix() for p in GAME.rglob("*")
                       if p.is_file() and not any(x in (".godot", ".git") for x in p.relative_to(GAME).parts)
                       and p.suffix != ".uid" and p.name != ".DS_Store")
    owner = {}
    for cid, (_e, _b, files) in COMPONENTS.items():
        for f in files:
            owner.setdefault(f, []).append(cid)
    missing = [p for p in inventory if p not in owner and p not in EXCLUSIONS]
    extra = [p for p in owner if p not in inventory]
    if missing or extra:
        raise SystemExit(f"inventory mismatch: unassigned {missing}, unknown {extra}")
    files = [{"path": p, "sha256": sha(GAME / p), "role": ROLES.get(Path(p).suffix, "file"), "component_ids": owner[p]}
             for p in inventory if p in owner]
    comps = [{"id": cid, "explanation": e, "beat_ids": b, "files": f} for cid, (e, b, f) in COMPONENTS.items()]
    excerpts, pairs = [], []
    for i, b in enumerate(beats):
        rem = (b.get("shot") or {}).get("remotion") or {}
        if not rem.get("pattern", "").startswith("GodotDevWorkbench") or not rem.get("props", {}).get("code"):
            continue
        p = rem["props"]
        path = p["path"].replace("res://", "")
        n = len(p["code"].split("\n"))
        text = "\n".join((GAME / path).read_text().splitlines()[p["startLine"] - 1:p["startLine"] - 1 + n])
        if text != p["code"]:
            raise SystemExit(f"{b['beat_id']}: displayed code differs from {path}")
        excerpts.append({"beat_id": b["beat_id"], "path": path, "start_line": p["startLine"], "end_line": p["startLine"] + n - 1,
                         "text": text})
        nxt = beats[i + 1]
        media = nxt["shot"].get("evidence_media")
        if not media:
            raise SystemExit(f"{b['beat_id']}: next beat {nxt['beat_id']} has no evidence media")
        pairs.append({"code_beat": b["beat_id"], "result_beat": nxt["beat_id"],
                      "observation": nxt.get("observation") or nxt["role_note"],
                      "media": {"path": media, "sha256": sha(REEL / media)}})
    data = {"schema_version": 1, "teaching_contract": "code-then-result-v1",
            "game": {"project_dir": "godot", "source_revision": SHA, "engine": "Godot 4.7.2.stable.official.ed1daf0bf"},
            "files": files, "components": comps, "excerpts": excerpts,
            "exclusions": [{"path": p, "reason": r} for p, r in EXCLUSIONS.items()],
            "code_result_pairs": pairs}
    (REEL / "gamedev-evidence.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"gamedev-evidence.json: {len(files)} files, {len(EXCLUSIONS)} exclusions, {len(comps)} components, "
          f"{len(excerpts)} excerpts, {len(pairs)} code/result pairs")


if __name__ == "__main__":
    main()

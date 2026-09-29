#!/usr/bin/env python3
"""Generate image candidates with FLUX.1-schnell (mflux, local) and log one sidecar per seed.

    gen/.venv-art/bin/python gen/art_generate.py gen/prompts/ART-PC-01.json --seeds 11 23 37 41 59 73
"""
import argparse, json, subprocess, time
from importlib.metadata import version
from pathlib import Path
from common import ROOT, new_run_id, rel, thumbnail_image, write_sidecar

ap = argparse.ArgumentParser()
ap.add_argument("spec")
ap.add_argument("--seeds", type=int, nargs="+", required=True)
ap.add_argument("--prompt-override", help="replace the prompt for a targeted re-generation (logged verbatim)")
a = ap.parse_args()
spec = json.loads(Path(a.spec).read_text())
prompt = a.prompt_override or spec["prompt"]

for seed in a.seeds:
    run_id = new_run_id(spec["asset_id"], seed)
    out = ROOT / "gen" / "raw" / spec["asset_id"] / f"{run_id}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["mflux-generate", "--model", "schnell", "--prompt", prompt, "--seed", str(seed),
           "--steps", str(spec.get("steps", 4)), "--width", str(spec["width"]), "--height", str(spec["height"]),
           "--quantize", str(spec.get("quantize", 4)), "--output", str(out)]
    t0 = time.time()
    subprocess.run(cmd, check=True, cwd=ROOT / "gen")
    thumb = thumbnail_image(out, spec["asset_id"], run_id)
    side = write_sidecar({
        "asset_id": spec["asset_id"], "run_id": run_id,
        "model": "black-forest-labs/FLUX.1-schnell", "model_version": f"mflux {version('mflux')}, {spec.get('quantize', 4)}-bit",
        "license": "Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction",
        "prompt": prompt, "negative_prompt": spec.get("negative_prompt", ""),
        "settings": {"seed": seed, "width": spec["width"], "height": spec["height"], "steps": spec.get("steps", 4),
                     "quantize": spec.get("quantize", 4), "seconds": round(time.time() - t0, 1)},
        "raw_outputs": [rel(out)], "thumbnail": rel(thumb), "storyboard_panels": spec["storyboard_panels"],
    })
    print(side)

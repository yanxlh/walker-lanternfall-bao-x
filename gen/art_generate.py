#!/usr/bin/env python3
"""Generate image candidates with FLUX.1-schnell (mflux, local) and log one sidecar per image.

The model is loaded once per invocation and reused for every pose x seed.

    gen/.venv-art/bin/python gen/art_generate.py gen/prompts/ART-PC-01.json --seeds 11 23
    gen/.venv-art/bin/python gen/art_generate.py gen/prompts/ART-PC-01.json --seeds 5 --poses hurt defeat
    gen/.venv-art/bin/python gen/art_generate.py gen/prompts/ART-EN-01.json --seeds 3 7 9

A spec either has one "prompt", or a "template" containing {pose} plus a "poses" list of
{"name": ..., "text": ...}; the full expanded prompt is what gets logged.
"""
import argparse
import json
import time
from importlib.metadata import version
from pathlib import Path

from common import ROOT, new_run_id, rel, thumbnail_image, write_sidecar

ap = argparse.ArgumentParser()
ap.add_argument("spec")
ap.add_argument("--seeds", type=int, nargs="+", required=True)
ap.add_argument("--poses", nargs="*", help="only these pose names (default: all)")
a = ap.parse_args()
spec = json.loads(Path(a.spec).read_text())

if "poses" in spec:
    jobs = [(p["name"], spec["template"].format(pose=p["text"])) for p in spec["poses"] if not a.poses or p["name"] in a.poses]
else:
    jobs = [(None, spec["prompt"])]

from mflux.models.common.config.model_config import ModelConfig
from mflux.models.flux.variants.txt2img.flux import Flux1

quantize = spec.get("quantize", 4)
flux = Flux1(model_config=ModelConfig.schnell(), quantize=quantize)

for pose, prompt in jobs:
    for seed in a.seeds:
        run_id = new_run_id(spec["asset_id"], seed) + (f"-{pose}" if pose else "")
        out = ROOT / "gen" / "raw" / spec["asset_id"] / f"{run_id}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        image = flux.generate_image(seed=seed, prompt=prompt, num_inference_steps=spec.get("steps", 4),
                                    width=spec["width"], height=spec["height"])
        image.save(path=str(out))
        thumb = thumbnail_image(out, spec["asset_id"], run_id)
        settings = {"seed": seed, "width": spec["width"], "height": spec["height"], "steps": spec.get("steps", 4),
                    "quantize": quantize, "seconds": round(time.time() - t0, 1)}
        if pose:
            settings["pose"] = pose
        side = write_sidecar({
            "asset_id": spec["asset_id"], "run_id": run_id,
            "model": "black-forest-labs/FLUX.1-schnell", "model_version": f"mflux {version('mflux')} (Python API), {quantize}-bit",
            "license": "Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction",
            "prompt": prompt, "negative_prompt": spec.get("negative_prompt", ""),
            "settings": settings, "raw_outputs": [rel(out)], "thumbnail": rel(thumb),
            "storyboard_panels": spec["storyboard_panels"],
        })
        print(side.name, settings["seconds"], "s", flush=True)

# SOURCES

`walker-lanternfall-bao-x` · Bao Xing · CSYE 7270 Assignment 2

Everything in this repository is original to this project or was generated for it by the local models below. The per-run record — prompt, settings, seed, decision, reason, every edit, file path, storyboard panel — is [ASSET-LOG.md](ASSET-LOG.md) (rendered from the JSON sidecars in `gen/log/`). Rejected results are kept as thumbnails and contact sheets in `gen/thumbs/` and `gen/rejected/`.

## Starting point

- A **blank Godot 4.7.2 project**; no code or assets were copied from a starter.
- The protagonist concept (the Lamp-Head Courier) comes from my Assignment 1, [yanxlh/walker-jumpman-bao-x](https://github.com/yanxlh/walker-jumpman-bao-x), which extended [nikbearbrown/walker-jumpman](https://github.com/nikbearbrown/walker-jumpman). No file from either repository is included here.

## Generative models (all run locally on a MacBook, Apple M4 Pro, 16 GB, macOS 26)

| Model | Exact revision | Runtime | Licence / terms | Used for |
|---|---|---|---|---|
| [black-forest-labs/FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell) | `741f7c3` | mflux 0.20.0 (MLX 0.32.2) Python API; 4-bit copy saved locally with `mflux-save` | Apache-2.0 | ART-PC-01, ART-EN-01, ART-EN-02, ART-ENV-01, ART-ENV-02, ART-FX-01, ART-FX-02, ART-FX-03, ART-PK-01 |
| [stabilityai/stable-audio-open-1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0) | `f21265c` | diffusers 0.40.0, torch 2.14.0 (MPS), fp32; sampler fix in `gen/sfx_sampler_fix.py` | Stability AI Community License (free for non-commercial use and for organisations under USD 1 M revenue; outputs owned by the user) — accepted on Hugging Face by Bao | SFX-01 … SFX-06b |
| [facebook/musicgen-medium](https://huggingface.co/facebook/musicgen-medium) | `d3bd7b0` | transformers 5.17.0, torch 2.14.0 (MPS), fp16 | weights CC-BY-NC-4.0 (non-commercial; this is non-commercial coursework); AudioCraft code MIT | MUS-01, MUS-02 |
| [facebook/musicgen-melody](https://huggingface.co/facebook/musicgen-melody) | `68d653a` | same as above | weights CC-BY-NC-4.0 | first MUS-02 batch only — all four rejected, none shipped |

No paid service, API key or school-hosted generator was used. FLUX.1-schnell is guidance-distilled and takes no negative prompt; exclusions are written into its positive prompts, as each log entry notes.

## What the prompts never contain

No living artist's name or style, no copyrighted character, no brand, no existing song or recording (no stem splitting, no audio-to-audio from a real track), no real person's voice. MUS-02 was generated from text only; the melody-conditioned attempt used this project's own MUS-01 as its condition.

## Processing tools (all local, all edits logged)

| Tool | Version | Role |
|---|---|---|
| Godot | 4.7.2.stable.official.ed1daf0bf | the game; also rasterises the storyboard SVGs for comparison |
| Python (via uv 0.12.19) | 3.12 | pipeline scripts in `gen/`, `design/`, `scripts/` |
| Pillow · numpy · scipy | 12.3.0 · 2.5.3 · 1.18.1 | figure detection, background keying, Lab palette lock, seamless tiling |
| librosa · soundfile | 1.0.0 · 0.14.0 | beat tracking, bar-aligned loops, crossfades, SFX trimming, OGG Vorbis encoding (libsndfile) |
| matplotlib | 3.11.2 | waveform/spectrogram thumbnails for audio log entries |
| torchsde | 0.2.6 | Brownian noise for Stable Audio Open's sampler |

## Other material

- **Font:** Godot's built-in default font (bundled with the engine), used by the HUD.
- **Storyboard, character blockout and palettes:** drawn by scripts in `design/` from simple shapes; no generated or external art.
- **Code and documents:** written for this project with Claude (Anthropic) as a coding assistant; Claude is not an asset generator here. Who did what is in [FRICTIONAL.md](FRICTIONAL.md) and the README.

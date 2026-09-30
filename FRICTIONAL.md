# FRICTIONAL — how this slice actually got made

`walker-lanternfall-bao-x` · Bao Xing · CSYE 7270 Assignment 2

A daily diary, written on the day, of every attempt: **what I wanted, what came back, what I decided.** The "From the logs" bullets under each day are facts pulled from git, the ledger and ASSET-LOG so dates and numbers are exact; the rest is in my own words.

Who did what, in one line: I made the design decisions and every accept/reject call and did the playtests; Claude drafted documents, wrote the Godot code, tests and generation scripts, and ran the local models; FLUX.1-schnell, Stable Audio Open and MusicGen produced the raw art, sound and music.

---

## 2026-09-28 (Mon) — choosing the game, freezing the design

**From the logs**
- Started from a blank Godot 4.7.2 project instead of extending the A1 platformer; the Lamp-Head Courier carried over as the protagonist.
- Genre chosen: a survivors-like (auto-firing weapons, waves, XP gems, level-up cards). Scope chosen for the slice: 2 weapons with branching upgrades + 1 evolution (Sunflare Lighthouse), 3-minute runs.
- Models chosen: all local and open (FLUX.1-schnell, Stable Audio Open 1.0, MusicGen).
- CONCEPT, STORYBOARD (9 panels), CHARACTER-SHEET (12-pose blockout) and CHANGE-BRIEF committed; tag `design-v1` at 2026-09-28 15:21 EDT, before any generation.
- The first blockout script produced silhouettes that could not be told apart at 32 px (idle vs turn_side, levelup vs victory); poses were redrawn before the tag.

**What I wanted**

_Bao writes here._

**What came back**

_Bao writes here._

**What I decided, and why**

_Bao writes here._

---

## 2026-09-29 (Tue) — greybox, the aiming problem, and the first images

**From the logs**
- Greybox game built with 85 automated checks (logic 26, gameplay 37, audio 22).
- Balance probe with scripted bots: with the Beam firing along the direction of travel, bots died in 22–98 s at level 1–3 with 4–15 kills — running away pointed the Beam away from the enemies. Tuning-only fix (slower moths, more HP): still ≤ 22 kills. Nearest-enemy aim with the original tuning: 64–296 kills, one bot survived 3:00. I chose nearest-enemy aim → CONCEPT R1.
- Hugging Face licence acceptance was needed for FLUX.1-schnell and Stable Audio Open before download.
- MusicGen on CPU produced no 30 s clip in 19 minutes; moved to the Apple GPU (MPS): a 5 s clip in 67 s.
- First ART-PC-01 batch (FLUX, "flat vector" prompt, seeds 11 / 23 / 37): the character identity was consistent, but it came out as a shaded, 3D-looking illustration, FLUX ignored the requested 3 × 4 grid, and most figures were standing. I rejected all three: "不用3d就是2d像素游戏，然后不用太多动作" → CONCEPT R2 / CHARACTER-SHEET R2: 2D pixel art, 10 poses (the rubric minimum).
- Reducing a generated sprite to 32 px first turned the navy coat into black and the floor shadow into cream; the processing now keys out grey shadows and matches colours in Lab space.
- Running FLUX with one model kept loaded for many images looked fast at first (~40 s per image) and then collapsed: 53 s → 345 s → 1505 s → 6620 s. The process held 12 GB on a 16 GB Mac and lived in swap. Fix: a 4-bit copy of the model saved locally (9 GB), MLX's cache capped and cleared after every image, and one process per pose; active memory now stays at 9.6 GB.
- Pixel-art ART-PC-01: 10 poses x 2 seeds (+1 earlier test). At game size the frames were scaled to fill 32 px, so the lamp changed size from pose to pose; the processing now scales every frame so the lamp is 12 px. I took s11 for 8 poses and s23 for hurt and defeat, and had the defeat lamp recoloured brown because FLUX kept it lit.
- The other 8 sprites: 3 seeds each, judged on a mock 640 x 360 scene built from the candidates. Rejects included a stall sign with text-like marks, a beam too thin to survive 16 x 8, and two ground tiles that failed the seam check. By the end of the day: 48 art runs logged, 30 rejected with a reason.
- Contrast check against the ground: moth 0.40, courier 0.11, fog-wraith **0.03** — the wraith nearly disappears on the cobbles (prediction 4). Left for the muted playtest.
- MusicGen in fp32 grew to 14 GB and stalled in swap (first 30 s clip unfinished after 19 minutes); switched to fp16 on the GPU: a 10 s clip in 28 s.
- Music, same evening: four MUS-01 loops (MusicGen medium, 96 BPM prompt), each looped three times for listening. I kept the first one — "剩下的太乱了，后面的杂音太多". Measurements agreed: it had the steadiest beat, no fade-out ending and the least high-frequency energy.
- MUS-02 took two batches. The melody-conditioned model ignored the tempo (≈106 BPM) and one run was mostly hiss; Claude rejected those four on the measurements (I did not listen to them). The second batch used the same model as MUS-01; I listened to three base+layer mixes and chose s34 because "有种远古的感觉".
- The course email on audio (generate something every day, record rejections, trim/loop and listen ≥ 3 times, log every edit) arrived today; this diary starts using that structure.

**What I wanted**

_Bao writes here._

**What came back**

_Bao writes here._

**What I decided, and why**

_Bao writes here._

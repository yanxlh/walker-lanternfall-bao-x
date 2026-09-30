# FRICTIONAL — how this slice actually got made

`walker-lanternfall-bao-x` · Bao Xing · CSYE 7270 Assignment 2

A daily diary of every attempt: **what I wanted, what came back, what I decided.** The "From the logs" bullets are facts pulled from git, the ledger and ASSET-LOG so dates and numbers are exact. The three sections under each day were drafted by Claude from our working session — my own choices, and my own words in quotation marks where I gave a reason — and then checked by me; where I simply accepted a recommendation, the entry says so.

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

A game I would actually keep building this semester, not just an asset test. Instead of extending the A1 platformer, I wanted something like the Steam survivors games — "类似于一个steam游戏那种吸血鬼幸存者这种": several weapons to choose from, upgrades that branch in more than one direction, and two weapons that fuse into a super weapon once both are maxed ("两个武器升级到满级之后可以合成超级武器"). For the theme I chose option 1: my A1 character, the Lamp-Head Courier, in a fog-bound night market.

**What came back**

The real pushback was scope: every extra weapon means more art, more sounds, more de-duplication rules, more storyboard panels and more tests, with six days left and a 4K film still to make. Claude's first blockout of the character also failed its own silhouette test at 32 px — idle and turn-side, and level-up and victory, were the same black shape — and had to be redrawn before the design could be frozen.

**What I decided, and why**

- Scope for this slice: **2 weapons + 1 evolution** (Beam and Lamp-Moths, three levels each, fusing into the Sunflare Lighthouse); more weapons and recipes are written into CONCEPT as the semester goal.
- **All local, open models** (FLUX.1-schnell, Stable Audio Open, MusicGen) — I took the recommended option: every seed and setting can be logged, and nothing depends on download caps or paid credits.
- For the character art I chose approach A of the three Claude proposed: generate, then reduce to game size and **lock to a fixed palette**, so consistency is enforced by a script rather than hoped for.
- I read the four design documents and approved them unchanged, chose not to add hand-drawn panels, and made the repository **public**. The design was tagged `design-v1` before anything was generated.

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
- Stable Audio Open would not finish a single sound: RecursionError inside the sampler. A first guess (MPS float32 precision) was wrong; reproducing the sampler alone showed it fails on CPU too, always on the last step, where it asks for noise between sigma 0.3 and 0 — outside the range its noise tree was built for. That noise is multiplied by zero in that step, so `gen/sfx_sampler_fix.py` returns zeros there. Each sound still costs ~4.6 minutes, because the model always renders a ~47 s window and crops it.
- The course email on audio (generate something every day, record rejections, trim/loop and listen ≥ 3 times, log every edit) arrived today; this diary starts using that structure.

**What I wanted**

A greybox that plays like the design says — you only move, and the light does the fighting — and then real generated art and music in it by the end of the day. After Nick's email arrived that afternoon, also to follow it: generate something every day, listen, reject, and log it.

**What came back**

- The design itself had a hole. With the Beam firing where I walk, running away aimed it away from the enemies; the test bots died within 22–98 seconds. Tuning alone did not fix it. Aiming at the nearest enemy did.
- The first character images looked like a shaded 3D illustration, not a 2D pixel game, and FLUX ignored the pose grid. When the style was switched to pixel art, each pose came out well but the lamp changed size from frame to frame at 32 px until the processing normalised it.
- Some candidates had problems I would not have noticed at full size: a market stall with text-like marks on its sign, a beam so thin it vanished at 16 × 8, ground tiles whose seams showed when tiled, and a fog-wraith that almost disappears on the cobbles.
- Music: of four night-market loops, three sounded messy to me. The first attempt at the Sunflare layer came out at the wrong tempo or as hiss; the second batch worked.
- A lot of the day went into the machine rather than the art: FLUX and MusicGen both filled my 16 GB of memory and stalled in swap until they were reconfigured, and Stable Audio Open would not finish a single sound until a sampler bug was found and worked around.

**What I decided, and why**

- **Beam aims at the nearest enemy** — I chose this after seeing the bot results; it keeps "feet, not fingers" true (CONCEPT R1).
- **2D pixel art, and only as many poses as needed**: "不用3d就是2d像素游戏，然后不用太多动作". The first batch was rejected; the sheet keeps the rubric minimum of 10 poses (CONCEPT R2, CHARACTER-SHEET R2).
- For the 10 courier frames and the 8 other sprites I looked at the candidate sheets and a mock game screen built from them, and accepted Claude's recommended pick for each; the rejected ones and the reasons are in ASSET-LOG.
- **Music stays local:** I chose MusicGen over Suno (the recommended option — reproducible seeds, no download limit).
- **MUS-01:** I listened to all four loops three times and kept the first — "第一个，剩下的太乱了，后面的杂音太多". After that, the Sunflare layer's prompt was rewritten to avoid shakers and noise.
- **MUS-02:** I listened to three base + layer mixes and chose the first — "因为有种远古的感觉".
- The wraith's low contrast and the courier's small size are left for my muted playtest rather than changed blind (Claude also left the hurtbox size for that playtest).
- The storyboard's camera moves (push-in, tilt on a hit, zoom-out on Sunflare, the fog lifting at 3:00) were missing from the build; I asked for them to be added.

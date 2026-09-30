# ASSET-LOG

Rendered by `gen/render_log.py` from the JSON sidecars in `gen/log/`. Every run is listed, including rejects.
Tag `design-v1` precedes every timestamp below (checked by `scripts/audit_repo.py --stage final`).

## ART-PC-01

![ART-PC-01 contact sheet](gen/rejected/ART-PC-01-contact.png)

### ART-PC-01-20260929T202956Z-s11

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-29T20:36:19+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0, 4-bit |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 11, "width": 1536, "height": 1024, "steps": 4, "quantize": 4, "seconds": 382.6}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **reject** by Bao Xing at 2026-09-29T20:53:50+00:00 |
| Reason | Bao 2026-09-29: rendered as a shaded, 3D-looking illustration instead of 2D pixel art ("不用3d就是2d像素游戏"); FLUX also ignored the 3x4 grid and drew mostly standing poses. Best identity of the batch (brass lamp with spout, satchel, long coat) - kept as the look to carry into the pixel-art prompt. |
| Manual edits | — |
| Project files | — |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260929T202956Z-s11.png) |

**Prompt**

```
character model sheet of one small original courier character repeated in twelve poses, arranged in a neat grid of 3 rows and 4 columns on a plain flat white background, every pose the same character and the same size, full body, side view facing right unless noted. The character: an oversized round brass oil-lamp for a head with a glowing warm yellow glass lens, a narrow dark navy long coat, thin dark legs, a small brown leather satchel on the left hip. Style: simple flat vector shapes, thick uniform dark outline, no gradients, no texture, limited palette of warm yellow, cream, navy, brown and near-black, clean readable silhouette, video game sprite reference. Poses in reading order: front view standing; side view standing; back view standing; relaxed idle; walking with legs apart at contact; walking with legs together passing; arm thrust forward casting a beam of light; flinching backwards hurt; both arms raised cheering; radiant power pose with a large glow halo; collapsed lying on the ground with the lamp dimmed; triumphant victory pose. No text, no letters, no numbers, no labels, no watermark, no background scenery.
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled and mflux does not accept a negative prompt for it; exclusions (text, labels, scenery, gradients) are written into the positive prompt.
```

### ART-PC-01-20260929T203619Z-s23

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-29T20:43:41+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0, 4-bit |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 23, "width": 1536, "height": 1024, "steps": 4, "quantize": 4, "seconds": 442.1}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **reject** by Bao Xing at 2026-09-29T20:53:50+00:00 |
| Reason | Bao 2026-09-29: rendered as a shaded, 3D-looking illustration instead of 2D pixel art ("不用3d就是2d像素游戏"); FLUX also ignored the 3x4 grid and drew mostly standing poses. Also drew 20 figures, a diving-helmet head, one plain human head and one lamp-less silhouette. |
| Manual edits | — |
| Project files | — |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260929T203619Z-s23.png) |

**Prompt**

```
character model sheet of one small original courier character repeated in twelve poses, arranged in a neat grid of 3 rows and 4 columns on a plain flat white background, every pose the same character and the same size, full body, side view facing right unless noted. The character: an oversized round brass oil-lamp for a head with a glowing warm yellow glass lens, a narrow dark navy long coat, thin dark legs, a small brown leather satchel on the left hip. Style: simple flat vector shapes, thick uniform dark outline, no gradients, no texture, limited palette of warm yellow, cream, navy, brown and near-black, clean readable silhouette, video game sprite reference. Poses in reading order: front view standing; side view standing; back view standing; relaxed idle; walking with legs apart at contact; walking with legs together passing; arm thrust forward casting a beam of light; flinching backwards hurt; both arms raised cheering; radiant power pose with a large glow halo; collapsed lying on the ground with the lamp dimmed; triumphant victory pose. No text, no letters, no numbers, no labels, no watermark, no background scenery.
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled and mflux does not accept a negative prompt for it; exclusions (text, labels, scenery, gradients) are written into the positive prompt.
```

### ART-PC-01-20260929T204341Z-s37

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-29T20:49:55+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0, 4-bit |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 37, "width": 1536, "height": 1024, "steps": 4, "quantize": 4, "seconds": 374.0}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **reject** by Bao Xing at 2026-09-29T20:53:50+00:00 |
| Reason | Bao 2026-09-29: rendered as a shaded, 3D-looking illustration instead of 2D pixel art ("不用3d就是2d像素游戏"); FLUX also ignored the 3x4 grid and drew mostly standing poses. Also scattered layout with inconsistent figure sizes. |
| Manual edits | — |
| Project files | — |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260929T204341Z-s37.png) |

**Prompt**

```
character model sheet of one small original courier character repeated in twelve poses, arranged in a neat grid of 3 rows and 4 columns on a plain flat white background, every pose the same character and the same size, full body, side view facing right unless noted. The character: an oversized round brass oil-lamp for a head with a glowing warm yellow glass lens, a narrow dark navy long coat, thin dark legs, a small brown leather satchel on the left hip. Style: simple flat vector shapes, thick uniform dark outline, no gradients, no texture, limited palette of warm yellow, cream, navy, brown and near-black, clean readable silhouette, video game sprite reference. Poses in reading order: front view standing; side view standing; back view standing; relaxed idle; walking with legs apart at contact; walking with legs together passing; arm thrust forward casting a beam of light; flinching backwards hurt; both arms raised cheering; radiant power pose with a large glow halo; collapsed lying on the ground with the lamp dimmed; triumphant victory pose. No text, no letters, no numbers, no labels, no watermark, no background scenery.
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled and mflux does not accept a negative prompt for it; exclusions (text, labels, scenery, gradients) are written into the positive prompt.
```

### ART-PC-01-20260929T205508Z-s11-idle

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-29T20:55:50+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API), 4-bit |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 11, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 41.8, "pose": "idle"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **reject** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Superseded: earlier prompt without 'bright golden brass' gave a brown housing that maps off-palette. |
| Manual edits | — |
| Project files | — |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260929T205508Z-s11-idle.png) |

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, standing relaxed, arms hanging at the sides. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260929T205716Z-s11-turn_front

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-29T20:58:00+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API), 4-bit |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 11, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 44.7, "pose": "turn_front"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **modify** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Chosen for turn_front: large gold lamp, clear front view; s23 figure too small. |
| Manual edits | keyed white bg + grey shadow; mirrored to face right where the lens faced left; scaled so the lamp is 12 px (CHARACTER-SHEET rule 11-13 px), feet on the bottom row, coat centred; reduced 4x-supersampled to 32x32; locked to the 5-colour character palette in Lab space; 1-px ink outline |
| Project files | godot/assets/art/pc_sheet.png |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260929T205716Z-s11-turn_front.png) |

**Processing (every edit, in order)**

1. `{"utc": "2026-09-30T00:41:52+00:00", "tool": "gen/art_process.py", "mapping": "gen/mappings/ART-PC-01.json", "frame": "turn_front", "out": "godot/assets/art/pc_sheet.png", "index": 0, "mirror": false, "recolor": null, "lamp_px": 12.0, "frame_px": [32, 32], "palette": "character", "supersample": 4, "outline": true}`

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Front view, standing straight and facing the viewer, arms at the sides. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260929T205800Z-s23-turn_front

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-29T20:58:37+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API), 4-bit |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 23, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 36.4, "pose": "turn_front"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **reject** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Figure too small in frame; lamp detail lost at 32 px. |
| Manual edits | — |
| Project files | — |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260929T205800Z-s23-turn_front.png) |

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Front view, standing straight and facing the viewer, arms at the sides. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260929T205837Z-s11-idle

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-29T20:59:52+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API), 4-bit |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 11, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 75.8, "pose": "idle"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **modify** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Chosen for idle: 'bright golden brass' prompt keeps the housing gold, matches the palette. |
| Manual edits | keyed white bg + grey shadow; mirrored to face right where the lens faced left; scaled so the lamp is 12 px (CHARACTER-SHEET rule 11-13 px), feet on the bottom row, coat centred; reduced 4x-supersampled to 32x32; locked to the 5-colour character palette in Lab space; 1-px ink outline |
| Project files | godot/assets/art/pc_sheet.png |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260929T205837Z-s11-idle.png) |

**Processing (every edit, in order)**

1. `{"utc": "2026-09-30T00:41:52+00:00", "tool": "gen/art_process.py", "mapping": "gen/mappings/ART-PC-01.json", "frame": "idle", "out": "godot/assets/art/pc_sheet.png", "index": 1, "mirror": true, "recolor": null, "lamp_px": 12.0, "frame_px": [32, 32], "palette": "character", "supersample": 4, "outline": true}`

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, standing relaxed, arms hanging at the sides. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260929T205952Z-s23-idle

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-29T21:01:17+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API), 4-bit |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 23, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 84.6, "pose": "idle"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **reject** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Diving-helmet look and small figure; inconsistent with the s11 set. |
| Manual edits | — |
| Project files | — |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260929T205952Z-s23-idle.png) |

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, standing relaxed, arms hanging at the sides. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260929T210117Z-s11-walk_contact

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-29T21:03:01+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API), 4-bit |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 11, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 104.1, "pose": "walk_contact"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **modify** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Chosen for walk_contact: legs apart, same identity as the other s11 frames. |
| Manual edits | keyed white bg + grey shadow; mirrored to face right where the lens faced left; scaled so the lamp is 12 px (CHARACTER-SHEET rule 11-13 px), feet on the bottom row, coat centred; reduced 4x-supersampled to 32x32; locked to the 5-colour character palette in Lab space; 1-px ink outline |
| Project files | godot/assets/art/pc_sheet.png |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260929T210117Z-s11-walk_contact.png) |

**Processing (every edit, in order)**

1. `{"utc": "2026-09-30T00:41:52+00:00", "tool": "gen/art_process.py", "mapping": "gen/mappings/ART-PC-01.json", "frame": "walk_contact", "out": "godot/assets/art/pc_sheet.png", "index": 2, "mirror": true, "recolor": null, "lamp_px": 12.0, "frame_px": [32, 32], "palette": "character", "supersample": 4, "outline": true}`

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, walking mid-stride, front leg forward and back leg behind, legs wide apart. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260929T210301Z-s23-walk_contact

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-29T21:03:54+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API), 4-bit |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 23, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 53.2, "pose": "walk_contact"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **reject** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Drew an extra floating lamp beside the character. |
| Manual edits | — |
| Project files | — |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260929T210301Z-s23-walk_contact.png) |

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, walking mid-stride, front leg forward and back leg behind, legs wide apart. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260929T210354Z-s11-walk_passing

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-29T21:09:39+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API), 4-bit |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 11, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 345.1, "pose": "walk_passing"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **modify** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Chosen for walk_passing: knee raised, reads as the second walk frame. |
| Manual edits | keyed white bg + grey shadow; mirrored to face right where the lens faced left; scaled so the lamp is 12 px (CHARACTER-SHEET rule 11-13 px), feet on the bottom row, coat centred; reduced 4x-supersampled to 32x32; locked to the 5-colour character palette in Lab space; 1-px ink outline |
| Project files | godot/assets/art/pc_sheet.png |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260929T210354Z-s11-walk_passing.png) |

**Processing (every edit, in order)**

1. `{"utc": "2026-09-30T00:41:52+00:00", "tool": "gen/art_process.py", "mapping": "gen/mappings/ART-PC-01.json", "frame": "walk_passing", "out": "godot/assets/art/pc_sheet.png", "index": 3, "mirror": true, "recolor": null, "lamp_px": 12.0, "frame_px": [32, 32], "palette": "character", "supersample": 4, "outline": true}`

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, walking, one knee raised, legs passing each other. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260929T210939Z-s23-walk_passing

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-29T21:34:45+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API), 4-bit |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 23, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 1505.8, "pose": "walk_passing"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **reject** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Drew an extra lamp on a stand beside the character. |
| Manual edits | — |
| Project files | — |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260929T210939Z-s23-walk_passing.png) |

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, walking, one knee raised, legs passing each other. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260929T213445Z-s11-cast

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-29T23:25:06+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API), 4-bit |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 11, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 6620.6, "pose": "cast"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **modify** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Chosen for cast: arm thrust forward, reads as casting. |
| Manual edits | keyed white bg + grey shadow; mirrored to face right where the lens faced left; scaled so the lamp is 12 px (CHARACTER-SHEET rule 11-13 px), feet on the bottom row, coat centred; reduced 4x-supersampled to 32x32; locked to the 5-colour character palette in Lab space; 1-px ink outline |
| Project files | godot/assets/art/pc_sheet.png |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260929T213445Z-s11-cast.png) |

**Processing (every edit, in order)**

1. `{"utc": "2026-09-30T00:41:52+00:00", "tool": "gen/art_process.py", "mapping": "gen/mappings/ART-PC-01.json", "frame": "cast", "out": "godot/assets/art/pc_sheet.png", "index": 4, "mirror": true, "recolor": null, "lamp_px": 12.0, "frame_px": [32, 32], "palette": "character", "supersample": 4, "outline": true}`

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, one arm stretched straight forward, pointing and casting light. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260930T002916Z-s23-cast

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-30T00:29:52+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API); 4-bit copy saved locally with mflux-save from FLUX.1-schnell @ 741f7c3 |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 23, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 35.7, "peak_gb": 12.75, "pose": "cast"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **reject** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Extra floating orb and a green lens; off-identity. |
| Manual edits | — |
| Project files | — |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260930T002916Z-s23-cast.png) |

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, one arm stretched straight forward, pointing and casting light. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260930T002952Z-s23-hurt

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-30T00:30:50+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API); 4-bit copy saved locally with mflux-save from FLUX.1-schnell @ 741f7c3 |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 23, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 57.7, "peak_gb": 12.75, "pose": "hurt"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **modify** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Chosen for hurt: leaning back with a leg lifted, the clearest recoil. |
| Manual edits | keyed white bg + grey shadow; mirrored to face right where the lens faced left; scaled so the lamp is 12 px (CHARACTER-SHEET rule 11-13 px), feet on the bottom row, coat centred; reduced 4x-supersampled to 32x32; locked to the 5-colour character palette in Lab space; 1-px ink outline |
| Project files | godot/assets/art/pc_sheet.png |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260930T002952Z-s23-hurt.png) |

**Processing (every edit, in order)**

1. `{"utc": "2026-09-30T00:41:52+00:00", "tool": "gen/art_process.py", "mapping": "gen/mappings/ART-PC-01.json", "frame": "hurt", "out": "godot/assets/art/pc_sheet.png", "index": 5, "mirror": true, "recolor": null, "lamp_px": 12.0, "frame_px": [32, 32], "palette": "character", "supersample": 4, "outline": true}`

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, recoiling backwards in pain, leaning back, one leg lifted. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260930T003050Z-s23-levelup

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-30T00:32:00+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API); 4-bit copy saved locally with mflux-save from FLUX.1-schnell @ 741f7c3 |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 23, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 70.6, "peak_gb": 12.76, "pose": "levelup"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **reject** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Figure too small; the raised arms vanish at 32 px. |
| Manual edits | — |
| Project files | — |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260930T003050Z-s23-levelup.png) |

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, cheering with both arms raised high above the head. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260930T003238Z-s11-hurt

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-30T00:33:14+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API); 4-bit copy saved locally with mflux-save from FLUX.1-schnell @ 741f7c3 |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 11, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 36.0, "peak_gb": 12.75, "pose": "hurt"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **reject** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Recoil less readable than the s23 hurt at 32 px. |
| Manual edits | — |
| Project files | — |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260930T003238Z-s11-hurt.png) |

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, recoiling backwards in pain, leaning back, one leg lifted. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260930T003317Z-s11-levelup

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-30T00:33:55+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API); 4-bit copy saved locally with mflux-save from FLUX.1-schnell @ 741f7c3 |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 11, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 37.5, "peak_gb": 12.75, "pose": "levelup"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **modify** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Chosen for levelup: raised arm and big lamp read at 32 px; s23 figure too small. |
| Manual edits | keyed white bg + grey shadow; mirrored to face right where the lens faced left; scaled so the lamp is 12 px (CHARACTER-SHEET rule 11-13 px), feet on the bottom row, coat centred; reduced 4x-supersampled to 32x32; locked to the 5-colour character palette in Lab space; 1-px ink outline |
| Project files | godot/assets/art/pc_sheet.png |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260930T003317Z-s11-levelup.png) |

**Processing (every edit, in order)**

1. `{"utc": "2026-09-30T00:41:52+00:00", "tool": "gen/art_process.py", "mapping": "gen/mappings/ART-PC-01.json", "frame": "levelup", "out": "godot/assets/art/pc_sheet.png", "index": 6, "mirror": true, "recolor": null, "lamp_px": 12.0, "frame_px": [32, 32], "palette": "character", "supersample": 4, "outline": true}`

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, cheering with both arms raised high above the head. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260930T003358Z-s11-sunflare

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-30T00:34:37+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API); 4-bit copy saved locally with mflux-save from FLUX.1-schnell @ 741f7c3 |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 11, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 39.4, "peak_gb": 12.75, "pose": "sunflare"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **modify** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Chosen for sunflare: arms spread wide around a big glowing lamp. |
| Manual edits | keyed white bg + grey shadow; mirrored to face right where the lens faced left; scaled so the lamp is 12 px (CHARACTER-SHEET rule 11-13 px), feet on the bottom row, coat centred; reduced 4x-supersampled to 32x32; locked to the 5-colour character palette in Lab space; 1-px ink outline |
| Project files | godot/assets/art/pc_sheet.png |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260930T003358Z-s11-sunflare.png) |

**Processing (every edit, in order)**

1. `{"utc": "2026-09-30T00:41:52+00:00", "tool": "gen/art_process.py", "mapping": "gen/mappings/ART-PC-01.json", "frame": "sunflare", "out": "godot/assets/art/pc_sheet.png", "index": 7, "mirror": true, "recolor": null, "lamp_px": 12.0, "frame_px": [32, 32], "palette": "character", "supersample": 4, "outline": true}`

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, arms spread wide to both sides, the lamp head blazing with bright rays of light. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260930T003437Z-s23-sunflare

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-30T00:35:21+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API); 4-bit copy saved locally with mflux-save from FLUX.1-schnell @ 741f7c3 |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 23, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 43.7, "peak_gb": 12.75, "pose": "sunflare"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **reject** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Small figure, no spread-arms power pose. |
| Manual edits | — |
| Project files | — |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260930T003437Z-s23-sunflare.png) |

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, arms spread wide to both sides, the lamp head blazing with bright rays of light. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260930T003525Z-s11-defeat

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-30T00:36:14+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API); 4-bit copy saved locally with mflux-save from FLUX.1-schnell @ 741f7c3 |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 11, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 49.6, "peak_gb": 12.75, "pose": "defeat"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **reject** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Reads as sitting, not collapsed. |
| Manual edits | — |
| Project files | — |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260930T003525Z-s11-defeat.png) |

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Collapsed, lying flat on the ground on its side, the lamp head dark and unlit. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260930T003614Z-s23-defeat

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-30T00:37:16+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API); 4-bit copy saved locally with mflux-save from FLUX.1-schnell @ 741f7c3 |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 23, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 61.7, "peak_gb": 12.75, "pose": "defeat"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **modify** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Chosen for defeat: lying flat reads as collapsed; FLUX left the lamp lit despite the prompt. |
| Manual edits | keyed white bg + grey shadow; mirrored to face right where the lens faced left; scaled so the lamp is 12 px (CHARACTER-SHEET rule 11-13 px), feet on the bottom row, coat centred; reduced 4x-supersampled to 32x32; locked to the 5-colour character palette in Lab space; 1-px ink outline; hand edit: lamp gold and cream recoloured to satchel brown so the lamp reads as out |
| Project files | godot/assets/art/pc_sheet.png |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260930T003614Z-s23-defeat.png) |

**Processing (every edit, in order)**

1. `{"utc": "2026-09-30T00:41:52+00:00", "tool": "gen/art_process.py", "mapping": "gen/mappings/ART-PC-01.json", "frame": "defeat", "out": "godot/assets/art/pc_sheet.png", "index": 8, "mirror": true, "recolor": {"#F2B84B": "#8A5A3C", "#FFF1C9": "#8A5A3C"}, "lamp_px": 12.0, "frame_px": [32, 32], "palette": "character", "supersample": 4, "outline": true}`

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Collapsed, lying flat on the ground on its side, the lamp head dark and unlit. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260930T003720Z-s11-victory

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-30T00:38:17+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API); 4-bit copy saved locally with mflux-save from FLUX.1-schnell @ 741f7c3 |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 11, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 56.9, "peak_gb": 12.75, "pose": "victory"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **modify** by Bao Xing at 2026-09-30T00:41:38+00:00 |
| Reason | Chosen for victory: fist raised, same identity as s11 set. |
| Manual edits | keyed white bg + grey shadow; mirrored to face right where the lens faced left; scaled so the lamp is 12 px (CHARACTER-SHEET rule 11-13 px), feet on the bottom row, coat centred; reduced 4x-supersampled to 32x32; locked to the 5-colour character palette in Lab space; 1-px ink outline |
| Project files | godot/assets/art/pc_sheet.png |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260930T003720Z-s11-victory.png) |

**Processing (every edit, in order)**

1. `{"utc": "2026-09-30T00:41:52+00:00", "tool": "gen/art_process.py", "mapping": "gen/mappings/ART-PC-01.json", "frame": "victory", "out": "godot/assets/art/pc_sheet.png", "index": 9, "mirror": true, "recolor": null, "lamp_px": 12.0, "frame_px": [32, 32], "palette": "character", "supersample": 4, "outline": true}`

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, triumphant, one fist punched high into the air, feet planted wide. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```

### ART-PC-01-20260930T003817Z-s23-victory

| Field | Value |
|---|---|
| Created (UTC) | 2026-09-30T00:39:10+00:00 |
| Model / version | black-forest-labs/FLUX.1-schnell / mflux 0.20.0 (Python API); 4-bit copy saved locally with mflux-save from FLUX.1-schnell @ 741f7c3 |
| Runtime | local — arm64 macOS 26.6.2 (Apple M4 Pro, 16 GB) |
| Licence / terms | Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction |
| Settings | `{"seed": 23, "width": 512, "height": 512, "steps": 4, "quantize": 4, "seconds": 53.2, "peak_gb": 12.75, "pose": "victory"}` |
| Storyboard panels | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| Decision | **reject** by Bao Xing at 2026-09-30T00:41:39+00:00 |
| Reason | Small figure; no clear triumphant gesture. |
| Manual edits | — |
| Project files | — |
| Thumbnail | ![](gen/thumbs/ART-PC-01/ART-PC-01-20260930T003817Z-s23-victory.png) |

**Prompt**

```
16-bit pixel art video game sprite of one small original character: a courier whose head is an oversized round bright golden brass oil lamp with a glowing warm yellow glass lens and a small spout on top, wearing a long dark navy coat, thin dark legs and a small brown leather satchel on the hip. Side view facing right, triumphant, one fist punched high into the air, feet planted wide. Full body, one single character centered, plain flat white background, crisp hard-edged square pixels, flat 2D colours, limited palette of warm yellow, cream, navy, brown and near-black, 1-pixel dark outline, no 3D rendering, no shading, no gradients, no anti-aliasing, no text, no letters, no watermark
```

**Negative prompt**

```
N/A — FLUX.1-schnell is guidance-distilled; mflux accepts no negative prompt for it. Exclusions (3D shading, gradients, text, background) are written into the positive prompt.
```


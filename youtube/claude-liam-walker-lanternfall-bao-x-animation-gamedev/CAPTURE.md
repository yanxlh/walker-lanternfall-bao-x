# CAPTURE — how the film's new footage was made

Film: `claude-liam-walker-lanternfall-bao-x-animation-gamedev` · game source revision **5f09b7fa0f8555f588d68c9d63a1166d3daa23a1** (`FILM-SOURCE-REVISION.txt`) · Godot 4.7.2.stable.official.ed1daf0bf, GL Compatibility (OpenGL 4.1 Metal), macOS 26, Apple M4.

The film shows one new gameplay take, recorded by Bao on 20 November 2026 with `capture/capture-film-take.command`. Everything else it shows is committed repository material: Bao's 30 fps fixture strips (`captures/dash/r1`, `captures/dash/r2`, `captures/walk/r1`), the sheet, and recorded tool output, listed in SOURCES.md. Nothing is drawn, re-enacted or retimed; replays are labelled on screen.

## Isolated copy, never the repository

`capture-film-take.command` unpacks `git archive 5f09b7f godot` into `capture/copy/`, sets that copy's `window_width_override` / `window_height_override` from 1280 × 720 to 3840 × 2160 so Movie Maker writes 4K, copies in `capture/film_driver.gd` and `capture/film_main.tscn`, and imports once (`capture/import.log`, no `ERROR` lines).

## The take (`capture/take-dash.avi`)

Driver `capture/film_driver.gd`. It plays Lanternfall through the real input map: every key is an event parsed with `Input.parse_input_event` and flushed before the session's physics step. Disclosed fixtures, printed on every frame: no enemy spawns; seed 1; XP added for one level-up and the card offer set so the Courier's Dash card is first; for each interrupted dash a wraith (hp 9999) placed on the courier for one step and removed the next.

| | |
|---|---|
| Frames | 576 movie frames (3840 × 2160 MJPEG, 30 fps; PCM audio, muted bus), 575 log rows; movie frame N is row N, checked at the level-up screen (row and movie frame 99 show the cards, 100 do not). The extra movie frame is the last one |
| Events (movie frame) | xp added 20; offer set 21; card key 1 at 100; dashes start at 220 (no interrupt), 310, 380, 450; hits at 311 (startup frame 2: cancelled, no cooldown, hp 10 → 8), 384 (active frame 8: the dash carries on, hp 8 → 6), 458 (recovery frame 16: cancelled, cooldown 60, hp 6 → 4) |
| Frame 20 | the level-up opens with the game's own random offer (Thick Glass, Lamp-Moths, Hotter Flame); the fixture's offer shows from frame 21. The film's B11 starts at frame 21 |
| Dry run | the same script headless (`--fixed-fps 30`) → `capture/take-dash-dryrun.jsonl`: identical to the take's log apart from the courier's screen position columns |
| Hash | `capture/takes.sha256` (AVI 381,805,974 bytes) |

How the film uses it: B07 (the walk, frames 106–218, then a labelled replay), B11 (frames 21–250: the card screen, the card key, the first dash), B13 (frames 295–498: the three interrupted dashes). B07 and B13 show a 3x centre crop of the 4K frame, which the camera keeps on the courier; the crop is labelled.

## Not committed

The AVI, the isolated copy and every rendered video (`media/`, `exports/`, `mp3/`) stay out of git (`.gitignore`). The driver, the command, the seed and the source revision regenerate them; the two logs and the hash file are committed.

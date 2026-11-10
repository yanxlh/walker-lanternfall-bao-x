# Visual and audio QC — 9 November 2026

Done by Claude Code on the master (SHA-256 `1a06751d82b91360f93ca3bcf6e4702d447388fd56cabddb77f3ba84ff1e3ded`, 652.1 s). Frames were extracted and read; the audio was measured, not listened to. Bao subsequently confirmed that he watched and listened to the complete revised master. The toolkit's own Gate V report is `REPORT.md` in this folder (64 frames, 0 blocker, 0 major).

## Method

- The master was probed: 3840 × 2160 H.264 at 30 fps, AAC 48 kHz stereo.
- Frames were extracted at 15 %, 50 % and 85 % of every beat (96 frames) and read in four contact sheets.
- Every code beat's notes panel was read enlarged.
- All evidence and Remotion beats were sampled one by one before the master was built.
- Loudness was measured with ffmpeg `ebur128`: integrated −17.9 LUFS, loudness range 3.3 LU, true peak −2.1 dBFS. Narration beats were levelled to −18.6 … −17.2 LUFS; the game-sound beat to −17.6 LUFS.
- `silencedetect` (−50 dB, 1.5 s) found no silence.

## Defects found and fixed

| Where | Defect | Fix |
|---|---|---|
| B04 pilot | the code panel shows 14 lines; lines 33–39 were cut and a highlight fell on an invisible line | excerpt cut to lines 19–32, narration re-voiced |
| B23 | a 17-line excerpt would be cut the same way | excerpt cut to lines 148–161 |
| B27 | the editor screenshots show the Chinese editor UI; a Chinese label rendered as empty boxes | cropped to the profiler rows and graph only; English column labels and captions |
| B28 | body text small | font enlarged, contributions card shortened |
| B08 | footer said 12× crops | corrected to 4× |
| B24 | narration said the GPU copy's life over time matches; the capture shows it turning orange a little sooner | sentence re-voiced; callout shortened to fit its box |
| B24 sheet entry | a background render rewrote beat_sheet.json with B24's old audio fields | restored from the Kokoro timings; B24 rebuilt at 21.59 s |
| B11, B19 | third source note truncated (B11) or tight (B19) | shortened and re-rendered; the master was rebuilt |

## Checked and acceptable

- **Walker cold open and hesitant writer:** "decoration" is struck and replaced by "feedback".
- **Code beats:** every code beat is followed by its result.
- **Labels:** fixture, play-check and profiler material is labelled; held frames and replays are labelled.
- **Text:** no Chinese text anywhere in the film. Bao's words are in English.
- **B20:** the two paused frames are pixel-identical (no warning from the builder).
- **Ending:** Verdict, Your Turn read in full, and the locked outro ("Lanternfall, Sparked Again.", @NikBearBrown, mascot, stock jingle only).

## Human review update

- Bao subsequently confirmed end-to-end viewing and listening.
- This confirmation is the student's report; the automated review remains a sampled visual and measured-audio check.

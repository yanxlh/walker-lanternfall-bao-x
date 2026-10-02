```
Assignment: Assignment 2 - Generate Art, Sound, and Music for Your Game
Student: Bao Xing
Project name: walker-lanternfall-bao-x (game title: Lanternfall)
Game concept in one sentence: A lamp-headed courier is trapped in a fog-bound midnight market, and the light on his shoulders is his only weapon — keep moving, grow the light, and survive three minutes until the fog lifts.
GitHub repository/folder URL: https://github.com/yanxlh/walker-lanternfall-bao-x
Started from: a blank Godot 4.7.2 project. The protagonist (the Lamp-Head Courier) comes from my Assignment 1, yanxlh/walker-jumpman-bao-x, which extended nikbearbrown/walker-jumpman; no files from either were copied.
Submitted commit SHA: given in the Canvas submission comment (a file cannot contain the hash of the commit that contains it); the ZIP is `git archive` of that commit.
Source revision shown in the film: 8a6f9881e0e2858e523d22bb09f1a423695f04e1 — `godot/` is identical at the submitted commit (`git diff 8a6f988 <submitted> -- godot/` is empty).
Godot version and operating system: Godot 4.7.2.stable.official.ed1daf0bf (GL Compatibility) on macOS 26, Apple M4 Pro, 16 GB.
Generative models used (all local, no paid service): FLUX.1-schnell @ 741f7c3 (all 14 art assets); Stable Audio Open 1.0 @ f21265c (7 sound effects); MusicGen-medium @ d3bd7b0 (2 music loops); MusicGen-melody @ 68d653a (one MUS-02 batch, all rejected).
Final film URL and filename: <course media-space link> · claude-liam-walker-lanternfall-bao-x-gamedev.mp4
Final film SHA-256: 585a89d4a1818588e659e20b69f835176d490790bf03f49efec30b5538ddc779
Summary of my work: I chose the game (a survivors-like with two weapons, branching upgrades and one evolution), the theme, the scope and the local-only models, and committed the concept, storyboard, character sheet and change brief before any generation (tag design-v1). I picked every asset that shipped and listened to every sound-effect candidate before choosing (five MUS-02 layer candidates were rejected by an automated check I did not listen to; the log says so). I played the slice twice for the test report (sound on, then muted) and asked for the changes that came out of play: bullets that vanish on a hit, a fuller and then more broken-up map, blocking props, rising XP cost, tougher monsters over time and new cards. Claude wrote the Godot code, tests and generation scripts, ran the models and measured candidates; the documents record who decided what (FRICTIONAL.md).
Known limitations: one map, two weapons and one evolution, no saving; balance tuned only against my play and scripted bots; the fog-wraith has the lowest measured contrast against the ground (readable in my muted run); the r = 10 hurtbox also covers the lower lamp; gamepad bindings exist but are untested (the left stick can skip cards); my two playtests were on build 1b24721, before the final code-review fixes, which are covered by automated tests.
```

# Lanternfall — Particle Effects Change Brief

## Project and scope

This change adds two visual effects to Lanternfall, my 2D survival game set in a midnight market. Effect A confirms an enemy kill. Effect B makes the courier's movement easier to follow. Neither effect changes damage, collision, movement, enemy spawning, progression, input, or state-machine timing.

The current source is this game directory. The working snapshot was copied into the course repository at commit `9fa5d88`; no local `a5` tag or prior shader files are present. The previous asset brief is preserved at `design/CHANGE-BRIEF-assignment-2.md`. `godot/game/session.gd` owns the `enemy_killed(pos: Vector2)` signal, player reference, and game state. `godot/game/game_state.gd` defines MENU, PLAYING, LEVELUP, PAUSED, WON, and LOST. `godot/project.godot` sets a 640 × 360 logical viewport, a 1280 × 720 window, and the GL Compatibility renderer. The existing README records Godot 4.7.2.stable.official.ed1daf0bf; the installed executable was confirmed as the same version on 29 October 2026.

The proposed nodes are CPUParticles2D, retaining the existing renderer. Their property names were read from the installed 4.7.2 runtime before building. CPU particle scale uses `scale_amount_min`, `scale_amount_max`, and `scale_amount_curve`. A separate scratch GPU material will be converted for the required process-shader study; it will not replace the CPU effects or be used by gameplay.

## Alignment with the game design document

The reference is the Assignment 4 Game Design Document, version 0.3, dated 17 October 2026. This change supports P-02, Position over firing, by clarifying movement without adding an attack input. It supports P-03, Readable light, by using warm sparks against the cool market and keeping kill feedback understandable without sound.

Both effects retain the hard-edged pixel-art style and nearest-neighbor filtering described in Graphics and Styling. Avoid soft photographic textures or a large opaque glow. The courier and pickups must remain the brightest sustained objects; A may be briefly bright, while B stays subordinate to them. Check that A does not obscure the lamp-oil gem created by the same kill.

The post office, delivery contracts, persistent settlement improvements, additional couriers, and engineer turrets are planned features in the GDD. This assignment adds presentation to the existing three-minute prototype and does not claim to implement those systems.

## Effect A — Enemy-defeat sparks

### Job and trigger

A small burst of warm sparks marks the exact position where an enemy dies. It helps distinguish a kill from an ordinary hit during crowded play. The existing `Session.enemy_killed(pos)` signal supplies the event and position. The presentation layer listens to this signal and does not call `damage()` or change enemy state.

### Visual intent

- First 0.07 seconds: a compact, bright cluster establishes the event position.
- From 0.07 to 0.20 seconds: sparks spread outward and slow down.
- From 0.20 to 0.45 seconds: sparks shrink and fade completely.
- Use a pale yellow centre and orange dissipation against the dark market floor. Check the effect against bright lantern props and puddles as well as the darkest floor.
- The burst should span about one character height initially and no more than two character heights near its widest point. Judge it at the actual 1280 × 720 window size.
- Speed and size vary between particles. Normal gameplay repeats must not use a fixed seed.
- One spark emitter is sufficient initially. Additional layers require a documented design revision.

### Initial settings

| Part | Setting | Initial value |
|---|---|---|
| Node | type | CPUParticles2D |
| Emission | amount | 16 |
| Emission | one_shot | true |
| Emission | emitting at scene load | false |
| Emission | explosiveness | 1.0 |
| Emission | lifetime | 0.45 s |
| Emission | shape | point |
| Process | direction | (1, 0) |
| Process | spread | 180 degrees |
| Process | initial velocity min / max | 25 / 55 logical pixels per second |
| Process | gravity | (0, 12) |
| Process | damping min / max | 20 / 30 |
| Process | scale_amount_min / scale_amount_max | 0.7 / 1.2 |
| Process | scale curve, normalized time:value | 0:1, 0.2:0.85, 1:0 |
| Process | colour ramp, normalized time:RGBA | 0:(1,0.95,0.65,1), 0.35:(1,0.6,0.2,0.85), 1:(0.65,0.2,0.05,0) |
| Draw | texture | new code-generated 3 × 3 hard-edged pixel spark texture |
| Draw | material | CanvasItemMaterial, additive blend |
| Coordinates | local_coords | false |
| Startup | preprocess | 0 |

Store these settings in `godot/effects/defeat_sparks.tscn`. Commit the texture-generation script and its output; do not modify existing source textures.

### Retrigger and lifecycle rules

Use overlap: every accepted event creates a separate burst at the signal's position. Each burst belongs to a persistent presentation root, not the enemy that is about to be freed. Parent motion must not drag previously emitted sparks.

Permit at most 32 live bursts, for a maximum of 512 allocated particles. When all slots are occupied, ignore additional events until a slot is free. This cap is part of the acceptance rule and must be tested explicitly. Two events 0.10 seconds apart must produce two separate live instances below the cap. No burst fires on scene load. Restart clears all old instances. Burst processing freezes outside PLAYING and resumes without replaying the event.

### Preview and evidence

Use a representative portion of the real market floor with the courier visible for scale. Trigger at frame 10; enable a second event at frame 13 for the retrigger fixture. Capture at 30 fps. Read frames 10, 12, 15, 20, 30, and 50. If first visible emission occurs one frame later, record the offset. Label these captures as fixtures.

The configuration test reads every setting above from the instantiated scene and its resources. The state test drives kills through normal gameplay processing and input, rather than directly calling the presentation trigger. Check event position, no emission at load, two-event overlap, cap behavior, restart cleanup, and survival after the enemy is freed. Visibility and readability require my own check in the running game.

## Effect B — Courier lantern trail

### Job and condition

A short trail of fading embers reinforces the courier's direction of travel without hiding nearby enemies. It is a trail, not a second burst. Read the player position and displacement from the existing session. Emit only while the game is PLAYING, the effect is visible, and the player has actually moved. Stop when any condition ends. Actual position displacement prevents emission while input pushes the player against a blocker.

### Visual intent

- First 0.10 seconds after movement begins: a few embers appear close to the courier's feet.
- During steady movement: embers remain behind in world space, making a short broken trail rather than a continuous beam.
- After stopping: stop spawning immediately; existing particles disappear within 0.35 seconds.
- Keep the trail dimmer and smaller than Effect A. Its length should remain around one to two character heights at normal speed.
- Fade from amber to dark orange while shrinking. Vary particle scale and speed slightly.
- Use a spherical emission region with a 3-pixel radius, a process feature absent from A's point emission.

### Initial settings

| Part | Setting | Initial value |
|---|---|---|
| Node | type | CPUParticles2D |
| Emission | amount | 24 |
| Emission | one_shot | false |
| Emission | emitting at scene load | false |
| Emission | explosiveness | 0 |
| Emission | lifetime | 0.35 s |
| Emission | shape / sphere radius | sphere / 3 logical pixels |
| Process | direction / spread | (0,-1) / 25 degrees |
| Process | initial velocity min / max | 2 / 6 logical pixels per second |
| Process | gravity | (0,-4) |
| Process | damping min / max | 1 / 3 |
| Process | scale_amount_min / scale_amount_max | 0.35 / 0.7 |
| Process | scale curve, normalized time:value | 0:0.7, 0.2:1, 1:0 |
| Process | colour ramp, normalized time:RGBA | 0:(1,0.7,0.25,0.55), 0.5:(0.8,0.35,0.08,0.3), 1:(0.3,0.1,0.02,0) |
| Draw | texture | same code-generated spark texture |
| Draw | material | CanvasItemMaterial, additive blend |
| Coordinates | local_coords | false |
| Startup | preprocess | 0 |

Store these settings in `godot/effects/lantern_trail.tscn`. This effect is not a value-driven feedback loop; runtime code does not change `amount`.

### Pause, hiding, and startup

The first scene frame contains no trail because the player has not moved. Preprocessing is zero intentionally: a movement trail must not appear before movement. Freeze particle simulation during PAUSED and LEVELUP. While hidden, stop emission and allow existing particles to expire when simulation is active. On becoming visible, do not replay movement that happened while hidden. Reset the previous-position sample on restart or teleport so neither creates a streak.

### Preview and evidence

Use the same real background and camera scale. Begin movement at frame 10 and stop at frame 40. Inspect frames 10, 12, 20, 39, 40, 45, 51, and 60 at 30 fps. Separate fixtures cover pause/resume and hidden/visible transitions.

Read back every configured value, including the sphere emission shape. Test movement start/stop, pushing against a blocker, paused and hidden behavior, and restart. Check visually that the trail stays in world space and does not cover the player or obscure enemies.

## Predicted failures and checks

1. An obsolete Godot property name leaves a default value. A configuration read-back test should detect the mismatch. Intentionally rename one A property to a Godot 3 name, run the test, inspect the running effect, record the outcome, and restore it.
2. Scene values drift from this brief. Intentionally alter one A value without changing the brief; the configuration test must fail. Restore the original value afterward.
3. A burst disappears with the killed enemy. A state test must confirm the burst remains alive after the enemy is freed.
4. A second kill restarts the first burst. The rapid-repeat fixture and state test must show two independent instances below the cap.
5. The trail emits while stationary or after a teleport. Test the actual-displacement condition and reset behavior.
6. Yellow sparks disappear against bright props. Compare real captures on dark and bright market backgrounds and record my running-game verdict.

## Performance predictions and budgets

| Effect | Peak allocation | Predicted extra headless CPU time | Predicted extra GPU time | Budget |
|---|---:|---:|---:|---|
| A, 32 overlapping bursts | 512 particles | below 0.8 ms/frame | below 0.5 ms/frame | CPU delta ≤ 1.0 ms and GPU delta ≤ 0.75 ms |
| B, continuous movement | 24 particles | below 0.15 ms/frame | below 0.15 ms/frame | CPU delta ≤ 0.25 ms and GPU delta ≤ 0.25 ms |

These are predictions, not measurements. Compare CPU effects on both CPU and GPU time. Measure an empty-scene control, game with effects off, A at its cap, and B during continuous movement. Report means and spread, hardware, engine, renderer, and source revision. Use the Visual Profiler on a real GPU for off/on GPU comparisons. If this renderer or machine does not expose that measurement, record the limitation rather than relabeling CPU time or FPS as GPU time.

A headless run draws no particles. A GPU-particle process therefore has a near-zero headless processing price by construction; that number cannot establish its on-screen cost. CPU particles still perform CPU processing headlessly. Vsync may make off/on FPS identical even when rendering cost differs.

## Tuning and acceptance

For each effect, preserve a first strip and record my first running-game observation. Make at least one observation-driven revision per effect. Before each edit, record the old and new value and predict the visible difference. Change one setting, recapture, compare, and keep or revert after actual play. If kept, append a dated revision here so the scene, test, and brief agree.

Existing tests must retain their assertions and baseline counts. Effects may read gameplay state but never write it. Existing shaders, collision, movement, inputs, state timing, and source textures stay unchanged. Record results only after the corresponding check is performed.

## Revisions

Revisions are listed below in the order they were made. The design above is the initial record.

### 29 October 2026 — approved event revision and gameplay integration

The confirmed gameplay design now triggers Effect A on every successful weapon hit, including nonlethal hits, rather than only on a kill. The original design above remains as the initial record. The particle values are unchanged; this is an event/design revision, not an observation-driven visual tuning revision. The existing resource and preview filenames `defeat_sparks` are retained to preserve the first fixture and configuration evidence; they now serve the weapon-hit effect.

`Session.damage()` will publish a new read-only `weapon_hit(pos: Vector2)` signal after its existing dead-enemy guard. The listener spawns A at that enemy position. No damage amount, hit detection, cooldown, death order, or input behavior changes. Beam, Lamp-Moths, and Sunflare all use this same existing damage method. The overlap cap remains 32 and includes lethal and nonlethal hits together.

The presentation controller is attached once to Session. It owns transient bursts independently of enemies, clears them on restart and terminal states, and freezes A outside PLAYING. Level-up celebrations use the separate policy below. Tests drive normal physics and real input; fixture setup may seed enemies or place gems but may not invoke the presentation trigger or the damage function directly.

#### Extra effect — level-up celebration

This additional one-shot effect marks each `Session.leveled_up(level)` event at the courier. It does not replace Effect B. It uses CPUParticles2D, 32 particles, one_shot=true, emitting=false at load, lifetime=0.7 s, explosiveness=1, preprocess=0, sphere emission with radius=12, direction=(0,-1), spread=180, initial velocity=35..65, gravity=(0,8), damping=15..25, scale_amount=0.8..1.5, and local_coords=false. Its scale curve is (0,1), (0.25,0.9), (1,0), with the same zero-tangent interpolation as A. Its colour ramp is 0:(1,1,0.8,1), 0.4:(1,0.75,0.2,0.8), 1:(1,0.4,0.05,0). Use the existing generated spark texture, nearest filtering, and an additive CanvasItemMaterial.

It should read as a wider gold celebration around the courier, spread rapidly for the first 0.2 s, then shrink and disappear by 0.7 s. It continues during LEVELUP so the card overlay does not freeze it on its first frame, freezes during PAUSED, and clears on restart, MENU, WON, or LOST. Overlap is allowed up to four celebrations (128 particles), after which further events are ignored until a slot is free. The ordinary A budget remains separate. Predict celebration CPU delta below 0.25 ms/frame and GPU delta below 0.25 ms/frame; budget both at 0.4 ms/frame at four simultaneous bursts. These numbers are unmeasured predictions.

#### Effect B integration details

The approved movement trail uses the settings specified above. Attach its emitter to the presentation root, tracking the courier's global position plus (0,7) logical pixels to place it at the feet. Previously emitted particles stay in world space. Compare actual displacement once per physics frame after Session has stepped. A discontinuity greater than twice the expected per-frame movement plus 4 pixels is treated as a teleport and resets the sample without emission. Stop spawning outside PLAYING; freeze its simulation in PAUSED and LEVELUP. While hidden, stop spawning but allow existing particles to expire whenever the game is PLAYING. Restart clears old particles and resets position history.

Configuration tests read every named setting for all three scenes. State checks cover nonlethal/lethal hits, rapid hit overlap, upgrade celebrations, actual movement, idle, pause, hidden state, and restart. A human still judges whether the effects are visible, distinct, well-sized, and legible behind the card screen and against the real level.


### 29 October 2026 — approved visibility trial r1

Human observation: “The level-up sparks and movement trail are not obvious”. The student approved the following two independent revisions before editing:

- Upgrade celebration: change its draw layer from the world canvas below HUD layer 10 to a dedicated CanvasLayer 11 (`godot/effects/level_up_overlay.tscn`). Synchronize the overlay transform with the world canvas transform so the burst remains aligned with the courier as the camera moves. Its particle settings, lifetime and trigger are unchanged. Predict that it remains visible above the dark upgrade veil and cards instead of being covered.
- Effect B: change only its colour/alpha ramp. At normalized t=0 alpha is 0.95 instead of 0.55; at t=0.5 alpha is 0.70 instead of 0.30; the t=1 alpha remains 0. All RGB values, timing, count, scale and motion remain unchanged. Predict stronger amber visibility from startup through steady movement, with the same stop/fade duration.

This is an approved trial, pending the student's post-change verdict. Earlier source is preserved in `evidence/assignment-6/tuning/r0-source/`. It is source evidence, not a captured frame strip. Before/after windowed captures remain required before claiming a completed tuning cycle.


## 29 October 2026 — approved upgrade portrait anchor

The student requested that upgrade sparks appear on the small character displayed in the upgrade UI instead of at the middle of the screen. This supersedes the earlier world-camera alignment for the celebration only. The shared portrait rectangle is (8,256,96,96); mapping the sprite torso origin (16,23) from its 32-pixel frame gives HUD-local anchor (56,325). The celebration overlay uses the HUD transform, independently of the game camera. The HUD reads the same portrait rectangle as before; its layout and card controls are unchanged. Particle size, count, timing, colour and motion remain unchanged. Movement and hit particles are unchanged. The post-change visual verdict is pending.


### 29 October 2026 — portrait placement kept

The student accepted the upgrade portrait placement after viewing the updated game (“That works”). Keep the celebration at the UI portrait torso, HUD-local (56,325), above the upgrade UI. No additional particle parameter changes are made. The movement-trail visibility trial still awaits its own explicit verdict.


### 29 October 2026 — movement trail accepted

The student explicitly confirmed that the revised movement trail is sufficiently visible. Keep the colour/alpha ramp at alpha 0.95/0.70/0 for t=0/0.5/1, with other values unchanged. This is a running-game verdict. Before/after fixture strips still need to be captured and compared; no such image evidence is claimed by this entry.


### 29 October 2026 — approved Effect A scale trial r1

Observation: the student watched the weapon-hit sparks in the integrated game and reported no problem (“Done; no problem”). The `r0` fixture strip (`captures/defeat_sparks/r0/`) was then read against this brief. The widest point (about 1.6–1.8 courier heights) and the complete fade before 0.45 s match. The initial cluster is smaller than "about one character height": 0.35 courier height on the first visible frame and 0.65 by 0.07 s.

The student approved one change: `scale_amount_max` 1.2 → 1.8. Count, speed, spread, damping, gravity, colour ramp, scale curve, `scale_amount_min` (0.7) and lifetime are unchanged.

Prediction: on the first visible frame the cluster grows from 11 × 12 to about 15 × 15 screen pixels (about 0.45 courier height), with more pure-white pixels. Early sparks are 3–4 pixels wider and the largest sparks are visibly bigger. At 0.20 s the spread stays about 45 pixels wide, with about 1.5 times as many lit pixels. The widest point is about 55–62 pixels, still under two courier heights (68 pixels). Fade timing is unchanged, with no sparks at strip frames 30 and 50. The change is not expected to make the first frame a full character height. A faster initial speed would breach the two-height limit, and sphere emission would remove A's contrast with B.

This is an approved trial, pending the r1 capture comparison and the student's running-game verdict. Pre-change source is preserved in `evidence/assignment-6/tuning/a-r0-source/`.


### 29 October 2026 — Effect A scale r1 kept

The student played the revised game and kept the change (“Keep it; it is clearer”). Effect A's current `scale_amount_max` is 1.8; `scale_amount_min` remains 0.7 and every other value in the initial settings table is unchanged. The scene, `godot/tests/test_defeat_sparks_config.gd` and this entry agree. Comparison: `captures/defeat_sparks/comparison-r0-r1/COMPARISON.md`.

Quoted student feedback in this report is translated into English from the recorded conversation.

---

## 2026-11-09 — 中文修订草稿：我希望玩家怎样读懂这些效果

> 写作说明：这一节由 Codex 根据已有场景、代码和记录，用第一人称中文协助整理，供 Bao 审阅。第一人称表达设计意图，不代表新增的本人试玩证词。上面的原始简报和历次修订完整保留；本节不是开发前写成或提交的文件，不能补造“第一次提示前提交”的时间顺序。当前参数以下表和场景文件为准。

### 我这次要做什么

我想让玩家不用听声音，也能看懂两件事：攻击有没有打中，以及角色正在往哪里走。A 是命中火花，B 是角色脚边的移动余烬。A 原来只想表现击杀，后来已改为每次有效命中，包括没有打死敌人的命中；不能再把它解释成“敌人死亡”的专属提示。

事件来自 `godot/game/session.gd` 的 `weapon_hit(pos)`，在 `damage()` 排除已死亡敌人后发出。`godot/effects/particle_presentation.gd` 只监听事件并创建画面。B 读取 `session.player.global_position`、玩家速度和 `state.current`，比较相邻物理帧的位置；有移动输入但被障碍挡住时，不应该冒出尾迹。

B 是移动尾迹，不是环境效果，也不是数值驱动的反馈循环。我没有把血量或速度映射到 `amount_ratio`。B 使用半径 3 个逻辑像素的球形发射区域（在 2D 中是圆盘），A 从一个点发射；这是两者明确不同的发射特征。“移动尾迹”是画面功能，不表示启用了 GPU 的内建粒子轨迹。

### A：我想看到的命中火花

我希望命中位置先亮一下，让我知道这一击落在哪里；接着散成几颗火星，最后缩小、变暗、消失。它应该短促，不应该变成一团一直亮着的光，掩盖敌人或地上的灯油。

- **起始约 0–0.07 秒：**紧凑的淡黄色亮点标出命中位置。相邻命中可能重叠，但每次命中有自己的火花。
- **约 0.07–0.20 秒：**亮点散开，变成可分辨的黄橙色碎火星，速度逐渐降低。
- **约 0.20–0.45 秒：**火星变深橙、缩小并变透明，结束时不留亮点。

我会在最暗的深蓝石板地面，以及灯笼、摊位亮部和水洼附近判断它，而不是只看编辑器灰底。重点是火星与背景的明暗差，不是“黄色和蓝色不同”就算通过。也要看命中火花会不会和黄色灯油混淆；这是一项待检验的风险，目前不能写成我已经看出的问题。

尺寸用角色作参照，在项目实际的 1280×720 窗口检查。最初目标是起始约一个角色高，最宽不超过两个角色高。已有 r1 帧条测量显示起始仍只有约 0.41 个角色高，所以“起始一个角色高”尚未达到，不能因为后面散得够宽就算满足。

我不想每次都是完全相同的图案：方向、速度和尺寸各有差异，正常游戏不固定随机种子。目前没有额外的随机色相和旋转；颜色随年龄变化不等于每粒随机色相。A 只有一个火星发射器，负责短闪、散开和消退，没有单独的闪光层或烟雾层。如果实际画面说明一个发射器不够，再另立修订，不能写成已经做了多层。

### B：我想看到的移动尾迹

角色一动，脚边就出现几颗小余烬，停下后它们很快消失。我想用它补充移动方向，不想让它抢过角色灯头的注意力。

- **开始移动约 0–0.10 秒：**脚边逐渐出现稀疏的琥珀色小颗粒，不是一下铺满。
- **持续移动：**旧颗粒留在走过的位置，形成断断续续的短线；视觉目标约一至两个角色高，实际长度仍需在游戏窗口检查。
- **停下后 0–0.35 秒：**立即停止出生，已有颗粒继续变暗、缩小并消失；不留下长时间的光路。

我会用与 A 相同的暗地面、亮灯笼、摊位和水洼来检查。B 应该比 A 小、更克制，但不能暗到只在放大截图里看得见。它先略微长大，再缩小，颜色从琥珀变深橙，透明度一路降低；这样不是仅仅把同一个亮点淡出去。速度和尺寸有小范围随机变化。目前一个发射器就负责这条短尾迹，没有独立烟雾层。

### 当前设置：这些值服务于上面的画面目标

A：`godot/effects/defeat_sparks.tscn`；B：`godot/effects/lantern_trail.tscn`。名称沿用历史，A 的触发含义已经改成命中。

| 分类 | 设置 | A 当前值 | B 当前值 |
|---|---|---|---|
| 节点 | 类型、原因 | CPUParticles2D；保留现有 2D Compatibility 渲染路径，小规模粒子 | 同左 |
| 发射 | `amount` | 16 | 24 |
| 发射 | `one_shot` / 初始 `emitting` | true / false | false / false |
| 发射 | `explosiveness` / `lifetime` | 1 / 0.45 秒 | 0 / 0.35 秒 |
| 发射 | 形状 | point（0） | sphere（1），半径 3 逻辑像素 |
| 处理 | `direction` / `spread` | (1,0) / 180° | (0,-1) / 25° |
| 处理 | `initial_velocity_min/max` | 25 / 55 | 2 / 6 |
| 处理 | `gravity` | (0,12) | (0,-4) |
| 处理 | `damping_min/max` | 20 / 30 | 1 / 3 |
| 处理 | `scale_amount_min/max` | 0.7 / 1.8 | 0.35 / 0.7 |
| 处理 | 缩放曲线，归一化年龄:倍率 | 0:1，0.2:0.85，1:0 | 0:0.7，0.2:1，1:0 |
| 处理 | 颜色与透明度，年龄:RGBA | 0:(1,.95,.65,1)；.35:(1,.6,.2,.85)；1:(.65,.2,.05,0) | 0:(1,.7,.25,.95)；.5:(.8,.35,.08,.70)；1:(.3,.1,.02,0) |
| 绘制 | 纹理、过滤 | `res://assets/particles/spark.png`，3×3 硬边火星，nearest | 同左 |
| 绘制 | 材质、混合 | CanvasItemMaterial，additive（blend_mode=1） | 同左 |
| 绘制 | `z_index` | 3 | 1 |
| 坐标 | `local_coords` | false，已出生的粒子留在世界空间 | false，移动时把旧余烬留在身后 |
| 启动 | `preprocess` | 0 | 0，移动前不预先铺出尾迹 |
| 变化 | 固定种子 | 正常游戏不固定；对比夹具固定种子 | 同左 |

速度单位为逻辑像素/秒；曲线控制点使用场景里的零切线插值。两者都是 2D，没有 3D billboard 或网格设置；也没有 GPU `visibility_rect` / `visibility_aabb`。不能给 CPU 节点硬填 GPU 专属属性。配置测试读取上面已命名的场景设置；本次仅整理文档，没有修改场景或测试。

### 我要求它遵守的规则，以及怎样证明

| 规则 | 当前实现/验收条件 | 证据与检查办法 |
|---|---|---|
| A 只响应允许的命中 | PLAYING 中收到 `weapon_hit(pos)`，且未达到上限时创建；场景加载不发射 | `test_particles_state.gd` 检查正常游戏产生的非致命/致命命中、位置和初始状态；配置测试读 `emitting=false` |
| A 连续命中不切掉前一发 | overlap，每事件新实例；同一寿命内两次事件应有两个实例 | 状态测试检验实例；30 fps 夹具在帧 10、13 触发，帧条检查视觉重叠 |
| A 有上限 | 同时最多 32 个，满时忽略新事件，释放槽位后再接收 | 状态测试和边界测试查上限；峰值分配 32×16=512 粒子 |
| 敌人释放不带走 A | A 挂在持久展示根节点上，不是敌人子节点 | 状态测试确认敌人释放后火花实例仍存活；实机检查是否突然消失 |
| A 的父级移动 | 已发射粒子不被父级平移拖走，因为 `local_coords=false` | 配置测试读值；移动父级的窗口夹具验证世界空间效果，不能仅靠无头状态声称看起来正确 |
| A 暂停、重开和结束 | 非 PLAYING 速度为 0；重开、MENU、WON、LOST 清理旧爆发 | 状态/边界测试；窗口里检查恢复时不重放命中 |
| B 开始/停止 | PLAYING、可见、实际位移>0.01 且未超过瞬移阈值时发射；任一条件不成立就停止出生 | 状态/边界测试覆盖走动、静止、顶住障碍；帧条核对停下后消退 |
| B 不连接瞬移路线 | 位移大于 `player.speed × delta × 2 + 4` 时当作不连续移动，不发射该帧，并更新位置采样 | 边界测试查瞬移与重开；实机看是否留下长线 |
| B 暂停与隐藏 | 游戏 PAUSED/LEVELUP：停止出生、模拟冻结；隐藏：停止出生，PLAYING 时旧粒子继续衰减但不绘制；若同时暂停，旧粒子冻结 | 状态测试查 `emitting`、`speed_scale`；窗口夹具检查隐藏/显示后是否补发 |
| 整棵树暂停 | 当前 P/Esc 改游戏状态，不等于设置 `SceneTree.paused`；继承默认暂停模式时，树暂停也停止更新 | 区分已测的游戏状态暂停与尚无新增记录的整树暂停；不能把两者混写 |
| B 首帧 | 场景载入没有移动，`emitting=false`，没有预先存在的尾迹 | 初始状态测试；第一帧窗口截图仍需本人确认 |
| 明暗、尺寸、遮挡 | A 不盖住灯油；B 不盖住玩家/敌人；暗处和亮处都可读 | 必须在实际窗口用眼睛看；帧条辅助，无头测试不证明观感 |

无头模式能证明参数、信号、实例数量和状态策略，不能画出粒子。帧条适合逐帧比较尺寸、扩散和消退。真正玩游戏才能判断视线是否来得及辨认、亮道具是否干扰、密集命中是否杂乱。这三种证据不能互相替代。

### 帧条要怎样读

背景必须用真实夜市区域，角色同屏作比例尺。暗地面和亮道具区域各检查一次；现有 A 独立夹具主要是暗地面，不能把它当成已完成亮背景检查。

A 以 30 fps，触发帧记作 T=10，读取 T、T+2、T+5、T+10、T+20、T+40，即 10、12、15、20、30、50：

| 帧 | 我预期读到的内容 |
|---|---|
| 10 | 起始紧凑亮点，确认位置；不要用这一帧替代最大尺寸判断 |
| 12 | 约 0.067 秒，火星开始分开，亮度不应成为遮挡物 |
| 15 | 约 0.167 秒，向外散开的黄橙碎火星，已开始变小、变暗 |
| 20 | 约 0.333 秒，稀疏暗橙残余，不应仍是完整白团 |
| 30 | 约 0.667 秒，A 已消失 |
| 50 | 约 1.333 秒，无残留，也没有自行重新发射 |

另用帧 13 的第二次事件看重叠。Movie Maker 文件从 0 编号，已有记录中首次可见在文件 9；必须注明文件编号与触发标签的偏移，不能把两者强行当作同一个时刻。

B 从帧 10 开始移动，帧 40 停止。读 10/12 看启动是否自然；20/39 看稳定短尾迹与脚边位置；40 看是否停止出生；45 看残余是否明显变弱；51/60 看是否消失。另拍暂停前后、隐藏前后，不能拿稳态图片证明停止策略。

### 我预先担心的失败

1. **参数拼成 Godot 3 名称。**效果看似触发但速度或尺寸回到默认值。用配置回读抓它；已有 `initial_velocity_min` 改成 `initial_velocity` 的变异测试失败记录，恢复后再测。
2. **第二次命中被吞掉。**只对一个仍在发射的 one-shot 节点设置 `emitting=true`，可能没有新爆发。检查同寿命内两个实例，再看快速连击帧条。
3. **火花随敌人一起消失。**检查敌人释放后的实例寿命，并在游戏里看击杀瞬间是否突然断掉。
4. **亮背景把火花吃掉，或火花与灯油混淆。**在灯笼、摊位亮部、水洼和暗石板旁分别触发，比较明度与辨识；目前是预测，尚无足够实测结论。
5. **尾迹顶墙也冒，或者瞬移连成一条线。**用实际位移测试、障碍/瞬移边界测试和停止后的帧条检查。
6. **材质或层级让正确计算的粒子看不见。**检查纹理非空、additive 材质、绘制层和透明度曲线；升级效果过去被 HUD 遮住就是需区分处理与绘制的例子。
7. **开销超预算。**比较相同条件的 off/on 增量，不用锁帧后的 FPS 推算 GPU 耗时；代理渲染器的结果必须单独标明。

### 价格预测、预算和已有结果

下面的预测保留原简报数字，不把已经知道的测量结果倒写成“事前预测”。CPU 效果同时比较 CPU 和 GPU。单位均为 ms/帧。

| 效果 | 峰值分配 | 原 CPU 预测 / 预算 | 原 GPU 预测 / 预算 | 已记录测量 |
|---|---:|---|---|---|
| A | 32×16=512 | <0.8 / ≤1.0 | <0.5 / ≤0.75 | 10月29日 CPU +0.0222，Mobile/Vulkan GPU +0.5392；GPU 超过预测但低于预算 |
| B | 24 | <0.15 / ≤0.25 | <0.15 / ≤0.25 | 同批 CPU +0.0030，代理 GPU +0.1077；在预算内 |
| 升级庆祝（额外） | 4×32=128 | <0.25 / ≤0.4 | <0.25 / ≤0.4 | 同批 CPU +0.0070，代理 GPU +0.9103；GPU 超预算 |

上述 GPU 数值来自 Mobile/Vulkan（MoltenVK）覆盖运行，不是发布用 GL Compatibility 的测量。本机 Compatibility 的 GPU 读数全为 0，表示没有可用计时，不表示零成本。A 的 Visual Profiler 另有 8.32 ms 选帧尖峰尚未解释，不能只挑均值说所有情况都好。11月9日无头复测 CPU 增量 A/B/庆祝为 +0.0379/+0.0052/+0.0269，不能与10月的 GPU 数据假装成同一次配对测量。原始方法、试验范围和记录见 `evidence/assignment-6/cost/FINAL-COMPARISON.md`、`TEST-REPORT.md` revision 3。

### 额外升级庆祝的定位

这不是 B。它监听 `leveled_up(level)`，现在放在升级界面的小角色身上，HUD 坐标 (56,325)，CanvasLayer 11。0–0.2 秒向外散开，之后变橙、缩小，到 0.7 秒消失；应围住小角色而不妨碍读卡。实际大小与亮背景观感仍需本人描述。

参数：CPUParticles2D，amount=32，one_shot=true，emitting=false，explosiveness=1，lifetime=.7，sphere 半径12，direction=(0,-1)，spread=180°，速度35–65，gravity=(0,8)，damping=15–25，scale=.8–1.5，缩放曲线 0:1/.25:.9/1:0；RGBA 为 0:(1,1,.8,1)/.4:(1,.75,.2,.8)/1:(1,.4,.05,0)。纹理和加法材质同 A，local_coords=false，preprocess=0。最多4次重叠；LEVELUP 继续播放，PAUSED 冻结，重开和终态清理。此前本人接受了头像位置，但不能据此声称通过性能预算。

### 不动的边界

碰撞、移动、输入、状态机及其时序、已有测试预期、第五次作业的手写着色器和其他对象均保持不变。展示层只读游戏状态，不修改它。本次文档整理没有补做 A 的历史调参，也没有改任何游戏参数。

### 我的判决与 Claude 的读图，要分开记录

历史上 A 的本人反馈是“完成，没问题”，之后 Claude 从 r0 帧条指出起始团小于设计目标，才提出最大缩放 1.2→1.8；后来本人反馈“保留，更清楚”。这不能改写成本人先在游戏中发现了具体缺陷。B 则有本人“尾迹不明显”的记录，对应 alpha .55/.30/0→.95/.70/0，后来确认够明显。

截至本次修订，没有新增的本人15分钟试玩记录，也没有新增的本人对 Claude 判读的同意/分歧结论。Codex 本次只短暂操作到游戏内约28秒，不能替本人完成这项证词。Codex 在聊天中曾把“火花不够醒目、可能与灯光或掉落物混淆”说成观察，现更正为待验证的预测；不能用那句话补齐 A 的观察驱动修订。

下一次本人记录时，应先描述亲眼看到的尺寸、亮度、扩散、消退和背景，再比较 Claude 的帧条判读。若一致就明确写“没有分歧”并说明一致在哪；若不同就说明哪一段、哪种背景不同。这里不预填结论。

### 六个简答

1. **节点与缺少的功能。**A、B 都是 CPUParticles2D。11月9日用本机 Godot 4.7.2 的 `ClassDB.class_get_property_list` 核对：有 `emission_shape`、`scale_amount_min`，没有 `amount_ratio`、`visibility_rect`、`sub_emitter`、`trail_enabled`；对应 GPU 节点有后四项。若以后要用这些功能，要另行设计，不能直接照抄 GPU 属性。在线 [CPU 类参考](https://docs.godotengine.org/en/stable/classes/class_cpuparticles2d.html) 仅作辅助；4.7 专属网页本次无法访问，不能声称已核对那份固定版本网页。
2. **父级移动。**`local_coords=false`，A 已出生的火花留在世界空间，不随父级平移；相机移动仍会改变它在屏幕中的投影位置。
3. **重触发与峰值。**每次允许的命中新建实例，最多32个同时存活，峰值分配512粒子；达到上限就忽略后续事件。512是容量上限，不保证每一帧都有512粒子可见。
4. **无头成本与垂直同步。**无头模式不绘制粒子、也不执行 GPU 粒子过程，因此 GPU 特效的相关无头成本接近零，仍可能有节点/脚本管理开销。A、B 是 CPU 节点，无头仍有模拟成本。开启 vsync 的 off/on FPS **没有测量记录**，不能填成60/60；即使两者同样锁帧，也不代表成本一样。
5. **B 首帧、预处理、暂停与隐藏。**当前 `emitting=false, preprocess=0`，第一帧没有尾迹。只把 preprocess 改成非零，并不会凭空满足移动条件，也不能声称载入就该有尾迹；若另做“持续发射且预热”的对照夹具，才会预先填充粒子，而未预热会从空逐渐填充。这个开/关对照目前未新增实机证据。游戏暂停/升级时停止出生且冻结；隐藏且 PLAYING 时不绘制、不出生，旧粒子继续消退。整树暂停与游戏状态暂停须分别记录。
6. **发射、处理、绘制。**发射决定多少、何时、从哪里出生：amount、one_shot、explosiveness、lifetime、emission_shape；处理决定出生后怎样变：速度、方向、扩散、重力、阻尼、颜色/透明度/缩放曲线；绘制决定怎样显示：纹理、CanvasItemMaterial、additive、过滤和层级。local_coords 属于坐标策略，preprocess 属于启动策略。

### 过程着色器怎样对应设计意图

游戏 A/B 使用 CPU 节点，没有自定义过程着色器。`godot/shaders/particles_generated.gdshader` 是另外的 GPU 学习副本，不能当成游戏实际使用的代码。以下是辅助解读，仍需本人核对后用自己的理解解释：

- 第3行 `shader_type particles`：这是更新粒子状态的过程着色器，不是画火星纹理的 canvas_item 着色器。
- 第225–275行 `start()`：初始化出生位置、随机速度等；第139行随机速度范围对应 A 的25–55，第149行随机尺寸对应0.7–1.8。
- 第277–379行 `process()`：每帧更新粒子；第311/324行施加重力，第328–336行阻尼减速，对应“先散开，再慢下来”。
- 第160行采样尺寸曲线，第161行采样颜色渐变，对应“变小、由浅黄变橙并透明”；第352行写入 COLOR，第364–371行把尺寸作用到变换。颜色和尺寸纹理都必须实际绑定，不能代码里有采样就算画面正确；旧版缺绑定的问题已在 r2 修复。
- 第293–299、376–378行处理年龄与到期关闭，对应0.45秒结束。纹理 `spark.png` 和 CanvasItemMaterial 的加法混合属于绘制端，不能靠过程着色器弥补被 HUD 遮挡或纹理缺失。

这张对应表由代理协助整理，不替代学生自己写注释的要求。以前的行号解释和修复证据见 `TEST-REPORT.md` 与 `evidence/assignment-6/shader-study-fixed/README.md`。


### 9 November 2026 — approved Effect A colour-ramp trial r2

Observation: the student looked at the weapon-hit sparks in the running game and reported “The hit sparks are not eye-catching enough.” Claude's reading of the kept r1 strip:
- The sparks are bright only until about 0.10 s.
- At 0.20 s they are mid-orange, with 21 of 189 lit pixels bright.
- From 0.30 s they are dark specks.
- The first white frames coincide with the enemy's own hit flash.

The full reading is in `TUNING.md`.

The student approved one change ("Approve"): the colour ramp's middle stop moves from 0.35:(1,0.6,0.2,0.85) to 0.6:(1,0.75,0.3,1.0). The start stop 0:(1,0.95,0.65,1) and the end stop 1:(0.65,0.2,0.05,0) are unchanged. Count, speed, spread, damping, gravity, scale range, scale curve, lifetime and texture are unchanged.

Prediction (full version in `TUNING.md`): the burst stays bright yellow until about 0.27 s instead of 0.20 s. At 0.20 s it is light yellow-orange, with roughly six times as many bright pixels. It then turns orange and disappears by the same frame as before. Footprint and widest point are unchanged.

This is an approved trial, pending the r2 capture comparison and the student's running-game verdict. Pre-change source is preserved in `evidence/assignment-6/tuning/a-r1-source/`.

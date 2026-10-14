Assignment: Assignment 3 - Your First 3D Game Assets with Claude, the Blender MCP, and Blender
Student: Bao Xing
Project name: walker-lanternfall-bao-x (Lanternfall)
GitHub repository URL: https://github.com/yanxlh/walker-lanternfall-bao-x
Git tag and submitted commit SHA: NOT CREATED — preparation only; user requested no submission
Game-source revision shown in the film: PENDING FINAL A3 FILM
Godot version, Blender version, and operating system: Godot 4.7.2.stable.official.ed1daf0bf; Blender 5.2.2 LTS; macOS 26 on Apple M4 Pro
The three assets and what each is for: Lantern Gate — market-entrance landmark and static blocker; Supply Stack — obstacle beside a market stall; Lamp-oil Shrine — collectible landmark near the upgrade area
MCP project and version, or script route: Blender MCP route for all three assets — mcp-for-blender 2.1.9 (add-on 1.8, uvx, DISABLE_TELEMETRY=true, telemetry consent off, all libraries and generators off). On 2026-10-13 the first coding session had no MCP tools and built the assets with background scripts (kept in tools/blender/script_route/); on 2026-10-14 the MCP connected and every asset was rebuilt with one execute_blender_code call per object, saved verbatim in tools/blender/build_<asset>.py
My hand edit in Blender: Selected OilGem, rotated it 20 degrees around Z, applied Rotation, saved oil_shrine.blend, and re-exported the GLB with File > Export. Before applying, the Item transform showed Z = 20 degrees; afterward it returned to 0 degrees because the rotation had been baked into the mesh. An independent vertex check recovered exactly 20 degrees (maximum delta 1.49e-8), and the re-exported GLB passed all A3 checks.
Checks run (command and result), re-run 2026-10-14 after the hand edit: Godot --headless --import exit 0, no ERROR lines; test_a3_assets.gd 17/17 PASS; test_lantern_gate.gd 14/14 PASS; test_logic 32/32, test_gameplay 65/65, test_audio 25/25 (Assignment 2, 122/122) PASS; scripts/audit_repo.py --stage final 0 problems
Final film URL and filename: PENDING — do not submit this file with placeholders
Final film SHA-256: PENDING
Summary of my changes: Added three simple metre-scale Blender assets, their .blend sources, .glb exports, build scripts and measurement records; simplified the original over-complex gate to the six-primitive course limit; placed all three in a lit Godot 3D room; added numeric import/placement/budget checks and labelled evidence. Rebuilt all three through the Blender MCP and saved every call as the build scripts; rotated the shrine's gem by hand in Blender.
Known limitations: the final three-asset room still needs Bao's human view from front/rear/below; from below, the Supply Stack's barrel cap and the crate underside are coplanar and flicker (z-fighting); the required A3 Brutalist explainer remains pending.
Changed games since Assignment 2: no

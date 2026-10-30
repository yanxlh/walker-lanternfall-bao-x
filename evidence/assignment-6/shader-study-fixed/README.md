# GPU study texture binding repair

Revision 2 restores the resources lost during conversion to ShaderMaterial. The generated shader itself is unchanged. `color_ramp` now references a GradientTexture1D with the CPU effect's three colors at 0, 0.35 and 1. `scale_curve` references a CurveTexture with points (0,1), (0.2,0.85) and (1,0), matching the CPU curve. World coordinates and a conservative visibility rectangle are explicit. Gameplay never loads this study scene.

A windowed Mobile/Vulkan Movie Maker run captured the CPU effect on the left and the generated GPU material on the right, at 30 FPS. Both bursts begin at fixture frame 10. The retained original frames and contact sheet show bright yellow/white sparks first, orange sparks expanding at frame 12, smaller/dimmer remnants at frame 15, and no visible sparks by frame 20. Tiny particles may become invisible before the configured 0.45-second lifetime ends. CPU/GPU random trajectories differ; this is lifecycle/color/size verification, not a pixel identity claim or a student tuning verdict.

`test_shader_study_config.gd` checks both texture types, all gradient stops/colors, sampled curve values, lifetime/count/world coordinates, generated-shader reference, and isolation from gameplay: 21 assertions passed. Results are in `evidence/shader_study_config.json`. No source effect scene or generated shader was edited.

To reproduce: run `res://previews/shader_study/comparison_preview.tscn` with `--rendering-method mobile --rendering-driver vulkan --fixed-fps 30 --write-movie <new-output>/frame.png --quit-after 60`. Use a windowed process; headless rendering cannot establish appearance.

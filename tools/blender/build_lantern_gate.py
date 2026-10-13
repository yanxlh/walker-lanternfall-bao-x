"""Build Lanternfall's Assignment 3 Lantern Gate and export a binary glTF.

Run only through Blender's background mode; paths are relative to repository root.
"""
from __future__ import annotations

import json
from pathlib import Path

import bpy


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "godot" / "a3" / "lantern_gate.glb"
LOG = ROOT / "evidence" / "a3" / "lantern_gate-build.json"


def material(name: str, color: tuple[float, float, float, float], metallic=0.0, emission=None):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = 0.45
    if emission:
        bsdf.inputs["Emission Color"].default_value = emission
        bsdf.inputs["Emission Strength"].default_value = 2.5
    return mat


def cube(name, dims, centre, mat=None):
    bpy.ops.mesh.primitive_cube_add(location=centre)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    return obj


def cylinder(name, radius, depth, centre, mat, vertices=10):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=centre)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    return obj


def cone(name, radius, depth, centre, mat):
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=radius, radius2=0.06, depth=depth, location=centre)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    return obj


def build_lantern(prefix, x, brass, wood, glow):
    cube(prefix + "Glow", (0.30, 0.30, 0.42), (x, 0.0, 2.18), glow)
    for dx in (-0.17, 0.17):
        for dy in (-0.17, 0.17):
            cube(prefix + f"Frame_{dx}_{dy}", (0.035, 0.035, 0.50), (x + dx, dy, 2.18), brass)
    cube(prefix + "Bottom", (0.40, 0.40, 0.05), (x, 0.0, 1.92), wood)
    cone(prefix + "Roof", 0.27, 0.22, (x, 0.0, 2.55), wood)


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0

    brass = material("AgedBrass", (0.42, 0.24, 0.08, 1.0), metallic=0.75)
    wood = material("DarkWood", (0.12, 0.045, 0.025, 1.0))
    glow = material("EmberGlass", (1.0, 0.34, 0.06, 1.0), emission=(1.0, 0.12, 0.01, 1.0))

    cube("GateBase", (0.80, 0.80, 0.18), (0.0, 0.0, 0.09), wood)
    cylinder("GatePost", 0.12, 2.37, (0.0, 0.0, 1.365), brass)
    cube("GateCrossArm", (1.20, 0.16, 0.16), (0.0, 0.0, 2.55), brass)
    cube("GateFinial", (0.16, 0.16, 0.30), (0.0, 0.0, 2.70), brass)
    build_lantern("LeftLantern", -0.33, brass, wood, glow)
    build_lantern("RightLantern", 0.33, brass, wood, glow)

    # Blender importer suffix route: these meshes become collision-only static bodies.
    cube("BaseCollider-convcolonly", (0.80, 0.80, 0.32), (0.0, 0.0, 0.16))
    cube("PostCollider-convcolonly", (0.42, 0.42, 2.55), (0.0, 0.0, 1.275))

    bpy.context.view_layer.update()
    visual = [o for o in scene.objects if o.type == "MESH" and not o.name.endswith("-convcolonly")]
    tri_count = sum(len(p.vertices) - 2 for o in visual for p in o.data.polygons)
    mins = [min((o.matrix_world @ v.co)[i] for o in visual for v in o.data.vertices) for i in range(3)]
    maxs = [max((o.matrix_world @ v.co)[i] for o in visual for v in o.data.vertices) for i in range(3)]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=str(OUT),
        export_format="GLB",
        export_yup=True,
        export_apply=True,
        export_materials="EXPORT",
    )
    record = {
        "asset": "Lantern Gate",
        "output": str(OUT.relative_to(ROOT)),
        "visual_bounds_blender_xyz_m": [round(maxs[i] - mins[i], 4) for i in range(3)],
        "origin_blender_xyz_m": [0.0, 0.0, 0.0],
        "visual_triangles": tri_count,
        "triangle_budget": 240,
        "materials": sorted(m.name for m in (brass, wood, glow)),
        "colliders": {
            "BaseCollider-convcolonly": [0.80, 0.80, 0.32],
            "PostCollider-convcolonly": [0.42, 0.42, 2.55],
        },
    }
    LOG.write_text(json.dumps(record, indent=2) + "\n")
    print("A3_BUILD " + json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    main()

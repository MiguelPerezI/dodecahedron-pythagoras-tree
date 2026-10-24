"""Render OBJ files written by scripts/make_tree.py with Blender (Cycles, CPU).

    blender -b --python scripts/render_blender.py -- job.json

job.json:
{
  "objs": [{"path": "out/a.obj", "color": "depth" | [r, g, b], "highlight": "out/b.obj"}],
  "view": [x, y, z],            # camera direction (from target towards camera)
  "target": [x, y, z],
  "ortho_scale": 5.0,           # orthographic camera; omit for perspective
  "lens": 50,
  "distance": 12,
  "resolution": [1600, 1200],
  "samples": 64,
  "background": "light" | "dark",
  "output": "paper/figures/x.png"
}
Depth groups ("g depthN" in the OBJ) get a graded colour; a "highlight" OBJ is
drawn in red (used to mark clashing dodecahedra).
"""
import json
import sys

import bpy
from mathutils import Vector

job = json.load(open(sys.argv[sys.argv.index("--") + 1]))

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = job.get("samples", 64)
scene.cycles.use_denoising = True
scene.render.resolution_x, scene.render.resolution_y = job.get("resolution", [1600, 1200])
scene.render.film_transparent = False
scene.view_settings.view_transform = "AgX" if "AgX" in [i.identifier for i in scene.view_settings.bl_rna.properties["view_transform"].enum_items] else "Filmic"

dark = job.get("background", "light") == "dark"
world = bpy.data.worlds.new("w")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.02, 0.02, 0.022, 1) if dark else (0.92, 0.92, 0.9, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.35 if dark else 0.45
scene.world = world


def material(name, rgb, rough=0.45, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m


# graded palette, root dark slate -> leaves warm ivory
PALETTE = [(0.035, 0.045, 0.09), (0.06, 0.13, 0.26), (0.10, 0.28, 0.40), (0.20, 0.45, 0.45),
           (0.45, 0.60, 0.38), (0.80, 0.68, 0.30), (0.92, 0.80, 0.45), (0.97, 0.90, 0.65)]
if dark:
    PALETTE = [(0.62, 0.05, 0.04), (0.75, 0.75, 0.75), (0.62, 0.62, 0.62), (0.52, 0.52, 0.52),
               (0.45, 0.45, 0.45), (0.40, 0.40, 0.40), (0.36, 0.36, 0.36), (0.33, 0.33, 0.33)]
RED = material("red", (0.80, 0.06, 0.04), 0.35)

objs = []
for spec in job["objs"]:
    before = set(bpy.data.objects)
    bpy.ops.wm.obj_import(filepath=spec["path"], use_split_groups=True, forward_axis="Y", up_axis="Z")
    new = [o for o in bpy.data.objects if o not in before]
    for o in new:
        if spec.get("color", "depth") == "depth":
            name = o.name.split(".")[0]
            k = int(name.split("depth")[-1]) if "depth" in name else 0
            mat = material(f"d{k}", PALETTE[min(k, len(PALETTE) - 1)])
        else:
            mat = material("flat", tuple(spec["color"]))
        o.data.materials.clear()
        o.data.materials.append(mat)
        for p in o.data.polygons:
            p.use_smooth = False
    objs += new
    if spec.get("highlight"):
        before = set(bpy.data.objects)
        bpy.ops.wm.obj_import(filepath=spec["highlight"], use_split_groups=False, forward_axis="Y", up_axis="Z")
        for o in set(bpy.data.objects) - before:
            o.data.materials.clear()
            o.data.materials.append(RED)
            objs.append(o)

# bevel-free crisp edges: add a thin wireframe-ish outline via Freestyle
scene.render.use_freestyle = True
scene.render.line_thickness_mode = "ABSOLUTE"
scene.render.line_thickness = job.get("line", 0.8)
fs = scene.view_layers[0].freestyle_settings
ls = fs.linesets[0] if fs.linesets else fs.linesets.new("l")
if ls.linestyle is None:
    ls.linestyle = bpy.data.linestyles.new("ls")
ls.select_by_visibility = True
ls.select_by_edge_types = True
ls.select_silhouette = True
ls.select_border = True
ls.select_crease = True
ls.linestyle.color = (0.04, 0.04, 0.05) if not dark else (0.0, 0.0, 0.0)

target = Vector(job.get("target", [0, 0, 0]))
view = Vector(job.get("view", [1.0, -1.6, 0.9])).normalized()
cam_data = bpy.data.cameras.new("cam")
if "ortho_scale" in job:
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = job["ortho_scale"]
else:
    cam_data.lens = job.get("lens", 50)
cam = bpy.data.objects.new("cam", cam_data)
scene.collection.objects.link(cam)
cam.location = target + view * job.get("distance", 12)
# camera looks at the target with world +Z as screen-up
cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
scene.camera = cam

# key / fill / rim lights
for loc, energy, size in [((6, -6, 9), 1500, 6), ((-8, -3, 4), 400, 8), ((0, 9, 6), 600, 5), ((0, 0, -9), 150, 10)]:
    ld = bpy.data.lights.new("L", "AREA")
    ld.energy = energy * (0.8 if dark else 1.0)
    ld.size = size
    lo = bpy.data.objects.new("L", ld)
    lo.location = target + Vector(loc)
    lo.rotation_euler = (target - lo.location).to_track_quat("-Z", "Y").to_euler()
    scene.collection.objects.link(lo)

scene.render.filepath = job["output"]
bpy.ops.render.render(write_still=True)
print("rendered", job["output"])

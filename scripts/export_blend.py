"""Export the tree mesh of the original Blender scene to out/dragon7.npz.

    blender -b ~/Downloads/DODC_4.blend --python scripts/export_blend.py

Saves the object-space vertices (V), triangle indices (T), material index per
triangle (M) and the object's world matrix (mw).  Only triangles are kept; the
few quads and n-gons in the scene come from manual edits.
"""
from pathlib import Path

import bpy
import numpy as np

target = Path(__file__).resolve().parents[1] / "out" / "dragon7.npz"
obj = bpy.data.objects["000DodecaDragon7"]
me = obj.data
V = np.array([v.co[:] for v in me.vertices])
polys = [(list(p.vertices), p.material_index) for p in me.polygons]
T = np.array([p for p, _ in polys if len(p) == 3])
M = np.array([m for p, m in polys if len(p) == 3])
target.parent.mkdir(exist_ok=True)
np.savez(target, V=V, T=T, M=M, mw=np.array(obj.matrix_world))
print(f"exported {len(V)} vertices, {len(T)} triangles of {len(polys)} polygons to {target}")

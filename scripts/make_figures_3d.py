"""Write OBJ meshes and Blender job files for the 3-D figures, then render.

    python scripts/make_figures_3d.py [--no-render] [--samples 64]
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dodecatree.clash import find_clashes                                # noqa: E402
from dodecatree.geometry import face_normals                             # noqa: E402
from dodecatree.io import write_obj                                      # noqa: E402
from dodecatree.legacy import LEGACY_D, LEGACY_G, legacy_maps            # noqa: E402
from dodecatree.tree import all_faces, crown_maps, grow                  # noqa: E402
from scripts.clash_study import d_of_g, optimal_owner                    # noqa: E402

MESH = ROOT / "out" / "meshes"
JOBS = ROOT / "out" / "jobs"
FIG = ROOT / "paper" / "figures"
A0 = face_normals()[0]
SIDE = np.cross(A0, [1, 0, 0])            # perpendicular to the crown axis
SIDE /= np.linalg.norm(SIDE)
G_STAR = 5 ** -0.5
THETA_STAR = np.degrees(np.arccos(G_STAR))


def frame(nodes, view, margin=1.08, aspect=4 / 3):
    P = np.concatenate([n.vertices for n in nodes])
    view = np.asarray(view, float) / np.linalg.norm(view)
    up = np.array([0, 0, 1.0]) - view * view[2]
    if np.linalg.norm(up) < 1e-6:
        up = np.array([0, 1.0, 0])
    up /= np.linalg.norm(up)
    right = np.cross(up, view)
    x, y = P @ right, P @ up
    c = P.mean(axis=0)
    c = c + right * ((x.max() + x.min()) / 2 - c @ right) + up * ((y.max() + y.min()) / 2 - c @ up)
    w, h = np.ptp(x), np.ptp(y)
    return c.tolist(), float(margin * max(w, h * aspect))


def job(name, objs, nodes, view, **kw):
    target, scale = frame(nodes, view)
    spec = {"objs": objs, "view": list(map(float, view)), "target": target, "ortho_scale": scale,
            "distance": 30, "resolution": [1600, 1200], "samples": 64, "output": str(FIG / f"{name}.png")}
    spec.update(kw)
    p = JOBS / f"{name}.json"
    p.write_text(json.dumps(spec, indent=1))
    return p


def main(render=True, samples=64):
    MESH.mkdir(parents=True, exist_ok=True)
    JOBS.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    jobs = []

    # The view down the crown axis is tilted a little so that depth reads.
    top = A0 + 0.18 * SIDE
    side = SIDE * np.cos(0.35) + A0 * np.sin(0.35) + np.array([0.25, 0, 0])

    art = grow(legacy_maps("cells", 45.0), 5, order="tree")
    write_obj(MESH / "artwork.obj", art)
    jobs.append(job("render_artwork_side", [{"path": str(MESH / "artwork.obj")}], art, side, samples=samples))
    jobs.append(job("render_artwork_top", [{"path": str(MESH / "artwork.obj")}], art, top, samples=samples))

    for k in range(4):
        nodes = grow(crown_maps(LEGACY_G, LEGACY_D, np.radians(45)), k, order="tree")
        write_obj(MESH / f"level{k}.obj", nodes)
        jobs.append(job(f"render_level{k}", [{"path": str(MESH / f"level{k}.obj")}], art, side,
                        samples=samples, resolution=[900, 900]))

    pyth = grow(crown_maps(G_STAR, 1 + G_STAR, np.radians(THETA_STAR)), 5, order="tree")
    write_obj(MESH / "pythagorean.obj", pyth)
    jobs.append(job("render_pythagorean_side", [{"path": str(MESH / "pythagorean.obj")}], pyth, side, samples=samples))
    jobs.append(job("render_pythagorean_top", [{"path": str(MESH / "pythagorean.obj")}], pyth, top, samples=samples))

    owner, _ = optimal_owner()
    F = crown_maps(LEGACY_G, LEGACY_D, np.radians(45))
    bad = all_faces(F, 3, "thirty", owner)
    hit = sorted({i for x in find_clashes(bad) if x["relation"] != "parent-child" for i in (x["i"], x["j"])})
    write_obj(MESH / "allfaces_artwork_ok.obj", [n for i, n in enumerate(bad) if i not in set(hit)])
    write_obj(MESH / "allfaces_artwork_clash.obj", [bad[i] for i in hit])
    iso = np.array([1.0, -1.3, 0.8])
    jobs.append(job("render_allfaces_clash", [{"path": str(MESH / "allfaces_artwork_ok.obj"),
                                               "highlight": str(MESH / "allfaces_artwork_clash.obj")}],
                    bad, iso, samples=samples, resolution=[1200, 1200]))

    g = 0.35
    good = all_faces(crown_maps(g, d_of_g(g), np.radians(45)), 4, "thirty", owner)
    write_obj(MESH / "allfaces_certified.obj", good)
    jobs.append(job("render_allfaces_certified", [{"path": str(MESH / "allfaces_certified.obj")}],
                    good, iso, samples=samples, resolution=[1200, 1200]))

    if render:
        for j in jobs:
            print("rendering", j.name, flush=True)
            subprocess.run(["blender", "-b", "--python", str(ROOT / "scripts" / "render_blender.py"), "--", str(j)],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        to_jpeg()


def to_jpeg(quality=90):
    """The paper includes JPEG versions of the renders (smaller PDF, arXiv-friendly)."""
    from PIL import Image
    for png in sorted(FIG.glob("render_*.png")):
        im = Image.open(png).convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[3])
        bg.save(png.with_suffix(".jpg"), quality=quality, optimize=True)


if __name__ == "__main__":
    s = sys.argv[sys.argv.index("--samples") + 1] if "--samples" in sys.argv else 64
    main(render="--no-render" not in sys.argv, samples=int(s))

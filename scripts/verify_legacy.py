"""Check that the Python construction reproduces the original artwork.

1. Port vs. compiled C++: the solid, five-child build of
   DedocaedroTREEverCELLS.cpp (made by scripts/build_legacy.sh) is compared
   vertex by vertex with dodecatree.legacy, in the same pre-order.
2. Port vs. the Blender scene: every clean dodecahedron in the mesh
   000DodecaDragon7 of DODC_4.blend (exported by scripts/export_blend.py)
   is matched to a node of the depth-5 tree.
3. Port vs. the clean formulation with exact constants (dodecatree.tree.crown_maps).

usage: python scripts/verify_legacy.py out/legacy_cells_solid.stl out/dragon7.npz
"""
import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dodecatree.geometry import FACES, VERTICES, axis_angle            # noqa: E402
from dodecatree.io import read_ascii_stl                                  # noqa: E402
from dodecatree.legacy import LEGACY_D, LEGACY_G, legacy_maps             # noqa: E402
from dodecatree.tree import crown_frames, crown_maps, grow                # noqa: E402


def check_cpp(stl_path, depth=3):
    tris = read_ascii_stl(stl_path)
    per_node = 36
    assert len(tris) % per_node == 0
    nodes = grow(legacy_maps("cells", 45.0), depth, order="legacy")
    assert len(nodes) == len(tris) // per_node, (len(nodes), len(tris) // per_node)
    worst = 0.0
    for i, n in enumerate(nodes):
        V = n.vertices
        ref = np.array([(V[f[0]], V[f[j]], V[f[j + 1]]) for f in FACES for j in (1, 2, 3)])
        worst = max(worst, np.abs(tris[i * per_node:(i + 1) * per_node] - ref).max())
    print(f"[C++] {len(nodes)} nodes, max |python - C++| = {worst:.2e}")
    return worst


def clean_components(npz_path):
    d = np.load(npz_path)
    V, T = d["V"], d["T"]
    u, inv = np.unique(np.round(V, 5), axis=0, return_inverse=True)
    Tw = inv.ravel()[T]
    n = len(u)
    rows = np.r_[Tw[:, 0], Tw[:, 1], Tw[:, 2]]
    cols = np.r_[Tw[:, 1], Tw[:, 2], Tw[:, 0]]
    A = sp.coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
    _, lab = connected_components(A, directed=False)
    comps = [u[lab == c] for c in range(lab.max() + 1)]
    return comps, len(T)


def check_blend(npz_path, depth=5):
    comps, ntri = clean_components(npz_path)
    clean = [P for P in comps if len(P) == 20]
    nodes = grow(legacy_maps("cells", 45.0), depth)
    centers = np.array([n.t for n in nodes])
    tree = cKDTree(centers)
    matched, errs, depth_hist = set(), [], {}
    for P in clean:
        c = P.mean(axis=0)
        dist, i = tree.query(c)
        n = nodes[i]
        # vertex-set distance (order free)
        D = np.linalg.norm(P[:, None] - n.vertices[None], axis=2)
        e = max(D.min(axis=1).max(), D.min(axis=0).max()) / n.scale
        if e < 5e-3:
            matched.add(i)
            errs.append(e)
            depth_hist[n.depth] = depth_hist.get(n.depth, 0) + 1
    unmatched = len(clean) - len(errs)
    print(f"[Blender] mesh: {ntri} triangles, {len(comps)} components, {len(clean)} clean 20-vertex dodecahedra")
    print(f"[Blender] matched {len(errs)} of them to distinct tree nodes "
          f"({len(matched)} distinct), unmatched {unmatched}; "
          f"max relative vertex error {max(errs):.2e}")
    total = {k: 5 ** k for k in range(depth + 1)}
    print("[Blender] matches by depth:", {k: f"{depth_hist.get(k, 0)}/{total[k]}" for k in total})
    displaced_stats(clean, nodes, tree)
    return len(matched), unmatched


def _pose(P):
    """Best (scale, rotation, centre) placing VERTICES onto the 20 points P."""
    c = P.mean(axis=0)
    s = np.linalg.norm(P - c, axis=1).mean() / np.linalg.norm(VERTICES[0])
    Q = (P - c) / s
    best = (np.inf, None)
    from scipy.spatial.transform import Rotation
    for R in Rotation.random(40, random_state=1).as_matrix():
        for _ in range(15):
            j = np.linalg.norm(Q[:, None] - (VERTICES @ R.T)[None], axis=2).argmin(axis=1)
            U, _, Wt = np.linalg.svd(VERTICES[j].T @ Q)
            R = Wt.T @ np.diag([1, 1, np.sign(np.linalg.det(Wt.T @ U.T))]) @ U.T
        e = np.linalg.norm(Q - VERTICES[j] @ R.T, axis=1).max()
        if e < best[0]:
            best = (e, R)
    return s, best[1], c, best[0]


def displaced_stats(clean, nodes, tree):
    """For clean dodecahedra that are not bit-exact: how far are they from a node?"""
    from dodecatree.geometry import symmetry_group
    G = symmetry_group()
    offs, rots, fits = [], [], []
    for P in clean:
        c = P.mean(axis=0)
        _, i = tree.query(c)
        n = nodes[i]
        D = np.linalg.norm(P[:, None] - n.vertices[None], axis=2)
        if max(D.min(axis=1).max(), D.min(axis=0).max()) / n.scale < 5e-3:
            continue
        s, R, c, fit = _pose(P)
        Rn = n.A / n.scale
        rel = min(np.degrees(np.arccos(np.clip((np.trace(R @ (Rn @ g).T) - 1) / 2, -1, 1))) for g in G)
        offs.append(np.linalg.norm(c - n.t) / n.scale)
        rots.append(rel)
        fits.append(fit)
    print(f"[Blender] the {len(offs)} non-exact clean dodecahedra are regular (max fit error "
          f"{max(fits):.3f}), lie within {max(offs):.2f} node sizes of a tree node "
          f"(median {np.median(offs):.3f}) and are rotated by at most {max(rots):.2f} deg")


def check_formal():
    leg = legacy_maps("cells", 45.0)
    best = crown_maps(LEGACY_G, LEGACY_D, np.radians(45.0))
    print("[formal] legacy map vs exact-constant map, per child:")
    for k, ((A, t), (B, s), (m, e)) in enumerate(zip(leg, best, crown_frames())):
        ax, ang = axis_angle(A / LEGACY_G)
        print(f"   child {k}: twist axis.e_k = {ax @ e:+.4f}, angle = {np.degrees(ang):.3f} deg, "
              f"|A-A*|/g = {np.abs(A - B).max() / LEGACY_G:.1e}, |t-t*| = {np.linalg.norm(t - s):.1e}")
    n_leg = grow(leg, 5)
    n_for = grow(best, 5)
    dev = max(np.abs(a.vertices - b.vertices).max() for a, b in zip(n_leg, n_for))
    print(f"[formal] depth-5 trees differ by at most {dev:.3e} (tree diameter ~ 4)")


if __name__ == "__main__":
    stl = sys.argv[1] if len(sys.argv) > 1 else "out/legacy_cells_solid.stl"
    npz = sys.argv[2] if len(sys.argv) > 2 else "out/dragon7.npz"
    check_cpp(stl)
    if Path(npz).exists():
        check_blend(npz)
    check_formal()

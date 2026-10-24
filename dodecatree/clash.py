"""Exact collision ("clash") detection between the dodecahedra of a tree.

Two placed copies of B are convex polytopes, so the separating-axis theorem
is exact: their interiors are disjoint iff some axis among the 6 face-normal
directions of each copy and the 15 x 15 cross products of their edge
directions separates their projections.  Overlap volumes are computed
exactly as the volume of the intersection of the 24 half-spaces.
"""
import numpy as np
from scipy.optimize import linprog
from scipy.spatial import ConvexHull, HalfspaceIntersection, cKDTree

from .geometry import CIRCUMRADIUS, INRADIUS, VERTICES, edges, face_normals

_N6 = []                                          # one normal per opposite pair
for f in face_normals():
    if not any(abs(f @ g + 1) < 1e-9 for g in _N6):
        _N6.append(f)
_N6 = np.array(_N6)
assert len(_N6) == 6
_E15 = []
for a, b in edges():
    e = VERTICES[b] - VERTICES[a]
    e /= np.linalg.norm(e)
    if not any(abs(abs(e @ f) - 1) < 1e-9 for f in _E15):
        _E15.append(e)
_E15 = np.array(_E15)
assert len(_E15) == 15
assert np.allclose(np.abs(face_normals() @ _N6.T).max(axis=1), 1)


def penetration(n1, n2):
    """Minimum projection overlap over all separating-axis candidates,
    relative to the smaller node's scale.  <= 0 means disjoint interiors
    (0 = touching); > 0 means the interiors intersect."""
    R1, R2 = n1.A / n1.scale, n2.A / n2.scale
    axes = [ _N6 @ R1.T, _N6 @ R2.T ]
    e1, e2 = _E15 @ R1.T, _E15 @ R2.T
    cr = np.cross(e1[:, None, :], e2[None, :, :]).reshape(-1, 3)
    nr = np.linalg.norm(cr, axis=1)
    axes.append(cr[nr > 1e-9] / nr[nr > 1e-9, None])
    ax = np.concatenate(axes)
    p1, p2 = n1.vertices @ ax.T, n2.vertices @ ax.T
    ov = np.minimum(p1.max(0), p2.max(0)) - np.maximum(p1.min(0), p2.min(0))
    return ov.min() / min(n1.scale, n2.scale)


def _halfspaces(n):
    """Rows [a, b] with a.x + b <= 0 for the placed copy n."""
    R = n.A / n.scale
    nn = face_normals() @ R.T
    off = n.scale * INRADIUS + nn @ n.t
    return np.hstack([nn, -off[:, None]])


def overlap_volume(n1, n2):
    """Exact volume of n1 ∩ n2 (0 if the interiors are disjoint)."""
    H = np.vstack([_halfspaces(n1), _halfspaces(n2)])
    # Chebyshev centre: maximise r s.t. a.x + r|a| <= -b
    norm = np.linalg.norm(H[:, :3], axis=1)
    res = linprog([0, 0, 0, -1], A_ub=np.hstack([H[:, :3], norm[:, None]]),
                  b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
    if not res.success or res.x[3] < 1e-12:
        return 0.0
    hs = HalfspaceIntersection(H, res.x[:3])
    return ConvexHull(hs.intersections).volume


def relation(w1, w2):
    """Genealogical relation of two words (tree order: child = word + (k,))."""
    if len(w1) > len(w2):
        w1, w2 = w2, w1
    if w2[:len(w1)] == w1:
        return "parent-child" if len(w2) == len(w1) + 1 else "ancestor"
    if len(w1) == len(w2) and w1[:-1] == w2[:-1]:
        return "siblings"
    return "other"


def find_clashes(nodes, tol=1e-9, volumes=False):
    """All pairs of nodes whose interiors intersect.

    Returns a list of dicts (i, j, relation, depth, pen[, vol]).  `depth` is
    the larger of the two node depths, i.e. the generation at which the
    clash first appears.
    """
    C = np.array([n.t for n in nodes])
    r = np.array([n.scale for n in nodes]) * CIRCUMRADIUS
    tree = cKDTree(C)
    rmax = r.max()
    out = []
    for i in range(len(nodes)):
        for j in tree.query_ball_point(C[i], r[i] + rmax):
            if j <= i or np.linalg.norm(C[i] - C[j]) >= r[i] + r[j]:
                continue
            pen = penetration(nodes[i], nodes[j])
            if pen > tol:
                rec = dict(i=i, j=j, relation=relation(nodes[i].word, nodes[j].word),
                           depth=max(nodes[i].depth, nodes[j].depth), pen=pen)
                if volumes:
                    rec["vol"] = overlap_volume(nodes[i], nodes[j])
                out.append(rec)
    return out

"""Exact geometry of the regular dodecahedron used by the tree.

The base solid B is the dodecahedron with midradius 1 whose 20 vertices are
the points (+-1/phi, +-1/phi, +-1/phi), (0, +-1, +-1/phi^2) and its cyclic
permutations.  Vertex and face numbering follow the original C++ program
(legacy/DedocaedroTREEverCELLS.cpp) so that results can be compared index by
index.
"""
from itertools import product

import numpy as np

PHI = (1 + 5 ** 0.5) / 2
G1 = 1 / PHI          # 0.618...
G2 = 1 / PHI ** 2     # 0.381...

VERTICES = np.array([
    (G2, 0.0, 1.0), (-G2, 0.0, 1.0), (-G1, G1, G1), (0.0, 1.0, G2),
    (G1, G1, G1), (0.0, -1.0, G2), (G1, -G1, G1), (-G1, -G1, G1),
    (G2, 0.0, -1.0), (-G2, 0.0, -1.0), (-G1, -G1, -G1), (0.0, -1.0, -G2),
    (G1, -G1, -G1), (G1, G1, -G1), (0.0, 1.0, -G2), (-G1, G1, -G1),
    (1.0, -G2, 0.0), (-1.0, G2, 0.0), (-1.0, -G2, 0.0), (1.0, G2, 0.0),
])

# Faces as listed in the legacy Pentagon(...) calls.  Face 0 is the "crown"
# face whose five edges carry the children in the original program.
FACES = [
    (0, 1, 2, 3, 4), (1, 0, 6, 5, 7), (2, 3, 14, 15, 17), (1, 2, 17, 18, 7),
    (5, 7, 18, 10, 11), (6, 5, 11, 12, 16), (0, 6, 16, 19, 4),
    (4, 19, 13, 14, 3), (16, 12, 8, 13, 19), (14, 13, 8, 9, 15),
    (17, 15, 9, 10, 18), (11, 10, 9, 8, 12),
]

EDGE_LENGTH = 2 * G2                       # 0.7639...
MIDRADIUS = 1.0
CIRCUMRADIUS = float(np.linalg.norm(VERTICES[0]))           # sqrt(3)/phi
INRADIUS = float(np.linalg.norm(VERTICES[list(FACES[0])].mean(axis=0)))  # 0.8507...
VOLUME = (15 + 7 * 5 ** 0.5) / 4 * EDGE_LENGTH ** 3
FACE_AREA = 0.25 * np.sqrt(5 * (5 + 2 * 5 ** 0.5)) * EDGE_LENGTH ** 2
SURFACE = 12 * FACE_AREA


def face_normals():
    """Outward unit normals of the 12 faces, in FACES order."""
    out = []
    for f in FACES:
        c = VERTICES[list(f)].mean(axis=0)
        out.append(c / np.linalg.norm(c))
    return np.array(out)


def edges():
    """The 30 edges as sorted vertex pairs."""
    es = set()
    for f in FACES:
        for i in range(5):
            a, b = f[i], f[(i + 1) % 5]
            es.add((min(a, b), max(a, b)))
    return sorted(es)


def crown_edges():
    """The five edges of face 0 in the order used by the legacy children.

    Child k of the original program sits on the k-th of these edges:
    k=0: v0v1, k=1: v1v2, k=2: v2v3, k=3: v3v4, k=4: v4v0.
    """
    f = FACES[0]
    return [(f[i], f[(i + 1) % 5]) for i in range(5)]


def rotation(axis, angle):
    """Right-handed rotation by `angle` (radians) about the unit vector `axis`."""
    a = np.asarray(axis, float)
    a = a / np.linalg.norm(a)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * K @ K


def axis_angle(R):
    """Inverse of `rotation`: returns (unit axis, angle in [0, pi])."""
    ang = np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1))
    if ang < 1e-12:
        return np.array([0.0, 0.0, 1.0]), 0.0
    if abs(ang - np.pi) < 1e-6:
        w, v = np.linalg.eigh((R + R.T) / 2)
        return v[:, np.argmax(w)], ang
    ax = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]])
    return ax / np.linalg.norm(ax), ang


def symmetry_group():
    """The 60 rotations of the icosahedral group I that preserve VERTICES."""
    key = {tuple(np.round(v, 9)) for v in VERTICES}
    gens = [rotation(face_normals()[0], 2 * np.pi / 5),
            rotation(VERTICES[0], 2 * np.pi / 3)]
    group = [np.eye(3)]
    frontier = [np.eye(3)]
    while frontier:
        new = []
        for M in frontier:
            for G in gens:
                P = G @ M
                if not any(np.allclose(P, Q, atol=1e-9) for Q in group):
                    group.append(P)
                    new.append(P)
        frontier = new
    assert len(group) == 60
    for M in group:
        assert {tuple(np.round(v, 9)) for v in VERTICES @ M.T} == key
    return np.array(group)


def triangles(V):
    """Fan-triangulate the 12 pentagons of a placed copy with vertices V (20x3)."""
    tris = []
    for f in FACES:
        for i in (1, 2, 3):
            tris.append((V[f[0]], V[f[i]], V[f[i + 1]]))
    return np.array(tris)


def _self_check():
    vs = VERTICES
    d = np.linalg.norm(vs[:, None] - vs[None], axis=2)
    assert np.isclose(np.sort(d[0])[1], EDGE_LENGTH)
    for a, b in edges():
        assert np.isclose(d[a, b], EDGE_LENGTH)
        assert np.isclose(np.linalg.norm((vs[a] + vs[b]) / 2), MIDRADIUS)
    assert len(edges()) == 30
    n = face_normals()
    for f, nn in zip(FACES, n):
        assert np.allclose((vs[list(f)] @ nn), INRADIUS)
    assert set(map(tuple, (np.sign(np.round(vs, 9)) != 0).astype(int))) <= set(product((0, 1), repeat=3))


_self_check()

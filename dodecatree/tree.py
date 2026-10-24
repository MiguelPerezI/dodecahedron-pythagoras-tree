"""The dodecahedral Pythagoras tree as an IFS with condensation.

A tree is given by a base solid B (the unit-midradius dodecahedron) and a
finite list of contracting similarities f_k(x) = A_k x + t_k.  The tree is
the unique non-empty compact set with

    T = B  U  f_1(T) U ... U f_N(T),

and its depth-n approximation consists of the images f_w(B) for all words w
of length <= n.  A node is stored as (word, A, t) with A = scale * rotation.
"""
from dataclasses import dataclass

import numpy as np

from .geometry import FACES, VERTICES, crown_edges, edges, face_normals, rotation, symmetry_group


@dataclass(frozen=True)
class Node:
    word: tuple
    A: np.ndarray
    t: np.ndarray

    @property
    def depth(self):
        return len(self.word)

    @property
    def scale(self):
        return float(np.cbrt(np.linalg.det(self.A)))

    @property
    def vertices(self):
        return VERTICES @ self.A.T + self.t


def grow(maps, depth, order="legacy"):
    """All nodes f_w(B) with |w| <= depth.

    order="legacy" reproduces the C++ recursion, in which the node reached
    by choosing k1, then k2, ... is f_kn o ... o f_k1 (B) and nodes are
    emitted in pre-order.  order="tree" uses f_k1 o ... o f_kn (B), so that
    a node's children are its own images f_w o f_k (B) and sit on its own
    edges.  Both orders produce the same set of nodes.
    """
    out = []

    def rec(word, A, t):
        out.append(Node(word, A, t))
        if len(word) == depth:
            return
        for k, (Ak, tk) in enumerate(maps):
            if order == "legacy":     # f_k o (current)
                rec(word + (k,), Ak @ A, Ak @ t + tk)
            else:                     # (current) o f_k
                rec(word + (k,), A @ Ak, A @ tk + t)

    rec((), np.eye(3), np.zeros(3))
    return out


def crown_frames():
    """For each crown edge k: (m_k, e_k), the unit midpoint direction and the
    unit edge direction oriented as in the legacy rotation axes."""
    frames = []
    for a, b in crown_edges():
        m = (VERTICES[a] + VERTICES[b]) / 2
        e = VERTICES[a] - VERTICES[b]
        frames.append((m / np.linalg.norm(m), e / np.linalg.norm(e)))
    return frames


# Twist signs of the five legacy children about the cyclically oriented crown
# edges.  (The C++ writes -angle for children 3 and 4, but their axes are typed
# with the opposite orientation, so all five twists agree.)
LEGACY_TWIST_SIGNS = (+1, +1, +1, +1, +1)


def crown_maps(g, d, theta, signs=LEGACY_TWIST_SIGNS):
    """The clean ("formal") version of the legacy maps with exact constants:

        f_k(x) = g Rot(e_k, s_k theta) x + d m_k ,   k = 0..4,

    where m_k is the unit direction of the midpoint of the k-th edge of the
    crown face, e_k the unit direction of that edge, and theta in radians.
    """
    return [(g * rotation(e, s * theta), d * m)
            for (m, e), s in zip(crown_frames(), signs)]


# ---------------------------------------------------------------------------
# Extensions of the crown tree to all twelve faces
# ---------------------------------------------------------------------------

def face_rotations():
    """For each face j a rotation gamma_j of the symmetry group with
    gamma_j(face 0) = face j.  Because the crown tree has the dihedral
    symmetry of its crown face, the choice among the five such rotations
    does not affect gamma_j(T_crown)."""
    n = face_normals()
    group = symmetry_group()
    return [next(G for G in group if np.allclose(G @ n[0], n[j], atol=1e-9))
            for j in range(len(FACES))]


def edge_faces():
    """For each edge of geometry.edges(): the two faces containing it, and
    for each of those faces the crown index k such that gamma_j maps crown
    edge k onto it.  Returns a list of [(j, k), (j', k')] (lower face first)."""
    Gs = face_rotations()
    mids = {tuple(np.round((VERTICES[a] + VERTICES[b]) / 2, 6)): i
            for i, (a, b) in enumerate(edges())}
    out = [[] for _ in mids]
    for j, G in enumerate(Gs):
        for k, (a, b) in enumerate(crown_edges()):
            m = (VERTICES[a] + VERTICES[b]) / 2 @ G.T
            out[mids[tuple(np.round(m, 6))]].append((j, k))
    assert all(len(x) == 2 for x in out)
    return out


def lowest_face_owner():
    """Edge ownership in which every edge belongs to its lower-numbered face."""
    return [ef[0][0] for ef in edge_faces()]


def all_faces(maps, depth, mode="twelve", owner=None):
    """Grow crown trees on every face of the root.

    mode="twelve": the union of the twelve rotated copies gamma_j(T_crown)
        sharing the root, so every edge of the root carries two "twin"
        children, one from each adjacent face.
    mode="thirty": every root edge e carries a single branch, the one
        coming from the face owner[e] (default: the lower-numbered face).
        The branch is gamma_j(f_k(T_crown)); its twist is +theta about e
        oriented counter-clockwise around the owning face.
    mode="ifs30": the IFS of the 30 maps gamma_j f_k gamma_j^-1 (one per edge,
        chosen by `owner`) applied at every node, so every node sprouts on
        all 30 of its own edges.

    First letters of words encode (face j, edge k) as 5 j + k.
    """
    Gs = face_rotations()
    if owner is None:
        owner = lowest_face_owner()
    chosen = []
    for e, ef in enumerate(edge_faces()):
        if mode == "twelve":
            chosen.extend(ef)
        else:
            chosen.extend(jk for jk in ef if jk[0] == owner[e])
    if mode == "ifs30":
        fam = [(Gs[j] @ maps[k][0] @ Gs[j].T, Gs[j] @ maps[k][1]) for j, k in chosen]
        return grow(fam, depth, order="tree")
    crown = grow(maps, depth, order="tree")
    nodes = [crown[0]]
    for j, k in sorted(chosen):
        G = Gs[j]
        nodes.extend(Node((5 * j + k,) + n.word[1:], G @ n.A, G @ n.t)
                     for n in crown[1:] if n.word[0] == k)
    return nodes

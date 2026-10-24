"""Computer-assisted proof that a tree is self-avoiding at *every* depth.

Setting.  T = B U f_1(T) U ... U f_N(T) (the crown tree) and, optionally,
a root with its own children, T_root = B U r_1(T) U ... U r_M(T).

Claim.  Two nodes have intersecting interiors only if one is the parent of
the other, provided a convex polytope Q exists with

  (1) B ⊆ Q and f_k(Q) ⊆ Q for all k            (so T ⊆ Q);
  (2) for j != k the pieces of r_j(P_L) and r_k(P_L) have disjoint interiors,
      where P_L = U_{|w|<L} f_w(B)  U  U_{|w|=L} f_w(Q) ⊇ T;
  (3) int B ∩ r_k f_j(Q) = ∅ for all k, j;
  (4) conditions (2) and (3) also for the crown maps themselves (r = f).

Proof sketch.  Take nodes f_u(B) ≠ f_v(B), strip their common prefix with
the similarity f_w^{-1}.  If one word becomes empty and the other has length
1 they are parent and child.  If one is empty and the other has length >= 2,
(3) separates them.  Otherwise the words start with different letters j ≠ k
and the two nodes lie in r_j(P_L) and r_k(P_L), separated by (2).

Q is the fixed point of the support-function iteration
h <- max(h_B, max_k [u . t_k + g h_Q(R_k^T u)]) over a fixed set of
directions u, which converges geometrically (ratio g).  Interior overlap of
two convex polytopes is decided with the Chebyshev-ball LP: the largest ball
inside both has radius r; r <= 0 means disjoint interiors and -r is a
certified separation margin.
"""
import numpy as np
from scipy.optimize import linprog
from scipy.spatial import ConvexHull, HalfspaceIntersection

from .geometry import CIRCUMRADIUS, INRADIUS, VERTICES, face_normals
from .tree import grow

_HB = np.hstack([face_normals(), -INRADIUS * np.ones((12, 1))])   # a.x + b <= 0


def invariant_polytope(maps, n_seed=4, n_random=400, tol=1e-13, seed=0):
    """Vertices of a polytope Q with B ⊆ Q and f_k(Q) ⊆ Q, and the residual."""
    pts = np.concatenate([n.vertices for n in grow(maps, n_seed)])
    U = ConvexHull(pts).equations[:, :3]
    X = np.random.default_rng(seed).normal(size=(n_random, 3))
    U = np.vstack([U, X]) / np.linalg.norm(np.vstack([U, X]), axis=1, keepdims=True)
    hB = (VERTICES @ U.T).max(axis=0)
    h = (pts @ U.T).max(axis=0)
    c = pts.mean(axis=0)

    def verts(h):
        return HalfspaceIntersection(np.hstack([U, -h[:, None]]), c).intersections

    for _ in range(500):
        V = verts(h)
        new = np.maximum(hB, np.max([U @ t + ((V @ A.T) @ U.T).max(axis=0) for A, t in maps], axis=0))
        done = np.abs(new - h).max() < tol
        h = new
        if done:
            break
    # Outer-round by 1e-9 and re-verify the inclusion on the actual vertices.
    h = h + 1e-9
    V = verts(h)
    resid = max(((V @ A.T + t) @ U.T - h).max() for A, t in maps)
    resid = max(resid, (VERTICES @ U.T - h).max())
    return V, resid


def _place(H, A, t):
    """Half-spaces of A X + t from those of X (rows a.x + b <= 0), normalised."""
    a = H[:, :3] @ np.linalg.inv(A)
    b = H[:, 3] - a @ t
    nr = np.linalg.norm(a, axis=1)
    return np.hstack([a / nr[:, None], (b / nr)[:, None]])


def overlap_radius(H1, H2):
    """Radius of the largest ball inside both polytopes (negative: separated)."""
    H = np.vstack([H1, H2])
    res = linprog([0, 0, 0, -1], A_ub=np.hstack([H[:, :3], np.ones((len(H), 1))]),
                  b_ub=-H[:, 3], bounds=[(None, None)] * 4, method="highs")
    return res.x[3]


def _compose(m1, m2):
    return m1[0] @ m2[0], m1[0] @ m2[1] + m1[1]


def certify(maps, root_maps=None, L=1, symmetric_pairs=None):
    """Run the checks (1)-(4).  Returns a dict of margins; the tree is
    certified self-avoiding iff result["certified"] is True.

    symmetric_pairs: optional list of (j, k) root-branch pairs that represent
    all pairs up to a symmetry of the configuration (saves time).
    """
    V, resid = invariant_polytope(maps)
    HQ = ConvexHull(V).equations
    RQ = np.linalg.norm(V, axis=1).max()

    def pieces(m):
        out = []

        def rec(A, t, lev):
            s = np.cbrt(np.linalg.det(A))
            if lev < L:
                out.append((_place(_HB, A, t), t, s * CIRCUMRADIUS))
                for Ak, tk in maps:
                    rec(A @ Ak, A @ tk + t, lev + 1)
            else:
                out.append((_place(HQ, A, t), t, s * RQ))
        rec(*m, 0)
        return out

    def branch_margin(fam, pairs):
        worst = -np.inf
        P = {}
        for j, k in pairs:
            for i in (j, k):
                if i not in P:
                    P[i] = pieces(fam[i])
            for H1, c1, r1 in P[j]:
                for H2, c2, r2 in P[k]:
                    if np.linalg.norm(c1 - c2) < r1 + r2:
                        worst = max(worst, overlap_radius(H1, H2))
        return worst

    def root_margin(fam):
        return max(overlap_radius(_HB, _place(HQ, *_compose(r, f))) for r in fam for f in maps)

    n = len(maps)
    out = {"Q_vertices": len(V), "Q_residual": float(resid)}
    out["crown_siblings"] = branch_margin(maps, [(j, k) for j in range(n) for k in range(j + 1, n)])
    out["crown_root_vs_grandchildren"] = root_margin(maps)
    ok = resid <= 0 and out["crown_siblings"] < 0 and out["crown_root_vs_grandchildren"] < 0
    if root_maps is not None:
        m = len(root_maps)
        pairs = symmetric_pairs or [(j, k) for j in range(m) for k in range(j + 1, m)]
        out["root_siblings"] = branch_margin(root_maps, pairs)
        out["root_vs_grandchildren"] = root_margin(root_maps)
        ok = ok and out["root_siblings"] < 0 and out["root_vs_grandchildren"] < 0
    out["certified"] = bool(ok)
    return out

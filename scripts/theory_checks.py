"""Numerical checks of every proposition stated in the preprint.

usage: python scripts/theory_checks.py  > out/theory_checks.txt
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dodecatree.certify import certify                                    # noqa: E402
from dodecatree.clash import find_clashes                                  # noqa: E402
from dodecatree.geometry import (CIRCUMRADIUS, EDGE_LENGTH, FACE_AREA,     # noqa: E402
                                 INRADIUS, PHI, SURFACE, VERTICES, VOLUME,
                                 edges, face_normals, rotation, symmetry_group)
from dodecatree.legacy import LEGACY_D, LEGACY_G                           # noqa: E402
from dodecatree.tree import crown_frames, crown_maps, grow                 # noqa: E402


def axes(vectors):
    out = []
    for v in vectors:
        v = v / np.linalg.norm(v)
        if not any(abs(abs(v @ w) - 1) < 1e-9 for w in out):
            out.append(v)
    return np.array(out)


def main():
    print("== base solid")
    print(f"edge {EDGE_LENGTH:.6f}  inradius {INRADIUS:.6f}  midradius 1  circumradius {CIRCUMRADIUS:.6f}")
    print(f"volume {VOLUME:.6f}  face area {FACE_AREA:.6f}  surface {SURFACE:.6f}")
    n = face_normals()
    a0 = n[0]
    print("crown normal a0 =", np.round(a0, 6), " = (0,1,phi)/|.|:", np.allclose(a0, np.array([0, 1, PHI]) / np.linalg.norm([0, 1, PHI])))
    dih = np.degrees(np.arccos(-n[0] @ n[1]))
    print(f"dihedral angle {np.degrees(np.arccos(n[0] @ n[1])):.4f} between normals -> dihedral {180 - np.degrees(np.arccos(n[0] @ n[1])):.4f} deg; |cos| = {abs(n[0] @ n[1]):.6f} = 1/sqrt5 {1 / 5 ** .5:.6f}")
    (m0, e0) = crown_frames()[0]
    print(f"angle(edge-midpoint axis m_k, a0) = {np.degrees(np.arccos(m0 @ a0)):.4f} deg; m_k.a0 = {m0 @ a0:.6f}")

    print("\n== tight frames (frame operator S = sum a a^T)")
    five = axes(n)
    two = axes([(VERTICES[a] + VERTICES[b]) / 2 for a, b in edges()])
    three = axes(VERTICES)
    for name, A in [("5-fold (face) axes", five), ("2-fold (edge) axes", two), ("3-fold (vertex) axes", three)]:
        S = A.T @ A
        print(f"{name}: {len(A)} lines, S = {S[0, 0]:.6f} I ? {np.allclose(S, S[0, 0] * np.eye(3))}")
    nb = [k for k in range(12) if abs(n[0] @ n[k] - 1 / 5 ** .5) < 1e-9]
    print("neighbours of face 0:", nb, " sum (a0.ak)^2 =", sum((n[0] @ n[k]) ** 2 for k in nb))
    print("every edge direction is a 2-fold axis:",
          all(any(abs(abs((VERTICES[b] - VERTICES[a]) @ w) / EDGE_LENGTH - 1) < 1e-9 for w in two) for a, b in edges()))

    print("\n== symmetry of the crown map family")
    maps = crown_maps(LEGACY_G, LEGACY_D, np.radians(45))
    G = symmetry_group()

    def same_family(F1, F2):
        return all(any(np.allclose(A, B, atol=1e-9) and np.allclose(t, s, atol=1e-9) for B, s in F2) for A, t in F1)
    stab = [M for M in G if np.allclose(M @ a0, a0)]
    rot_ok = all(same_family([(M @ A @ M.T, M @ t) for A, t in maps], maps) for M in stab)
    # a mirror fixing the crown face: reflection in the plane spanned by a0 and m0
    nrm = np.cross(a0, m0)
    nrm /= np.linalg.norm(nrm)
    Mi = np.eye(3) - 2 * np.outer(nrm, nrm)
    mir_ok = same_family([(Mi @ A @ Mi.T, Mi @ t) for A, t in maps], maps)
    other = [M for M in G if not np.allclose(M @ a0, a0)]
    other_ok = any(same_family([(M @ A @ M.T, M @ t) for A, t in maps], maps) for M in other)
    print(f"C5 about a0 ({len(stab)} rotations) permutes the maps: {rot_ok}; mirror through a0, m0: {mir_ok}; any other icosahedral rotation: {other_ok}")
    for th in (0, 90):
        F = crown_maps(LEGACY_G, LEGACY_D, np.radians(th))
        print(f"theta={th}: mirror symmetric: {same_family([(Mi @ A @ Mi.T, Mi @ t) for A, t in F], F)}")

    print("\n== measures")
    for name, g in [("artwork", LEGACY_G), ("pythagorean 1/sqrt5", 5 ** -.5)]:
        dim = np.log(5) / np.log(1 / g)
        print(f"{name}: g={g:.6f} 5g^2={5 * g * g:.6f} 5g^3={5 * g ** 3:.6f}  similarity dim {dim:.6f}"
              f"  total volume/V0 {1 / (1 - 5 * g ** 3):.6f}  total surface/S0 {1 / (1 - 5 * g * g) if 5 * g * g < 1 else float('inf'):.4f}")
    print(f"artwork g vs 1/sqrt5: relative {(LEGACY_G * 5 ** .5 - 1) * 100:+.3f}%")
    print("volume bound for sprouting on all 30 edges: g <= 30^(-1/3) =", 30 ** (-1 / 3), "; artwork 30 g^3 =", 30 * LEGACY_G ** 3)
    print("volume bound for the crown: g <= 5^(-1/3) =", 5 ** (-1 / 3))

    print("\n== the Pythagorean member g* = 1/sqrt5, theta = 45")
    kappa = (LEGACY_D - 1) / LEGACY_G
    for label, d in [("d = 1 + kappa g*", 1 + kappa * 5 ** -.5), ("d = artwork", LEGACY_D)]:
        F = crown_maps(5 ** -.5, d, np.radians(45))
        cl = [x for x in find_clashes(grow(F, 5, order="tree")) if x["relation"] != "parent-child"]
        cert = certify(F, L=1)
        print(f"{label} = {d:.6f}: non-joint clashes to depth 5: {len(cl)}; certificate {cert['certified']} "
              f"(siblings {cert['crown_siblings']:.2e}, root/grandchildren {cert['crown_root_vs_grandchildren']:.2e})")

    print("\n== the artwork's parameters")
    print(f"g = 0.36 (1+sqrt2)/2 = {LEGACY_G:.10f}   d = 1.125 (1+sqrt2)/2 = {LEGACY_D:.10f}   kappa = {kappa:.6f}")
    print(f"if `gold` had been the golden ratio: g = {0.36 * PHI:.6f}, d = {1.125 * PHI:.6f}")
    print(f"child: circumradius {LEGACY_G * CIRCUMRADIUS:.6f}, centre at {LEGACY_D:.6f}, "
          f"gap between parent edge midpoint and child centre {LEGACY_D - 1:.6f} < child midradius {LEGACY_G:.6f}")
    print(f"diameter of the tree's bounding box (depth 6): ",
          np.ptp(np.concatenate([x.vertices for x in grow(maps, 6)]), axis=0))


if __name__ == "__main__":
    main()

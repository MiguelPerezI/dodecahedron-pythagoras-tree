"""Clash analysis of the crown tree and of its extensions to all faces.

Writes out/clash_study.json with
  * "legacy":   clash census of the artwork's tree (theta = 45 deg) and of
                theta = 0, 90 deg, depth 5, plus the all-depth certificate;
  * "pairs":    penetration of two adjacent children vs theta for the four
                relative twist orientations;
  * "extensions": census of the all-faces variants at the artwork's parameters;
  * "phase":    (theta, g) grid for the crown tree and for the best
                one-child-per-edge all-faces tree ("thirty", optimal ownership),
                each point with a numerical census and the certificate.

usage: python scripts/clash_study.py [--quick]
"""
import json
import sys
import time
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dodecatree.certify import certify                                   # noqa: E402
from dodecatree.clash import find_clashes, overlap_volume, penetration    # noqa: E402
from dodecatree.geometry import FACES, VOLUME, edges, rotation            # noqa: E402
from dodecatree.legacy import LEGACY_D, LEGACY_G, legacy_maps             # noqa: E402
from dodecatree.tree import (Node, all_faces, crown_frames, crown_maps,   # noqa: E402
                             edge_faces, face_rotations, grow)

KAPPA = (LEGACY_D - 1) / LEGACY_G      # child centre sits KAPPA*g beyond the parent's edge midpoint


def d_of_g(g):
    return 1 + KAPPA * g


def census(nodes):
    cl = find_clashes(nodes)
    c = Counter()
    first = None
    for x in cl:
        if x["relation"] == "parent-child":
            continue
        c[f'{x["depth"]}:{x["relation"]}'] += 1
        first = x["depth"] if first is None else min(first, x["depth"])
    joints = [x for x in cl if x["relation"] == "parent-child"]
    n_pc = sum(1 for n in nodes if n.depth > 0)
    return {"nodes": len(nodes), "non_joint": sum(c.values()), "by_depth": dict(sorted(c.items())),
            "first_clash_depth": first, "joints_overlapping": len(joints), "parent_child_pairs": n_pc}


# ---------------------------------------------------------------------------
def optimal_owner():
    """Edge ownership minimising adjacent clockwise-clockwise pairs (MILP)."""
    ef = edge_faces()
    E = edges()
    eid = {e: i for i, e in enumerate(E)}
    pairs = []
    for j, f in enumerate(FACES):
        es = [eid[tuple(sorted((f[i], f[(i + 1) % 5])))] for i in range(5)]
        pairs += [(j, es[i], es[(i + 1) % 5]) for i in range(5)]
    nE, nP = len(E), len(pairs)
    rows, lb = [], []
    for p, (C, e1, e2) in enumerate(pairs):
        row, const = np.zeros(nE + nP), 0
        for e in (e1, e2):            # not-owned(e, C) = 1 - o_e if C is e's first face else o_e
            if ef[e][0][0] == C:
                row[e] += 1
                const += 1
            else:
                row[e] -= 1
        row[nE + p] = 1               # y_p >= notowned1 + notowned2 - 1
        rows.append(row)
        lb.append(const - 1)
    res = milp(np.r_[np.zeros(nE), np.ones(nP)], integrality=np.ones(nE + nP),
               constraints=LinearConstraint(np.array(rows), lb, np.inf), bounds=Bounds(0, 1))
    o = np.round(res.x[:nE]).astype(int)
    owner = [ef[e][0][0] if o[e] else ef[e][1][0] for e in range(nE)]
    return owner, int(round(res.fun))


def all_faces_maps(maps, owner):
    """The 30 conjugated maps gamma_j f_k gamma_j^-1 of the ifs30 variant."""
    Gs = face_rotations()
    out = []
    for e, ef in enumerate(edge_faces()):
        j, k = next(jk for jk in ef if jk[0] == owner[e])
        out.append((Gs[j] @ maps[k][0] @ Gs[j].T, Gs[j] @ maps[k][1]))
    return out


def thirty_root_maps(maps, owner):
    Gs = face_rotations()
    out = []
    for e, ef in enumerate(edge_faces()):
        j, k = next(jk for jk in ef if jk[0] == owner[e])
        out.append((Gs[j] @ maps[k][0], Gs[j] @ maps[k][1]))
    return out


# ---------------------------------------------------------------------------
def pair_table(thetas):
    (m0, e0), (m1, e1) = crown_frames()[:2]   # crown edges 0 and 1 share vertex v1
    rows = []
    for th in thetas:
        t = np.radians(th)

        def pen(s0, s1):
            a = Node((0,), LEGACY_G * rotation(s0 * e0, t), LEGACY_D * m0)
            b = Node((1,), LEGACY_G * rotation(s1 * e1, t), LEGACY_D * m1)
            return penetration(a, b)
        rows.append({"theta": th, "ccw_ccw": pen(1, 1), "cw_cw": pen(-1, -1),
                     "in_in": pen(-1, 1), "out_out": pen(1, -1)})
    return rows


def phase_point(args):
    kind, th, g, owner, depth = args
    maps = crown_maps(g, d_of_g(g), np.radians(th))
    if kind == "crown":
        nodes = grow(maps, depth, order="tree")
    elif kind == "ifs30":
        nodes = all_faces(maps, depth, "ifs30", owner)
    else:
        nodes = all_faces(maps, depth, "thirty", owner)
    cen = census(nodes)
    rec = {"kind": kind, "theta": th, "g": g, "d": d_of_g(g), **cen, "certified": None}
    if cen["non_joint"] == 0:
        try:
            if kind == "crown":
                cert = certify(maps, L=1)
            elif kind == "ifs30":
                fam = all_faces_maps(maps, owner)
                cert = certify(fam, L=1)
            else:
                cert = certify(maps, root_maps=thirty_root_maps(maps, owner), L=1)
            rec["certified"] = cert["certified"]
            rec["margins"] = {k: float(v) for k, v in cert.items() if k not in ("certified",)}
        except Exception as exc:          # degenerate hull etc.
            rec["certified"] = False
            rec["error"] = repr(exc)
    return rec


def main(quick=False, phase_only=False):
    t0 = time.time()
    out = ROOT / "out" / ("clash_study_quick.json" if quick else "clash_study.json")
    if phase_only:
        res = json.loads(out.read_text())
        owner = res["optimal_owner"]["owner"]
        return run_phase(res, owner, quick, out, t0)
    res = {"parameters": {"g": LEGACY_G, "d": LEGACY_D, "kappa": KAPPA}}

    # 1. the artwork and its twist variants
    leg = {}
    for th in (0, 45, 90):
        maps = crown_maps(LEGACY_G, LEGACY_D, np.radians(th))
        nodes = grow(maps, 4 if quick else 5, order="tree")
        leg[th] = census(nodes)
        pc = next(i for i, n in enumerate(nodes) if n.word == (0,))
        leg[th]["joint_overlap_fraction"] = overlap_volume(nodes[0], nodes[pc]) / (VOLUME * LEGACY_G ** 3)
    leg["rounded_constants_45"] = census(grow(legacy_maps("cells", 45.0), 4 if quick else 5, order="tree"))
    leg["certificate_45"] = {k: (float(v) if not isinstance(v, bool) else v)
                             for k, v in certify(crown_maps(LEGACY_G, LEGACY_D, np.radians(45)), L=1).items()}
    leg["certificate_45_rounded"] = {k: (float(v) if not isinstance(v, bool) else v)
                                     for k, v in certify(legacy_maps("cells", 45.0), L=1).items()}
    leg["two_children_cpp_default"] = census(grow(legacy_maps("cells", 45.0)[:2], 8, order="tree"))
    res["legacy"] = leg
    print(f"[legacy] done {time.time() - t0:.0f}s", flush=True)

    # 2. adjacent pair orientations
    res["pairs"] = pair_table(list(range(0, 181, 5)))

    # 3. extensions at the artwork's parameters
    owner, min_bad = optimal_owner()
    res["optimal_owner"] = {"owner": owner, "min_cw_cw_pairs": min_bad,
                            "faces_owned": np.bincount(owner, minlength=12).tolist()}
    maps = crown_maps(LEGACY_G, LEGACY_D, np.radians(45))
    dep = 3 if quick else 4
    res["extensions"] = {
        "twelve": census(all_faces(maps, dep, "twelve")),
        "thirty_lowest": census(all_faces(maps, dep, "thirty")),
        "thirty_optimal": census(all_faces(maps, dep, "thirty", owner)),
        "ifs30_optimal": census(all_faces(maps, 2, "ifs30", owner)),
    }
    print(f"[extensions] done {time.time() - t0:.0f}s", flush=True)
    return run_phase(res, owner, quick, out, t0)


def run_phase(res, owner, quick, out, t0):
    """Phase diagrams over the full circle of twists.  The tree for -theta is
    not congruent to the tree for theta, and theta + 180 deg differs from
    theta beyond the first generation, so all of [-180, 180) is scanned."""
    gs = [round(x, 4) for x in np.arange(0.20, 0.5001, 0.05 if quick else 0.0125)]
    th_crown = list(range(-180, 180, 30 if quick else 5))
    th_all = list(range(-180, 180, 30 if quick else 10))
    jobs = [("crown", th, g, None, 3 if quick else 4) for th in th_crown for g in gs]
    jobs += [("thirty", th, g, owner, 2 if quick else 3) for th in th_all for g in gs]
    jobs += [("ifs30", 45, g, owner, 2) for g in gs]
    with Pool(4) as pool:
        res["phase"] = []
        for i, r in enumerate(pool.imap_unordered(phase_point, jobs, chunksize=2)):
            res["phase"].append(r)
            if i % 50 == 0:
                print(f"[phase] {i}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    out.write_text(json.dumps(res, indent=1, default=float))
    print(f"wrote {out} in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main(quick="--quick" in sys.argv, phase_only="--phase-only" in sys.argv)

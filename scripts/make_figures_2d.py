"""Diagrams for the preprint (matplotlib).  Reads out/clash_study.json.

    python scripts/make_figures_2d.py
"""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                                           # noqa: E402
import numpy as np                                                        # noqa: E402
from matplotlib.colors import ListedColormap                              # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection                   # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dodecatree.geometry import (FACES, INRADIUS, VERTICES, edges,          # noqa: E402
                                 face_normals)
from dodecatree.legacy import LEGACY_D, LEGACY_G                          # noqa: E402
from dodecatree.tree import crown_frames, crown_maps, edge_faces          # noqa: E402

FIG = ROOT / "paper" / "figures"
plt.rcParams.update({"font.family": "serif", "font.size": 9, "axes.linewidth": 0.6,
                     "mathtext.fontset": "cm", "savefig.dpi": 300})
INK, CERT, FREE, CLASH = "#1d2433", "#2f6f6a", "#9cc5a1", "#e9dcc9"


def phase(res):
    fig, axs = plt.subplots(2, 1, figsize=(6.6, 4.9), sharex=True)
    cmap = ListedColormap([CLASH, FREE, CERT])
    for ax, kind, title in [(axs[0], "crown", "crown tree (five children on the crown of every node)"),
                            (axs[1], "thirty", "all faces (one child per root edge, optimal owners)")]:
        P = [p for p in res["phase"] if p["kind"] == kind]
        th = sorted({p["theta"] for p in P})
        gs = sorted({p["g"] for p in P})
        Z = np.zeros((len(gs), len(th)))
        for p in P:
            Z[gs.index(p["g"]), th.index(p["theta"])] = 2 if p["certified"] else (1 if p["non_joint"] == 0 else 0)
        def edges(v):
            v = np.asarray(v, float)
            mid = (v[1:] + v[:-1]) / 2
            return np.r_[v[0] - (mid[0] - v[0]), mid, v[-1] + (v[-1] - mid[-1])]
        Z = np.ma.masked_where(np.isnan(Zn := np.where(np.isin(np.arange(len(th)), [th.index(p["theta"]) for p in P]), Z, np.nan)), Zn)
        ax.pcolormesh(edges(th), edges(gs), Z, cmap=cmap, vmin=0, vmax=2, shading="flat", edgecolors="face", linewidth=0, antialiased=False, rasterized=True)
        ax.set_title(title, fontsize=9)
        ax.set_ylabel(r"scale factor $g$")
        ax.axhline(5 ** -0.5, color=INK, lw=0.6, ls=(0, (4, 2)))
        ax.text(-178, 5 ** -0.5 + 0.005, r"$g^*=1/\sqrt{5}$", fontsize=7, color=INK)
    axs[1].set_xlabel(r"twist $\theta$ (degrees)")
    axs[1].set_xticks(range(-180, 181, 45))
    axs[0].plot([45], [LEGACY_G], marker="*", ms=10, mec=INK, mfc="#d1372a", mew=0.6)
    axs[0].annotate("artwork", (45, LEGACY_G), (5, 0.485), fontsize=7, arrowprops=dict(arrowstyle="-", lw=0.5))
    axs[0].plot([np.degrees(np.arccos(5 ** -0.5))], [5 ** -0.5], marker="o", ms=6, mec=INK, mfc="white", mew=0.8)
    axs[0].annotate(r"$(\theta^*, g^*)$", (63.43, 0.4472), (95, 0.485), fontsize=7, arrowprops=dict(arrowstyle="-", lw=0.5))
    axs[1].axhline(30 ** (-1 / 3), color="#8a3b2e", lw=0.6, ls=":")
    axs[1].text(140, 30 ** (-1 / 3) + 0.005, r"$30g^3=1$", fontsize=7, color="#8a3b2e")
    axs[1].plot([45], [0.35], marker="o", ms=5, mec=INK, mfc="white", mew=0.8)
    from matplotlib.patches import Patch
    fig.legend(handles=[Patch(fc=CERT, label="certified self-avoiding (all depths)"),
                        Patch(fc=FREE, label="no clash found (finite depth), not certified"),
                        Patch(fc=CLASH, label="clash")], loc="lower center", ncol=3, frameon=False, fontsize=7)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(FIG / "phase.pdf")
    plt.close(fig)


def pairs(res):
    R = res["pairs"]
    th = [r["theta"] for r in R]
    fig, ax = plt.subplots(figsize=(3.3, 2.3))
    ax.axhline(0, color=INK, lw=0.5)
    for key, lab, st in [("ccw_ccw", "coherent, +θ", "-"), ("cw_cw", "coherent, −θ", "--"),
                         ("in_in", "in–in = out–out", ":")]:
        ax.plot(th, [r[key] for r in R], st, lw=1.0, label=lab, color=INK if key != "cw_cw" else "#b23a2a")
    ax.axvline(45, color="#999", lw=0.5)
    ax.fill_between(th, 0, 0.14, color=CLASH, alpha=0.6, lw=0)
    ax.text(150, 0.125, "clash", fontsize=7)
    ax.set_xlim(0, 180)
    ax.set_ylim(-0.15, 0.14)
    ax.set_xticks([0, 45, 90, 135, 180])
    ax.set_xlabel(r"twist $\theta$ (degrees)")
    ax.set_ylabel("penetration / child size")
    ax.legend(fontsize=6, frameon=False, loc="lower left")
    fig.tight_layout()
    fig.savefig(FIG / "pairs.pdf")
    plt.close(fig)


def schlegel(res):
    """Edge ownership on a Schlegel diagram; face 11 (opposite the crown) is outermost."""
    n = face_normals()
    out_face = 11
    a = n[out_face]                     # project from just above face 11 onto the plane of face 0
    P = a * (INRADIUS * 1.35)
    plane_d = -INRADIUS                 # plane x.a = -INRADIUS (opposite face)
    u = np.cross(a, [0.3, 0.5, 0.8])
    u /= np.linalg.norm(u)
    v = np.cross(a, u)

    def proj(x):
        dirn = x - P
        s = (plane_d - P @ a) / (dirn @ a)
        y = P + s * dirn
        return np.array([y @ u, y @ v])
    Q = np.array([proj(x) for x in VERTICES])
    owner = res["optimal_owner"]["owner"]
    E = edges()
    ef = edge_faces()
    fig, ax = plt.subplots(figsize=(3.2, 3.2))
    centres = {j: Q[list(f)].mean(axis=0) for j, f in enumerate(FACES)}
    for j, f in enumerate(FACES):
        poly = Q[list(f)]
        if j == out_face:
            continue
        ax.fill(*poly.T, color="#f4efe6" if j else "#d9e6e3", lw=0)
        ax.text(*centres[j], str(j), ha="center", va="center", fontsize=6, color="#777")
    # edges: draw from the owner's side, offset toward the owner's centre, with an arrow
    # pointing counter-clockwise around the owner (= direction of the +theta twist axis)
    bad = []
    for e, (i, k) in enumerate(E):
        j = owner[e]
        pa, pb = Q[i], Q[k]
        f = FACES[j]
        pos = [f.index(i), f.index(k)]
        ccw_order = (pos[1] - pos[0]) % 5 == 1
        cen = centres[j] if j != out_face else Q.mean(axis=0) * 2 - (pa + pb) / 2
        off = 0.08 * (cen - (pa + pb) / 2) / np.linalg.norm(cen - (pa + pb) / 2)
        s, t = (pa, pb) if ccw_order else (pb, pa)
        ax.plot([pa[0], pb[0]], [pa[1], pb[1]], color=INK, lw=0.7)
        mid = (s + t) / 2 + off
        d = (t - s) * 0.18
        ax.annotate("", xy=mid + d, xytext=mid - d, arrowprops=dict(arrowstyle="-|>", lw=0.6, color="#2f6f6a", mutation_scale=6))
    # bad pairs: adjacent edges in a face, both not owned by it
    eid = {e: x for x, e in enumerate(E)}
    for j, f in enumerate(FACES):
        es = [eid[tuple(sorted((f[i], f[(i + 1) % 5])))] for i in range(5)]
        for i in range(5):
            e1, e2 = es[i], es[(i + 1) % 5]
            if owner[e1] != j and owner[e2] != j:
                vtx = f[(i + 1) % 5]
                c = centres[j] if j != out_face else Q.mean(axis=0)
                p = Q[vtx] + 0.22 * (c - Q[vtx]) if j != out_face else Q[vtx] * 1.08
                ax.plot(*p, marker="o", ms=5, mfc="#d1372a", mec="white", mew=0.5, zorder=5)
                bad.append((j, vtx))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"optimal edge ownership: {len(bad)} clockwise pairs", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "ownership.pdf")
    plt.close(fig)
    return bad


def construction():
    """Parent with the crown face, the five edge axes, and the twisted children."""
    fig = plt.figure(figsize=(3.4, 3.2))
    ax = fig.add_subplot(111, projection="3d")
    n = face_normals()

    def draw(V, alpha, fc, ec, lw):
        pc = Poly3DCollection([V[list(f)] for f in FACES], facecolor=fc, edgecolor=ec,
                              linewidths=lw, alpha=alpha)
        ax.add_collection3d(pc)
    fc = ["#ece7dc"] * 12
    fc[0] = "#9fc9bf"
    draw(VERTICES, 0.85, fc, INK, 0.5)
    for k, (A, t) in enumerate(crown_maps(LEGACY_G, LEGACY_D, np.radians(45))):
        if k == 0:
            draw(VERTICES @ A.T + t, 0.9, "#f1d9a6", INK, 0.45)
        else:
            draw(VERTICES @ A.T + t, 0.12, "#f1d9a6", "#9a8f7a", 0.25)
    for k, (m, e) in enumerate(crown_frames()):
        ax.quiver(*(m - 0.3 * e), *(0.6 * e), color="#b23a2a", lw=1.0, arrow_length_ratio=0.3)
    m0, e0 = crown_frames()[0]
    ax.text(*(m0 - 0.42 * e0 + [0, -0.05, 0.02]), "$e_0$", fontsize=8, color="#b23a2a")
    ax.text(*(m0 + [0.0, -0.32, -0.12]), "$m_0$", fontsize=8)
    ax.scatter(*m0, color=INK, s=6)
    ax.quiver(*(INRADIUS * n[0]), *(1.0 * n[0]), color="#2f6f6a", lw=1.0, arrow_length_ratio=0.12)
    ax.text(*(INRADIUS * n[0] + 1.05 * n[0]), "$a_0$", fontsize=8, color="#2f6f6a")
    ax.set_box_aspect((1, 1, 1))
    c = 0.75 * n[0]
    lim = 1.55
    ax.set_xlim(c[0] - lim, c[0] + lim)
    ax.set_ylim(c[1] - lim, c[1] + lim)
    ax.set_zlim(c[2] - lim, c[2] + lim)
    ax.view_init(elev=36, azim=40)
    ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    fig.savefig(FIG / "construction.pdf")
    plt.close(fig)


if __name__ == "__main__":
    FIG.mkdir(parents=True, exist_ok=True)
    res = json.loads((ROOT / "out" / "clash_study.json").read_text())
    phase(res)
    pairs(res)
    print("bad pairs on the Schlegel diagram:", schlegel(res))
    construction()
    print("figures written to", FIG)

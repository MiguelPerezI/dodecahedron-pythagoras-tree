"""Bracket the critical scale g_c(theta) beyond which the tree self-intersects.

For each twist theta, lo = largest g certified self-avoiding at all depths,
hi = smallest g for which a non-joint clash is found (search to depth 6).
d = 1 + kappa g as in the artwork.   usage: python scripts/critical_g.py
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dodecatree.certify import certify                     # noqa: E402
from dodecatree.clash import find_clashes                  # noqa: E402
from dodecatree.tree import all_faces, crown_maps, grow    # noqa: E402
from scripts.clash_study import d_of_g, optimal_owner, thirty_root_maps   # noqa: E402

OWNER, _ = optimal_owner()


def clashes(kind, g, th, depth):
    F = crown_maps(g, d_of_g(g), np.radians(th))
    nodes = grow(F, depth, order="tree") if kind == "crown" else all_faces(F, depth, "thirty", OWNER)
    return any(x["relation"] != "parent-child" for x in find_clashes(nodes))


def certified(kind, g, th):
    F = crown_maps(g, d_of_g(g), np.radians(th))
    if kind == "crown":
        return certify(F, L=1)["certified"]
    return certify(F, root_maps=thirty_root_maps(F, OWNER), L=1)["certified"]


def bracket(kind, th, lo, hi, depth, steps=10):
    """lo: certified, hi: clashing.  Bisect on certification first, then on clashes."""
    assert certified(kind, lo, th), (kind, th, lo)
    assert clashes(kind, hi, th, depth), (kind, th, hi)
    c_lo, c_hi = lo, hi                 # largest certified / smallest clashing
    for _ in range(steps):
        mid = (c_lo + c_hi) / 2
        if certified(kind, mid, th):
            c_lo = mid
        elif clashes(kind, mid, th, depth):
            c_hi = mid
        else:                           # undecided: shrink from both sides separately
            break
    return c_lo, c_hi


if __name__ == "__main__":
    out = {}
    for kind, th, lo, hi, depth in [("crown", 45, 0.40, 0.4472136, 6),
                                    ("crown", 63.43494882, 0.44, 0.50, 6),
                                    ("thirty", 45, 0.30, 0.40, 4)]:
        a, b = bracket(kind, th, lo, hi, depth)
        out[f"{kind}@{th:.2f}"] = [a, b]
        print(f"{kind:6s} theta={th:6.2f}: certified up to g={a:.5f}, clash found at g={b:.5f}", flush=True)
    (ROOT / "out" / "critical_g.json").write_text(json.dumps(out, indent=1))

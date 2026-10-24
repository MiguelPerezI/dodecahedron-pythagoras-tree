"""Generate a dodecahedral Pythagoras tree as STL/OBJ.

Examples
--------
The artwork (DODC_4.blend / tree_7.png / tree_11.png), reproduced exactly:
    python scripts/make_tree.py --preset artwork -o out/artwork_depth5.stl

The same tree with exact constants (no 2-decimal rounding):
    python scripts/make_tree.py --depth 5 -o out/crown_exact.stl

The C++ file's own default (two children, depth 2):
    python scripts/make_tree.py --preset cpp-default -o out/two_children.stl

A certified clash-free tree sprouting on all twelve faces:
    python scripts/make_tree.py --mode thirty --owner optimal --g 0.35 --depth 4 -o out/all_faces.stl
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dodecatree.io import write_binary_stl, write_obj                    # noqa: E402
from dodecatree.legacy import LEGACY_D, LEGACY_G, legacy_maps            # noqa: E402
from dodecatree.tree import all_faces, crown_maps, grow                  # noqa: E402

KAPPA = (LEGACY_D - 1) / LEGACY_G


def build(args):
    if args.preset == "artwork":
        return grow(legacy_maps("cells", 45.0), args.depth or 5, order="tree")
    if args.preset == "cpp-default":
        return grow(legacy_maps("cells", 45.0)[:2], args.depth or 2, order="tree")
    g = args.g
    d = args.d if args.d is not None else 1 + KAPPA * g
    maps = crown_maps(g, d, np.radians(args.theta))
    depth = args.depth or 5
    if args.mode == "crown":
        return grow([maps[k] for k in args.children], depth, order="tree")
    owner = None
    if args.owner == "optimal":
        from scripts.clash_study import optimal_owner
        owner, _ = optimal_owner()
    return all_faces(maps, depth, args.mode, owner)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--preset", choices=["artwork", "cpp-default"])
    p.add_argument("--mode", choices=["crown", "twelve", "thirty", "ifs30"], default="crown")
    p.add_argument("--depth", type=int)
    p.add_argument("--g", type=float, default=LEGACY_G, help="scale factor (default: the artwork's 0.4346)")
    p.add_argument("--d", type=float, help="child-centre distance (default 1 + kappa g; artwork 1.358)")
    p.add_argument("--theta", type=float, default=45.0, help="twist about the edge, degrees")
    p.add_argument("--children", type=int, nargs="+", default=[0, 1, 2, 3, 4],
                   help="which crown edges carry children (crown mode)")
    p.add_argument("--owner", choices=["lowest", "optimal"], default="optimal",
                   help="edge ownership for the all-faces modes")
    p.add_argument("-o", "--output", required=True)
    args = p.parse_args()
    nodes = build(args)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() == ".obj":
        write_obj(out, nodes)
    else:
        write_binary_stl(out, nodes)
    meta = {"nodes": len(nodes), "max_depth": max(n.depth for n in nodes), **vars(args)}
    out.with_suffix(".json").write_text(json.dumps(meta, indent=1))
    print(f"wrote {out}: {len(nodes)} dodecahedra")


if __name__ == "__main__":
    main()

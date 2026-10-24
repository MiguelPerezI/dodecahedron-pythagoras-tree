# The dodecahedral Pythagoras tree

Code, data and article for a Pythagoras tree built from regular dodecahedra
(Miguel Esteban Pérez Ibarra, ESFM-IPN). Article: *A Pythagoras Tree Grown from a Dodecahedron*,
`paper/dodecahedral_pythagoras_tree.pdf`.

* `paper/dodecahedral_pythagoras_tree.tex` (and `.pdf`) is the article; `arxiv/` holds the
  submission bundle (`bash scripts/make_arxiv.sh` rebuilds it).
* `dodecatree/` is the Python package:
  * `geometry.py`: the base dodecahedron (vertex and face order of the original C++), constants, symmetry group.
  * `legacy.py`: a faithful port of the original child maps, quirks included.
  * `tree.py`: the exact construction `f_k(x) = g Rot(e_k, θ) x + d m_k` as an IFS with condensation, plus the all-faces variants.
  * `clash.py`: exact separating-axis collision test and overlap volumes.
  * `certify.py`: a computer-assisted proof that a tree is self-avoiding at *every* depth.
  * `io.py`: STL and OBJ output.
* `legacy/` holds the original programs (`DedocaedroTREEverCELLS.cpp`, `DedocaedroA-copia.cpp`) and their headers.

## Quick start

```bash
python3 -m venv .venv && .venv/bin/pip install numpy scipy matplotlib
.venv/bin/python scripts/make_tree.py --preset artwork -o out/artwork.stl         # the artwork, depth 5
.venv/bin/python scripts/make_tree.py --g 0.4472136 --theta 63.4349488 --d 1.4472136 -o out/pythagorean.stl
.venv/bin/python scripts/make_tree.py --mode thirty --g 0.35 --depth 4 -o out/all_faces.stl
```

## Reproducing the paper

| step | command | output |
|---|---|---|
| build the original C++ | `bash scripts/build_legacy.sh` | `out/legacy_*.stl` |
| export the Blender scene | `blender -b ~/Downloads/DODC_4.blend --python scripts/export_blend.py` | `out/dragon7.npz` |
| port vs C++ vs Blender | `.venv/bin/python scripts/verify_legacy.py` | `out/verify_legacy.txt` |
| propositions | `.venv/bin/python scripts/theory_checks.py` | `out/theory_checks.txt` |
| clash study and phase diagrams (~1 h on 4 cores) | `.venv/bin/python scripts/clash_study.py` | `out/clash_study.json` |
| critical scale g_c | `.venv/bin/python scripts/critical_g.py` | `out/critical_g.json` |
| figures | `scripts/make_figures_2d.py`, `scripts/make_figures_3d.py` (needs Blender) | `paper/figures/` |

## Findings in one paragraph

The artwork (`tree_7.png`, `tree_11.png`, scene `DODC_4.blend`) is `DedocaedroTREEverCELLS.cpp` with all five
children enabled, depth 5, faces drawn solid: g = 0.36·(1+√2)/2 ≈ 0.4346, d = 1.125·(1+√2)/2 ≈ 1.358 and a
+45° twist about each crown edge. The Python port matches the compiled C++ to 5e-7. The tree is
certified self-avoiding at all depths: only parent–child joints overlap. The Pythagorean member
g = 1/√5, θ = arccos(1/√5), d = 1 + 1/√5 conserves surface area per generation (the six face axes form a
tight frame), touches without overlapping, and has a crown of Hausdorff dimension exactly 2. Growing
from all twelve faces is impossible at the artwork's proportions: a parity argument forces at least six
mis-twisted sibling pairs. It becomes possible, and certified, for g ≤ 0.35 at 45°.

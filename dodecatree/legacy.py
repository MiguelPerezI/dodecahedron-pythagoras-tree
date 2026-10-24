"""Faithful port of the child maps in the original C++ programs.

Every quirk is reproduced on purpose so that the port can be checked
number-for-number against the compiled originals:

* ``Matrix3D(axis, t)`` takes *degrees*, and its 'y' matrix is the transpose
  of the usual right-handed one (legacy/Matrix3D.cpp, lines 30-49).
* ``gold`` inside ``Draw1`` is (1 + sqrt 2)/2, not the golden ratio, so the
  scale factor is g = 0.36 (1 + sqrt 2)/2 = 0.43457... and the offset is
  d = 1.125 (1 + sqrt 2)/2 = 1.35800...
* Edge directions and edge-midpoint directions are typed in with two decimals
  (e.g. (0.5, 0.31, 0.81) for (1/2, 1/(2 phi), phi/2)).
* DedocaedroA-copia.cpp feeds radians where degrees are expected, so its
  rotations are tiny (pi/4 "degrees" ~ 0.785 deg); variant="acopia".

A child map is the affine map x -> g R x + p applied to the parent's *world*
coordinates, so the whole construction is an iterated function system with
condensation (see dodecatree.tree).
"""
import numpy as np

SQRT2_GOLD = (1 + 2 ** 0.5) / 2          # the constant named `gold` in Draw1
LEGACY_G = 0.36 * SQRT2_GOLD
LEGACY_D = 1.125 * SQRT2_GOLD

# (edge-midpoint direction p/d, h0 = xy-projection of the edge, h1 = edge, sign of twist)
_CHILDREN = [
    ((0.0, 0.0, 1.0), None, None, +1),
    ((-0.5, 0.31, 0.81), (-0.24, 0.62, 0.0), (-0.24, 0.62, -0.38), +1),
    ((-0.31, 0.81, 0.5), (0.62, 0.38, 0.0), (0.62, 0.38, -0.24), +1),
    ((0.31, 0.81, 0.5), (-0.62, 0.38, 0.0), (-0.62, 0.38, -0.24), -1),
    ((0.5, 0.31, 0.81), (0.24, 0.62, 0.0), (0.24, 0.62, -0.38), -1),
]


def mat3d(axis, t_deg):
    """Matrix3D(axis, t) from legacy/Matrix3D.cpp (degrees, legacy 'y' sign)."""
    c, s = np.cos(np.radians(t_deg)), np.sin(np.radians(t_deg))
    r, q = {"x": (1, 2), "y": (0, 2), "z": (0, 1)}[axis]
    M = np.eye(3)
    M[r, r], M[r, q], M[q, r], M[q, q] = c, -s, s, c
    return M


def _acos_between(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return np.arccos(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def legacy_maps(variant="cells", angle=45.0):
    """Return the five legacy child maps as a list of (A, p) with A = g R.

    variant="cells":  DedocaedroTREEverCELLS.cpp (twist `angle` degrees).
    variant="acopia": DedocaedroA-copia.cpp (radian/degree mix-up; `angle`
                      is ignored and the twist is pi/4 "degrees").
    """
    g, d = LEGACY_G, LEGACY_D
    maps = []
    for k, (pdir, h0, h1, sgn) in enumerate(_CHILDREN):
        if variant == "cells":
            twist = angle
            deg = 180 / 3.141592            # the C++ uses 360/(2*3.141592)
        elif variant == "acopia":
            twist = 3.1415926535 * 0.25     # 3.1415926535 * (1/RO) with RO = 4
            deg = 1.0                       # phi, teta left in radians
        else:
            raise ValueError(variant)
        if k == 0:
            R = mat3d("x", twist)
        else:
            ph = _acos_between(h0, (1, 0, 0)) * deg
            te = _acos_between(h1, (0, 0, -1)) * deg
            R = (mat3d("z", ph) @ mat3d("y", te) @ mat3d("z", sgn * twist)
                 @ mat3d("y", -te) @ mat3d("z", -ph))
        maps.append((g * R, d * np.array(pdir)))
    return maps

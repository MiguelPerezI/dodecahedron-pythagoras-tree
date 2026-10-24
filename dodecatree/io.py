"""STL input/output."""
import struct

import numpy as np

from .geometry import FACES, triangles


def read_ascii_stl(path):
    """Return an (n, 3, 3) array of triangles from an ASCII STL file."""
    pts = []
    with open(path, encoding="latin-1") as fh:
        for line in fh:
            s = line.split()
            if s and s[0] == "vertex":
                pts.append([float(x) for x in s[1:4]])
    return np.array(pts).reshape(-1, 3, 3)


def write_binary_stl(path, nodes, name=b"dodecahedral pythagoras tree"):
    """Write the solid dodecahedra of `nodes` as a binary STL."""
    tris = np.concatenate([triangles(n.vertices) for n in nodes])
    nrm = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True)
    rec = np.zeros(len(tris), dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
    rec["n"], rec["v"] = nrm, tris
    with open(path, "wb") as fh:
        fh.write(name[:80].ljust(80, b" "))
        fh.write(struct.pack("<I", len(tris)))
        fh.write(rec.tobytes())
    return len(tris)


def write_obj(path, nodes):
    """Write the nodes as an OBJ with true pentagonal faces and one group per depth."""
    with open(path, "w") as fh:
        fh.write("# dodecahedral pythagoras tree\n")
        base = 1
        for n in nodes:
            fh.write(f"g depth{n.depth}\n")
            for v in n.vertices:
                fh.write(f"v {v[0]:.8f} {v[1]:.8f} {v[2]:.8f}\n")
            for f in FACES:
                fh.write("f " + " ".join(str(base + i) for i in f) + "\n")
            base += 20

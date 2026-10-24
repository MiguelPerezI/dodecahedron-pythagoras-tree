#!/usr/bin/env bash
# Compile the original C++ programs (legacy/) and a solid, five-child build of
# DedocaedroTREEverCELLS.cpp used by scripts/verify_legacy.py.
#   bash scripts/build_legacy.sh
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
work="$here/out/legacy_build"
mkdir -p "$work"
cd "$work"
cp "$here"/legacy/{stl.hpp,stl.cpp,Vector3D.hpp,Vector3D.cpp,Matrix3D.hpp,Matrix3D.cpp} .
# Sources are Latin-1 with CRLF line ends.
iconv -f latin1 -t utf8 "$here/legacy/DedocaedroTREEverCELLS.cpp" | tr -d '\r' > cells.cpp
iconv -f latin1 -t utf8 "$here/legacy/DedocaedroA-copia.cpp" | tr -d '\r' > acopia.cpp

# Solid variant: Pentagon() emits the face as three triangles instead of
# edge struts, all five children are enabled, depth 3, no axis pole.
python3 - <<'EOF'
import re
s = open("cells.cpp").read()
s = re.sub(r"(void Torus::Pentagon\(.*?\)\{)(.*?)(\n\s*\}\s*\n)",
           lambda m: m.group(1) + "\n facet(v0,v1,v2); facet(v0,v2,v3); facet(v0,v3,v4);" + m.group(3),
           s, count=1, flags=re.S)
s = s.replace("int Bit2[5] = {1, 1, 0, 0, 0};", "int Bit2[5] = {1, 1, 1, 1, 1};")
s = s.replace("int n = 2;", "int n = 3;")
s = s.replace("t.Arista(Vector3D(0, 0, -5.0), Vector3D(0, 0, 5.0), 5.0)  ;", "")
open("cells_solid.cpp", "w").write(s)
EOF

for prog in cells acopia cells_solid; do
    g++ -O2 -o "$prog" "$prog.cpp" stl.cpp Vector3D.cpp Matrix3D.cpp
    mkdir -p "run_$prog"
    (cd "run_$prog" && "../$prog")
done
cp run_cells_solid/000DodecaDragon5.stl "$here/out/legacy_cells_solid.stl"
cp run_cells/000DodecaDragon5.stl "$here/out/legacy_cells_struts.stl"
cp run_acopia/000DodecaDragon5.stl "$here/out/legacy_acopia.stl"
echo "built: out/legacy_cells_solid.stl out/legacy_cells_struts.stl out/legacy_acopia.stl"

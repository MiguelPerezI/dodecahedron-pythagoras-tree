#!/usr/bin/env bash
# Build the arXiv submission bundle in arxiv/:
#   arxiv/dodecahedral_pythagoras_tree_arxiv.tar.gz  (tex + figures + anc/ code)
#   arxiv/METADATA.txt                               (title, abstract, categories)
# arXiv compiles the .tex itself; the ancillary files appear under "anc/" on the abstract page.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
PAPER=$ROOT/paper
OUT=$ROOT/arxiv
STAGE=$OUT/stage
rm -rf "$STAGE"
mkdir -p "$STAGE/figures" "$STAGE/anc"

cp "$PAPER/dodecahedral_pythagoras_tree.tex" "$STAGE/"
# only the figures the .tex actually includes
grep -o 'figures/[A-Za-z0-9_]*\.\(jpg\|pdf\|png\)' "$PAPER/dodecahedral_pythagoras_tree.tex" | sort -u |
  while read -r f; do cp "$PAPER/$f" "$STAGE/figures/"; done

# ancillary files: the code needed to reproduce every number and figure
cp -r "$ROOT/dodecatree" "$STAGE/anc/dodecatree"
cp -r "$ROOT/scripts" "$STAGE/anc/scripts"
cp -r "$ROOT/legacy" "$STAGE/anc/legacy"
cp "$ROOT/README.md" "$STAGE/anc/README.md"
mkdir -p "$STAGE/anc/out"
cp "$ROOT/out/clash_study.json" "$ROOT/out/critical_g.json" "$ROOT/out/theory_checks.txt" \
   "$ROOT/out/verify_legacy.txt" "$STAGE/anc/out/"
find "$STAGE/anc" -name '__pycache__' -prune -exec rm -rf {} +

# test-compile the staged copy exactly as arXiv will see it
( cd "$STAGE" && pdflatex -interaction=nonstopmode -halt-on-error dodecahedral_pythagoras_tree.tex >/dev/null \
             && pdflatex -interaction=nonstopmode -halt-on-error dodecahedral_pythagoras_tree.tex >/dev/null )
cp "$STAGE/dodecahedral_pythagoras_tree.pdf" "$OUT/dodecahedral_pythagoras_tree.pdf"
rm -f "$STAGE"/*.aux "$STAGE"/*.log "$STAGE"/*.out "$STAGE"/*.pdf

tar -czf "$OUT/dodecahedral_pythagoras_tree_arxiv.tar.gz" -C "$STAGE" .
rm -rf "$STAGE"
echo "bundle: $OUT/dodecahedral_pythagoras_tree_arxiv.tar.gz ($(du -h "$OUT/dodecahedral_pythagoras_tree_arxiv.tar.gz" | cut -f1))"

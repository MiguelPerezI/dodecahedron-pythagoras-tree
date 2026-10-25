#!/usr/bin/env bash
# Build the American Mathematical Monthly submission package in monthly/upload/.
# Required by the portal (upload/required/):
#   1_Manuscript_with_author_details.pdf   "Manuscript - with author details"
#   2_Manuscript_anonymous.pdf             "Manuscript - anonymous"
#   3_Cover_Letter.pdf                     "Cover Letter"
# Optional extras (upload/optional/):
#   LaTeX_source.zip                       "LaTeX Source Files" (asked for in the Instructions for Authors)
#   figures/Figure_N*.{jpg,eps}            figures saved separately (JPEG renders, EPS line art)
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/.." && pwd)
SRC=$HERE/source
UP=$HERE/upload
TEX=dodecahedral_tree_monthly

# 1. figures used by the manuscript, copied from the paper and stripped of metadata
mkdir -p "$SRC/figures"
for f in $(grep -o 'figures/[A-Za-z0-9_]*\.\(jpg\|pdf\)' "$SRC/$TEX.tex" | sort -u); do
  cp "$ROOT/paper/$f" "$SRC/$f"
  case "$f" in *.jpg) mogrify -strip "$SRC/$f" ;; esac
done

# 2. both PDFs
build() {  # $1 = output name, $2 = tex preamble prefix
  ( cd "$SRC"
    for _ in 1 2; do
      pdflatex -interaction=nonstopmode -halt-on-error -jobname="$1" "$2\\input{$TEX}" >/dev/null
    done
    rm -f "$1".aux "$1".log "$1".out )
}
rm -rf "$UP"; mkdir -p "$UP/required" "$UP/optional/figures"
build Manuscript_with_author_details ""
build Manuscript_anonymous "\\def\\ANONYMOUS{}"
mv "$SRC/Manuscript_with_author_details.pdf" "$UP/required/1_Manuscript_with_author_details.pdf"
mv "$SRC/Manuscript_anonymous.pdf" "$UP/required/2_Manuscript_anonymous.pdf"

# 3. figures saved separately, named by figure number
n=0; prev=""
while read -r f; do
  fig=$(awk -v f="$f" '/\\begin\{figure\}/{k++} index($0,f){print k; exit}' "$SRC/$TEX.tex")
  if [ "$fig" != "$prev" ]; then n=0; prev=$fig; fi
  n=$((n+1)); part=$(printf "\\x$(printf %x $((96+n)))")
  base="$UP/optional/figures/Figure_${fig}${part}"
  case "$f" in
    *.jpg) cp "$SRC/$f" "$base.jpg" ;;
    *.pdf) pdftops -eps "$SRC/$f" "$base.eps" ;;
  esac
done < <(grep -o 'figures/[A-Za-z0-9_]*\.\(jpg\|pdf\)' "$SRC/$TEX.tex")
# single-panel figures need no letter
for f in "$UP"/optional/figures/Figure_*a.*; do
  stem=${f%a.*}; ext=${f##*.}
  ls "${stem}b".* >/dev/null 2>&1 || mv "$f" "$stem.$ext"
done

# 4. LaTeX source zip (anonymous build is selected with \def\ANONYMOUS{}, see the header of the .tex)
( cd "$SRC" && zip -qr "$UP/optional/LaTeX_source.zip" "$TEX.tex" figures README_build.txt )

# 5. cover letter
( cd "$HERE/cover_letter" && pdflatex -interaction=nonstopmode -halt-on-error cover_letter.tex >/dev/null \
  && rm -f cover_letter.aux cover_letter.log cover_letter.out && mv cover_letter.pdf "$UP/required/3_Cover_Letter.pdf" )

pdfinfo "$UP/required/1_Manuscript_with_author_details.pdf" | grep Pages | sed 's/^/with author details: /'
pdfinfo "$UP/required/2_Manuscript_anonymous.pdf" | grep Pages | sed 's/^/anonymous:           /'
find "$UP" -type f | sort

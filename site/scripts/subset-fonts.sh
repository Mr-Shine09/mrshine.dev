#!/usr/bin/env bash
# Subset both site faces to Latin and emit woff2 (Plan.md §4.1).
# Requires fontTools: `brew install fonttools` or `pip install fonttools brotli`.
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=src/assets/fonts/source
OUT=src/assets/fonts
UNI="U+0020-007E,U+00A0-00FF,U+2010-2027,U+2030-205E,U+2708"   # U+2708 = ✈ for the motif

subset() { # $1 in.ttf  $2 out.woff2
  pyftsubset "$1" --output-file="$2" --flavor=woff2 --layout-features='*' \
    --unicodes="$UNI" --name-IDs='*' --notdef-outline
  printf '%s  %s bytes\n' "$2" "$(stat -f%z "$2")"
}

mkdir -p "$SRC/geist-sans"
for w in Regular Medium; do
  f="$SRC/geist-sans/Geist-$w.ttf"
  [ -f "$f" ] || curl -fsSL -o "$f" \
    "https://raw.githubusercontent.com/vercel/geist-font/main/packages/next/dist/fonts/geist-sans/Geist-$w.ttf"
done
[ -f "$SRC/geist-sans/OFL.txt" ] || curl -fsSL -o "$SRC/geist-sans/OFL.txt" \
  "https://raw.githubusercontent.com/vercel/geist-font/main/OFL.txt"

subset "$SRC/geist-pixel/GeistPixel-Regular-VariableFont_ELSH.ttf" "$OUT/geist-pixel.woff2"
subset "$SRC/geist-sans/Geist-Regular.ttf" "$OUT/geist-sans.woff2"
subset "$SRC/geist-sans/Geist-Medium.ttf"  "$OUT/geist-sans-medium.woff2"

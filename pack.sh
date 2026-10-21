#!/usr/bin/env bash
set -euo pipefail

SHELLDIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ver="${1:?用法: ./pack.sh VERSION}"
[[ "$ver" =~ ^[a-zA-Z0-9._-]+$ ]] || { echo "版本号只能包含字母、数字、点、下划线和连字符" >&2; exit 1; }

"${PYTHON:-python3}" "$SHELLDIR/scripts/validate_packages.py" "$SHELLDIR/data"
for variant in hapin_arabic hapin_cyrillic hapin_mixed_arabic_cyrillic; do
  (
    cd "$SHELLDIR/data/$variant"
    archive="../clover_${variant}.schema-${ver}.zip"
    rm -f "$archive"
    zip -5 "$archive" ./*.yaml opencc/*
  )
done

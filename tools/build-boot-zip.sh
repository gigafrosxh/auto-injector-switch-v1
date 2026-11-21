#!/bin/bash
# Baut dist/teria-boot-<version>.zip: Inhalt wird 1:1 auf die FAT32-Partition der SD-Karte entpackt.
set -euo pipefail
cd "$(dirname "$0")/.."
VERSION=${1:-$(cat VERSION)}
STAGE=$(mktemp -d); trap 'rm -rf "$STAGE"' EXIT
mkdir -p "$STAGE/bootloader/ini" "$STAGE/switchroot/teria"
cp boot/teria/teria.ini "$STAGE/bootloader/ini/teria.ini"
cp boot/teria/icon_teria.bmp boot/teria/bootlogo_teria.bmp "$STAGE/switchroot/teria/"
mkdir -p dist
OUT="$PWD/dist/teria-boot-$VERSION.zip"
rm -f "$OUT"
(cd "$STAGE" && zip -qr -X "$OUT" .)
echo "dist/teria-boot-$VERSION.zip"

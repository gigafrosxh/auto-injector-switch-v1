#!/bin/bash
# Baut dist/teria-base_<version>_all.deb aus os/teria-base. Laeuft auf Linux und macOS (dpkg-deb noetig).
set -euo pipefail
cd "$(dirname "$0")/.."
VERSION=${1:-$(cat VERSION)}
# Debian-Versionen: "-rc.1" muss als "~rc.1" geschrieben werden, damit 0.1.0~rc.1 < 0.1.0 gilt
DEBVER=${VERSION/-/\~}
OUT=dist
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT
chmod 755 "$STAGE"

cp -R os/teria-base/. "$STAGE/"
find "$STAGE" -name .DS_Store -delete
sed "s/@VERSION@/$DEBVER/" "$STAGE/DEBIAN/control.in" > "$STAGE/DEBIAN/control"
rm "$STAGE/DEBIAN/control.in"
echo "$VERSION" > "$STAGE/usr/lib/teria/version"
mkdir -p "$OUT"
DEB="$OUT/teria-base_${DEBVER}_all.deb"
dpkg-deb --root-owner-group -Zxz --build "$STAGE" "$DEB" >/dev/null
echo "$DEB"

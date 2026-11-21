#!/bin/bash
# Baut die Teria-Pakete aus os/<paket> nach dist/<paket>_<version>_all.deb.
#   tools/build-deb.sh [version] [paket ...]     (Standard: teria-base teria-shell)
# Laeuft auf Linux und macOS (dpkg-deb noetig). Gibt die Pfade der Pakete aus.
set -euo pipefail
cd "$(dirname "$0")/.."
VERSION=${1:-$(cat VERSION)}
shift || true
PKGS=("$@")
[ ${#PKGS[@]} -gt 0 ] || PKGS=(teria-base teria-shell)
# Debian-Versionen: "-rc.1" muss als "~rc.1" geschrieben werden, damit 0.1.0~rc.1 < 0.1.0 gilt
DEBVER=${VERSION/-/\~}
mkdir -p dist
for pkg in "${PKGS[@]}"; do
    STAGE=$(mktemp -d)
    chmod 755 "$STAGE"
    cp -R "os/$pkg/." "$STAGE/"
    find "$STAGE" \( -name .DS_Store -o -name __pycache__ \) -prune -exec rm -rf {} +
    sed "s/@VERSION@/$DEBVER/g" "$STAGE/DEBIAN/control.in" > "$STAGE/DEBIAN/control"
    rm "$STAGE/DEBIAN/control.in"
    [ "$pkg" = teria-base ] && echo "$VERSION" > "$STAGE/usr/lib/teria/version"
    DEB="dist/${pkg}_${DEBVER}_all.deb"
    dpkg-deb --root-owner-group -Zxz --build "$STAGE" "$DEB" >/dev/null
    rm -rf "$STAGE"
    echo "$DEB"
done

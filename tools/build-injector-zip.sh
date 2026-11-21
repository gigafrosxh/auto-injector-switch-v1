#!/bin/bash
# Baut dist/teria-injector-windows-<version>.zip (ohne Payload und ohne TegraRcmSmash).
set -euo pipefail
cd "$(dirname "$0")/.."
VERSION=${1:-$(cat VERSION)}
mkdir -p dist
OUT="$PWD/dist/teria-injector-windows-$VERSION.zip"
rm -f "$OUT"
(cd injector && zip -qr -X "$OUT" windows -x '*.bin' -x '*/config.json' -x '*/approved.txt' -x '*.log*' -x '*.DS_Store')
echo "dist/teria-injector-windows-$VERSION.zip"

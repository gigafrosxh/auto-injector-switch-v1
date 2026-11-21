#!/bin/bash
# Installiert Teria per SSH auf der Switch. Fragt vor jedem Schreibschritt nach.
#
#   tools/deploy.sh [--host daniel@192.168.178.69]
#
# Fuer ein laufendes Linux (Switchroot Ubuntu oder Teria): installiert nur das Paket
# teria-base. Das eigenstaendige Teria-System wird ueber das SD-Paket installiert
# (docs/INSTALLATION.md). Nie eMMC, nie Formatieren, nie Payloads.
set -euo pipefail
cd "$(dirname "$0")/.."
HOST=daniel@192.168.178.69
while [ $# -gt 0 ]; do
    case "$1" in
        --host) HOST=$2; shift ;;
        -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
        *) echo "Unbekannte Option: $1"; exit 2 ;;
    esac
    shift
done

ask() { local a; read -r -p "$1 [ja/NEIN] " a; [ "$a" = ja ]; }

DEB=$(tools/build-deb.sh)
echo "Paket gebaut: $DEB"
echo "Ziel: $HOST"
ssh "$HOST" 'uname -a; . /etc/os-release; echo "$PRETTY_NAME"; dpkg-query -W -f "installiert: teria-base \${Version}\n" teria-base 2>/dev/null || echo "teria-base noch nicht installiert"'

if ask "teria-base auf $HOST installieren?"; then
    scp -q "$DEB" "$HOST:/tmp/teria-base.deb"
    ssh -t "$HOST" 'sudo apt-get install -y /tmp/teria-base.deb && rm -f /tmp/teria-base.deb && teria info'
else
    echo "Paket nicht installiert."
fi

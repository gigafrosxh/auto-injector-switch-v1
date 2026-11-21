#!/bin/bash
# Installiert Teria per SSH auf der Switch. Fragt vor jedem Schreibschritt nach.
#
#   tools/deploy.sh [--host daniel@192.168.178.69] [--boot] [--yes-paket]
#
#   --boot   zusaetzlich den Hekate-Eintrag "Teria" auf die SD-Karte kopieren
#            (bootloader/ini/teria.ini + switchroot/teria/*.bmp). Eigene Rueckfrage.
#
# Schreibt ausschliesslich ins Linux-rootfs (Paketinstallation) bzw. auf die
# FAT32-Partition der SD-Karte. Nie auf den eMMC, nie Formatieren, nie Payloads.
set -euo pipefail
cd "$(dirname "$0")/.."
HOST=daniel@192.168.178.69
BOOT=0
while [ $# -gt 0 ]; do
    case "$1" in
        --host) HOST=$2; shift ;;
        --boot) BOOT=1 ;;
        -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
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

if [ "$BOOT" = 1 ]; then
    ZIP=$(tools/build-boot-zip.sh)
    # FAT32-Partition der SD-Karte finden und pruefen, dass sie wirklich auf der SD liegt
    SD=$(ssh "$HOST" 'for p in $(lsblk -rno NAME,FSTYPE | awk "\$2==\"vfat\"{print \$1}"); do
            d=$(lsblk -no PKNAME /dev/$p); [ "$(cat /sys/block/$d/device/type 2>/dev/null)" = SD ] || continue
            m=$(lsblk -no MOUNTPOINT /dev/$p); [ -n "$m" ] && [ -d "$m/bootloader" ] && { echo "$m"; break; }
         done')
    if [ -z "$SD" ]; then echo "Keine eingehaengte SD-Bootpartition mit bootloader/ gefunden."; exit 1; fi
    echo "SD-Bootpartition: $SD"
    echo "Es werden NUR diese Dateien angelegt/ersetzt:"
    unzip -Z1 "$ZIP" | grep -v '/$' | sed 's/^/  /'
    if ask "Booteintrag auf die SD-Karte kopieren?"; then
        scp -q "$ZIP" "$HOST:/tmp/teria-boot.zip"
        # shellcheck disable=SC2029  # $SD soll lokal eingesetzt werden
        ssh "$HOST" "cd \"$SD\" && unzip -o -q /tmp/teria-boot.zip && sync && rm -f /tmp/teria-boot.zip && ls -la bootloader/ini switchroot/teria"
        echo "Fertig. Beim naechsten Start zeigt Hekate unter \"More configs\" den Eintrag Teria."
    else
        echo "Booteintrag nicht kopiert."
    fi
fi

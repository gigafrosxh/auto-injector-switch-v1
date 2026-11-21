#!/bin/bash
# Baut das eigenstaendige Teria-System (Debian trixie arm64 + Switchroot-Kernel/L4T).
#
#   sudo tools/build-image.sh [version] [ausgabeordner]
#
# Ergebnis in <ausgabeordner> (Standard dist/):
#   teria-<version>-sd.zip   Inhalt 1:1 auf die FAT32-Partition der SD-Karte entpacken,
#                            dann in Hekate: Nyx > Tools > Partition SD > Flash Linux
#   teria-<version>.manifest Paketliste des Images
#
# Laeuft nur auf Linux arm64 (z. B. GitHub-Runner ubuntu-24.04-arm) mit root-Rechten.
# Das Skript schreibt ausschliesslich in Arbeitsverzeichnisse unter $WORK. Es partitioniert,
# formatiert oder flasht kein echtes Laufwerk; mke2fs arbeitet nur auf einer Image-Datei.
set -euo pipefail
cd "$(dirname "$0")/.."
REPO=$PWD
VERSION=${1:-$(cat VERSION)}
OUT=$(realpath -m "${2:-dist}")
WORK=${WORK:-$(mktemp -d /var/tmp/teria-build.XXXXXX)}
ROOT=$WORK/rootfs
SUITE=trixie
MIRROR=http://deb.debian.org/debian
L4T_REPO=https://theofficialgman.github.io/l4t-debs
L4T_KEY_FPR=1B920C89A4283780164AE26773A65EDFE6C919A5
LABEL=SWR-TER
KEYRING_DEB=http://deb.debian.org/debian/pool/main/d/debian-archive-keyring/debian-archive-keyring_2025.1_all.deb
KEYRING_SHA=9ea7778e443144ca490668737a8ab22dd3e748bb99e805e22ec055abeb3c7fac
PART_SIZE=4290772992   # Teilgroesse, die Hekate fuer switchroot/install/l4t.NN erwartet

[ "$(id -u)" -eq 0 ] || { echo "Bitte mit sudo ausfuehren."; exit 1; }
[ "$(dpkg --print-architecture)" = arm64 ] || { echo "Nur auf arm64 (nativ) unterstuetzt."; exit 1; }
for t in mmdebstrap mke2fs e2fsck zip gpg curl sha256sum; do command -v $t >/dev/null || { echo "Fehlt: $t"; exit 1; }; done

log() { printf '\n==> %s\n' "$*"; }
pkgs() { grep -v -E '^\s*(#|$)' "$1" | tr '\n' ' '; }

# L4T-Schluessel gegen den gepinnten Fingerabdruck pruefen
fpr=$(gpg --show-keys --with-colons "$REPO/os/image/apt/theofficialgman-L4T.asc" | awk -F: '/^fpr/{print $10; exit}')
[ "$fpr" = "$L4T_KEY_FPR" ] || { echo "L4T-Schluessel hat falschen Fingerabdruck: $fpr"; exit 1; }

cleanup() {
    for m in dev/pts dev proc sys run; do mountpoint -q "$ROOT/$m" && umount -l "$ROOT/$m"; done
    return 0
}
trap cleanup EXIT

log "Teria $VERSION: Debian $SUITE arm64 nach $ROOT"
mkdir -p "$WORK" "$OUT"
DEBVER=${VERSION/-/\~}
"$REPO/tools/build-deb.sh" "$VERSION" >/dev/null
TERIA_DEB=$REPO/dist/teria-base_${DEBVER}_all.deb

# Debian-Archivschluessel fuer trixie (der des Build-Hosts ist evtl. zu alt), Hash gepinnt
curl -fsSL -o "$WORK/keyring.deb" "$KEYRING_DEB"
echo "$KEYRING_SHA  $WORK/keyring.deb" | sha256sum -c --quiet
dpkg-deb -x "$WORK/keyring.deb" "$WORK/keyring"
KEYRING=$WORK/keyring/usr/share/keyrings/debian-archive-keyring.gpg

mmdebstrap --arch=arm64 --variant=important --keyring="$KEYRING" \
    --components="main contrib non-free non-free-firmware" \
    --include="$(pkgs os/image/packages-debian.txt | tr ' ' ',' | sed 's/,$//')" \
    --aptopt='APT::Install-Recommends "false"' \
    --dpkgopt='path-exclude=/usr/share/doc/*' --dpkgopt='path-include=/usr/share/doc/*/copyright' \
    --dpkgopt='path-exclude=/usr/share/man/*' \
    "$SUITE" "$ROOT" \
    "deb $MIRROR $SUITE main contrib non-free non-free-firmware" \
    "deb $MIRROR $SUITE-updates main contrib non-free non-free-firmware" \
    "deb http://security.debian.org/debian-security $SUITE-security main contrib non-free non-free-firmware"

log "Chroot vorbereiten"
for m in proc sys dev dev/pts run; do mkdir -p "$ROOT/$m"; done
mount -t proc proc "$ROOT/proc"; mount -t sysfs sys "$ROOT/sys"
mount --bind /dev "$ROOT/dev"; mount --bind /dev/pts "$ROOT/dev/pts"; mount -t tmpfs tmpfs "$ROOT/run"
cp /etc/resolv.conf "$ROOT/etc/resolv.conf"
printf '#!/bin/sh\nexit 101\n' > "$ROOT/usr/sbin/policy-rc.d"; chmod 755 "$ROOT/usr/sbin/policy-rc.d"
in_root() { chroot "$ROOT" /usr/bin/env DEBIAN_FRONTEND=noninteractive LC_ALL=C.UTF-8 "$@"; }

log "L4T-Repo einbinden"
install -D -m 644 os/image/apt/theofficialgman-L4T.asc "$ROOT/etc/apt/keyrings/theofficialgman-L4T.asc"
echo "deb [signed-by=/etc/apt/keyrings/theofficialgman-L4T.asc] $L4T_REPO l4t noble" > "$ROOT/etc/apt/sources.list.d/l4t.list"
# libpcre3 (von nvidia-l4t-multimedia gebraucht) gibt es in trixie nicht mehr, nur in bookworm (per Pin begrenzt)
echo "deb $MIRROR bookworm main" > "$ROOT/etc/apt/sources.list.d/bookworm-compat.list"
install -m 644 os/image/apt/teria-l4t.pref "$ROOT/etc/apt/preferences.d/teria-l4t.pref"
in_root apt-get update

log "Switchroot-Kernel, Module, Firmware und L4T-Treiber"
# switch-bsp kopiert sonst beim Installieren Bootdateien auf eine SD-Karte
mkdir -p "$ROOT/opt/switchroot" "$ROOT/etc/apport/blacklist.d" "$ROOT/var/lib/dbus"
touch "$ROOT/opt/switchroot/image_prep"
# shellcheck disable=SC2046
in_root apt-get install -y --no-install-recommends $(pkgs os/image/packages-l4t.txt)
[ -d "$ROOT/lib/modules/4.9.140-l4t" ] || { echo "Kernelmodule fehlen."; exit 1; }
[ -f "$ROOT/opt/switchroot/bootstack/uImage" ] || { echo "Bootstack fehlt."; exit 1; }

log "teria-base"
cp "$TERIA_DEB" "$ROOT/tmp/teria-base.deb"
in_root apt-get install -y /tmp/teria-base.deb
rm -f "$ROOT/tmp/teria-base.deb"

log "Systemeinstellungen"
cp -a os/image/overlay/. "$ROOT/"
sed -i 's/^# *de_DE.UTF-8/de_DE.UTF-8/; s/^# *en_US.UTF-8/en_US.UTF-8/' "$ROOT/etc/locale.gen"
in_root locale-gen
in_root update-locale LANG=de_DE.UTF-8
ln -sf /usr/share/zoneinfo/Europe/Vienna "$ROOT/etc/localtime"; echo Europe/Vienna > "$ROOT/etc/timezone"
echo teria > "$ROOT/etc/hostname"
for g in sudo audio video plugdev netdev bluetooth input render dialout; do in_root getent group $g >/dev/null || in_root groupadd -r $g; done
in_root useradd -m -s /bin/bash -G sudo,audio,video,plugdev,netdev,bluetooth,input,render,dialout teria
echo 'teria:teria' | in_root chpasswd
in_root chage -d 0 teria        # Passwort muss beim ersten Anmelden geaendert werden
in_root systemctl enable lightdm.service NetworkManager.service ssh.service teria-firstboot.service teria-emmc-guard.service
in_root systemctl set-default graphical.target

log "Aufraeumen"
in_root apt-get clean
rm -f "$ROOT/usr/sbin/policy-rc.d" "$ROOT/etc/resolv.conf"
ln -sf ../run/NetworkManager/resolv.conf "$ROOT/etc/resolv.conf"
rm -f "$ROOT"/etc/ssh/ssh_host_*        # werden beim ersten Start neu erzeugt
: > "$ROOT/etc/machine-id"; rm -f "$ROOT/var/lib/dbus/machine-id"
rm -rf "$ROOT"/var/lib/apt/lists/* "$ROOT"/tmp/* "$ROOT"/var/log/*.log
# shellcheck disable=SC2016  # dpkg-Format, kein Shell-Ausdruck
in_root dpkg-query -W -f '${Package}\t${Version}\n' > "$OUT/teria-$VERSION.manifest"
cleanup

log "ext4-Image ($LABEL)"
used=$(du -sxm "$ROOT" | cut -f1)
size=$(( (used * 13 / 10 + 768 + 3) / 4 * 4 ))   # +30 % +768 MiB, auf 4 MiB gerundet
IMG=$WORK/teria.img
rm -f "$IMG"; truncate -s "${size}M" "$IMG"
mke2fs -q -F -t ext4 -L "$LABEL" -E root_owner=0:0 -d "$ROOT" "$IMG"
e2fsck -fy "$IMG" >/dev/null || [ $? -le 1 ]
echo "rootfs: ${used} MiB belegt, Image ${size} MiB"

log "SD-Paket"
SD=$WORK/sd
rm -rf "$SD"; mkdir -p "$SD/bootloader/ini" "$SD/switchroot/teria" "$SD/switchroot/install" "$SD/extras/bootloader/ini"
cp -r "$ROOT/opt/switchroot/bootstack/." "$SD/switchroot/teria/"
rm -f "$SD/switchroot/teria/bootlogo_ubuntu.bmp" "$SD/switchroot/teria/icon_ubuntu_hue.bmp" "$SD/switchroot/teria/.cleanup"
cp boot/teria/icon_teria.bmp boot/teria/bootlogo_teria.bmp "$SD/switchroot/teria/"
cp boot/teria/teria.ini "$SD/bootloader/ini/teria.ini"
cp boot/teria/teria-usb.ini "$SD/extras/bootloader/ini/teria-usb.ini"
split -b "$PART_SIZE" -d -a 2 "$IMG" "$SD/switchroot/install/l4t."
(cd "$SD" && find . -type f -print0 | sort -z | xargs -0 sha256sum > "$WORK/SHA256SUMS" && mv "$WORK/SHA256SUMS" SHA256SUMS)
ZIP=$OUT/teria-$VERSION-sd.zip
rm -f "$ZIP"
(cd "$SD" && zip -q -r -9 "$ZIP" .)
ls -la "$OUT"
[ "${KEEP_WORK:-0}" = 1 ] || rm -rf "$WORK"
echo "Fertig: $ZIP"

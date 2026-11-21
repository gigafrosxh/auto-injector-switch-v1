# shellcheck shell=bash
# Gemeinsame Funktionen fuer Teria. Wird von /usr/bin/teria und den Diensten geladen.
#
# Grundregel: Teria schreibt NIE auf den internen eMMC (NAND) der Switch.
# Speicher wird ueber den Kartentyp erkannt (sysfs device/type = "MMC" bzw. "SD"),
# nicht ueber den Geraetenamen: unter Switchroot ist /dev/mmcblk0 die SD-Karte.

TERIA_VERSION_FILE=${TERIA_LIB:-/usr/lib/teria}/version
R2P=/sys/devices/r2p

teria_version() { cat "$TERIA_VERSION_FILE" 2>/dev/null || echo unbekannt; }

# Liest eine Datei, gibt bei Fehler "?" aus.
rd() { local v; v=$(cat "$1" 2>/dev/null) && printf '%s' "$v" || printf '?'; }

# Alle mmcblk-Geraete eines Typs (MMC = interner eMMC, SD = SD-Karte).
mmc_disks_of_type() {
    local want=$1 d
    for d in /sys/block/mmcblk[0-9]*; do
        [ -e "$d" ] || continue
        case "${d##*/}" in *boot*|*rpmb*) continue ;; esac
        [ "$(rd "$d/device/type")" = "$want" ] && echo "${d##*/}"
    done
}

# Zugehoerige Hardware-Partitionen (boot0/boot1) eines eMMC.
emmc_hw_parts() { local d; for d in /sys/block/"$1"boot*; do [ -e "$d" ] && echo "${d##*/}"; done; }

# Basisgeraet, auf dem / liegt (z. B. mmcblk0).
root_disk() {
    local src
    src=$(findmnt -no SOURCE / 2>/dev/null)
    [ "$src" = /dev/root ] && src=$(sed -n 's/.*root=\([^ ]*\).*/\1/p' /proc/cmdline)
    src=$(readlink -f "$src" 2>/dev/null || echo "$src")
    lsblk -no PKNAME "$src" 2>/dev/null | head -n1
}

# Status des eMMC-Schutzes: "geschuetzt", "offen", "nicht sichtbar" oder "rootfs auf eMMC".
emmc_guard_state() {
    local disks d p state=geschuetzt
    disks=$(mmc_disks_of_type MMC)
    [ -z "$disks" ] && { echo "nicht sichtbar"; return; }
    for d in $disks; do
        [ "$(root_disk)" = "$d" ] && { echo "rootfs auf eMMC"; return; }
        [ "$(rd "/sys/block/$d/ro")" = 1 ] || state=offen
        for p in $(emmc_hw_parts "$d"); do
            [ "$(rd "/sys/block/$p/force_ro")" = 1 ] || state=offen
        done
    done
    echo "$state"
}

r2p_available() { [ -w "$R2P/action" ] || [ -r "$R2P/action" ]; }

need_root() {
    if [ "$(id -u)" -ne 0 ]; then
        exec sudo -- "$0" "$@"
    fi
}

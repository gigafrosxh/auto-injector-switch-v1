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

# FAT32-Bootpartition auf der SD-Karte (Hekate, switchroot/), z. B. mmcblk0p1.
sd_boot_part() {
    local d p
    for d in $(mmc_disks_of_type SD); do
        for p in /sys/block/"$d"/"$d"p*; do
            [ -e "$p" ] || continue
            [ "$(lsblk -no FSTYPE "/dev/${p##*/}" 2>/dev/null)" = vfat ] && { echo "${p##*/}"; return 0; }
        done
    done
    return 1
}

# Haengt die FAT32-Partition der SD unter /run/teria/sd ein (root). Gibt den Pfad aus.
sd_mount() {
    local part mp=/run/teria/sd
    mountpoint -q "$mp" && { echo "$mp"; return 0; }
    part=$(sd_boot_part) || return 1
    mkdir -p "$mp"
    mount -t vfat -o rw,nosuid,nodev,noexec,umask=077 "/dev/$part" "$mp" || return 1
    echo "$mp"
}

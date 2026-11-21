#!/bin/sh
# Teria Rettungs-Skript: wird einmalig ueber die Kernel-Kommandozeile gestartet
# (systemd.mount-extra + systemd.run in teria.ini) und liegt auf der FAT32-Partition.
#  1. sammelt Logs nach /mnt/sd/teria-debug/
#  2. schaltet Bildschirmtastatur und automatische Anmeldung ein
#  3. stellt teria.ini wieder her und startet die grafische Oberflaeche
# Schreibt nur ins Teria-rootfs und auf die FAT32-Partition der SD, nie auf den eMMC.
SD=/mnt/sd
OUT=$SD/teria-debug
mkdir -p "$OUT"
exec >"$OUT/rescue.log" 2>&1
set -x
date
uname -a
cat /proc/cmdline

# --- 1. Logs
journalctl --list-boots --no-pager
journalctl -b -1 --no-pager -o short-monotonic > "$OUT/journal-vorher.txt" 2>&1
journalctl -b -1 -p warning --no-pager > "$OUT/journal-vorher-warnungen.txt" 2>&1
journalctl -b 0 --no-pager -o short-monotonic > "$OUT/journal-jetzt.txt" 2>&1
cp /var/log/Xorg.0.log "$OUT/Xorg.0.log" 2>/dev/null
cp /var/log/Xorg.0.log.old "$OUT/Xorg.0.log.old" 2>/dev/null
cp /var/log/lightdm/*.log "$OUT/" 2>/dev/null
systemctl --failed --no-pager > "$OUT/failed-units.txt" 2>&1
systemctl status lightdm nv-l4t-usb-device-mode nvfb nvfb-early nv teria-firstboot teria-emmc-guard --no-pager -l > "$OUT/status.txt" 2>&1
systemctl list-unit-files --no-pager --state=enabled > "$OUT/enabled.txt" 2>&1
dmesg > "$OUT/dmesg.txt" 2>&1
ls -la /dev/dri /dev/fb* /dev/nvhost* /dev/tegra* > "$OUT/devices.txt" 2>&1
lsmod > "$OUT/lsmod.txt" 2>&1
cat /etc/X11/xorg.conf > "$OUT/xorg.conf" 2>&1
ls -la /usr/lib/xorg/modules/drivers /usr/lib/aarch64-linux-gnu/tegra > "$OUT/xorg-drivers.txt" 2>&1
dpkg -l > "$OUT/dpkg.txt" 2>&1
id teria; chage -l teria
df -h; lsblk -o NAME,SIZE,TYPE,FSTYPE,LABEL,MOUNTPOINT,RO
cat /etc/os-release

# --- 2. Bildschirmtastatur und automatische Anmeldung
mkdir -p /etc/lightdm/lightdm-gtk-greeter.conf.d /etc/lightdm/lightdm.conf.d
cat > /etc/lightdm/lightdm-gtk-greeter.conf.d/60-tastatur.conf <<'EOF'
[greeter]
keyboard=onboard --xid --layout=Compact --theme=Nightshade
a11y-states=+keyboard
keyboard-position=50%,center -0;100% 35%
EOF
cat > /etc/lightdm/lightdm.conf.d/70-autologin.conf <<'EOF'
[Seat:*]
autologin-user=teria
autologin-user-timeout=0
autologin-session=teria
EOF
groupadd -rf autologin; usermod -aG autologin teria
# Erzwungenen Passwortwechsel aufheben (Passwort bleibt "teria"), sonst scheitert die Autoanmeldung
chage -d "$(date +%Y-%m-%d)" teria
chage -l teria

# USB-Netzwerk (Mac/PC per USB-C) einschalten, falls vorhanden
systemctl enable --now nv-l4t-usb-device-mode.service
systemctl status nv-l4t-usb-device-mode.service --no-pager -l
ip addr

# --- 3. teria.ini zuruecksetzen (Rettungs-Parameter entfernen) und Oberflaeche starten
if [ -f "$SD/bootloader/ini/teria.ini" ]; then
    sed -i 's/^bootargs_extra=.*/bootargs_extra=SYSTEMD_CGROUP_ENABLE_LEGACY_FORCE=1/' "$SD/bootloader/ini/teria.ini"
    cat "$SD/bootloader/ini/teria.ini"
fi
sync
systemctl restart lightdm.service
sleep 20
systemctl status lightdm --no-pager -l
cp /var/log/Xorg.0.log "$OUT/Xorg.0.log.nach-neustart" 2>/dev/null
cp /var/log/lightdm/*.log "$OUT/" 2>/dev/null
journalctl -b 0 -u lightdm --no-pager > "$OUT/lightdm-journal.txt" 2>&1
echo FERTIG
sync

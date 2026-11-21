#!/bin/bash
# Zwei Starts mit derselben Einrichtung prüfen, vollständig im Wegwerfcontainer.
set -eu
cd "$(dirname "$0")/.."
docker run --rm -i -v "$PWD/os/teria-base/usr/lib/teria/setup-from-sd:/setup:ro" debian:trixie bash -eu <<'TEST'
export TERIA_LIB=/tmp/lib
mkdir -p "$TERIA_LIB" /tmp/sd /etc/NetworkManager/system-connections
cat > "$TERIA_LIB/lib.sh" <<'LIB'
sd_mount() { echo /tmp/sd; }
umount() { :; }
sync() { :; }
LIB
input=/tmp/sd/teria-setup.txt
profile=/etc/NetworkManager/system-connections/teria-Beispiel.nmconnection
printf 'wlan_name=Beispiel\nwlan_passwort=erstes-testwort\n' > "$input"
bash /setup
grep -qx 'psk=erstes-testwort' "$profile"
[ "$(stat -c %a "$profile")" = 600 ]
grep -qx 'wlan_name=' "$input"
grep -qx 'wlan_passwort=' "$input"
cp "$profile" /tmp/original
bash /setup
cmp "$profile" /tmp/original
# SD-Datei aus 0.3.1 mit stehen gebliebenem Namen.
printf 'wlan_name=Beispiel\nwlan_passwort=\n' > "$input"
bash /setup
cmp "$profile" /tmp/original
printf 'wlan_name=Beispiel\nwlan_passwort=zweites-testwort\n' > "$input"
bash /setup
grep -qx 'psk=zweites-testwort' "$profile"
printf 'wlan_name=Gast\nwlan_passwort=\n' > "$input"
bash /setup
guest=/etc/NetworkManager/system-connections/teria-Gast.nmconnection
grep -qx 'ssid=Gast' "$guest"
if grep -q 'wifi-security' "$guest"; then exit 1; fi
mv /etc/NetworkManager/system-connections /tmp/profiles
printf 'wlan_name=Beispiel\nwlan_passwort=erneut-versuchen\n' > "$input"
if bash /setup; then exit 1; fi
grep -qx 'wlan_passwort=erneut-versuchen' "$input"
TEST

#!/bin/bash
# Im CI-Container mit frischem HOME, Xvfb und eigenem Sitzungsbus ausführen.
set -eu
test -r /usr/share/xfce4/panel/plugins/power-manager-plugin.desktop
xfce4-panel --disable-wm-check > "$HOME/panel.log" 2>&1 &
panel_pid=$!
trap 'kill "$panel_pid" 2>/dev/null || true; wait "$panel_pid" 2>/dev/null || true' EXIT
# Xfce lädt Module je nach Konfiguration im Panel oder in einem Wrapper-Prozess.
for ((i = 0; i < 100; i++)); do
    kill -0 "$panel_pid" 2>/dev/null || break
    if grep -Fqs '/xfce4/panel/plugins/libxfce4powermanager.so' /proc/[0-9]*/maps; then
        echo 'Xfce hat die Energieanzeige geladen.'
        exit 0
    fi
    sleep 0.1
done
cat "$HOME/panel.log" >&2
echo 'Energieanzeige wurde in der Teria-Leiste nicht geladen.' >&2
exit 1

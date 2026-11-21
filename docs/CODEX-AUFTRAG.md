# Auftrag für Codex: Teria weiterentwickeln

Repo: https://github.com/gigafrosxh/auto-injector-switch-v1 (lokal: `/Volumes/ExterneSSD/teria`)
Issues: https://github.com/gigafrosxh/auto-injector-switch-v1/issues
Meilensteine: https://github.com/gigafrosxh/auto-injector-switch-v1/milestones

Lies zuerst `AGENTS.md` (Arbeitsregeln, Versionierung, Sicherheitsregeln), `README.md`,
`docs/ARCHITEKTUR.md`, `docs/INSTALLATION.md` und `CHANGELOG.md`. Arbeite die Aufgaben unten
in dieser Reihenfolge ab, jeweils mit Issue, Commit `Closes #N`, CHANGELOG-Eintrag und Release
nach den Regeln in `AGENTS.md` (Release-Titel „Teria vX.Y.Z“, CI erstellt das Release beim Tag).

## Stand (21.11.2026)

- Teria 0.3.1 läuft auf der Switch des Nutzers (Debian trixie arm64 + Switchroot-Kernel 4.9.140-l4t, L4T 32.3.1).
- Branch `fix/0.3.2` enthält fertige, noch nicht veröffentlichte Fixes für #33 (Bibliotheksfilter,
  Helligkeit per udev, zram lz4, Ladeanzeige, Store ohne Passwort). Der Bibliotheksfilter ist auf der Switch getestet.
- Die Oberfläche lässt sich am Mac mit Beispieldaten prüfen:
  `TERIA_SHELL_MOCK=1 os/teria-shell/usr/bin/teria-shell --browser`.
- Das Image baut nur die CI (`ubuntu-24.04-arm`, Job `image`). Lokal: `tools/build-deb.sh`, `shellcheck`.

## Aufgaben

1. **0.3.2 fertigstellen** (#33): Branch `fix/0.3.2` prüfen, den USB-Gerätemodus reparieren
   (`nv-l4t-usb-device-mode.service` endet mit Exit 127 „Befehl nicht gefunden“ im Skript
   `/opt/nvidia/l4t-usb-device-mode/nv-l4t-usb-device-mode-start.sh`; fehlendes Werkzeug im Image
   ergänzen oder Dienst sauber ersetzen), CI grün, nach `main` mergen, Tag `v0.3.2`.
2. **#29**: Kompatibilität der L4T-Pakete mit trixie dokumentieren (was läuft, welche Pins nötig sind),
   Ergebnis in `docs/`, Issue schließen.
3. **0.4.0 Einrichtungsassistent** (#27): Vollbild-Assistent in `teria-shell` beim ersten Start
   (Sprache, Zeitzone, WLAN, Benutzername/Passwort mit Bildschirmtastatur), danach deaktiviert.
   `teria-setup.txt` von der SD bleibt als Alternative erhalten.
4. **0.4.0 Injector, nur Windows-Teile**: #10 (payloads.json), #11 (Hekate-Update-Assistent),
   #12 (Injector-Bundle im Release). **#9 nicht bearbeiten**, das entscheidet der Nutzer selbst.
5. **0.5.0** (#13, #14, #15): Leistungsprofile ausbauen, Statusanzeige, Dock-Erkennung.
6. **0.6.0** (#19, #20): apt-Repository über GitHub Pages, `teria update` mit Rollback.

Neue Fehler, die du findest: als `[Bug]` mit Label P0–P3 anlegen und nach den Prioritätsregeln einplanen.

## Harte Grenzen

- **Nichts auf der Switch ausführen, installieren oder flashen** (kein SSH auf 192.168.178.69, kein Zugriff auf die SD-Karte).
  Tests auf dem Gerät macht der Nutzer.
- Nie den internen eMMC beschreiben, nichts formatieren oder löschen, keine Payloads injizieren.
- Auf dem Mac nichts systemweit installieren (kein brew install). Arbeite nur im Repo.
- Versionen bleiben unter 1.0; RCs nur vor einer Major-Version.
- Kein Force-Push auf `main`, keine Änderung an GitHub-Einstellungen.

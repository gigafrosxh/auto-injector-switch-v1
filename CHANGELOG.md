# Changelog

Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionen nach SemVer (unter 1.0).

## [Unreleased]

### Behoben
- `zramswap.service` schlägt beim Start nicht mehr fehl: Ist `/dev/zram0` schon vom L4T-BSP als Swap eingerichtet, wird der Dienst übersprungen (#77).

### Geändert
- Auf GitHub ist immer die höchste Version „Latest“, auch Patch-Releases. Nachträglich gebaute ältere Versionen übernehmen das nicht mehr (#79).

## [0.6.1] - 2026-11-23

### Behoben
- Joy-Cons funktionieren in gestarteten Apps wieder als Maus und Tastatur; in der Teria-Oberfläche bleiben sie aus. Moduswechsel und neu verbundene Controller werden zuverlässig abgeglichen (#76).
- Der SSH-Schutz greift beim Update sofort, nicht erst nach dem Neustart. Einrichtungsassistent und `teria-setup.txt` lehnen `teria` und den Benutzernamen als Passwort ab, damit SSH nicht überraschend aus bleibt (#76).

## [0.6.0] - 2026-11-23

### Neu
- WLAN mit Benutzername und Passwort (WPA2/WPA3-Enterprise, z. B. Schule, Firma, eduroam): Der WLAN-Dialog fragt bei solchen Netzen zusätzlich den Benutzernamen ab und verbindet per PEAP/MSCHAPv2. Das Netz verbindet sich danach automatisch (#74).

## [0.5.2] - 2026-11-22

### Behoben
- Das Schnellmenü zeigt den eMMC-Schutz nur noch als aktiv, wenn er es wirklich ist. Beim Ausschalten und Neustarten ist „Abbrechen“ vorgewählt. App-Dateinamen mit Sonderzeichen werden ignoriert, damit sie keinen Code in der Oberfläche ausführen können (#67).

## [0.5.1] - 2026-11-22

### Behoben
- Der Teria-Ladebildschirm von Hekate steht nicht mehr auf dem Kopf (#64).

## [0.5.0] - 2026-11-22

### Neu
- Neues Design „Glas“: Liquid Glass trifft PS5. Statusleiste, Bereichsauswahl, Systemkacheln, Karten, Schnellmenü und Tastenhinweise sind Glasflächen, Auswahl und Hauptknopf im PS5-Stil. Der Glas-Effekt nutzt vorberechnete Weichzeichner und bleibt ohne GPU schnell (75 ms pro Schritt auf der Switch) (#59).

## [0.4.6] - 2026-11-22

### Sicherheit
- SSH startet erst, wenn kein Konto mehr ein Standardpasswort wie `teria` hat. Vorher war die Switch mit dem bekannten Passwort und sudo-Rechten über WLAN und USB erreichbar (#65).

## [0.4.5] - 2026-11-22

### Behoben
- In der Teria-Oberfläche sind Joy-Cons und Pro Controller nicht mehr zusätzlich Maus und Tastatur. Es erscheint kein Zeiger mehr, Tasten lösen nicht mehr doppelt aus, und es öffnen sich keine Apps mehr durch versehentliche Klicks. Im Desktop-Modus bleibt die Maus-Belegung aktiv (#61).

## [0.4.4] - 2026-11-22

### Behoben
- Die Oberfläche reagiert etwa siebenmal schneller: Ohne GPU-Beschleunigung zeichnet WebKit weiche Schatten, Weichzeichner und Größen-Animationen bei jedem Schritt neu. Diese Effekte sind entfernt, ein Schritt in der Kachelreihe braucht auf der Switch 63 statt 449 ms (#57).

## [0.4.3] - 2026-11-21

### Behoben
- In der Konsolenansicht ist kein Mauszeiger mehr zu sehen, nur noch im Desktop-Modus. Touch und Controller funktionieren weiter (#53).

## [0.4.2] - 2026-11-21

### Behoben
- Apps aus der Konsolenansicht öffnen sich maximiert im Vordergrund statt unsichtbar hinter der Teria-Oberfläche. Die Home-Taste holt Teria zurück; solange eine App vorn ist, steuert der Controller nicht mehr die verdeckte Oberfläche (#52).

## [0.4.1] - 2026-11-21

### Behoben
- Wer aus dem Desktop-Modus per Home-Taste, Fensterliste oder Alt+Tab zur Teria-Oberfläche zurückkehrt, beendet den Desktop-Modus. Leiste und Dock verdecken die Oberfläche nicht mehr (#49).

## [0.4.0] - 2026-11-21

### Neu
- Beim ersten Start eines neuen Images richtet ein Vollbild-Assistent Sprache, Zeitzone, WLAN und das persönliche Konto ein. Touch, Joy-Cons und Bildschirmtastatur werden unterstützt (#27).

## [0.3.7] - 2026-11-21

### Behoben
- Die APT-Einstellungen lassen nur L4T 32.3.x zu, auch wenn das L4T-Repo neuere Versionen oder BSP-Metapakete wie `nvidia-bsp-32-7` anbietet. Ein Akzeptanztest mit synthetischen Paketlisten prüft das in der CI (#45).

## [0.3.6] - 2026-11-21

### Dokumentiert
- Paketstände, Xorg-ABI und APT-Pins für L4T unter Debian trixie sind mit dem Release-Manifest abgeglichen (#29).

## [0.3.5] - 2026-11-21

### Behoben
- Das Image enthält die Netzwerkwerkzeuge, die der L4T-Dienst für die USB-Brücke und die Adressvergabe an den angeschlossenen Rechner aufruft (#33).

## [0.3.4] - 2026-11-21

### Behoben
- Der Desktop-Modus installiert die Energieanzeige für die Xfce-Leiste. Damit kann das Panel `power-manager-plugin` beim Start laden (#42).

## [0.3.3] - 2026-11-21

### Behoben
- Terminal und andere Apps lassen sich aus der Teria-Bibliothek öffnen. Fehlgeschlagene Startversuche erscheinen nicht im Verlauf (#40).

## [0.3.2] - 2026-11-21

### Behoben
- Ein über die SD eingerichtetes WPA-Profil behält seinen Schlüssel beim nächsten Start (#35).
- WLAN-Status und Netzwerksuche lesen Doppelpunkte und Rückstriche in Netzwerknamen korrekt (#36).
- In Mesh-Netzen zeigt die Netzwerkliste den verbundenen Zugangspunkt und dessen Signalstärke (#37).
- Netze mit Apostrophen und Rückstrichen lassen sich aus dem WLAN-Dialog auswählen und verbinden (#38).
- Aus #33 sind außerdem die Filter für Xfce-Dialoge und den App-Verlauf, die Ladeleistungsanzeige, die Rechte für die Helligkeitssteuerung und den Store sowie die Umstellung von zram auf lz4 enthalten.

## [0.3.1] - 2026-11-21

### Behoben
- Teria blieb beim Start mit Debian-systemd 257 auf dem Switch-Kernel 4.9 hängen: `SYSTEMD_CGROUP_ENABLE_LEGACY_FORCE=1` im Booteintrag (#31)
- Ohne Tastatur war keine Anmeldung möglich (#32): automatische Anmeldung, Bildschirmtastatur im Anmeldebildschirm, kein erzwungener Passwortwechsel mehr
- Grafische Oberfläche startete nicht: LightDM wartet nicht mehr auf die Grafik-Meldung von logind, der Bildschirm (fbdev) gilt als Grafikgerät von seat0

### Neu
- `teria-setup.txt` auf der SD: WLAN, Passwort und automatische Anmeldung am PC/Mac eintragen; Passwörter werden nach der Übernahme gelöscht
- Bootprotokolle unter `teria-logs/` auf der SD (letzte 5 Starts)
- USB-Gerätemodus (Netzwerk über USB-C zum PC/Mac) ist eingeschaltet

## [0.3.0] - 2026-11-21

### Neu
- Teria-Oberfläche `teria-shell` nach den Mockups (#30): Startbildschirm mit Kachelreihe und Vorschau, Schnellmenü, Bibliothek, Store mit geprüften Debian-Paketen, App-Seite mit Installation, Einstellungen (Netzwerk, Bluetooth, Anzeige & Ton, Energie & Leistung, Sicherheit, Über Teria)
- Bedienung mit Joy-Cons und Pro Controller über evdev, Tastatur und Touch (#28)
- Desktop-Modus mit Leiste oben und Dock links, Arc-Dark, Papirus-Icons, Ubuntu-Schrift, Anmeldung im Teria-Design (#26)
- `teria perf eco|ausgewogen|max`: Leistungsprofile über CPU- und GPU-Taktgrenzen
- Neustart in Hekate und Paketinstallation über polkit-Helfer, Store installiert nur Pakete aus dem Katalog

### Geändert
- Teria startet standardmäßig in die Teria-Sitzung; die Xfce-Sitzung bleibt bei der Anmeldung wählbar
- Der Einrichtungsassistent (#27) ist nach 0.4.0 verschoben

## [0.2.0] - 2026-11-21

### Neu
- Teria ist ein eigenständiges System: rootfs aus Debian trixie arm64 statt Ubuntu (#17)
- Switchroot-Kernel 4.9.140-l4t, Module, Firmware und L4T 32.3.1 aus dem L4T-Repo im Image (#21)
- Eigener Bootstack `switchroot/teria/`, Booteintrag mit Label `SWR-TER` (#22)
- SD-Paket für Hekate „Flash Linux“ (`switchroot/install/l4t.NN`, SHA256SUMS) (#18)
- Erststart-Dienst: Partition vergrößern, SSH-Schlüssel, Maschinen-ID (#23)
- Teststart vom USB-Stick ohne Ubuntu zu überschreiben (`teria-usb.ini`) (#25)
- Anleitung `docs/INSTALLATION.md` (#24)
- Mockups in `docs/mockups/`

### Geändert
- os-release: auf Debian `ID=teria`, `ID_LIKE=debian`; auf Ubuntu bleibt `ID=ubuntu`

## [0.1.0] - 2026-11-21

### Neu
- Paket `teria-base` mit os-release-Branding (#2)
- Werkzeug `teria`: info, akku, temp, guard, reboot (r2p), wachbleiben (#3)
- eMMC-Schreibschutz beim Booten und per udev (#4)
- Hekate-Eintrag „Teria“ mit Icon und Bootlogo (#5)
- `tools/deploy.sh` mit Rückfragen (#6)
- CI mit shellcheck, Paketbau, Installationstest und Release-Assets (#7)
- Analyse der Switch in `docs/SWITCH-ANALYSE.md` (#8)

### Geändert
- Auto-Injector nach `injector/windows/` verschoben (#1)

# Changelog

Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionen nach SemVer (unter 1.0).

## [Unreleased]

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

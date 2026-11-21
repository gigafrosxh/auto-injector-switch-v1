# Changelog

Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionen nach SemVer (unter 1.0).

## [Unreleased]

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

# Teria statt Ubuntu installieren

Teria ab 0.2.0 ist ein eigenständiges System (Debian trixie arm64 + Switchroot-Kernel 4.9.140-l4t und L4T 32.3.1).
Es ersetzt Switchroot Ubuntu auf der Linux-Partition der SD-Karte. Der interne eMMC wird dabei nie angefasst.

> **Achtung:** „Flash Linux“ überschreibt die komplette Linux-Partition (bei dir `SWR-NOB`, 64 GB).
> Alles, was in Ubuntu gespeichert ist, ist danach weg. Erst sichern.

## Weg A: ohne Risiko testen (USB-Stick am Dock)

Ubuntu bleibt unverändert.

1. `teria-<version>-sd.zip` am PC/Mac entpacken.
2. Die Teile zu einem Image zusammensetzen:
   - macOS/Linux: `cat switchroot/install/l4t.* > teria.img`
   - Windows: `copy /b switchroot\install\l4t.00 + switchroot\install\l4t.01 teria.img` (alle Teile in Reihenfolge)
3. `teria.img` mit balenaEtcher auf einen USB-Stick (mind. 8 GB) schreiben. **Den richtigen Stick wählen.**
4. Auf die FAT32-Partition der SD-Karte kopieren (Ubuntu-Dateien bleiben):
   - `switchroot/teria/` (Bootdateien)
   - `extras/bootloader/ini/teria-usb.ini` nach `bootloader/ini/`
5. Switch ins Dock, USB-Stick ans Dock, in Hekate **More configs → Teria (USB-Test)** starten.

## Weg B: Teria statt Ubuntu (überschreibt Ubuntu)

1. **Sichern** (in Ubuntu, oder per SSH vom PC):
   ```bash
   tar czf /media/daniel/SWITCH\ SD/ubuntu-home-backup.tgz -C /home daniel   # oder auf einen USB-Stick
   ```
   Die FAT32-Partition hat genug Platz (55 GB), Dateien über 4 GB gehen dort aber nicht; dann auf einen Stick oder den PC sichern.
2. Switch ausschalten, SD-Karte in den PC (oder Hekate → Tools → USB Tools → SD Card als UMS).
3. `teria-<version>-sd.zip` **auf die FAT32-Partition** entpacken. Neu dazu kommen:
   `bootloader/ini/teria.ini`, `switchroot/teria/`, `switchroot/install/l4t.00…`, `SHA256SUMS`.
4. SD zurück, Hekate starten: **Nyx → Tools → Partition SD → Flash Linux**. Hekate schreibt `l4t.*` auf die Linux-Partition.
   Danach kann `switchroot/install/` gelöscht werden.
5. In Hekate **More configs → Teria** starten.
6. Teria meldet `teria` automatisch an. WLAN und eigenes Passwort trägst du vorher in `teria-setup.txt` ein (siehe unten).
   Beim ersten Start wird die Partition automatisch auf die volle Größe gebracht.

Den alten Eintrag `L4T-noble.ini` kann man danach löschen, er bootet ja ins überschriebene System nicht mehr sinnvoll.

## Einrichtung ohne Tastatur: teria-setup.txt

Auf der FAT32-Partition der SD liegt `teria-setup.txt`. Am PC/Mac ausfüllen, bevor Teria startet:

```
wlan_name=MeinWLAN
wlan_passwort=geheim
passwort=mein-neues-passwort
automatische_anmeldung=ja
```

Teria leert WLAN-Name und WLAN-Passwort auf der SD, sobald das WLAN-Profil gespeichert ist.
Das Benutzerpasswort entfernt Teria nach erfolgreicher Übernahme ebenfalls aus der Datei.
Wenn Teria 0.3.1 die WLAN-Verbindung nach einem Neustart verloren hat, trage WLAN-Name und
WLAN-Passwort einmal neu ein. Für ein neues offenes Netz genügt der WLAN-Name.

## Bootprotokolle

90 Sekunden nach jedem Start legt Teria Protokolle unter `teria-logs/` auf der FAT32-Partition ab
(Journal, Xorg, LightDM, Netzwerk). Die letzten fünf Starts bleiben erhalten. Lesen: Hekate → Tools →
USB Tools → SD Card an den PC/Mac.

## Zurück zu Ubuntu

Das Switchroot-Ubuntu-Image (`switchroot-ubuntu-noble-*.7z`) erneut auf die SD entpacken und wieder **Flash Linux**.
Danach das gesicherte Home zurückspielen.

## Was Teria vom Switchroot-Projekt übernimmt

Nur die gerätespezifischen Teile aus dem L4T-Repo: `switch-bsp` (Kernel, Module, Firmware, Bootstack),
`nvidia-l4t-*` 32.3.1 (GPU-Treiber), das dazu passende Xorg 1.20 und `libx11`, `joycond` und die Switch-Regeln
für Touch, Audio, Dock und Joystick-Maus. Alles andere kommt aus Debian.

# boot/

Hekate-Booteintrag fuer Teria. Teria 0.1 nutzt Kernel, Device Tree und initramfs
von Switchroot Ubuntu Noble (`/switchroot/ubuntu-noble/`) und bringt nur einen
eigenen Menue-Eintrag mit Icon und Bootlogo mit.

| Datei im Repo | Ziel auf der SD-Karte (FAT32-Partition) |
|---|---|
| `teria/teria.ini` | `bootloader/ini/teria.ini` |
| `teria/icon_teria.bmp` | `switchroot/teria/icon_teria.bmp` |
| `teria/bootlogo_teria.bmp` | `switchroot/teria/bootlogo_teria.bmp` |

Der bestehende Eintrag `L4T-noble.ini` bleibt unangetastet; beide starten dasselbe System.
Installieren: `tools/deploy.sh --boot` (fragt vorher nach) oder Dateien von Hand kopieren.

Bilder neu erzeugen: `python3 tools/make-bootart.py boot/teria` (braucht Pillow).
Das Bootlogo ist 720x1280 und um 90 Grad gedreht, weil das Display der Switch hochkant verbaut ist.

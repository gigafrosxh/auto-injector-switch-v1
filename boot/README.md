# boot/

Hekate-Einträge und Bilder für Teria.

| Datei im Repo | Ziel auf der SD-Karte (FAT32-Partition) |
|---|---|
| `teria/teria.ini` | `bootloader/ini/teria.ini` |
| `teria/teria-usb.ini` | `bootloader/ini/teria-usb.ini` (nur für den Teststart vom USB-Stick) |
| `teria/icon_teria.bmp`, `teria/bootlogo_teria.bmp` | `switchroot/teria/` |

Kernel, initramfs, Device Trees, ATF und U-Boot (`bl31.bin`, `bl33.bin`, `boot.scr`, `uImage`, `initramfs`,
`nx-plat.dtimg`) kommen beim Image-Bau aus dem Paket `switch-bsp` und landen im SD-Paket unter `switchroot/teria/`.
Die Linux-Partition heißt `SWR-TER`; Switchroot Ubuntu (`SWR-NOB`) wird nicht angesprochen.

Bilder neu erzeugen: `python3 tools/make-bootart.py boot/teria` (braucht Pillow).
Das Bootlogo ist 720x1280 und um 90 Grad gedreht, weil das Display der Switch hochkant verbaut ist.

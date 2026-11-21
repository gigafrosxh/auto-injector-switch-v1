# Architektur

```
 PC / Mac                              Nintendo Switch V1
 ─────────────                         ───────────────────────────────────────────
 injector/  ── RCM (USB 0955:7321) ──▶ Hekate (RAM)
 (Payload nur mit SHA256 + Freigabe)        │  bootloader/ini/teria.ini  → /switchroot/teria/
                                            ▼
                                      bl31 (ATF) → bl33 (U-Boot) → boot.scr
                                            ▼
                                      Switchroot-Kernel 4.9.140-l4t + initramfs + nx-plat.dtimg
                                            ▼  sucht Partition mit Label SWR-TER
                                      Teria rootfs (SD, ext4 SWR-TER)
                                       ├─ Debian trixie arm64            Basis, Xfce, NetworkManager, SSH
                                       ├─ L4T-Repo (nur Geräteteile)     switch-bsp, nvidia-l4t-* 32.3.1,
                                       │                                 Xorg 1.20 + libx11 (L4T), joycond
                                       ├─ teria-base                     teria, eMMC-Schutz, Erststart, os-release,
                                       │                                 Root-Helfer (perf, reboot-hekate, pkg) mit polkit
                                       └─ teria-shell                    Konsolen-Oberfläche: Python-Dienst auf 127.0.0.1
                                                                         + WebKitGTK-Vollbild, Joy-Cons über evdev,
                                                                         Desktop-Modus (xfwm4, xfce4-panel als Dock)
```

Build: `tools/build-image.sh` (mmdebstrap, nativ auf arm64 in der CI) → ext4-Image `SWR-TER` →
`switchroot/install/l4t.NN` (Hekate „Flash Linux“) + Bootstack aus `switch-bsp` + Teria-Logos → `teria-<v>-sd.zip`.

Das Paket `teria-base` läuft auch weiterhin als Schicht in Switchroot Ubuntu (dort bleibt `ID=ubuntu`).

| Pfad | Inhalt |
|---|---|
| `os/teria-base/` | Paketbaum, wird von `tools/build-deb.sh` gebaut |
| `os/teria-shell/` | Oberfläche (Dienst `server.py`, `www/`, Sitzung, Desktop-Design) |
| `boot/teria/` | Hekate-Eintrag, Icon, Bootlogo |
| `injector/windows/` | Auto-Injector für Windows (PowerShell + TegraRcmSmash) |
| `tools/` | Bau- und Installationsskripte |
| `os/image/` | Paketlisten, apt-Pins, L4T-Schlüssel, Dateien für das rootfs |
| `docs/` | Installation, Analyse, Architektur, Sicherheit |
| `release-notes/` | Texte für GitHub-Releases |

Versionen: SemVer unter 1.0 (`0.MINOR.PATCH`). Release-Candidates gibt es nur vor einer
Major-Version (`v1.0.0-rc.1`, …), nie vor Minor/Patch. Release-Titel: „Teria v0.2.1“. Die CI baut bei jedem Tag `v*` die Assets und
hängt sie ans Release; Tags mit `-` werden als Vorabversion markiert.

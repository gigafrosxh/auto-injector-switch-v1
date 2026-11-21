# Architektur

```
 PC / Mac                              Nintendo Switch V1
 ─────────────                         ───────────────────────────────────────────
 injector/  ── RCM (USB 0955:7321) ──▶ Hekate 6.5.5 (RAM)
 (Payload nur mit SHA256 + Freigabe)        │  bootloader/ini/teria.ini   (Teria-Eintrag)
                                            │  bootloader/ini/L4T-noble.ini (Original, unverändert)
                                            ▼
                                      Switchroot-Kernel 4.9.140-l4t, L4T R32.3.1
                                            ▼
                                      Ubuntu Noble 24.04 rootfs (SD, ext4 SWR-NOB)
                                       └─ teria-base (.deb)
                                           ├─ /usr/bin/teria             Werkzeug
                                           ├─ teria-emmc-guard.service   eMMC schreibgeschützt
                                           ├─ udev-Regel                 eMMC sofort sperren + ausblenden
                                           ├─ os-release (dpkg-divert)   „Teria 0.x“
                                           └─ motd                       Begrüßung
```

| Pfad | Inhalt |
|---|---|
| `os/teria-base/` | Paketbaum, wird von `tools/build-deb.sh` gebaut |
| `boot/teria/` | Hekate-Eintrag, Icon, Bootlogo |
| `injector/windows/` | Auto-Injector für Windows (PowerShell + TegraRcmSmash) |
| `tools/` | Bau- und Installationsskripte |
| `docs/` | Analyse, Architektur, Sicherheit |
| `release-notes/` | Texte für GitHub-Releases |

Versionen: SemVer unter 1.0 (`0.MINOR.PATCH`). Vor jeder neuen Minor-Version gibt es Vorabversionen
(`v0.2.0-rc.1`, …). Release-Titel: „Teria v0.2.1“. Die CI baut bei jedem Tag `v*` die Assets und
hängt sie ans Release; Tags mit `-` werden als Vorabversion markiert.

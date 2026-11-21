# Analyse der Switch (Stand 21.11.2026)

Per SSH ausgelesen, nur lesend. Gerät: Nintendo Switch V1 (2017, „icosa“, Tegra X1 / T210), ungepatcht.

## System

| | |
|---|---|
| Distribution | Switchroot L4T Ubuntu Noble 24.04.4 LTS |
| Kernel | `4.9.140-l4t` (#139 SMP PREEMPT, 4. Mai 2026), aarch64 |
| L4T / BSP | NVIDIA L4T R32.3.1 (`nvidia-l4t-*` 32.3.1), `switch-bsp` 5.1.2-32+24.04, `nvidia-bsp-32-3` |
| Paketquellen | ports.ubuntu.com (noble, -updates, -backports, -security) + `theofficialgman.github.io/l4t-debs` (l4t noble, Prio 511) |
| Desktop | Unity (lightdm, X11), Bildschirmtastatur `onboard` |
| RAM / Swap | 3,9 GiB, 3 GiB zram |
| Hostname | `daniel-switch` |

Switch-spezifische Pakete: `switch-bsp`, `switch-l4t-configs`, `switch-dock-handler` (`dock-hotplug`),
`switch-joystick-mouse`, `switch-touch-rules`, `switch-alsa-ucm2`, `switch-multimedia`, `switch-unity`,
`switch-dconf-customizations`, `switch-flatpak`, `joycond`, `nintendo-switch-meta`.

## Speicher und Boot

| Gerät | Typ (sysfs) | Inhalt |
|---|---|---|
| `mmcblk0` (119 GB) | **SD** | SD-Karte, `sdhci-tegra.0` |
| `mmcblk0p1` (55 GB, FAT32, „SWITCH SD“) | | Hekate, Bootdateien |
| `mmcblk0p2` (64 GB, ext4, „SWR-NOB“) | | Linux-rootfs `/` |
| interner eMMC | – | **nicht sichtbar**, Switchroot blendet ihn aus |

Wichtig: Unter Switchroot ist `mmcblk0` die **SD-Karte**. Teria erkennt den eMMC deshalb nie über den Namen,
sondern über `/sys/block/*/device/type` (`MMC` = eMMC, `SD` = SD-Karte).

SD-Karte, FAT32-Partition:

```
hekate_ctcaer_6.5.5.bin
bootloader/hekate_ipl.ini        autoboot=0, bootwait=3, updater2p=0
bootloader/nyx.ini               umsemmcrw=0 (eMMC-UMS nur lesend)
bootloader/ini/L4T-noble.ini     l4t=1, boot_prefixes=/switchroot/ubuntu-noble/, id=SWR-NOB, r2p_action=self
switchroot/ubuntu-noble/         bl31.bin, bl33.bin (ATF/U-Boot), boot.scr, uImage, initramfs,
                                 nx-plat.dtimg (Device Trees), bootlogo_ubuntu.bmp (720x1280, 32 bit),
                                 icon_ubuntu_hue.bmp (192x192, 32 bit), README_CONFIG.txt
```

Kein Atmosphère, kein emuMMC auf der Karte.

Kernel-Kommandozeile (Auszug): `root=/dev/mmcblk0p2 rootlabel=SWR-NOB access=m2 swr_dir=/switchroot/ubuntu-noble/
pmc_r2p.enabled=1 pmc_r2p.action=self consoleblank=0 nvdec_enabled=0 systemd.unified_cgroup_hierarchy=0`.

Bootkette: RCM → Hekate 6.5.5 (per Auto-Injector) → `L4T-noble.ini` → ATF (`bl31`) → U-Boot (`bl33`) → `boot.scr`
→ `uImage` + `initramfs` + DT aus `nx-plat.dtimg` → systemd.

## Device Tree

`model = "Nintendo Switch (2017)"`, `compatible = "nvidia,odin", "nintendo,icosa", "nintendo,nx", "nvidia,tegra210"`.
Knoten u. a. für `dfll-max77621` (CPU-Spannung), `extcon` (Dock/USB), `gpio-keys`, `backlight`, `bluedroid_pm`, `gpu`.

## Treiber und Hardware

- Module: `nvgpu`, `brcmfmac` (WLAN), `hci_uart`/`btbcm` (Bluetooth), `joycon_serdev` (Joy-Cons an der Schiene).
- `/sys/devices/r2p` (Treiber `tegra-r2p`): Reboot 2 Payload, aktuell `action=self`, `param1=1`, `param2=1`.
- Akku `battery` (Li-Ion, 139 Zyklen, 99 % Nennkapazität), Ladegrenze 85 % (`usb/charge_control_limit`),
  Joy-Con-Akkus als `nintendo_switch_controller_battery_serial0-0/1-0`.
- 12 Thermalzonen (CPU, GPU, PLL, Board, PMIC, Ladechip, Akku, Lüfterschätzung).
- `nvpmodel` im Modus „Console“, `jetson_clocks` vorhanden. nvpmodel meldet Rechtefehler bei
  `/sys/kernel/tegra_cpufreq/overclock` und `pwm-fan/fan_profile` (Thema für #13).
- CPU-Governors: interactive, conservative, ondemand, userspace, powersave, performance, schedutil.

## Auffälligkeiten

- `joycon_serdev: Failed sending uart packet; ret=-110` mehrfach im dmesg (Joy-Cons an der Schiene, harmlos solange sie funktionieren).
- `brcmfmac: chanspec failed (-5)` (bekannt bei L4T 32.3, ohne Auswirkung).
- Standby nach 10 min Inaktivität im Akkubetrieb (`sleep-inactive-battery-timeout=600`): unterbricht SSH-Sitzungen.
  Teria bringt dafür `teria wachbleiben`.

## Folgerungen für Teria

1. Teria 0.x setzt **auf** Switchroot auf, statt Kernel und BSP selbst zu bauen: Kernel 4.9 + L4T 32.3.1 sind
   eng an Switchroot-Patches gebunden, ein eigener Kernel bringt erst einmal nur Risiko.
2. Auslieferung als Debian-Paket (`teria-base`), das sich sauber entfernen lässt.
3. Eigener Hekate-Eintrag statt Änderung an `L4T-noble.ini`: der Original-Eintrag bleibt als Rückweg.
4. eMMC-Schutz über Kartentyp, nicht Gerätename.
5. Reboot 2 Payload ist verfügbar und ersetzt RCM für Neustarts; `ums`-Modi mit eMMC werden nie angeboten.

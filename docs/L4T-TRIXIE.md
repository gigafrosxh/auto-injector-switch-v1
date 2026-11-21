# L4T 32.3.1 unter Debian trixie

Teria v0.3.4 verbindet Debian 13 arm64 mit dem Switchroot-Kernel 4.9.140-l4t. Das veröffentlichte Image ließ sich in der arm64-CI bauen und als ext4-Datei prüfen. Für v0.3.1 belegt der Gerätetest den Start der grafischen Sitzung und die Bedienung der Bibliothek. Aussagen über die Paketinstallation beziehen sich auf v0.3.4. [Release-Manifest](https://github.com/gigafrosxh/auto-injector-switch-v1/releases/download/v0.3.4/teria-0.3.4.manifest) · [Image-Prüfung](https://github.com/gigafrosxh/auto-injector-switch-v1/actions/runs/44928704009) · [Gerätebericht #33](https://github.com/gigafrosxh/auto-injector-switch-v1/issues/33)

| Bestandteil | Im Image installiert | Bedeutung für trixie |
|---|---|---|
| Kernel, Firmware, Grafiktreiber | `switch-bsp` 5.1.2-34+24.04, `nvidia-l4t-*` 32.3.1-20191209225816 | Die NVIDIA-Pakete hängen teilweise von exakt derselben Buildversion ab. Kernelmodule, Firmware und Userspace als Satz behandeln. |
| Xorg und Eingabe | Server 2:1.20.13-1ubuntu1~20.04.8, Eingabetreiber libinput 1.2.1-1 | Dieser Server stellt Video- und Eingabe-ABI 24 bereit. Der reguläre trixie-Server 21.1 verwendet Video-ABI 25. Das getrennte Datenpaket `xserver-common` 21.1.16 kommt aus Debian und erfüllt die Mindestversion des L4T-Servers. |
| X11-Clientbibliothek | `libx11-6`, `libx11-data`, `libx11-xcb1` jeweils 2:1.8.7-1-l4t | Dies ist die getestete Kombination mit den L4T-Patches. Für einen Wechsel allein der X11-Clientbibliothek auf die trixie-Version fehlt ein Gerätetest. |
| OpenGL/EGL | Debian GLVND 1.7.0-1+b2 und L4T 3D-Core, X11 und Wayland 32.3.1 | Der Debian-Dispatcher und die NVIDIA-Bibliotheken lassen sich gemeinsam installieren. Die Shell deaktiviert WebKit-Hardwarebeschleunigung. Der sichtbare Startbildschirm belegt daher keine EGL-Beschleunigung. |
| Multimedia | Debian GStreamer 1.26.2, Plugins base/good, NVIDIA-Multimedia 32.3.1, `libpcre3` 2:8.39-15 | Die GStreamer-Basisbibliotheken erfüllen die Paketabhängigkeiten. NVIDIA-Multimedia braucht zusätzlich die alte PCRE-Bibliothek aus bookworm. Ein Hardware-Decodertest bleibt offen. |
| Controller und Dock | `joycond` 0.6-1, `switch-dock-handler` 3.0-2 | Beide Pakete sind im Manifest enthalten. Für Dock-Hotplug und den vollständigen Eingabepfad enthält der CI-Lauf keinen Gerätetest. |

## Quellen und Pins

Der Image-Build bindet die signierte L4T-Suite ausschließlich mit der Komponente `noble` ein. Der fremde Paketbestand hat grundsätzlich Priorität 100. Für BSP, ausgewählte Gerätetreiber, den Xorg-Server und die zusammengehörigen X11-Pakete gilt 1001. Damit kann APT auch ein bereits installiertes, neueres Debian-libX11 durch die L4T-Fassung ersetzen. Der Build erlaubt diesen Downgrade ausdrücklich. Die Debian-Varianten der in den Preferences gesperrten Grafikpakete haben Priorität −1. [Buildskript](../tools/build-image.sh) · [Paketlisten und Pins](../os/image/apt/teria-l4t.pref) · [L4T-Paketindex](https://theofficialgman.github.io/l4t-debs/dists/l4t/noble/binary-arm64/Packages) · [Debian-Xorg](https://packages.debian.org/trixie/xserver-xorg-core)

Bookworm ist grundsätzlich mit −1 gesperrt. Für `libpcre3` gilt die Ausnahme 500. GLVND und GStreamer kommen aus trixie. Seit v0.3.7 steht die Versionsgrenze für `nvidia-l4t-*` vor allen anderen Regeln: nur 32.3.x hat 1001, jede andere Version und die BSP-Metapakete ab `nvidia-bsp-32-4` haben −1. `tests/check_apt_pin.sh` prüft das in der CI mit nachgebauten Paketlisten. [Issue #45](https://github.com/gigafrosxh/auto-injector-switch-v1/issues/45) · [APT-Prioritäten](https://manpages.debian.org/trixie/apt/apt_preferences.5.en.html)

Für die Freigabe eines neuen Treibersatzes sind ein grafischer Login, eine EGL-Anwendung mit angezeigtem Renderer und Videowiedergabe mit nachgewiesenem NVIDIA-Decoder getrennt zu prüfen. Beim USB-Gerätemodus kommt ein Test der Adressvergabe am angeschlossenen Rechner hinzu. Die Bibliotheksansicht allein deckt diese Pfade nicht ab.

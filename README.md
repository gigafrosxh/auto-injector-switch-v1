# auto-injector-switch-v1

Windows-Hintergrundtool fuer eine **ungepatchte Nintendo Switch V1** (Tegra X1, RCM):
Sobald die Switch im RCM-Modus per USB angeschlossen wird, injiziert es automatisch
**Hekate**, und zwar nur, wenn der SHA256 der Payload-Datei stimmt.
Kein manuelles Klicken in TegraRcmGUI mehr bei jedem Kaltstart.

*English summary: a small PowerShell watcher that detects a Switch V1 in RCM
(USB `0955:7321`) and auto-injects a SHA256-pinned Hekate payload via TegraRcmSmash.
Nothing is written to the console's NAND/BOOT0. Injection is disabled until you run `-Approve`.*

## Eigenschaften

- Erkennt die Switch im RCM (USB `0955:7321`) alle 2 Sekunden.
- Prueft **vor jeder Injektion** den SHA256 des Payloads gegen den konfigurierten Hash
  und injiziert genau die geprueften Bytes. Bei Abweichung: keine Injektion.
- **Ohne Freigabe keine Injektion.** Die Freigabe (`-Approve`) ist an den Hash gebunden.
- Ein Versuch pro Einstecken (max. 3 Wiederholungen bei Fehler), danach erst wieder nach
  dem Abziehen.
- Schreibt nichts auf die Switch: kein NAND, kein BOOT0, kein AutoRCM. Das Payload landet nur im RAM.
- Laeuft unsichtbar als Windows-Aufgabe bei der Anmeldung, ohne Adminrechte.
- Log in `autoinject.log`.

## Voraussetzungen

1. **Windows 10/11** mit Windows PowerShell 5.1 (vorinstalliert).
2. **TegraRcmGUI** von https://github.com/eliboa/TegraRcmGUI/releases installieren und
   darueber den **libusbK-Treiber (APX)** einrichten. Das Tool nutzt das mitgelieferte
   `TegraRcmSmash.exe`. TegraRcmGUI selbst danach schliessen, sonst blockiert es das Geraet.
3. **Hekate** von https://github.com/CTCaer/hekate/releases laden und
   `hekate_ctcaer_X.Y.Z.bin` in den Ordner `payload/` legen.
   Hekate und TegraRcmSmash sind bewusst **nicht** im Repo enthalten.

Der voreingestellte Hash gehoert zu `hekate_ctcaer_6.5.5.bin`:

```
09752ABD207803708ADD6E22151E94B71FFBAAFF769D1BAD759584B76EF6F05E
```

Pruefe ihn selbst: `Get-FileHash payload\hekate_ctcaer_6.5.5.bin`.

## Installation

```powershell
# 1. Release-ZIP entpacken, z. B. nach C:\Tools\auto-injector-switch-v1
# 2. Hekate-Payload nach payload\ kopieren
# 3. Optional: config.example.json nach config.json kopieren und anpassen
# 4. Test ohne Injektion (Switch im RCM anschliessen, Strg+C zum Beenden):
powershell -ExecutionPolicy Bypass -File .\SwitchAutoInject.ps1 -DryRun
# 5. Freigabe erteilen:
powershell -ExecutionPolicy Bypass -File .\SwitchAutoInject.ps1 -Approve
# 6. Autostart einrichten:
powershell -ExecutionPolicy Bypass -File .\install-autostart.ps1
```

Falls Windows die Skripte als "aus dem Internet" blockiert: `Get-ChildItem -Recurse | Unblock-File`.

## Konfiguration (`config.json`)

| Schluessel | Standard | Bedeutung |
|---|---|---|
| `PayloadPath` | `payload\hekate_ctcaer_6.5.5.bin` | Payload-Datei, relativ zum Skriptordner oder absolut |
| `PayloadSha256` | Hash von Hekate 6.5.5 | Erwarteter SHA256. Nach einem Hekate-Update anpassen und neu `-Approve` ausfuehren |
| `SmashExe` | `C:\Program Files (x86)\TegraRcmGUI\TegraRcmSmash.exe` | Pfad zu TegraRcmSmash |
| `PollSeconds` | `2` | Abfrageintervall |
| `MaxTries` | `3` | Versuche pro Einstecken |

Alle Werte lassen sich auch per Parameter setzen, z. B. `-PayloadPath D:\hekate.bin -PayloadSha256 ...`.

## Befehle

| Befehl | Wirkung |
|---|---|
| `SwitchAutoInject.ps1` | Dauerbetrieb (so laeuft der Autostart) |
| `SwitchAutoInject.ps1 -DryRun` | Nur erkennen und Hash pruefen |
| `SwitchAutoInject.ps1 -Once` | Eine Injektion, dann beenden |
| `SwitchAutoInject.ps1 -Approve` | Freigabe erteilen |
| `SwitchAutoInject.ps1 -Revoke` | Freigabe zuruecknehmen |
| `install-autostart.ps1` | Aufgabe "SwitchAutoInject" anlegen und starten |
| `uninstall-autostart.ps1` | Aufgabe entfernen |

## Grenzen: Kaltstart braucht weiterhin RCM

Eine ausgeschaltete V1 startet immer Horizon, ausser sie wird ins RCM gebracht:
Jig in die rechte Joy-Con-Schiene, VOL+ halten, Power druecken. Danach reicht es, das
USB-Kabel einzustecken; den Rest erledigt dieses Tool.

**AutoRCM** wuerde den Jig ersparen, beschreibt aber BOOT0 im eMMC. Dieses Tool richtet
das absichtlich nicht ein.

## Neustarts ohne RCM (Switchroot Linux)

Switchroot-Linux unterstuetzt "Reboot 2 Payload": Ein normaler Neustart landet wieder in
Hekate, ganz ohne PC und Jig. Gesteuert ueber `r2p_action` in der Boot-Config
(`self` = wieder Linux, `bootloader` = Hekate-Menue, `normal` = Hekate-Autoboot) oder im
laufenden System:

```bash
echo bootloader | sudo tee /sys/devices/r2p/action   # naechster Neustart -> Hekate-Menue
sudo reboot
```

Bestimmten Eintrag aus `hekate_ipl.ini` starten (hier Eintrag 1):

```bash
echo self | sudo tee /sys/devices/r2p/action
echo 1    | sudo tee /sys/devices/r2p/param1
echo 0    | sudo tee /sys/devices/r2p/param2
sudo reboot
```

Vorsicht: `action=ums` mit `param1` 1 bis 3 gibt den **eMMC** per USB am PC frei. Nur
`param1=0` (SD-Karte) verwenden. Auch aus Hekate selbst geht "Reboot -> Hekate" ohne RCM.

## Haftung

Nutzung auf eigene Gefahr. Nur fuer eigene Geraete. Lizenz: MIT.

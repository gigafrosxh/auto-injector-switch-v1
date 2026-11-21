# Sicherheitsregeln

Diese Regeln gelten für jeden Code in diesem Repo und für jede Arbeit an der Switch.

1. **Nie auf den internen eMMC (NAND) schreiben.** Kein BOOT0/BOOT1, kein AutoRCM, keine eMMC-UMS.
   Teria setzt den eMMC beim Booten und per udev schreibgeschützt (`teria guard status`).
2. **Nie Laufwerke formatieren oder löschen.** Kein Skript in diesem Repo partitioniert oder formatiert.
3. **Keine unbekannten Payloads.** Der Injector schickt nur Dateien, deren SHA256 exakt dem gepinnten Hash
   entspricht, und erst nach ausdrücklicher Freigabe (`-Approve`).
4. **Vor jeder Payload-Injektion und vor jedem Schreiben auf die Switch wird gefragt.** `tools/deploy.sh`
   fragt einzeln für Paket und Booteintrag.
5. Reboot 2 Payload: nur `self` und `bootloader`. `ums` mit `param1` 1–3 (eMMC) wird nie verwendet.

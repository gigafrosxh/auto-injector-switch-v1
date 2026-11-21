# AGENTS.md – Arbeitsregeln für teria

Teria ist eine OS-Schicht (Paket `teria-base`) über Switchroot L4T Ubuntu Noble für eine unpatched Nintendo Switch V1. Vorbild für den Ablauf ist [folio](https://github.com/gigafrosxh/folio).

## Repo-Aufbau

- `os/teria-base/` – Debian-Paket (os-release, `teria`-Werkzeug, eMMC-Guard)
- `boot/` – Hekate-Eintrag, Icon, Bootlogo
- `injector/windows/` – Auto-Injector für Windows
- `tools/` – Build- und Deploy-Skripte
- `docs/` – Architektur, Sicherheit, Switch-Analyse
- `release-notes/<version>.md` – Release-Notizen, CI erstellt das Release beim Tag
- `CHANGELOG.md`, `VERSION`

## Vor jeder Aufgabe

- Offene GitHub-Issues prüfen und das passende Issue abarbeiten.
- Commit mit `Closes #N`.
- Issues auf Deutsch: `[Feature]`, `[Bug]`, `[Sicherheit]`, `[Doku]` …
- Jedes Issue hat ein Label P0–P3, dazu `sicherheit` und `bereich: *` wo passend.

## Versionierung und Releases

- Jedes Update ist ein Release. Zuerst Eintrag unter `[Unreleased]` im `CHANGELOG.md`.
- Minor (0.1, 0.2 …) pro neuem Feature, Patch pro Bugfix.
- Jeder `[Bug]` bekommt ein eigenes Patch-Release.
- Major nur auf Zuruf des Nutzers nach einem Feature-Set.
- *RCs nur vor einer Major-Version* (`1.0.0-rc.N`), nie vor Minor/Patch. Nach SemVer ist `x.0.0-rc.N` älter als `x.0.0`.
- Release-Titel: `Teria v0.2.1`.

## Prioritäten nach jedem Release

- P0 → `x.y.1`
- P1 → `x.y.2`
- P2 → `x.y.3`
- P3 → `x.y.4`
- Leere Stufen entfallen. Ein neues P0 kommt immer ins nächste Release.
- Ablauf: fixen → Release → testen → Issues anlegen → Prioritäten prüfen.

## Sicherheitsregeln (Switch und System)

- Niemals interne NAND/eMMC beschreiben.
- Nichts formatieren oder löschen, was der Nutzer nicht freigegeben hat.
- Keine unbekannten Payloads ausführen. Payload-Injektion nur nach Rückfrage.
- Nichts auf der Switch flashen oder installieren (`teria-base`, Boot-Eintrag, `deploy.sh`) ohne Rückfrage. Lesend inspizieren ist erlaubt.
- Auf dem Rechner des Nutzers nichts installieren, aktualisieren oder systemweit ändern (z. B. brew) ohne Zustimmung.
- Codex nur auf ausdrücklichen Wunsch.

## Qualität

- Shell-Skripte müssen `shellcheck` bestehen (CI).
- `tools/build-deb.sh` muss ein installierbares Paket bauen (CI-Installationstest).

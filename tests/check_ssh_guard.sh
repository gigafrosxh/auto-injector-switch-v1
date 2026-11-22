#!/bin/bash
# ssh-guard (#65): SSH nur ohne Standardpasswort. Laeuft als root in einem Debian-Container.
set -euo pipefail
G=/usr/lib/teria/ssh-guard
id teria >/dev/null 2>&1 || useradd -m -u 1000 teria
echo 'teria:teria' | chpasswd
if "$G"; then echo "FEHLER: Standardpasswort nicht erkannt"; exit 1; fi
echo 'teria:ein-eigenes-Passwort' | chpasswd
"$G" || { echo "FEHLER: eigenes Passwort blockiert SSH"; exit 1; }
useradd -m -u 1001 anna && echo 'anna:anna' | chpasswd
if "$G"; then echo "FEHLER: Passwort gleich Benutzername nicht erkannt"; exit 1; fi
passwd -l anna >/dev/null
"$G" || { echo "FEHLER: gesperrtes Konto blockiert SSH"; exit 1; }
echo "ssh-guard ok"

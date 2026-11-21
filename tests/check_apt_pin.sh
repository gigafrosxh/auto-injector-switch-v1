#!/bin/bash
# Akzeptanztest fuer os/image/apt/teria-l4t.pref (#45).
# Baut ein synthetisches APT-Repo mit Origin theofficialgman-L4T und prueft mit apt-cache policy,
# dass nur L4T 32.3.x installierbar ist, auch wenn neuere Versionen angeboten werden.
# Laeuft in einem Debian-Container, braucht nur apt.
set -euo pipefail

PREF="${1:-$(dirname "$0")/../os/image/apt/teria-l4t.pref}"
PREF="$(cd "$(dirname "$PREF")" && pwd)/$(basename "$PREF")"
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT

# Ein Repo im Layout von l4t-debs: Suite l4t, Komponente als Verzeichnis
mkrepo() { # mkrepo <name> <eintraege: paket=version ...>
    local dir="$T/$1"; shift
    mkdir -p "$dir"
    : > "$dir/Packages"
    for e in "$@"; do
        printf 'Package: %s\nVersion: %s\nArchitecture: all\nMaintainer: test\nFilename: pool/%s_%s_all.deb\nSize: 1\nDescription: test\n\n' \
            "${e%%=*}" "${e#*=}" "${e%%=*}" "${e#*=}" >> "$dir/Packages"
    done
    {
        printf 'Origin: theofficialgman-L4T\nLabel: L4T\nSuite: l4t\nCodename: l4t\nDate: %s\nSHA256:\n' "$(date -Ru)"
        printf ' %s %s Packages\n' "$(sha256sum "$dir/Packages" | cut -d' ' -f1)" "$(wc -c < "$dir/Packages")"
    } > "$dir/Release"
}

policy() { # policy <repo...> -- <paket>
    local repos=() pkg
    while [ "$1" != -- ]; do repos+=("$1"); shift; done
    pkg="$2"
    : > "$T/sources.list"
    for r in "${repos[@]}"; do echo "deb [trusted=yes] file:$T/$r ./" >> "$T/sources.list"; done
    rm -rf "$T/lists" "$T/cache"; mkdir -p "$T/lists/partial" "$T/cache/archives/partial"
    local o=(-o "Dir::Etc::SourceList=$T/sources.list" -o Dir::Etc::SourceParts=/nonexistent
             -o "Dir::Etc::Preferences=$PREF" -o Dir::Etc::PreferencesParts=/nonexistent
             -o "Dir::State::Lists=$T/lists" -o "Dir::Cache=$T/cache" -o APT::Get::List-Cleanup=false -o APT::Sandbox::User=root)
    apt-get "${o[@]}" -qq update >/dev/null
    apt-cache "${o[@]}" policy "$pkg"
}

candidate() { policy "$@" | awk '/Candidate:/ {print $2}'; }

fail=0
expect() { # expect <beschreibung> <soll> <ist>
    if [ "$2" = "$3" ]; then echo "ok   $1: $3"; else echo "FEHLER $1: erwartet $2, erhalten $3"; fail=1; fi
}

mkrepo noble nvidia-l4t-core=32.3.1-20191209225816 nvidia-bsp-32-3=1.0-6 switch-bsp=5.1.2-1
mkrepo noble-32-7 nvidia-l4t-core=32.7.4-20230608212426 nvidia-bsp-32-7=1.0-10
mkrepo nur-neu nvidia-l4t-core=32.7.4-20230608212426 nvidia-l4t-3d-core=35.1.0-1

expect "32.3.1 und 32.7.4 angeboten" 32.3.1-20191209225816 "$(candidate noble noble-32-7 -- nvidia-l4t-core)"
expect "nur 32.7.4 angeboten" "(none)" "$(candidate nur-neu -- nvidia-l4t-core)"
expect "L4T 35 angeboten" "(none)" "$(candidate nur-neu -- nvidia-l4t-3d-core)"
expect "Metapaket nvidia-bsp-32-7" "(none)" "$(candidate noble noble-32-7 -- nvidia-bsp-32-7)"
expect "Metapaket nvidia-bsp-32-3" 1.0-6 "$(candidate noble noble-32-7 -- nvidia-bsp-32-3)"
expect "nvidia-bsp-32-3 mit Priorität 1001" 1.0-6 "$(policy noble -- nvidia-bsp-32-3 | awk '/1001/ {print "1.0-6"; exit}')"
expect "switch-bsp" 5.1.2-1 "$(candidate noble -- switch-bsp)"

echo
policy noble noble-32-7 -- nvidia-l4t-core
exit "$fail"

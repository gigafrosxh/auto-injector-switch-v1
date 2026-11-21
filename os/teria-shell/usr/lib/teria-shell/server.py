"""Teria-Shell: lokaler Dienst fuer die Konsolen-Oberflaeche.

Stellt die Oberflaeche (www/) und eine kleine JSON-API auf 127.0.0.1 bereit.
Nur Standardbibliothek; Gtk wird optional fuer Icons genutzt.

Mit TERIA_SHELL_MOCK=1 (oder ausserhalb von Linux) liefert die API Beispieldaten,
damit sich die Oberflaeche am PC/Mac entwickeln und pruefen laesst.
"""
import configparser
import glob
import json
import mimetypes
import os
import queue
import re
import shlex
import shutil
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
WWW = os.path.join(HERE, "www")
CATALOG = os.path.join(HERE, "catalog.json")
MOCK = os.environ.get("TERIA_SHELL_MOCK") == "1" or not sys.platform.startswith("linux")
STATE_DIR = os.path.join(os.path.expanduser("~"), ".local", "share", "teria")
RECENT = os.path.join(STATE_DIR, "recent.json")
VERSION_FILE = "/usr/lib/teria/version"

EVENTS = []          # Warteschlangen der verbundenen SSE-Clients
EVENTS_LOCK = threading.Lock()
JOBS = {}            # Installationsauftraege


def emit(kind, data):
    with EVENTS_LOCK:
        for q in list(EVENTS):
            try:
                q.put_nowait((kind, data))
            except queue.Full:
                pass


def run(cmd, timeout=10):
    """Fuehrt einen Befehl aus und gibt (rc, stdout) zurueck. Nie eine Shell."""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return 1, ""


def rd(path, default=None):
    try:
        with open(path) as f:
            return f.read().strip()
    except OSError:
        return default


# ---------------------------------------------------------------- Systemzustand

def battery():
    b = "/sys/class/power_supply/battery"
    cap = rd(b + "/capacity")
    jc = []
    for d in sorted(glob.glob("/sys/class/power_supply/nintendo_switch_controller_battery_*")):
        lvl = rd(d + "/capacity_level", "?")
        jc.append({"name": "Joy-Con " + ("L" if d.endswith("serial0-0") else "R" if d.endswith("serial1-0") else d[-3:]),
                   "level": {"Full": "Voll", "High": "Hoch", "Normal": "Mittel", "Low": "Niedrig", "Critical": "Kritisch"}.get(lvl, lvl)})
    full, design = rd(b + "/charge_full"), rd(b + "/charge_full_design")
    power = rd(b + "/power_now")
    return {
        "capacity": int(cap) if cap and cap.isdigit() else None,
        "charging": rd(b + "/status") == "Charging",
        "power_w": round(abs(int(power)) / 1e6, 1) if power and power.lstrip("-").isdigit() else None,
        "cycles": rd(b + "/cycle_count"),
        "health": round(int(full) * 100 / int(design)) if full and design and design != "0" else None,
        "limit": (lambda v: v if v and v not in ("0", "100") else None)(rd("/sys/class/power_supply/usb/charge_control_limit")),
        "joycons": jc,
    }


def temps():
    out = {}
    for z in glob.glob("/sys/class/thermal/thermal_zone*"):
        t = rd(z + "/type")
        if t in ("CPU-therm", "GPU-therm"):
            v = rd(z + "/temp")
            if v and v.lstrip("-").isdigit():
                out[t.split("-")[0].lower()] = round(int(v) / 1000)
    return out


def wifi():
    rc, radio = run(["nmcli", "-t", "radio", "wifi"])
    rc2, active = run(["nmcli", "-t", "-f", "ACTIVE,SSID,SIGNAL,FREQ", "dev", "wifi"])
    ssid, signal, band = None, None, None
    for line in active.splitlines():
        parts = line.split(":")
        if parts and parts[0] == "yes":
            ssid, signal = parts[1], parts[2] if len(parts) > 2 else None
            freq = parts[3] if len(parts) > 3 else ""
            band = "5 GHz" if freq.startswith("5") else "2,4 GHz" if freq else None
    return {"on": radio == "enabled", "ssid": ssid, "signal": signal, "band": band}


def bluetooth():
    rc, out = run(["bluetoothctl", "show"])
    on = "Powered: yes" in out
    rc, devs = run(["bluetoothctl", "devices", "Connected"])
    names = [l.split(" ", 2)[2] for l in devs.splitlines() if l.startswith("Device ") and len(l.split(" ", 2)) == 3]
    return {"on": on, "connected": names}


def docked():
    for p in glob.glob("/sys/class/extcon/*/state"):
        s = rd(p, "")
        if "DP=1" in s or "HDMI=1" in s:
            return True
    return False


def brightness():
    rc, cur = run(["brightnessctl", "-m"])
    # Format: device,class,current,percent,max
    m = re.search(r",(\d+)%,", cur)
    return int(m.group(1)) if m else None


def volume():
    rc, out = run(["pactl", "get-sink-volume", "@DEFAULT_SINK@"])
    m = re.search(r"(\d+)%", out)
    rc, mute = run(["pactl", "get-sink-mute", "@DEFAULT_SINK@"])
    return {"value": int(m.group(1)) if m else None, "muted": "yes" in mute}


def perf():
    return rd("/run/teria/perf", "ausgewogen")


def emmc():
    rc, out = run(["teria", "guard", "status"])
    first = out.splitlines()[0] if out else ""
    val = first.split(":", 1)[1].strip() if ":" in first else "unbekannt"
    return val.replace("geschuetzt", "geschützt")


def storage():
    st = os.statvfs("/")
    return {"free_gb": round(st.f_bavail * st.f_frsize / 1e9), "total_gb": round(st.f_blocks * st.f_frsize / 1e9)}


def state():
    if MOCK:
        return MOCK_STATE
    return {
        "user": os.environ.get("USER", "teria"),
        "version": rd(VERSION_FILE, "?"),
        "battery": battery(),
        "temps": temps(),
        "wifi": wifi(),
        "bluetooth": bluetooth(),
        "docked": docked(),
        "brightness": brightness(),
        "volume": volume(),
        "perf": perf(),
        "emmc": emmc(),
        "storage": storage(),
    }


# ---------------------------------------------------------------- Apps

DESKTOP_DIRS = ["/usr/share/applications", "/usr/local/share/applications",
                os.path.expanduser("~/.local/share/applications"),
                "/var/lib/flatpak/exports/share/applications",
                os.path.expanduser("~/.local/share/flatpak/exports/share/applications")]
HIDDEN = {"teria-shell.desktop", "xfce4-session-logout.desktop", "xfce4-mail-reader.desktop", "xfce4-web-browser.desktop",
          "xfce4-file-manager.desktop", "xfce4-terminal-emulator.desktop", "thunar-bulk-rename.desktop",
          "onboard-settings.desktop", "blueman-adapters.desktop", "panel-preferences.desktop", "nm-connection-editor.desktop",
          "xfce4-settings-editor.desktop", "xfce4-terminal-settings.desktop", "thunar-settings.desktop",
          "org.xfce.mousepad-settings.desktop", "xfce-settings-manager.desktop", "debian-uxterm.desktop", "debian-xterm.desktop"}
# Einstellungsdialoge von Xfce gehoeren in den Desktop-Modus, nicht in die Konsolen-Oberflaeche
HIDDEN_CATS = {"X-XFCE-SettingsDialog", "X-XFCE-HardwareSettings", "X-XFCE-PersonalSettings", "X-XFCE-SystemSettings", "DesktopSettings", "HardwareSettings"}


def category(cats):
    c = set(cats.split(";"))
    if "Game" in c:
        return "spiele"
    if c & {"AudioVideo", "Audio", "Video", "Player"}:
        return "medien"
    if c & {"Development", "IDE"}:
        return "entwicklung"
    if c & {"Settings", "System", "TerminalEmulator", "FileManager", "Monitor"}:
        return "system"
    return "apps"


def list_apps():
    if MOCK:
        return MOCK_APPS
    lang = os.environ.get("LANG", "de").split("_")[0]
    seen, apps = set(), []
    for d in DESKTOP_DIRS:
        for f in sorted(glob.glob(os.path.join(d, "*.desktop"))):
            aid = os.path.basename(f)
            if aid in seen or aid in HIDDEN:
                continue
            cp = configparser.RawConfigParser(interpolation=None, strict=False)
            try:
                cp.read(f, encoding="utf-8")
                e = cp["Desktop Entry"]
            except (configparser.Error, KeyError, UnicodeDecodeError):
                continue
            if e.get("Type") != "Application" or e.get("NoDisplay", "false") == "true" or e.get("Hidden", "false") == "true":
                continue
            if e.get("Terminal", "false") == "true" or set(e.get("Categories", "").split(";")) & HIDDEN_CATS:
                continue
            only = e.get("OnlyShowIn", "")
            if only and "XFCE" not in only and "Teria" not in only:
                continue
            seen.add(aid)
            apps.append({"id": aid, "name": e.get("Name[%s]" % lang) or e.get("Name", aid),
                         "comment": e.get("Comment[%s]" % lang) or e.get("Comment", ""),
                         "category": category(e.get("Categories", "")), "icon": e.get("Icon", "")})
    recent = load_recent()
    order = {a: i for i, a in enumerate(recent)}
    for a in apps:
        a["recent"] = order.get(a["id"])
    apps.sort(key=lambda a: (order.get(a["id"], 10_000), a["name"].lower()))
    return apps


def load_recent():
    try:
        with open(RECENT) as f:
            return json.load(f)
    except (OSError, ValueError):
        return []


def remember(aid):
    r = [a for a in load_recent() if a != aid]
    r.insert(0, aid)
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(RECENT, "w") as f:
        json.dump(r[:30], f)


def launch(aid):
    if MOCK:
        return True
    if not re.fullmatch(r"[\w.\-+]+\.desktop", aid or ""):
        return False
    if not any(os.path.exists(os.path.join(d, aid)) for d in DESKTOP_DIRS):
        return False
    subprocess.Popen(["gtk-launch", aid[:-8]], start_new_session=True,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    remember(aid)
    return True


_ICON_THEME = None


def icon_path(name):
    """Sucht eine Icon-Datei ueber Gtk (falls vorhanden), sonst in hicolor/pixmaps."""
    global _ICON_THEME
    if not name:
        return None
    if os.path.isabs(name) and os.path.exists(name):
        return name
    try:
        if _ICON_THEME is None:
            import gi
            gi.require_version("Gtk", "3.0")
            from gi.repository import Gtk
            _ICON_THEME = Gtk.IconTheme.get_default() or False
        if _ICON_THEME:
            info = _ICON_THEME.lookup_icon(name, 256, 0)
            if info:
                return info.get_filename()
    except Exception:
        _ICON_THEME = False
    for pat in ("/usr/share/icons/hicolor/256x256/apps/%s.png", "/usr/share/icons/hicolor/scalable/apps/%s.svg",
                "/usr/share/icons/hicolor/128x128/apps/%s.png", "/usr/share/pixmaps/%s.png", "/usr/share/pixmaps/%s.svg"):
        p = pat % name
        if os.path.exists(p):
            return p
    return None


# ---------------------------------------------------------------- Store

def catalog():
    with open(CATALOG) as f:
        items = json.load(f)
    if MOCK:
        for it in items:
            it["installed"] = it["pkg"] in ("geany", "vlc")
        return items
    names = [it["pkg"] for it in items]
    rc, out = run(["dpkg-query", "-W", "-f", "${Package} ${db:Status-Status}\n"] + names)
    inst = {l.split()[0] for l in out.splitlines() if l.endswith(" installed")}
    for it in items:
        it["installed"] = it["pkg"] in inst
    return items


def install(pkg):
    allowed = {it["pkg"] for it in catalog()}
    if pkg not in allowed:
        return None
    jid = str(int(time.time() * 1000))
    JOBS[jid] = {"pkg": pkg, "status": "laeuft", "progress": 0}

    def work():
        if MOCK:
            for i in range(1, 11):
                time.sleep(0.3)
                JOBS[jid]["progress"] = i * 10
                emit("job", dict(JOBS[jid], id=jid))
            JOBS[jid]["status"] = "fertig"
        else:
            p = subprocess.Popen(["pkexec", "/usr/lib/teria/pkg", "install", pkg],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in p.stdout:
                m = re.search(r"(\d+)%", line)
                if m:
                    JOBS[jid]["progress"] = int(m.group(1))
                    emit("job", dict(JOBS[jid], id=jid))
            JOBS[jid]["status"] = "fertig" if p.wait() == 0 else "fehler"
        emit("job", dict(JOBS[jid], id=jid))

    threading.Thread(target=work, daemon=True).start()
    return jid


# ---------------------------------------------------------------- Aktionen

def act(action, body):
    """Fuehrt eine Aktion aus der Oberflaeche aus. Gibt (ok, info) zurueck."""
    if MOCK:
        apply_mock(action, body)
        return True, None
    v = body.get("value")
    if action == "wifi":
        return run(["nmcli", "radio", "wifi", "on" if v else "off"])[0] == 0, None
    if action == "wifi-connect":
        ssid, pw = str(body.get("ssid", "")), str(body.get("password", ""))
        cmd = ["nmcli", "dev", "wifi", "connect", ssid] + (["password", pw] if pw else [])
        rc, out = run(cmd, timeout=45)
        return rc == 0, out
    if action == "bluetooth":
        return run(["bluetoothctl", "power", "on" if v else "off"])[0] == 0, None
    if action == "brightness":
        return run(["brightnessctl", "set", "%d%%" % max(5, min(100, int(v)))])[0] == 0, None
    if action == "volume":
        return run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "%d%%" % max(0, min(150, int(v)))])[0] == 0, None
    if action == "perf" and v in ("eco", "ausgewogen", "max"):
        return run(["pkexec", "/usr/lib/teria/perf", v], timeout=30)[0] == 0, None
    if action == "power":
        cmds = {"reboot": ["systemctl", "reboot"], "poweroff": ["systemctl", "poweroff"],
                "suspend": ["systemctl", "suspend"], "hekate": ["pkexec", "/usr/lib/teria/reboot-hekate"],
                }
        if v == "logout":
            emit("quit", {})
            return True, None
        if v in cmds:
            subprocess.Popen(cmds[v], start_new_session=True)
            return True, None
    if action == "mode":
        if v == "desktop":
            subprocess.Popen(["/usr/lib/teria-shell/desktop-mode", "start"], start_new_session=True)
            emit("hide", {})
        else:
            subprocess.Popen(["/usr/lib/teria-shell/desktop-mode", "stop"], start_new_session=True)
            emit("show", {})
        return True, None
    if action == "keyboard":
        subprocess.Popen(["onboard"], start_new_session=True)
        return True, None
    return False, "unbekannte Aktion"


def wifi_networks():
    if MOCK:
        return [{"ssid": "Heimnetz", "signal": 88, "secure": True, "active": True},
                {"ssid": "Heimnetz-Gast", "signal": 61, "secure": True, "active": False},
                {"ssid": "FRITZ!Box 7590", "signal": 34, "secure": True, "active": False}]
    rc, out = run(["nmcli", "-t", "-f", "IN-USE,SSID,SIGNAL,SECURITY", "dev", "wifi", "list", "--rescan", "auto"], timeout=20)
    nets = {}
    for line in out.splitlines():
        parts = re.split(r"(?<!\\):", line)
        if len(parts) < 4 or not parts[1]:
            continue
        ssid = parts[1].replace("\\:", ":")
        sig = int(parts[2]) if parts[2].isdigit() else 0
        if ssid not in nets or nets[ssid]["signal"] < sig:
            nets[ssid] = {"ssid": ssid, "signal": sig, "secure": parts[3] not in ("", "--"), "active": parts[0] == "*"}
    return sorted(nets.values(), key=lambda n: (not n["active"], -n["signal"]))


def system_info():
    if MOCK:
        return MOCK_INFO
    rc, out = run(["teria", "info"])
    info = {}
    for line in out.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            if k.strip() and v.strip():
                info[k.strip()] = v.strip()
    return info


# ---------------------------------------------------------------- Controller (evdev)

def gamepad_thread():
    """Liest Joy-Cons/Pro Controller ueber evdev und schickt Tasten an die Oberflaeche."""
    try:
        import evdev
        from evdev import ecodes as e
    except ImportError:
        return
    # Nintendo-Belegung: A rechts (BTN_EAST), B unten (BTN_SOUTH)
    keymap = {e.BTN_EAST: "a", e.BTN_SOUTH: "b", e.BTN_NORTH: "x", e.BTN_WEST: "y",
              e.BTN_START: "plus", e.BTN_SELECT: "minus", e.BTN_MODE: "home",
              e.BTN_TL: "l", e.BTN_TR: "r",
              e.BTN_DPAD_UP: "up", e.BTN_DPAD_DOWN: "down", e.BTN_DPAD_LEFT: "left", e.BTN_DPAD_RIGHT: "right"}
    watched = {}
    while True:
        for path in evdev.list_devices():
            if path in watched:
                continue
            try:
                dev = evdev.InputDevice(path)
                caps = dev.capabilities().get(e.EV_KEY, [])
            except OSError:
                continue
            if e.BTN_SOUTH in caps or e.BTN_EAST in caps:
                watched[path] = dev
                threading.Thread(target=read_pad, args=(dev, keymap, e, watched, path), daemon=True).start()
        time.sleep(3)


def read_pad(dev, keymap, e, watched, path):
    stick = {"x": 0, "y": 0}
    try:
        for ev in dev.read_loop():
            if ev.type == e.EV_KEY and ev.value == 1 and ev.code in keymap:
                key = keymap[ev.code]
                if key == "home":
                    subprocess.Popen(["wmctrl", "-a", "Teria"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                emit("pad", {"key": key})
            elif ev.type == e.EV_ABS and ev.code in (e.ABS_HAT0X, e.ABS_HAT0Y) and ev.value != 0:
                emit("pad", {"key": {(e.ABS_HAT0X, -1): "left", (e.ABS_HAT0X, 1): "right",
                                     (e.ABS_HAT0Y, -1): "up", (e.ABS_HAT0Y, 1): "down"}[(ev.code, ev.value)]})
            elif ev.type == e.EV_ABS and ev.code in (e.ABS_X, e.ABS_Y):
                info = dev.absinfo(ev.code)
                mid = (info.max + info.min) / 2
                rel = (ev.value - mid) / ((info.max - info.min) / 2 or 1)
                axis = "x" if ev.code == e.ABS_X else "y"
                d = -1 if rel < -0.6 else 1 if rel > 0.6 else 0
                if d and d != stick[axis]:
                    emit("pad", {"key": ("left" if d < 0 else "right") if axis == "x" else ("up" if d < 0 else "down")})
                stick[axis] = d
    except OSError:
        pass
    watched.pop(path, None)


def ticker():
    while True:
        time.sleep(5)
        if EVENTS:
            try:
                emit("state", state())
            except Exception:
                pass


# ---------------------------------------------------------------- HTTP

class Handler(BaseHTTPRequestHandler):
    server_version = "TeriaShell"

    def log_message(self, *a):
        pass

    def send_json(self, obj, code=200):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_file(self, path):
        try:
            with open(path, "rb") as f:
                data = f.read()
        except OSError:
            return self.send_error(404)
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache" if path.endswith((".html", ".js", ".css")) else "max-age=3600")
        self.end_headers()
        self.wfile.write(data)

    def allowed(self):
        # Nur die eigene Oberflaeche darf die API benutzen (Schutz gegen fremde Webseiten)
        origin = self.headers.get("Origin")
        host = self.headers.get("Host", "")
        return host.startswith(("127.0.0.1:", "localhost:")) and (origin is None or origin == "http://" + host)

    def do_GET(self):
        if not self.allowed():
            return self.send_error(403)
        u = urlparse(self.path)
        p = u.path
        if p == "/api/state":
            return self.send_json(state())
        if p == "/api/apps":
            return self.send_json(list_apps())
        if p == "/api/store":
            return self.send_json(catalog())
        if p == "/api/wifi":
            return self.send_json(wifi_networks())
        if p == "/api/info":
            return self.send_json(system_info())
        if p.startswith("/api/icon/"):
            name = p[len("/api/icon/"):]
            if not re.fullmatch(r"[\w.\-+]+", name):
                return self.send_error(404)
            path = icon_path(name)
            return self.send_file(path) if path else self.send_error(404)
        if p == "/api/events":
            return self.events()
        rel = os.path.normpath(p.lstrip("/") or "index.html")
        if rel.startswith(".."):
            return self.send_error(404)
        full = os.path.join(WWW, rel)
        if os.path.isdir(full):
            full = os.path.join(full, "index.html")
        return self.send_file(full)

    def do_POST(self):
        if not self.allowed() or self.headers.get("Content-Type", "").split(";")[0] != "application/json":
            return self.send_error(403)
        n = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            return self.send_error(400)
        p = urlparse(self.path).path
        if p == "/api/launch":
            return self.send_json({"ok": launch(body.get("id"))})
        if p == "/api/install":
            jid = install(body.get("pkg"))
            return self.send_json({"ok": jid is not None, "job": jid})
        if p.startswith("/api/action/"):
            ok, info = act(p[len("/api/action/"):], body)
            return self.send_json({"ok": ok, "info": info})
        self.send_error(404)

    def events(self):
        q = queue.Queue(maxsize=100)
        with EVENTS_LOCK:
            EVENTS.append(q)
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            while True:
                try:
                    kind, data = q.get(timeout=15)
                    msg = "event: %s\ndata: %s\n\n" % (kind, json.dumps(data))
                except queue.Empty:
                    msg = ": ping\n\n"
                self.wfile.write(msg.encode())
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
        finally:
            with EVENTS_LOCK:
                EVENTS.remove(q)


def serve(port=0):
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    threading.Thread(target=ticker, daemon=True).start()
    if not MOCK:
        threading.Thread(target=gamepad_thread, daemon=True).start()
    return srv


# ---------------------------------------------------------------- Beispieldaten

MOCK_STATE = {
    "user": "daniel", "version": "0.3.0",
    "battery": {"capacity": 78, "charging": True, "power_w": 5.2, "cycles": "140", "health": 99, "limit": "85",
                "joycons": [{"name": "Joy-Con L", "level": "Hoch"}, {"name": "Joy-Con R", "level": "Niedrig"}]},
    "temps": {"cpu": 47, "gpu": 48},
    "wifi": {"on": True, "ssid": "Heimnetz", "signal": "88", "band": "5 GHz"},
    "bluetooth": {"on": True, "connected": ["Joy-Con (L)", "Joy-Con (R)"]},
    "docked": False, "brightness": 64, "volume": {"value": 40, "muted": False},
    "perf": "ausgewogen", "emmc": "geschützt", "storage": {"free_gb": 54, "total_gb": 63},
}
MOCK_INFO = {"System": "Teria 0.3.0 (Debian GNU/Linux 13, Switchroot L4T)", "Geraet": "Nintendo Switch (2017)",
             "Kernel": "4.9.140-l4t", "L4T": "R32.3.1 (switch-bsp 5.1.2-34+24.04)", "eMMC": "geschützt",
             "Root": "/dev/mmcblk0p2 auf mmcblk0"}
MOCK_APPS = [
    {"id": "orbitfall.desktop", "name": "Orbitfall", "comment": "Kapitel 3 · Der Ring um Teria", "category": "spiele", "icon": "", "art": "t-orbit", "recent": 0},
    {"id": "sternenlaeufer.desktop", "name": "Sternenläufer", "comment": "Endlos-Rennen durchs All", "category": "spiele", "icon": "", "art": "t-sterne", "recent": 1},
    {"id": "pixelgarten.desktop", "name": "Pixelgarten", "comment": "Gemütliches Aufbauspiel", "category": "spiele", "icon": "", "art": "t-pixel", "recent": 2},
    {"id": "abendrot.desktop", "name": "Abendrot", "comment": "Erkundung bei Sonnenuntergang", "category": "spiele", "icon": "", "art": "t-berg", "recent": 3},
    {"id": "code-studio.desktop", "name": "Code-Studio", "comment": "Entwicklungsumgebung", "category": "entwicklung", "icon": "", "art": "t-code"},
    {"id": "wellen.desktop", "name": "Wellen", "comment": "Musik", "category": "medien", "icon": "", "art": "t-wellen"},
    {"id": "firefox-esr.desktop", "name": "Browser", "comment": "Im Internet surfen", "category": "apps", "icon": "", "glyph": "globe"},
    {"id": "xfce4-terminal.desktop", "name": "Terminal", "comment": "Befehlszeile", "category": "system", "icon": "", "glyph": "term"},
    {"id": "thunar.desktop", "name": "Dateien", "comment": "Dateien verwalten", "category": "system", "icon": "", "glyph": "folder"},
]


def apply_mock(action, body):
    v = body.get("value")
    if action == "wifi":
        MOCK_STATE["wifi"]["on"] = bool(v)
    elif action == "bluetooth":
        MOCK_STATE["bluetooth"]["on"] = bool(v)
    elif action == "brightness":
        MOCK_STATE["brightness"] = int(v)
    elif action == "volume":
        MOCK_STATE["volume"]["value"] = int(v)
    elif action == "perf":
        MOCK_STATE["perf"] = v

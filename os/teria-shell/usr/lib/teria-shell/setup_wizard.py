"""Lokaler Erststartdialog. Zugangsdaten verlassen den Prozess ausschließlich über stdin."""
import json
import queue
import subprocess
import threading

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk

import server


def run(stage):
    events = queue.Queue()
    server.EVENTS.append(events)
    threading.Thread(target=server.gamepad_thread, daemon=True).start()
    window = Gtk.Window(title="Teria")
    window.fullscreen()
    window.connect("delete-event", lambda *_: True)
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8, margin=16)
    window.add(box)
    title = Gtk.Label()
    box.pack_start(title, False, False, 0)
    pages = Gtk.Stack()
    box.pack_start(pages, False, False, 0)
    keyboard = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
    box.pack_start(keyboard, True, False, 0)
    message = Gtk.Label(wrap=True)
    box.pack_start(message, False, False, 0)
    actions = Gtk.ButtonBox()
    box.pack_end(actions, False, False, 0)
    entries = {}
    target = None
    page = 0
    shifted = False
    saved = stage == "rename"
    language = Gtk.ToggleButton(label="Deutsch")
    language.connect("toggled", lambda b: b.set_label("English" if b.get_active() else "Deutsch"))
    screens = [
        ("Sprache und Zeitzone", [("zone", "Zeitzone", "Europe/Vienna")]),
        ("WLAN", [("ssid", "Netzwerkname (leer für offline)", ""), ("wifiPassword", "WLAN-Passwort (leer für offenes Netz)", "")]),
        ("Persönliches Konto", [("name", "Benutzername", "teria"), ("password", "Passwort (mindestens 8 Zeichen)", ""), ("repeat", "Passwort wiederholen", "")]),
    ]

    def remember(entry, _):
        nonlocal target
        target = entry
        return False

    for index, (_, fields) in enumerate(screens):
        grid = Gtk.Grid(column_spacing=12, row_spacing=5)
        if index == 0:
            grid.attach(Gtk.Label(label="Systemsprache", xalign=0), 0, 0, 1, 1)
            grid.attach(language, 1, 0, 1, 1)
        for row, (key, label, initial) in enumerate(fields, 1):
            entry = Gtk.Entry(text=initial, hexpand=True)
            entry.set_visibility(key not in ("password", "repeat", "wifiPassword"))
            entry.connect("focus-in-event", remember)
            entries[key] = entry
            grid.attach(Gtk.Label(label=label, xalign=0), 0, row, 1, 1)
            grid.attach(entry, 1, row, 1, 1)
        pages.add_named(grid, str(index))

    def press(_, char):
        nonlocal shifted
        if char == "⇧":
            shifted = not shifted
            draw_keyboard()
            return
        if target is None:
            return
        pos = target.get_position()
        selection = target.get_selection_bounds()
        if selection:
            start, end = selection
            target.delete_text(start, end)
            pos = start
        if char == "⌫":
            if not selection and pos:
                target.delete_text(pos - 1, pos)
                pos -= 1
        else:
            pos = target.insert_text(" " if char == "Leerzeichen" else char, pos)
        target.set_position(pos)

    def draw_keyboard():
        for row in keyboard.get_children():
            row.destroy()
        rows = (["1234567890-_.", "qwertzuiopü+", "asdfghjklöä@", "yxcvbnm/,:ß"]
                if not shifted else ["!\u0022§$%&()=?*#'", "QWERTZUIOPÜ~", "ASDFGHJKLÖÄ;", "YXCVBNM[]{}\\|<>"])
        for keys in [*rows, ["⇧", "Leerzeichen", "⌫"]]:
            row = Gtk.Box(homogeneous=True, spacing=3)
            for char in keys:
                button = Gtk.Button(label=char)
                button.connect("clicked", press, char)
                row.pack_start(button, True, True, 0)
            keyboard.pack_start(row, False, False, 0)
        keyboard.show_all()

    def show_page():
        title.set_markup(f"<big><b>{screens[page][0]}</b> · {page + 1}/3</big>")
        pages.set_visible_child_name(str(page))
        previous.set_sensitive(page > 0)
        forward.set_label("Speichern" if page == 2 else "Weiter")
        entries[screens[page][1][0][0]].grab_focus()

    def restart_page():
        title.set_text("Einrichtung gespeichert")
        pages.hide()
        keyboard.hide()
        previous.hide()
        message.set_text("Beim Neustart übernimmt Teria die Einstellungen für dein Konto.")
        forward.set_label("Jetzt neu starten")
        forward.grab_focus()

    def advance(_, delta):
        nonlocal page, saved
        message.set_text("")
        if saved:
            if subprocess.run(["systemctl", "reboot"]).returncode:
                message.set_text("Bitte starte Teria über das Systemmenü neu.")
            return
        if delta < 0 or page < 2:
            page += delta
            show_page()
            return
        values = {k: entry.get_text() for k, entry in entries.items()}
        if values.pop("repeat") != values["password"]:
            message.set_text("Die Passwörter stimmen nicht überein.")
            return
        values["locale"] = "en_US.UTF-8" if language.get_active() else "de_DE.UTF-8"
        result = subprocess.run(["pkexec", "/usr/lib/teria/setup-account"], input=json.dumps(values),
                                text=True, capture_output=True)
        if result.returncode:
            message.set_text(result.stderr.strip() or "Einrichtung fehlgeschlagen")
            return
        for k in ("password", "repeat", "wifiPassword"):
            entries[k].set_text("")
        saved = True
        restart_page()

    previous = Gtk.Button(label="Zurück")
    forward = Gtk.Button(label="Weiter")
    for button, delta in ((previous, -1), (forward, 1)):
        button.connect("clicked", advance, delta)
        actions.add(button)

    def pad():
        while not events.empty():
            kind, data = events.get_nowait()
            if kind != "pad":
                continue
            key = data["key"]
            if key in ("up", "down", "left", "right"):
                window.child_focus(getattr(Gtk.DirectionType, key.upper()))
            elif key == "a":
                focus = window.get_focus()
                if isinstance(focus, Gtk.Button):
                    focus.clicked()
                elif isinstance(focus, Gtk.Entry):
                    keyboard.get_children()[0].get_children()[0].grab_focus()
            elif key == "b" and page and not saved:
                advance(None, -1)
            elif key == "plus":
                advance(None, 1)
        return True

    draw_keyboard()
    window.show_all()
    if saved:
        restart_page()
    else:
        show_page()
    GLib.timeout_add(80, pad)
    Gtk.main()

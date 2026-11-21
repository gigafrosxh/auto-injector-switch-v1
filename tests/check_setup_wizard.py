"""Erststart im installierten Paket unter Xvfb mit simuliertem Root-Helfer."""
import json
import sys
from unittest.mock import patch

sys.path.insert(0, "/usr/lib/teria-shell")
import setup_wizard as wizard
from gi.repository import GLib, Gtk

result = []


def descendants(widget):
    yield widget
    if isinstance(widget, Gtk.Container):
        for child in widget.get_children():
            yield from descendants(child)


def check():
    try:
        window, = Gtk.Window.list_toplevels()
        items = list(descendants(window))
        buttons = {w.get_label(): w for w in items if isinstance(w, Gtk.Button)}
        buttons["Weiter"].clicked()
        buttons["Weiter"].clicked()
        stack, = [w for w in items if isinstance(w, Gtk.Stack)]
        entries = [w for w in descendants(stack.get_visible_child()) if isinstance(w, Gtk.Entry)]
        for entry in entries:
            entry.set_text("beispiel" if entry.get_visibility() else "SicheresPasswort42")
        buttons["Weiter"].clicked()
        assert buttons["Weiter"].get_label() == "Jetzt neu starten"
        settings = json.loads(helper.call_args.kwargs["input"])
        assert settings["name"] == "beispiel" and settings["password"] == "SicheresPasswort42"
        assert settings["ssid"] == "" and settings["locale"] == "de_DE.UTF-8"
        result.append(True)
    finally:
        Gtk.main_quit()
    return False


with patch.object(wizard.server, "gamepad_thread"), patch.object(wizard.subprocess, "run") as helper:
    helper.return_value.returncode = 0
    GLib.idle_add(check)
    wizard.run("pending")
assert result == [True]

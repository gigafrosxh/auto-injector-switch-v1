"""Paketinstallation auf einem virtuellen X-Display über die App-API prüfen."""
import json
import os
from pathlib import Path
import sys
import tempfile
import time
from urllib.request import Request, urlopen


def main():
    with tempfile.TemporaryDirectory() as home:
        os.environ["HOME"] = home
        os.environ["XDG_DATA_HOME"] = str(Path(home) / ".local/share")
        os.environ.pop("TERIA_SHELL_MOCK", None)
        sys.path.insert(0, "/usr/lib/teria-shell")
        import server

        apps = Path(os.environ["XDG_DATA_HOME"]) / "applications"
        apps.mkdir(parents=True)
        marker = Path(home) / "gestartet"
        app = apps / "teria-starttest.desktop"
        entry = "[Desktop Entry]\nType=Application\nName=Teria-Starttest\nExec={}\n"
        app.write_text(entry.format(f"/usr/bin/touch {marker}"))
        broken = apps / "teria-defekt.desktop"
        broken.write_text(entry.format("/nicht-vorhanden/teria-test"))

        http = server.serve()
        url = f"http://127.0.0.1:{http.server_port}/api/"
        def launch(name):
            req = Request(url + "launch", data=json.dumps({"id": name}).encode(),
                          headers={"Content-Type": "application/json"})
            with urlopen(req, timeout=15) as response:
                return json.load(response)["ok"]

        try:
            with urlopen(url + "apps", timeout=5) as response:
                assert app.name in {item["id"] for item in json.load(response)}
            assert launch(app.name), "Desktop-Eintrag konnte nicht gestartet werden"
            for _ in range(50):
                if marker.exists():
                    break
                time.sleep(0.1)
            assert marker.exists(), "Start wurde bestätigt, aber die Anwendung lief nicht"
            assert not launch(broken.name), "Ungültiger Programmaufruf als Erfolg gemeldet"
            assert server.load_recent() == [app.name], "App-Verlauf stimmt nicht"
        finally:
            http.shutdown()
            http.server_close()


if __name__ == "__main__":
    main()

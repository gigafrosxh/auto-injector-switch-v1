"""Regressionstests für die nmcli-Ausgaben im Teria-WLAN-Menü."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "os/teria-shell/usr/lib/teria-shell"))
import server


class WifiTests(unittest.TestCase):
    def test_status_and_scan_preserve_names(self):
        for ssid in ("Heimnetz", "Wohnung:5G", "Gast\\", "A\\:B", "Tom's WLAN"):
            with self.subTest(ssid=ssid):
                encoded = ssid.replace("\\", "\\\\").replace(":", "\\:")
                rows = [(0, "enabled"), (0, f"yes:{encoded}:82:5180 MHz"),
                        (0, f"*:{encoded}:82:WPA2")]
                with patch.object(server, "run", side_effect=rows), patch.object(server, "MOCK", False):
                    self.assertEqual(server.wifi(), {"on": True, "ssid": ssid, "signal": "82", "band": "5 GHz"})
                    self.assertEqual(server.wifi_networks(), [{"ssid": ssid, "signal": 82, "secure": True, "active": True, "enterprise": False}])

    def test_active_access_point_wins_in_either_order(self):
        lines = ["*:Mesh:52:WPA2", ":Mesh:82:WPA2", ":Gast:55:--", ":Gast:77:--"]
        for rows in (lines, reversed(lines)):
            with patch.object(server, "run", return_value=(0, "\n".join(rows))), patch.object(server, "MOCK", False):
                self.assertEqual(server.wifi_networks(), [
                    {"ssid": "Mesh", "signal": 52, "secure": True, "active": True, "enterprise": False},
                    {"ssid": "Gast", "signal": 77, "secure": False, "active": False, "enterprise": False},
                ])

    def test_enterprise_network_is_marked(self):
        with patch.object(server, "run", return_value=(0, "*:Schule:70:WPA2 802.1X")), patch.object(server, "MOCK", False):
            self.assertEqual(server.wifi_networks(), [
                {"ssid": "Schule", "signal": 70, "secure": True, "active": True, "enterprise": True}])

    def test_enterprise_connect_builds_peap_profile(self):
        calls = []

        def fake(cmd, timeout=10):
            calls.append(cmd)
            return 0, ""
        with patch.object(server, "run", side_effect=fake), patch.object(server, "MOCK", False):
            ok, _ = server.act("wifi-connect", {"ssid": "Schule", "identity": "max.muster", "password": "geheim"})
        self.assertTrue(ok)
        add = next(c for c in calls if c[:3] == ["nmcli", "connection", "add"])
        for k, v in (("wifi-sec.key-mgmt", "wpa-eap"), ("802-1x.eap", "peap"), ("802-1x.phase2-auth", "mschapv2"),
                     ("802-1x.identity", "max.muster"), ("ssid", "Schule")):
            self.assertEqual(add[add.index(k) + 1], v)
        self.assertEqual(calls[-1], ["nmcli", "connection", "up", "id", "Teria Schule"])


if __name__ == "__main__":
    unittest.main()

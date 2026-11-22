#!/usr/bin/env python3
"""Weichgezeichnete Hintergruende fuer die Glas-Flaechen der Teria-Oberflaeche erzeugen.

Die Switch hat fuer WebKit keine GPU-Beschleunigung, `backdrop-filter: blur()` ist dort zu
langsam. Stattdessen bekommen Glas-Flaechen ein vorberechnetes, weichgezeichnetes Bild.

Aufruf (macOS, nutzt sips):  tools/blur-image.py <eingabe.jpg> <ausgabe.jpg> [radius]
"""
import os
import struct
import subprocess
import sys
import tempfile

W, H = 320, 180          # Arbeitsgroesse; das Ergebnis wird danach auf 1280x720 hochskaliert


def sips(*args):
    subprocess.run(["sips", *args], check=True, stdout=subprocess.DEVNULL)


def read_bmp(path):
    data = open(path, "rb").read()
    off = struct.unpack_from("<I", data, 10)[0]
    w, h = struct.unpack_from("<ii", data, 18)
    bpp = struct.unpack_from("<H", data, 28)[0] // 8
    row = (w * bpp + 3) & ~3
    px = []
    for y in range(abs(h)):
        src = (abs(h) - 1 - y) if h > 0 else y
        base = off + src * row
        px.append([tuple(data[base + x * bpp + c] for c in (2, 1, 0)) for x in range(w)])
    return w, abs(h), px


def write_bmp(path, w, h, px):
    row = (w * 3 + 3) & ~3
    body = bytearray()
    for y in range(h - 1, -1, -1):
        line = bytearray()
        for r, g, b in px[y]:
            line += bytes((b, g, r))
        body += line + b"\0" * (row - w * 3)
    head = b"BM" + struct.pack("<IHHI", 54 + len(body), 0, 0, 54)
    info = struct.pack("<IiiHHIIiiII", 40, w, h, 1, 24, 0, len(body), 2835, 2835, 0, 0)
    open(path, "wb").write(head + info + body)


def box(line, r):
    n = len(line)
    out = []
    acc = [0, 0, 0]
    for i in range(-r, r + 1):
        p = line[min(max(i, 0), n - 1)]
        for c in range(3):
            acc[c] += p[c]
    k = 2 * r + 1
    for i in range(n):
        out.append(tuple(acc[c] // k for c in range(3)))
        a, b = line[min(i + r + 1, n - 1)], line[max(i - r, 0)]
        for c in range(3):
            acc[c] += a[c] - b[c]
    return out


def blur(px, r, passes=3):
    for _ in range(passes):          # drei Box-Durchgaenge ~ Gauss
        px = [box(line, r) for line in px]
        cols = [box([px[y][x] for y in range(len(px))], r) for x in range(len(px[0]))]
        px = [[cols[x][y] for x in range(len(cols))] for y in range(len(px))]
    return px


def main():
    src, dst = sys.argv[1], sys.argv[2]
    r = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    with tempfile.TemporaryDirectory() as t:
        small = os.path.join(t, "s.bmp")
        sips("-s", "format", "bmp", "-z", str(H), str(W), src, "--out", small)
        w, h, px = read_bmp(small)
        out = os.path.join(t, "o.bmp")
        write_bmp(out, w, h, blur(px, r))
        sips("-s", "format", "jpeg", "-s", "formatOptions", "82", "-z", "720", "1280", out, "--out", dst)


if __name__ == "__main__":
    main()

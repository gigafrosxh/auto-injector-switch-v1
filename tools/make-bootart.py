#!/usr/bin/env python3
"""Erzeugt das Teria-Bootlogo (720x1280, um 90 Grad gegen den Uhrzeigersinn gedreht, wie Hekate es auf dem Switch-Panel erwartet)
und das Menue-Icon (192x192) als 32-Bit-BMP. Nur Pillow, keine Schriftdateien:
der Schriftzug ist geometrisch gezeichnet.

Aufruf: python3 tools/make-bootart.py boot/teria
"""
import sys, os
from PIL import Image, ImageDraw, ImageFilter

BG_TOP, BG_BOT = (12, 14, 30), (30, 16, 58)
ACCENT = (62, 224, 197)
INK = (236, 238, 245)

def gradient(w, h):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        c = tuple(int(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOT))
        for x in range(w):
            px[x, y] = c
    return img

def letters(d, x, y, s, color):
    """Zeichnet TERIA mit Strichstaerke s*0.22 ab (x, y), Hoehe s. Gibt Breite zurueck."""
    t = max(2, int(s * 0.2)); w = int(s * 0.72); gap = int(s * 0.28)
    cx = x
    # T
    d.rectangle([cx, y, cx + w, y + t], fill=color)
    d.rectangle([cx + w // 2 - t // 2, y, cx + w // 2 + t // 2, y + s], fill=color)
    cx += w + gap
    # E
    d.rectangle([cx, y, cx + t, y + s], fill=color)
    for yy in (y, y + s // 2 - t // 2, y + s - t):
        d.rectangle([cx, yy, cx + w - (t if yy != y and yy != y + s - t else 0), yy + t], fill=color)
    cx += w + gap
    # R
    d.rectangle([cx, y, cx + t, y + s], fill=color)
    bowl = s // 2 + t // 2
    d.rounded_rectangle([cx, y, cx + w, y + bowl], radius=bowl // 2, outline=color, width=t)
    d.polygon([(cx + w // 3, y + bowl - t // 2), (cx + w // 3 + t, y + bowl - t // 2),
               (cx + w + t // 3, y + s), (cx + w - t + t // 3, y + s)], fill=color)
    cx += w + gap
    # I
    d.rectangle([cx, y, cx + t, y + s], fill=color)
    cx += t + gap
    # A
    d.polygon([(cx, y + s), (cx + t, y + s), (cx + w // 2 + t // 2, y), (cx + w // 2 - t // 2, y)], fill=color)
    d.polygon([(cx + w, y + s), (cx + w - t, y + s), (cx + w // 2 - t // 2, y), (cx + w // 2 + t // 2, y)], fill=color)
    d.rectangle([cx + w // 4, y + int(s * 0.62), cx + w - w // 4, y + int(s * 0.62) + t * 3 // 4], fill=color)
    cx += w
    return cx - x

def mark(img, cx, cy, r):
    """Planet mit Orbit: Ring + gefuellter Kreis + kleiner Mond."""
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse([cx - r * 1.6, cy - r * 1.6, cx + r * 1.6, cy + r * 1.6], fill=ACCENT + (40,))
    glow = glow.filter(ImageFilter.GaussianBlur(r * 0.5))
    img.paste(glow, (0, 0), glow)
    d = ImageDraw.Draw(img)
    shade = tuple(int(c * 0.72) for c in ACCENT)
    box = [cx - r, cy - r, cx + r, cy + r]
    d.ellipse(box, fill=shade)
    d.ellipse([cx - r, cy - r, cx + r * 0.7, cy + r * 0.7], fill=ACCENT)
    d.ellipse([cx - r * 1.7, cy - r * 0.45, cx + r * 1.7, cy + r * 0.45], outline=INK, width=max(2, r // 9))
    # hintere Ringhaelfte verschwindet hinter dem Planeten
    d.chord(box, 180, 360, fill=ACCENT)
    mr = max(3, r // 5)
    d.ellipse([cx + r * 1.35 - mr, cy - r * 0.9 - mr, cx + r * 1.35 + mr, cy - r * 0.9 + mr], fill=INK)

def bootlogo():
    W, H = 1280, 720
    img = gradient(W, H).convert("RGBA")
    mark(img, W // 2, 300, 70)
    d = ImageDraw.Draw(img)
    s = 64
    probe = Image.new("RGB", (10, 10)); width = letters(ImageDraw.Draw(probe), 0, 0, s, INK)
    letters(d, (W - width) // 2, 450, s, INK)
    d.rectangle([W // 2 - 40, 545, W // 2 + 40, 549], fill=ACCENT)
    # Hekate erwartet das Bild hochkant (Panel ist physisch hochkant verbaut)
    return img.convert("RGB").rotate(90, expand=True)

def icon():
    S = 192
    img = gradient(S, S).convert("RGBA")
    mark(img, S // 2, S // 2 - 14, 38)
    d = ImageDraw.Draw(img)
    s = 22
    probe = Image.new("RGB", (10, 10)); width = letters(ImageDraw.Draw(probe), 0, 0, s, INK)
    letters(d, (S - width) // 2, 148, s, INK)
    return img.convert("RGB")

def save_bmp32(img, path):
    img.convert("RGBA").save(path, format="BMP")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "boot/teria"
    os.makedirs(out, exist_ok=True)
    save_bmp32(bootlogo(), os.path.join(out, "bootlogo_teria.bmp"))
    save_bmp32(icon(), os.path.join(out, "icon_teria.bmp"))
    print("ok:", out)

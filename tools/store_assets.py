#!/usr/bin/env python3
"""Play Store brand assets from the REAL app icon vector — no new art, no hands.
Renders 2 files (4x supersampled → downscaled for crisp edges):
  store/store-icon-512.png        512x512  hi-res listing icon
  store/feature-graphic-1024x500.png       feature graphic (gradient + name + tasbih motif)
Source of truth = android/.../ic_launcher_foreground.xml (tasbih beads) + colors.xml bg.
Run:  python3 tools/store_assets.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "store")
BG = (0x16, 0x18, 0x26)               # ic_launcher_background #161826

# tasbih beads from ic_launcher_foreground.xml, viewport 108 → (cx, cy, r, hexfill)
BEADS = [
    (54, 32, 9, "#9184d9"),
    (76, 54, 7, "#B3A9EC"),
    (32, 54, 7, "#B3A9EC"),
    (68, 72, 6, "#7A6FCB"),
    (40, 72, 6, "#7A6FCB"),
    (54, 78, 5, "#C9C1F4"),
]


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def font(sz, bold=True):
    for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/SFNSRounded.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()


def draw_beads(d, ox, oy, scale):
    """Draw the tasbih ring; (ox,oy)=viewport origin on canvas, scale=px per viewport-unit."""
    for cx, cy, r, fill in BEADS:
        x, y, rr = ox + cx * scale, oy + cy * scale, r * scale
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=hx(fill) + (255,))


def icon_512():
    SS = 4
    W = 512 * SS
    img = Image.new("RGBA", (W, W), BG + (255,))
    d = ImageDraw.Draw(img)
    # map 108 viewport to full 512 square (matches launcher foreground framing)
    draw_beads(d, 0, 0, W / 108)
    img = img.resize((512, 512), Image.LANCZOS)
    p = os.path.join(OUT, "store-icon-512.png")
    img.convert("RGB").save(p)
    print("wrote", os.path.relpath(p, ROOT), img.size)


def feature_1024x500():
    SS = 2
    W, H = 1024 * SS, 500 * SS
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    # diagonal indigo→purple gradient (hero family)
    top, bot = (18, 20, 40), (46, 26, 66)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)) + (255,))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([W - 720 * SS, -160 * SS, W + 160 * SS, 360 * SS], fill=(145, 132, 217, 70))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120 * SS)))

    def px(v): return v * SS

    # LOGO tile on the far left (looks like the app icon), then two name+subtitle blocks
    tx, ty, ts = px(60), px(100), px(300)
    d.rounded_rectangle([tx, ty, tx + ts, ty + ts], radius=px(60), fill=BG + (255,))
    draw_beads(d, tx, ty, ts / 108)

    xtext = px(410)
    fname, fsub = font(px(78)), font(px(34), bold=False)
    white, purple = (255, 255, 255, 255), (179, 169, 236, 255)

    def block(name, sub, y):
        d.text((xtext + 2, y + 3), name, font=fname, fill=(0, 0, 0, 150))
        d.text((xtext, y), name, font=fname, fill=white)
        d.text((xtext + 2, y + px(92)), sub, font=fsub, fill=purple)

    block("Zikirci", "Reklamsız zikirmatik", px(96))
    block("Dhikrer", "Ad-free dhikr counter", px(276))

    img = img.resize((1024, 500), Image.LANCZOS)
    p = os.path.join(OUT, "feature-graphic-1024x500.png")
    img.convert("RGB").save(p)
    print("wrote", os.path.relpath(p, ROOT), img.size)


if __name__ == "__main__":
    icon_512()
    feature_1024x500()

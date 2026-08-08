#!/usr/bin/env python3
"""Wrap each app screenshot in a clean modern Android phone frame (with visible
volume + power side buttons). Output: store-screenshots/framed/<name>.png (alpha)."""
import os, sys, glob
from PIL import Image, ImageDraw, ImageFilter

SRC = "store-screenshots"
OUT = os.path.join(SRC, "framed")
os.makedirs(OUT, exist_ok=True)

BEZEL = 26          # black border around the screen
RIM = 8             # metal rim outside the bezel
SCREEN_RAD = 70     # screen corner radius
BODY_RAD = 96       # phone body corner radius
BTN_W = 12          # side button thickness (protrusion)
SHADOW = 60         # drop shadow blur/margin

BODY = (17, 19, 24, 255)      # phone body (near-black)
RIM_COL = (46, 49, 60, 255)   # subtle metal rim
BTN_COL = (32, 35, 44, 255)   # side buttons
BTN_HI = (70, 74, 86, 255)    # button highlight edge
HOLE = (6, 7, 10, 255)        # punch-hole camera


def rr_mask(size, rad):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], rad, fill=255)
    return m


def frame(path):
    shot = Image.open(path).convert("RGBA")
    sw, sh = shot.size
    # inner (screen) box within the body
    bx0 = SHADOW + BTN_W + RIM + BEZEL
    by0 = SHADOW + RIM + BEZEL
    body_w = sw + 2 * (BEZEL + RIM)
    body_h = sh + 2 * (BEZEL + RIM)
    W = body_w + 2 * (SHADOW + BTN_W)
    H = body_h + 2 * SHADOW
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # drop shadow
    sh_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh_layer)
    sd.rounded_rectangle([SHADOW + BTN_W, SHADOW, SHADOW + BTN_W + body_w, SHADOW + body_h],
                         BODY_RAD, fill=(0, 0, 0, 150))
    sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(SHADOW / 2.4))
    canvas.alpha_composite(sh_layer)

    d = ImageDraw.Draw(canvas)
    bxL = SHADOW + BTN_W
    byT = SHADOW
    # side buttons (left: volume rocker — the app's signature; right: power)
    vol_x0 = bxL - BTN_W + 2
    vol_top = byT + int(body_h * 0.26)
    for seg in range(2):  # volume up / down rocker (two pills)
        y0 = vol_top + seg * int(body_h * 0.11)
        y1 = y0 + int(body_h * 0.085)
        d.rounded_rectangle([vol_x0, y0, bxL + 4, y1], 6, fill=BTN_COL)
        d.rounded_rectangle([vol_x0, y0, vol_x0 + 3, y1], 6, fill=BTN_HI)
    pwr_x1 = bxL + body_w + BTN_W - 2
    pwr_y0 = byT + int(body_h * 0.30)
    d.rounded_rectangle([bxL + body_w - 4, pwr_y0, pwr_x1, pwr_y0 + int(body_h * 0.09)], 6, fill=BTN_COL)

    # metal rim + body
    d.rounded_rectangle([bxL, byT, bxL + body_w, byT + body_h], BODY_RAD, fill=RIM_COL)
    d.rounded_rectangle([bxL + RIM, byT + RIM, bxL + body_w - RIM, byT + body_h - RIM],
                        BODY_RAD - RIM, fill=BODY)

    # screen
    scr_x = bxL + RIM + BEZEL
    scr_y = byT + RIM + BEZEL
    canvas.paste(shot, (scr_x, scr_y), rr_mask((sw, sh), SCREEN_RAD))

    # punch-hole camera (top center of screen)
    r = 13
    cx = scr_x + sw // 2
    cy = scr_y + 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=HOLE)
    d.ellipse([cx - r + 3, cy - r + 3, cx + r - 3, cy + r - 3], outline=(40, 44, 70, 255), width=2)

    canvas.save(os.path.join(OUT, os.path.basename(path)))


def main():
    files = sorted(glob.glob(os.path.join(SRC, "*.png")))
    for f in files:
        frame(f)
        print("  framed", os.path.basename(f))
    print("done →", OUT)


if __name__ == "__main__":
    main()

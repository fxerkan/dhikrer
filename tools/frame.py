#!/usr/bin/env python3
"""Wrap each app screenshot in a clean modern phone frame. Runs per language and
per PLATFORM: reads store/<platform>/<lang>/_raw/*.png, writes .../framed/*.png (alpha).

  python3 tools/frame.py            # PLATFORM=android → Android frame (punch-hole, volume rocker)
  PLATFORM=ios python3 tools/frame.py   # iPhone frame (Dynamic Island, thin uniform bezel)
"""
import os, glob
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ["tr", "en", "ar"]
PLATFORM = os.environ.get("PLATFORM", "android")


def _font(sz):
    for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/SFNSRounded.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

SHADOW = 60          # drop shadow blur/margin (shared)


def rr_mask(size, rad):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], rad, fill=255)
    return m


def frame_android(shot):
    BEZEL, RIM, BTN_W = 26, 8, 12
    SCREEN_RAD, BODY_RAD = 70, 96
    BODY = (17, 19, 24, 255); RIM_COL = (46, 49, 60, 255)
    BTN_COL = (32, 35, 44, 255); BTN_HI = (70, 74, 86, 255); HOLE = (6, 7, 10, 255)
    sw, sh = shot.size
    body_w = sw + 2 * (BEZEL + RIM)
    body_h = sh + 2 * (BEZEL + RIM)
    W = body_w + 2 * (SHADOW + BTN_W)
    H = body_h + 2 * SHADOW
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    sh_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh_layer).rounded_rectangle(
        [SHADOW + BTN_W, SHADOW, SHADOW + BTN_W + body_w, SHADOW + body_h], BODY_RAD, fill=(0, 0, 0, 150))
    canvas.alpha_composite(sh_layer.filter(ImageFilter.GaussianBlur(SHADOW / 2.4)))

    d = ImageDraw.Draw(canvas)
    bxL, byT = SHADOW + BTN_W, SHADOW
    # side buttons (left: volume rocker — the app's signature; right: power)
    vol_x0 = bxL - BTN_W + 2
    vol_top = byT + int(body_h * 0.26)
    for seg in range(2):
        y0 = vol_top + seg * int(body_h * 0.11)
        y1 = y0 + int(body_h * 0.085)
        d.rounded_rectangle([vol_x0, y0, bxL + 4, y1], 6, fill=BTN_COL)
        d.rounded_rectangle([vol_x0, y0, vol_x0 + 3, y1], 6, fill=BTN_HI)
    pwr_x1 = bxL + body_w + BTN_W - 2
    pwr_y0 = byT + int(body_h * 0.30)
    d.rounded_rectangle([bxL + body_w - 4, pwr_y0, pwr_x1, pwr_y0 + int(body_h * 0.09)], 6, fill=BTN_COL)

    d.rounded_rectangle([bxL, byT, bxL + body_w, byT + body_h], BODY_RAD, fill=RIM_COL)
    d.rounded_rectangle([bxL + RIM, byT + RIM, bxL + body_w - RIM, byT + body_h - RIM], BODY_RAD - RIM, fill=BODY)

    scr_x, scr_y = bxL + RIM + BEZEL, byT + RIM + BEZEL
    canvas.paste(shot, (scr_x, scr_y), rr_mask((sw, sh), SCREEN_RAD))

    r, cx, cy = 13, scr_x + sw // 2, scr_y + 26  # punch-hole camera
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=HOLE)
    d.ellipse([cx - r + 3, cy - r + 3, cx + r - 3, cy + r - 3], outline=(40, 44, 70, 255), width=2)
    return canvas


def _avg_top(shot):
    """Average colour of the screenshot's top edge — used to blend the added iOS
    status-bar strip into the app's own header so it reads as one continuous screen."""
    row = shot.convert("RGB").crop((0, 0, shot.width, 6)).resize((1, 1), Image.LANCZOS)
    return row.getpixel((0, 0))


def _status_bar(d, x0, y0, sw, strip_h, bg):
    """Draw an iOS status bar (time left · signal/wifi/battery right) in a colour
    that contrasts the sampled strip bg (works on both light and dark themes)."""
    lum = 0.299 * bg[0] + 0.587 * bg[1] + 0.114 * bg[2]
    fg = (235, 235, 238) if lum < 130 else (20, 20, 22)
    cy = y0 + strip_h * 0.54
    # time (Apple's canonical 9:41)
    f = _font(int(strip_h * 0.30))
    d.text((x0 + sw * 0.085, cy), "9:41", font=f, fill=fg + (255,), anchor="lm")
    xr = x0 + sw * 0.915                       # right edge, glyphs laid right→left
    # battery: rounded body + terminal nub + inner fill
    bw, bh = strip_h * 0.50, strip_h * 0.24
    bx1, by0 = xr, cy - bh / 2
    d.rounded_rectangle([bx1 - bw, by0, bx1, by0 + bh], bh * 0.32, outline=fg + (170,), width=max(2, int(strip_h * 0.02)))
    nub_w = bh * 0.16
    d.rounded_rectangle([bx1 + 1, cy - bh * 0.22, bx1 + 1 + nub_w, cy + bh * 0.22], nub_w * 0.5, fill=fg + (170,))
    pad = bh * 0.14
    d.rounded_rectangle([bx1 - bw + pad, by0 + pad, bx1 - pad, by0 + bh - pad], bh * 0.16, fill=fg + (255,))
    # wifi: an upward fan (pieslice) left of the battery
    gap = sw * 0.028
    wr = strip_h * 0.30
    wcx = bx1 - bw - gap - wr
    wcy = cy + wr * 0.55
    d.pieslice([wcx - wr, wcy - wr, wcx + wr, wcy + wr], 230, 310, fill=fg + (255,))
    # cellular: four ascending dots left of the wifi
    dr = strip_h * 0.05
    dx = wcx - wr - gap
    for i in range(4):
        cxi = dx - i * dr * 3
        d.ellipse([cxi - dr, cy - dr, cxi + dr, cy + dr], fill=fg + (210,))


def frame_ios(shot):
    """Realistic modern iPhone: dark titanium rail with a polished outer edge, very
    round corners, an iOS status bar + Dynamic Island. The status bar lives in a strip
    added ABOVE the screenshot (filled with the app's own top colour) so it never
    overlaps the app content — mirroring the safe-area a real device would give."""
    BEZEL, RIM, EDGE, BTN_W = 16, 9, 4, 9
    SCREEN_RAD, BODY_RAD = 118, 152
    BODY = (13, 14, 16, 255)          # black bezel under the glass
    RAIL = (46, 48, 54, 255)          # graphite/black titanium rail
    EDGE_HI = (128, 131, 140, 255)    # polished chamfer highlight
    BTN = (30, 31, 35, 255); BTN_HI = (96, 99, 108, 255); ISLAND = (0, 0, 0, 255)
    sw, sh = shot.size

    # Build the on-glass "screen" = status-bar strip (blended) + the real screenshot.
    strip_h = int(sw * 0.105)
    bg = _avg_top(shot)
    screen = Image.new("RGBA", (sw, strip_h + sh), bg + (255,))
    screen.paste(shot, (0, strip_h))
    sd = ImageDraw.Draw(screen)
    _status_bar(sd, 0, 0, sw, strip_h, bg)
    iw, ih = int(sw * 0.30), int(strip_h * 0.46)          # Dynamic Island
    ix = (sw - iw) // 2
    iy = int(strip_h * 0.30)
    sd.rounded_rectangle([ix, iy, ix + iw, iy + ih], ih // 2, fill=ISLAND)
    sw2, sh2 = screen.size

    body_w = sw2 + 2 * (BEZEL + RIM)
    body_h = sh2 + 2 * (BEZEL + RIM)
    W = body_w + 2 * (SHADOW + BTN_W)
    H = body_h + 2 * SHADOW
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    sh_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh_layer).rounded_rectangle(
        [SHADOW + BTN_W, SHADOW, SHADOW + BTN_W + body_w, SHADOW + body_h], BODY_RAD, fill=(0, 0, 0, 160))
    canvas.alpha_composite(sh_layer.filter(ImageFilter.GaussianBlur(SHADOW / 2.4)))

    d = ImageDraw.Draw(canvas)
    bxL, byT = SHADOW + BTN_W, SHADOW
    # subtle side buttons flush with the rail (left: action + volume↑ + volume↓; right: side)
    lx0 = bxL - BTN_W + 3
    for y_frac, h_frac in [(0.155, 0.045), (0.255, 0.085), (0.360, 0.085)]:
        y0 = byT + int(body_h * y_frac); y1 = y0 + int(body_h * h_frac)
        d.rounded_rectangle([lx0, y0, bxL + 5, y1], 5, fill=BTN)
        d.line([(lx0 + 1, y0 + 3), (lx0 + 1, y1 - 3)], fill=BTN_HI, width=2)
    rx1 = bxL + body_w + BTN_W - 3
    sb_y0 = byT + int(body_h * 0.285); sb_y1 = sb_y0 + int(body_h * 0.135)
    d.rounded_rectangle([bxL + body_w - 5, sb_y0, rx1, sb_y1], 5, fill=BTN)
    d.line([(rx1 - 1, sb_y0 + 3), (rx1 - 1, sb_y1 - 3)], fill=BTN_HI, width=2)

    # polished outer edge → titanium rail → black bezel → screen
    d.rounded_rectangle([bxL, byT, bxL + body_w, byT + body_h], BODY_RAD, fill=EDGE_HI)
    d.rounded_rectangle([bxL + EDGE, byT + EDGE, bxL + body_w - EDGE, byT + body_h - EDGE], BODY_RAD - EDGE, fill=RAIL)
    d.rounded_rectangle([bxL + RIM, byT + RIM, bxL + body_w - RIM, byT + body_h - RIM], BODY_RAD - RIM, fill=BODY)

    scr_x, scr_y = bxL + RIM + BEZEL, byT + RIM + BEZEL
    canvas.paste(screen, (scr_x, scr_y), rr_mask((sw2, sh2), SCREEN_RAD))
    return canvas


FRAMERS = {"android": frame_android, "ios": frame_ios}


def main():
    framer = FRAMERS.get(PLATFORM, frame_android)
    for lang in LANGS:
        src = os.path.join(ROOT, "store", PLATFORM, lang, "_raw")
        out = os.path.join(ROOT, "store", PLATFORM, lang, "framed")
        if not os.path.isdir(src):
            continue
        os.makedirs(out, exist_ok=True)
        for f in sorted(glob.glob(os.path.join(src, "*.png"))):
            framer(Image.open(f).convert("RGBA")).save(os.path.join(out, os.path.basename(f)))
            print(f"  framed {PLATFORM}/{lang}/{os.path.basename(f)}")
    print("done →", os.path.join(ROOT, "store", PLATFORM, "<lang>", "framed"))


if __name__ == "__main__":
    main()

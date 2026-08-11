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

    def px(v): return int(v * SS)

    # clean diagonal gradient, lighter top-left → deep purple bottom-right (no diamond artifact)
    tl, br = (60, 54, 96), (24, 20, 44)
    lut = [tuple(int(tl[i] + (br[i] - tl[i]) * (v / 255)) for i in range(3)) for v in range(256)]
    xr = [x / (W - 1) for x in range(W)]
    rgb = Image.new("RGB", (W, H))
    rgb.putdata([lut[int((xf + yf) * 0.5 * 255)]
                 for yf in (y / (H - 1) for y in range(H)) for xf in xr])
    img = rgb.convert("RGBA")
    d = ImageDraw.Draw(img)

    # LOGO tile on the far left + a soft light halo behind it so the dark tile stands out
    ts = px(240)
    tx, ty = px(60), (H - ts) // 2
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([tx - px(80), ty - px(80), tx + ts + px(80), ty + ts + px(80)],
                                 fill=(150, 138, 214, 120))
    img.alpha_composite(halo.filter(ImageFilter.GaussianBlur(px(70))))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([tx, ty, tx + ts, ty + ts], radius=px(52), fill=BG + (255,))
    draw_beads(d, tx, ty, ts / 108)

    # text: title (with "er" of Dhikrer in a soft, slightly different tone) + TR + EN subtitles
    xtext, avail = px(350), W - px(350) - px(48)
    white = (245, 245, 250, 255)
    soft = (206, 198, 232, 255)   # subtle tone for "er"
    sub_c = (183, 169, 236, 255)
    sub_en = (150, 150, 180, 255)
    slog_c = (201, 193, 244, 255)  # tasbih C9C1F4 accent for the slogan
    TR = "Reklamsız, dikkat dağıtmayan, özelleştirilebilir zikirmatik."
    EN = "Ad-free, Distraction-free, Customizable Dhikr counter"
    SLOGAN = "You focus on the dhikr, let Dhikrer handle the counting."

    def fit(text, start, lo=16):
        for s in range(start, lo - 1, -1):
            f = font(px(s), bold=False)
            if d.textlength(text, font=f) <= avail:
                return f
        return font(px(lo), bold=False)

    ftitle = font(px(64))
    fs = fit(max([TR, EN], key=len), 32)
    fslog = fit(SLOGAN, 30)

    # title segments so "er" gets the soft tone
    y = px(120)
    x = xtext
    for seg, col in [("Zikirci (Dhikr", white), ("er", soft), (")", white)]:
        d.text((x + 2, y + 3), seg, font=ftitle, fill=(0, 0, 0, 150))
        d.text((x, y), seg, font=ftitle, fill=col)
        x += d.textlength(seg, font=ftitle)

    d.text((xtext, px(232)), TR, font=fs, fill=sub_c)
    d.text((xtext, px(290)), EN, font=fs, fill=sub_en)
    d.text((xtext, px(372)), SLOGAN, font=fslog, fill=slog_c)

    img = img.resize((1024, 500), Image.LANCZOS)
    p = os.path.join(OUT, "feature-graphic-1024x500.png")
    img.convert("RGB").save(p)
    print("wrote", os.path.relpath(p, ROOT), img.size)


if __name__ == "__main__":
    icon_512()
    feature_1024x500()

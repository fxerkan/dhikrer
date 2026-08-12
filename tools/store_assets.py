#!/usr/bin/env python3
"""Play Store brand assets from the REAL app icon vector — no new art, no hands.
Renders (4x/2x supersampled → downscaled for crisp edges):
  store/store-icon-512.png                    512x512  hi-res listing icon (shared)
  store/<lang>/feature-graphic-1024x500.png   per-language feature graphic
Each feature graphic shows: the tasbih logo tile, the localized product name
(Zikirci./Dhikrer./الذّاكِر.), a title line and the slogan as subtitle. Arabic
lays out RTL (logo right, text right-aligned).
Source of truth = android/.../ic_launcher_foreground.xml (tasbih beads) + colors.xml bg.
Run:  python3 tools/store_assets.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "store")
BG = (0x16, 0x18, 0x26)               # ic_launcher_background #161826
LANGS = ["tr", "en", "ar"]

# Product name (brand), title line, and slogan (shown as subtitle) — per language.
BRAND = {"tr": "Zikirci", "en": "Dhikrer", "ar": "الذّاكِر"}
# Brand rule: names ending in "er" (Dhikrer) always render the "er" in a distinct
# accent tone wherever the product name appears. (base, "er") per such language.
BRAND_HI = {"en": ("Dhikr", "er")}
TITLE = {
    "tr": "Reklamsız, dikkat dağıtmayan, özelleştirilebilir zikirmatik.",
    "en": "Ad-free, distraction-free, customizable dhikr counter.",
    "ar": "عدّاد ذِكر بلا إعلانات، بلا تشتيت، وقابل للتخصيص.",
}
SLOGAN = {
    "tr": "Sen zikrine odaklan, saymayı Zikirci'ye bırak.",
    "en": "You focus on the dhikr, let Dhikrer handle the counting.",
    "ar": "ركّز على ذِكرك، ودَع الذّاكِر يتكفّل بالعدّ.",
}

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


def font(sz, lang="en", bold=True):
    if lang == "ar":
        cands = ["/System/Library/Fonts/SFArabic.ttf",
                 "/System/Library/Fonts/Supplemental/Damascus.ttc"]
    else:
        cands = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
                 "/System/Library/Fonts/SFNSRounded.ttf"]
    for p in cands:
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


def feature_1024x500(lang):
    SS = 2
    W, H = 1024 * SS, 500 * SS
    rtl = lang == "ar"

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

    # LOGO tile (far left LTR / far right RTL) + a soft light halo behind it
    ts = px(240)
    tx = (W - px(60) - ts) if rtl else px(60)
    ty = (H - ts) // 2
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([tx - px(80), ty - px(80), tx + ts + px(80), ty + ts + px(80)],
                                 fill=(150, 138, 214, 120))
    img.alpha_composite(halo.filter(ImageFilter.GaussianBlur(px(70))))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([tx, ty, tx + ts, ty + ts], radius=px(52), fill=BG + (255,))
    draw_beads(d, tx, ty, ts / 108)

    # text column: product name (brand + accent dot) → title → slogan
    white = (245, 245, 250, 255)
    accent = (183, 169, 236, 255)   # tasbih accent-hi for the brand dot
    sub_c = (183, 169, 236, 255)
    slog_c = (201, 193, 244, 255)   # tasbih C9C1F4 accent for the slogan
    avail = W - px(350) - px(48)
    xtext = px(350)                 # LTR: left edge of text
    xright = W - px(350)            # RTL: right edge of text
    dkw = {"direction": "rtl"} if rtl else {}

    def fit(text, start, lo=16):
        for s in range(start, lo - 1, -1):
            f = font(px(s), lang, bold=False)
            if d.textlength(text, font=f, **dkw) <= avail:
                return f
        return font(px(lo), lang, bold=False)

    def line_rtl(y, text, fnt, fill):
        d.text((xright + 2, y + 3), text, font=fnt, fill=(0, 0, 0, 150), anchor="ra", **dkw)
        d.text((xright, y), text, font=fnt, fill=fill, anchor="ra", **dkw)

    def brand_segments(text, base_fill):
        """Split `text` into (segment, fill) parts so the product name's "er"
        suffix (e.g. Dhikrer) renders in the accent tone wherever it appears.
        Non-"er" names (Zikirci / الذّاكِر) pass straight through."""
        if lang not in BRAND_HI:
            return [(text, base_fill)]
        base, hi = BRAND_HI[lang]
        out = []
        for i, part in enumerate(text.split(base + hi)):
            if i:
                out += [(base, white), (hi, accent)]   # Dhikr (white) + er (accent)
            if part:
                out.append((part, base_fill))
        return out

    def draw_ltr(x, y, fnt, segments):
        for text, fill in segments:
            d.text((x + 2, y + 3), text, font=fnt, fill=(0, 0, 0, 150))
            d.text((x, y), text, font=fnt, fill=fill)
            x += d.textlength(text, font=fnt)

    # product name wordmark (brand + trailing "." accent), title, slogan.
    fbrand = font(px(76), lang)
    ftitle, fslog = fit(TITLE[lang], 34), fit(SLOGAN[lang], 32)
    brand = BRAND[lang]
    if rtl:
        line_rtl(px(112), brand, fbrand, white)
        bw = d.textlength(brand, font=fbrand, **dkw)
        d.text((xright - bw, px(112)), ".", font=fbrand, fill=accent, anchor="ra")  # dot left of RTL word
        line_rtl(px(268), TITLE[lang], ftitle, sub_c)
        line_rtl(px(348), SLOGAN[lang], fslog, slog_c)
    else:
        draw_ltr(xtext, px(112), fbrand, brand_segments(brand, white) + [(".", accent)])
        draw_ltr(xtext, px(268), ftitle, brand_segments(TITLE[lang], sub_c))
        draw_ltr(xtext, px(348), fslog, brand_segments(SLOGAN[lang], slog_c))

    img = img.resize((1024, 500), Image.LANCZOS)
    p = os.path.join(OUT, lang, "feature-graphic-1024x500.png")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    img.convert("RGB").save(p)
    print("wrote", os.path.relpath(p, ROOT), img.size)


if __name__ == "__main__":
    icon_512()
    for lang in LANGS:
        feature_1024x500(lang)

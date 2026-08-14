#!/usr/bin/env python3
"""Per-language feature hero set, PER PLATFORM. For each language it composites the
REAL framed screenshots (in that language) onto per-feature colored backgrounds with
a SINGLE-language headline (title + one subtitle). Screenshot text stays pixel-perfect
(real render) — nothing on-screen is redrawn.

  python3 tools/hero_set.py            # PLATFORM=android → 1562x3113 heroes (Play)
  PLATFORM=ios python3 tools/hero_set.py    # 1290x2796 heroes (App Store 6.9" iPhone)

Which features/text/colors belong to a platform is read from store/shared/copy.json
(single source of truth): android → volume-keys hero; ios → lock-mode hero instead
(iOS can't read hardware volume keys). No hands/fingers are ever drawn. The volume
callout highlights the phone's volume button with a glow ring + a "+1" bubble on the
real frame — never a drawn hand.

Inputs : store/<platform>/<lang>/framed/<screen>.png   (from shots.mjs → frame.py)
Outputs: store/<platform>/<lang>/hero-<slug>.png
"""
import json
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ["tr", "en", "ar"]
PLATFORM = os.environ.get("PLATFORM", "android")
COPY = json.load(open(os.path.join(ROOT, "store/shared/copy.json"), encoding="utf8"))

# App-store canvas per platform. iOS must be an EXACT App Store size — 1290x2796 is
# the 6.9" iPhone portrait size that covers every current iPhone.
CANVAS = {"android": (1562, 3113), "ios": (1290, 2796)}
W, H = CANVAS.get(PLATFORM, CANVAS["android"])

SHADOW = 60          # must match frame.py (used to locate the volume button)


def font(sz, lang="tr", bold=True):
    if lang == "ar":
        cands = ["/System/Library/Fonts/SFArabic.ttf",
                 "/System/Library/Fonts/Supplemental/Damascus.ttc",
                 "/Library/Fonts/Arial Unicode.ttf"]
    else:
        cands = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
                 "/System/Library/Fonts/SFNSRounded.ttf", "/Library/Fonts/Arial Bold.ttf"]
    for p in cands:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()


def gradient_bg(top, bot, accent):
    bg = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)) + (255,))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([W - 900, -300, W + 300, 700], fill=tuple(accent) + (60,))
    bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(180)))
    return bg


def place_phone(bg, framed_path):
    """Scale the framed phone to fit the lower portion of the canvas (leaving a
    headline band on top) and center it horizontally. Returns (x, y, scale) so the
    volume callout can be positioned in the same coordinate space."""
    ph = Image.open(framed_path).convert("RGBA")
    scale = min(H * 0.72 / ph.height, W * 0.86 / ph.width)
    pw, ph2 = int(ph.width * scale), int(ph.height * scale)
    x = (W - pw) // 2
    y = H - ph2 - int(H * 0.015)
    bg.alpha_composite(ph.resize((pw, ph2), Image.LANCZOS), (x, y))
    return x, y, scale, ph.height


def headline(bg, title, sub, accent_hi, lang):
    # Pillow is built with raqm here, so it shapes + bidi-reorders Arabic itself
    # from the raw logical string when given direction='rtl' — no pre-reshaping.
    d = ImageDraw.Draw(bg)
    rtl = lang == "ar"
    kw = {"direction": "rtl"} if rtl else {}
    f1, f2 = font(int(W * 0.072), lang), font(int(W * 0.039), lang, bold=False)
    margin = int(W * 0.059)
    tx = (W - margin) if rtl else margin
    anchor = ("r" if rtl else "l") + "a"
    y1, y2 = int(H * 0.048), int(H * 0.098)

    def shadow(y, text, fnt, fill):
        d.text((tx + 3, y + 4), text, font=fnt, fill=(0, 0, 0, 130), anchor=anchor, **kw)
        d.text((tx, y), text, font=fnt, fill=fill, anchor=anchor, **kw)

    shadow(y1, title, f1, (255, 255, 255, 255))
    shadow(y2, sub, f2, tuple(accent_hi) + (255,))


def volume_callout(bg, px, py, scale, fh, accent, accent_hi):
    """Glow ring + '+1' bubble on the phone's left volume button. Button center in
    framed space ≈ (SHADOW + a bit, SHADOW + body_h*0.33); mapped into canvas via
    the placement (px,py,scale)."""
    d = ImageDraw.Draw(bg)
    body_h = fh - 2 * SHADOW
    vb_x = int((SHADOW + 8) * scale) + px
    vb_y = int((SHADOW + body_h * 0.33) * scale) + py
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([vb_x - 150, vb_y - 150, vb_x + 150, vb_y + 150], fill=tuple(accent) + (120,))
    bg.alpha_composite(ring.filter(ImageFilter.GaussianBlur(60)))
    d.ellipse([vb_x - 62, vb_y - 62, vb_x + 62, vb_y + 62], outline=tuple(accent_hi), width=8)
    bx0, by0, bx1, by1 = vb_x - 300, vb_y - 70, vb_x - 96, vb_y + 70
    d.rounded_rectangle([bx0, by0, bx1, by1], 40, fill=tuple(accent) + (255,))
    d.polygon([(bx1, vb_y - 26), (bx1 + 34, vb_y), (bx1, vb_y + 26)], fill=tuple(accent))
    f = font(96)
    tw = d.textlength("+1", font=f)
    d.text(((bx0 + bx1) / 2 - tw / 2, vb_y - 56), "+1", font=f, fill=(255, 255, 255, 255))


def main():
    heroes = [(slug, h) for slug, h in COPY["heroes"].items() if PLATFORM in h["platforms"]]
    for lang in LANGS:
        framed_dir = os.path.join(ROOT, "store", PLATFORM, lang, "framed")
        out_dir = os.path.join(ROOT, "store", PLATFORM, lang)
        if not os.path.isdir(framed_dir):
            print("skip", lang, "(no framed dir)"); continue
        for slug, h in heroes:
            # A hero may PIN its screenshot to a fixed language (e.g. the "languages"
            # hero always shows the Arabic RTL screen, whatever the headline language),
            # while the headline still follows the current `lang`.
            slang = h.get("screen_lang", lang)
            framed = os.path.join(ROOT, "store", PLATFORM, slang, "framed", h["screen"] + ".png")
            if not os.path.exists(framed):
                print("  MISSING", os.path.relpath(framed, ROOT)); continue
            title, sub = h["text"][lang]
            bg = gradient_bg(h["bg_top"], h["bg_bot"], h["accent"])
            px, py, scale, fh = place_phone(bg, framed)
            if h.get("callout"):
                volume_callout(bg, px, py, scale, fh, h["accent"], h["accent_hi"])
            headline(bg, title, sub, h["accent_hi"], lang)
            out = os.path.join(out_dir, f"hero-{slug}.png")
            bg.convert("RGB").save(out, quality=95)
            print("wrote", os.path.relpath(out, ROOT), bg.size)


if __name__ == "__main__":
    main()

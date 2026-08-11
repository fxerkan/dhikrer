#!/usr/bin/env python3
"""Feature hero set for the Play listing. Composites the REAL framed Zikirci
screenshots onto per-feature colored backgrounds with a headline. Screenshot text
stays pixel-perfect (real render) — nothing on-screen is redrawn.

NOTE: no hands/fingers here. The volume-key "ghost hand" hero is generated with
Gemini nano banana (see tools/nano_banana.py) — never drawn locally.

Outputs (store-screenshots/hero-<slug>-v1.png, 1562x3113, portrait):
  ad-free, customize, easy, stats, languages
Run from anywhere:  python3 tools/hero_set.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "store", "store-screenshots")
FRAMED = os.path.join(SRC, "framed")

W, H = 1562, 3113
S = 0.88            # phone scale
PX, PY = 240, 470   # phone top-left on canvas


def font(sz, bold=True):
    for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/SFNSRounded.ttf", "/Library/Fonts/Arial Bold.ttf"]:
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
    ImageDraw.Draw(glow).ellipse([W - 900, -300, W + 300, 700], fill=accent + (60,))
    bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(180)))
    return bg


def place_phone(bg, framed_name):
    ph = Image.open(os.path.join(FRAMED, framed_name)).convert("RGBA")
    pw, ph2 = int(ph.width * S), int(ph.height * S)
    bg.alpha_composite(ph.resize((pw, ph2), Image.LANCZOS), (PX, PY))


def headline(bg, title, sub_tr, sub_en, accent_hi):
    d = ImageDraw.Draw(bg)
    f1, f2, f3 = font(112), font(60, bold=False), font(52, bold=False)

    def shadow(xy, text, fnt, fill):
        d.text((xy[0] + 3, xy[1] + 4), text, font=fnt, fill=(0, 0, 0, 130))
        d.text(xy, text, font=fnt, fill=fill)

    shadow((90, 150), title, f1, (255, 255, 255, 255))
    shadow((92, 292), sub_tr, f2, accent_hi + (255,))
    shadow((92, 372), sub_en, f3, (168, 170, 190, 255))


# slug, framed screen, bg top, bg bottom, accent, accent-hi, title(TR), sub(TR), sub(EN)
SPECS = [
    ("ad-free", "02-tespih-zumrut-v1.png", (10, 34, 28), (10, 52, 40), (46, 200, 150), (150, 235, 205),
     "Reklamsız. Çevrimdışı.", "Reklam yok, takip yok — her şey cihazında.",
     "No ads, no tracking — everything on your device."),
    ("customize", "08-ayarlar-lavanta-v1.png", (40, 22, 52), (62, 26, 66), (214, 140, 214), (238, 190, 236),
     "Tasarımı sana göre", "10 tema, sayaç şekilleri ve düzenler.",
     "10 themes, counter shapes & layouts."),
    ("easy", "03-birlesik-gul-v1.png", (46, 30, 20), (62, 40, 22), (240, 176, 92), (250, 214, 160),
     "Sade, kullanımı kolay", "Tek dokunuşla say — dağıtan hiçbir şey yok.",
     "One tap to count — zero clutter."),
    ("stats", "07-istatistik-okyanus-v1.png", (10, 30, 44), (12, 46, 60), (86, 182, 216), (168, 224, 244),
     "İlerlemeni izle", "Isı haritası, günlük ve haftalık istatistik.",
     "Heatmap, daily & weekly stats."),
    ("languages", "10-arapca-rtl-gece-v1.png", (24, 26, 38), (30, 36, 52), (150, 164, 192), (206, 214, 232),
     "Kendi dilinde zikret", "Çoklu dil ve tam sağdan-sola (RTL) desteği.",
     "Multi-language with full RTL support."),
]


def main():
    for slug, screen, top, bot, accent, accent_hi, title, sub_tr, sub_en in SPECS:
        bg = gradient_bg(top, bot, accent)
        place_phone(bg, screen)
        headline(bg, title, sub_tr, sub_en, accent_hi)
        out = os.path.join(SRC, f"hero-{slug}-v1.png")
        bg.convert("RGB").save(out, quality=95)
        print("wrote", os.path.relpath(out, ROOT), bg.size)


if __name__ == "__main__":
    main()

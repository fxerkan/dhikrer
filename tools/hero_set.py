#!/usr/bin/env python3
"""Per-language feature hero set for the Play listing. For each of tr/en/ar it
composites the REAL framed screenshots (in that language) onto per-feature
colored backgrounds with a SINGLE-language headline (title + one subtitle).
Screenshot text stays pixel-perfect (real render) — nothing on-screen is redrawn.

NOTE: no hands/fingers. The "count with the volume keys" hero highlights the
phone's volume button with a glow ring + a "+1" bubble drawn on the real frame —
never a drawn hand. (The Gemini nano-banana ghost-hand promo, if wanted, is
language-neutral and lives in tools/nano_banana.py.)

Inputs : store/<lang>/framed/<screen>.png   (from shots.mjs → frame.py)
Outputs: store/<lang>/hero-<slug>.png  (1562x3113, portrait)
Run:  python3 tools/hero_set.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ["tr", "en", "ar"]

W, H = 1562, 3113
S = 0.88            # phone scale
PX, PY = 240, 470   # phone top-left on canvas


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
    ImageDraw.Draw(glow).ellipse([W - 900, -300, W + 300, 700], fill=accent + (60,))
    bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(180)))
    return bg


def place_phone(bg, framed_path):
    ph = Image.open(framed_path).convert("RGBA")
    pw, ph2 = int(ph.width * S), int(ph.height * S)
    bg.alpha_composite(ph.resize((pw, ph2), Image.LANCZOS), (PX, PY))


def headline(bg, title, sub, accent_hi, lang):
    # Pillow is built with raqm here, so it shapes + bidi-reorders Arabic itself
    # from the raw logical string when given direction='rtl' — no pre-reshaping.
    d = ImageDraw.Draw(bg)
    rtl = lang == "ar"
    kw = {"direction": "rtl"} if rtl else {}
    f1, f2 = font(112, lang), font(60, lang, bold=False)
    tx = (W - 92) if rtl else 92
    anchor = ("r" if rtl else "l") + "a"

    def shadow(y, text, fnt, fill):
        d.text((tx + 3, y + 4), text, font=fnt, fill=(0, 0, 0, 130), anchor=anchor, **kw)
        d.text((tx, y), text, font=fnt, fill=fill, anchor=anchor, **kw)

    shadow(150, title, f1, (255, 255, 255, 255))
    shadow(304, sub, f2, accent_hi + (255,))


def volume_callout(bg, accent, accent_hi):
    """Glow ring around the phone's (left) volume button + a '+1' bubble. Coords
    from frame.py geometry (original framed space) scaled by S and offset by PX/PY."""
    d = ImageDraw.Draw(bg)
    vb_x = int(68 * S) + PX
    vb_y = int(965 * S) + PY
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([vb_x - 150, vb_y - 150, vb_x + 150, vb_y + 150], fill=accent + (120,))
    bg.alpha_composite(ring.filter(ImageFilter.GaussianBlur(60)))
    d.ellipse([vb_x - 62, vb_y - 62, vb_x + 62, vb_y + 62], outline=accent_hi, width=8)
    bx0, by0, bx1, by1 = vb_x - 300, vb_y - 70, vb_x - 96, vb_y + 70
    d.rounded_rectangle([bx0, by0, bx1, by1], 40, fill=accent + (255,))
    d.polygon([(bx1, vb_y - 26), (bx1 + 34, vb_y), (bx1, vb_y + 26)], fill=accent)
    f = font(96)
    tw = d.textlength("+1", font=f)
    d.text(((bx0 + bx1) / 2 - tw / 2, vb_y - 56), "+1", font=f, fill=(255, 255, 255, 255))


# slug, framed screen, bg-top, bg-bottom, accent, accent-hi, callout?, {lang:(title,sub)}
SPECS = [
    ("volume", "01-sayac-klasik-gece", (22, 24, 38), (38, 28, 62), (145, 132, 217), (183, 169, 236), True, {
        "tr": ("Ses tuşlarıyla say", "Ekran kapalıyken bile zikrine devam et."),
        "en": ("Count with volume keys", "Keep your dhikr going — even with the screen off."),
        "ar": ("عُدّ بأزرار الصوت", "تابع ذكرك حتى والشاشة مغلقة."),
    }),
    ("ad-free", "02-tespih-zumrut", (10, 34, 28), (10, 52, 40), (46, 200, 150), (150, 235, 205), False, {
        "tr": ("Reklamsız. Çevrimdışı.", "Reklam yok, takip yok — her şey cihazında."),
        "en": ("Ad-free. Offline.", "No ads, no tracking — everything on your device."),
        "ar": ("بلا إعلانات. دون اتصال.", "لا إعلانات ولا تتبّع — كل شيء على جهازك."),
    }),
    ("customize", "08-ayarlar-lavanta", (40, 22, 52), (62, 26, 66), (214, 140, 214), (238, 190, 236), False, {
        "tr": ("Tasarımı sana göre", "10+ tema, 30+ şekil ve özelleştirilebilir sayaç."),
        "en": ("Made your way", "10+ themes, 30+ shapes & a customizable counter."),
        "ar": ("بتصميم يناسبك", "10+ سمة و30+ شكل وعدّاد قابل للتخصيص."),
    }),
    ("easy", "03-birlesik-gul", (46, 30, 20), (62, 40, 22), (240, 176, 92), (250, 214, 160), False, {
        "tr": ("Sade, kullanımı kolay", "Dikkat dağıtan öğeler olmadan — tek dokunuşla say."),
        "en": ("Simple & easy to use", "Count with one tap — no distractions."),
        "ar": ("بسيط وسهل الاستخدام", "عُدّ بلمسة واحدة — دون أي تشتيت."),
    }),
    ("stats", "07-istatistik-okyanus", (10, 30, 44), (12, 46, 60), (86, 182, 216), (168, 224, 244), False, {
        "tr": ("İlerlemeni izle", "Isı haritası, günlük ve haftalık istatistik."),
        "en": ("Track your progress", "Heatmap, daily & weekly stats."),
        "ar": ("تابع تقدّمك", "خريطة حرارية وإحصاءات يومية وأسبوعية."),
    }),
    ("languages", "06-zikirler-gece", (24, 26, 38), (30, 36, 52), (150, 164, 192), (206, 214, 232), False, {
        "tr": ("Kendi dilinde zikret", "Çoklu dil ve tam sağdan-sola (RTL) desteği."),
        "en": ("Dhikr in your language", "Multi-language with full RTL support."),
        "ar": ("اذكر بلغتك", "لغات متعددة ودعم كامل للكتابة من اليمين لليسار."),
    }),
]


def main():
    for lang in LANGS:
        framed_dir = os.path.join(ROOT, "store", lang, "framed")
        out_dir = os.path.join(ROOT, "store", lang)
        if not os.path.isdir(framed_dir):
            print("skip", lang, "(no framed dir)"); continue
        for slug, screen, top, bot, accent, accent_hi, callout, txt in SPECS:
            framed = os.path.join(framed_dir, screen + ".png")
            if not os.path.exists(framed):
                print("  MISSING", os.path.relpath(framed, ROOT)); continue
            title, sub = txt[lang]
            bg = gradient_bg(top, bot, accent)
            place_phone(bg, framed)
            if callout:
                volume_callout(bg, accent, accent_hi)
            headline(bg, title, sub, accent_hi, lang)
            out = os.path.join(out_dir, f"hero-{slug}.png")
            bg.convert("RGB").save(out, quality=95)
            print("wrote", os.path.relpath(out, ROOT), bg.size)


if __name__ == "__main__":
    main()

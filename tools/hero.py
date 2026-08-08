#!/usr/bin/env python3
"""Feature hero graphic: the REAL Zikirci framed screen with the left volume
button highlighted + a '+1' callout, conveying 'count with the volume keys'.
Output: store-screenshots/hero-volume-keys-v1.png"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC = "store-screenshots"
framed = os.path.join(SRC, "framed", "01-sayac-klasik-gece-v1.png")

ACCENT = (145, 132, 217)       # nocturne accent
ACCENT_HI = (183, 169, 236)

def font(sz, bold=True):
    for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/SFNSRounded.ttf", "/Library/Fonts/Arial Bold.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

def main():
    ph = Image.open(framed).convert("RGBA")
    fw, fh = ph.size
    W, H = 1562, 3113
    # background: vertical gradient dark indigo -> deep purple
    bg = Image.new("RGBA", (W, H))
    top, bot = (22, 24, 38), (38, 28, 62)
    for y in range(H):
        t = y / H
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        ImageDraw.Draw(bg).line([(0, y), (W, y)], fill=(r, g, b, 255))
    # soft accent glow blob top-right
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([W - 900, -300, W + 300, 700], fill=ACCENT + (60,))
    bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(180)))

    # scale + place phone (right of center, leave left margin for callout)
    s = 0.88                       # larger phone -> nav / app name / theme toggle stay legible when the store shrinks the image
    pw, ph2 = int(fw * s), int(fh * s)
    phone = ph.resize((pw, ph2), Image.LANCZOS)
    px = 240                       # pinned: keeps room for the left '+1' callout; right bezel bleeds off-frame
    py = 470                       # pinned below the headline; bottom bezel bleeds off-frame (nav stays visible)
    # phone drop shadow already baked; place it
    bg.alpha_composite(phone, (px, py))

    d = ImageDraw.Draw(bg)
    # volume-button center (from frame.py geometry, original framed coords, scaled)
    vb_x = int(68 * s) + px            # left edge of phone body
    vb_y = int(965 * s) + py           # top volume button center

    # glow ring around the volume button
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    rd.ellipse([vb_x - 150, vb_y - 150, vb_x + 150, vb_y + 150], fill=ACCENT + (120,))
    bg.alpha_composite(ring.filter(ImageFilter.GaussianBlur(60)))
    d.ellipse([vb_x - 62, vb_y - 62, vb_x + 62, vb_y + 62], outline=ACCENT_HI, width=8)

    # "+1" bubble to the left of the button, with a connector
    bx0, by0, bx1, by1 = vb_x - 300, vb_y - 70, vb_x - 96, vb_y + 70
    d.rounded_rectangle([bx0, by0, bx1, by1], 40, fill=ACCENT + (255,))
    d.polygon([(bx1, vb_y - 26), (bx1 + 34, vb_y), (bx1, vb_y + 26)], fill=ACCENT)
    f1 = font(96)
    tw = d.textlength("+1", font=f1)
    d.text(((bx0 + bx1) / 2 - tw / 2, vb_y - 56), "+1", font=f1, fill=(255, 255, 255, 255))

    # headline text (top)
    fh1, fh2, fh3 = font(120), font(66, bold=False), font(58, bold=False)
    d.text((90, 150), "Ses tuşlarıyla say", font=fh1, fill=(255, 255, 255, 255))
    d.text((92, 300), "Ekran kapalıyken bile zikrine devam et.", font=fh2, fill=(210, 206, 235, 255))
    d.text((92, 384), "Count with the volume keys — even screen off.", font=fh3, fill=(150, 145, 180, 255))

    bg.convert("RGB").save(os.path.join(SRC, "hero-volume-keys-v1.png"), quality=95)
    print("wrote", os.path.join(SRC, "hero-volume-keys-v1.png"), bg.size)

if __name__ == "__main__":
    main()

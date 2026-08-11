#!/usr/bin/env python3
"""Add the standard top headline band to a pre-made (nano-banana) hero image, using
the SAME text style as tools/hero_set.py. Text only — draws no hands/graphics.

Usage: python3 tools/hero_caption.py IN.png OUT.png ACCENT_HEX "TITLE" "SUB_TR" "SUB_EN"
The band color is sampled from IN's top edge, so the join is seamless.
"""
import sys
from PIL import Image
import hero_set  # reuse font()/headline() and identical styling

BAND = 310  # keeps final aspect ratio under Play's 2:1 for the ~1536x2752 volume hero


def main():
    inp, out, hexc, title, sub_tr, sub_en = sys.argv[1:7]
    accent_hi = tuple(int(hexc[i:i+2], 16) for i in (0, 2, 4))
    im = Image.open(inp).convert("RGBA")
    W, Ht = im.size
    top = im.crop((0, 0, W, 6)).resize((1, 1)).getpixel((0, 0))  # avg top color

    canvas = Image.new("RGBA", (W, Ht + BAND), top)
    canvas.alpha_composite(im, (0, BAND))
    hero_set.headline(canvas, title, sub_tr, sub_en, accent_hi)

    assert (Ht + BAND) / W <= 2.0, "aspect ratio exceeds Play's 2:1"
    canvas.convert("RGB").save(out, quality=95)
    print("wrote", out, canvas.size, "ratio", round((Ht + BAND) / W, 3))


if __name__ == "__main__":
    main()

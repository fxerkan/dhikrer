#!/usr/bin/env python3
"""Self-check for the multi-platform store pipeline. Run: python3 tools/test_store.py
Asserts the copy.json single source stays consistent with the platform rules that
shots.mjs / frame.py / hero_set.py depend on. No framework — just asserts."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPY = json.load(open(os.path.join(ROOT, "store/shared/copy.json"), encoding="utf8"))
LANGS = ["tr", "en", "ar"]
# App Store exact sizes hero_set.py may target (must match Apple's accepted list).
IOS_OK_SIZES = {(1290, 2796), (1320, 2868)}


def heroes_for(platform):
    return {s: h for s, h in COPY["heroes"].items() if platform in h["platforms"]}


def main():
    # every hero fully localized (title + sub) in all langs
    for slug, h in COPY["heroes"].items():
        for lang in LANGS:
            t = h["text"][lang]
            assert len(t) == 2 and all(t), f"{slug}/{lang} incomplete headline"

    android, ios = heroes_for("android"), heroes_for("ios")
    assert len(android) == 6, f"android should showcase 6 heroes, got {len(android)}"
    assert len(ios) == 6, f"ios should showcase 6 heroes, got {len(ios)}"

    # The core platform difference: iOS can't read hardware volume keys, so no
    # volume hero/claim; it uses a lock hero instead.
    assert "volume" in android and "volume" not in ios, "iOS must NOT ship the volume hero"
    assert "lock" in ios, "iOS should ship the lock hero in the volume slot"
    for h in ios.values():
        assert not h.get("callout"), "iOS heroes have no volume callout"

    # listing copy present + within store limits
    for lang in LANGS:
        a = COPY["listing"]["android"][lang]
        assert len(a["short"]) <= 80, f"android/{lang} short desc >80"
        assert len(a["full"]) <= 4000
        i = COPY["listing"]["ios"][lang]
        assert len(i["subtitle"]) <= 30, f"ios/{lang} subtitle >30: {len(i['subtitle'])}"
        assert len(i["keywords"]) <= 100, f"ios/{lang} keywords >100"
        assert len(i["promo"]) <= 170, f"ios/{lang} promo >170"
        assert len(i["full"]) <= 4000
        assert "volume" not in i["full"].lower() and "ses tuş" not in i["full"].lower(), \
            f"ios/{lang} description must not claim volume-key counting"

    print("OK — copy.json consistent:", len(android), "android +", len(ios), "ios heroes,",
          "listings within App Store/Play limits")


if __name__ == "__main__":
    main()

# Zikirci / Dhikrer

Dhikr counter Android app: native Kotlin shell hosting the web UI
(`webapp-handoff/Zikirci.dc.html`, a self-rendering React app) in a fullscreen WebView. See
`tools/gen_app.mjs` for the webapp→assets pipeline; re-run `node tools/gen_app.mjs .`
after editing `webapp-handoff/Zikirci.dc.html` or `tools/langs.js`, then rebuild.

## Versioning

`versionName` is semver **MAJOR.MINOR.PATCH** (e.g. `1.0.4`). Bump per release in
`android/app/build.gradle.kts`:

- **MAJOR** — main features or large changes (new native module, redesign, breaking rework).
- **MINOR** — small feature additions or notable improvements, no big rework.
- **PATCH** — plain builds, bug fixes, tweaks.

Rules:
- Bumping a higher level resets the lower ones to 0 (`1.0.9` + feature → `1.1.0`; `1.4.2` + big change → `2.0.0`).
- `versionCode` is a separate monotonic counter — **+1 on every release**, never reset (Play Store requires it to only increase).
- Current: `1.2.3` / code `11`. History `1.0`–`1.5` (old 2-part scheme) maps to `1.0.0`–`1.0.5`.
- Name release APKs `Zikirci-Dhikrer-<versionName>.apk`.
- On every release, add the entry to `CHANGELOG.md` (EN) **and** `CHANGELOG.tr.md` (TR),
  including the ≤500-char Play Store / App Store "What's new" note.
- The settings footer version (`t.dev`) is **auto-stamped** by `tools/gen_app.mjs` from
  `versionName` on every regen — don't hand-edit `v…` in `langs.js`/`webapp` `t.dev`;
  bump `build.gradle.kts` and re-run `node tools/gen_app.mjs .`.

## Build

JDK 21, `./gradlew :app:assembleRelease`. Release signed with `android/zikirci-release.jks`.

## Store assets (per platform × per language: tr/en/ar)

`store/` is split by platform, with a single-source shared layer:

```
store/shared/copy.json   ← ALL localized copy (brand, dhikr names, hero headlines,
                            feature-graphic text, both stores' listing text). Edit HERE.
store/shared/store-icon-{512,1024}.png   ← icon: 512 (Play), 1024 no-alpha (App Store)
store/android/<lang>/    heroes + framed + feature-graphic-1024x500.png · LISTING.md · RELEASE.md
store/ios/<lang>/        heroes + framed · LISTING.md · RELEASE.md
store/watchos/           placeholder (future — mirror ios/ layout)
```

Rule: shared/edit-once copy lives in `copy.json`; platform-specific output (frames,
dimensions, feature graphic) lives under its platform. Adding Huawei = a new
`store/huawei/` reusing android assets + `copy.json`. **iOS differs from Android:** no
hardware volume-key counting (`docs/ios.md`) → iOS drops the volume hero, adds a lock
hero; no feature graphic (Play-only); iPhone frame; App Store 6.9" size (1290×2796).

Pipeline (from repo root, after `node tools/gen_app.mjs .`). `PLATFORM` env selects
android (default) or ios; each writes under `store/<platform>/<lang>/`:
1. `[PLATFORM=ios] node tools/shots.mjs` — throwaway `shot.html` from `app.html`, served
   on `:8790`, captures each platform's hero screens × tr/en/ar via headless Chrome →
   `_raw/`. Which screens per platform is read from `copy.json`. `shot.html`/`_shots/`
   auto-cleaned (never ship in the APK). `all` arg captures the full 15-screen gallery.
2. `[PLATFORM=ios] python3 tools/frame.py` — wraps each in a phone frame → `framed/`
   (Android punch-hole+rocker, or iPhone Dynamic Island).
3. `[PLATFORM=ios] python3 tools/hero_set.py` — composites framed screen + headline →
   `hero-<slug>.png`. Arabic headlines use Pillow's raqm (`direction='rtl'`), no reshaping.
4. `python3 tools/store_assets.py` — icons (both sizes) + per-language Play feature
   graphics (logo tile, localized name + title + slogan; Arabic RTL). Reads `copy.json`.

`tools/hero.py` / `tools/hero_caption.py` are the older TR-only / nano-banana-band flow,
superseded by `hero_set.py`. Legacy Play screenshots sit in `store/android/_legacy-screenshots/`.

## Roadmap (planned, not yet built)

Full Arabic (RTL) UI (verify + enable in the language picker) · Bluetooth headset
integration · dhikr audio narration (spoken playback) · statistics home-screen
widget · dhikr sharing. Full list lives in `README.md`.

Note: Arabic strings exist (`tools/langs.js` `ar`) and `gen_app.mjs` already
un-disables the `ar` option in the built `app.html`; RTL renders. What's left is
verification/polish + enabling it in the `webapp-handoff` source.

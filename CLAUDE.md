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

## Store listing images (per language: tr/en/ar)

Play Store heroes + framed screenshots are generated **per language** into
`store/<lang>/`. Each language uploads separately; the in-phone UI, brand
(`Zikirci.` / `Dhikrer.` / `الذّاكِر.`) and dhikr names are all localized, and
each hero carries a single-language headline (title + one subtitle).

Pipeline (run from repo root, after `node tools/gen_app.mjs .`):
1. `node tools/shots.mjs` — regenerates a throwaway `shot.html` from `app.html`
   (adds a sync state-injector), serves it on `:8790`, and captures the 6 hero
   screens × tr/en/ar via headless Chrome → `store/<lang>/_raw/`. `shot.html`
   and `_shots/` are auto-cleaned (they must never ship in the APK). `all` arg
   captures the full 15-screen gallery.
2. `python3 tools/frame.py` — wraps each into a phone frame → `store/<lang>/framed/`.
3. `python3 tools/hero_set.py` — composites framed screen + headline → `store/<lang>/hero-<slug>.png`.
   Arabic headlines rely on Pillow's raqm build (`direction='rtl'`), no reshaping libs.

`tools/hero.py` / `tools/hero_caption.py` are the older TR-only / nano-banana-band
flow, superseded by `hero_set.py` for the per-language set.

## Roadmap (planned, not yet built)

Full Arabic (RTL) UI (verify + enable in the language picker) · Bluetooth headset
integration · dhikr audio narration (spoken playback) · statistics home-screen
widget · dhikr sharing. Full list lives in `README.md`.

Note: Arabic strings exist (`tools/langs.js` `ar`) and `gen_app.mjs` already
un-disables the `ar` option in the built `app.html`; RTL renders. What's left is
verification/polish + enabling it in the `webapp-handoff` source.

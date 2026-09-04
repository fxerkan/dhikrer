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
- **All platforms share ONE version per release** — same semver name and the same build counter. Bump together:
  - `android/app/build.gradle.kts` → `versionName` + `versionCode`
  - `ios/App/App.xcodeproj/project.pbxproj` → `MARKETING_VERSION` (= `versionName`) + `CURRENT_PROJECT_VERSION` (= `versionCode`), in **both** Debug and Release configs
  - `package.json` → `version` (= `versionName`)
- Current: `1.3.2` / code `15`. History `1.0`–`1.5` (old 2-part scheme) maps to `1.0.0`–`1.0.5`.
- Name release APKs `Zikirci-Dhikrer-<versionName>.apk`.
- On every release, add the entry to `CHANGELOG.md` (EN) **and** `CHANGELOG.tr.md` (TR),
  including the ≤500-char Play Store / App Store "What's new" note. Also bump
  `store/release-notes.json` (`version` + per-locale `notes`, incl. `ar`) — the CI reads
  it to fill the App Store "What's New"; it only applies notes whose `version` matches the
  build, so stale notes are never shipped.
- **Publishing (CI/CD).** `.github/workflows/release.yml` (see [`.github/RELEASE_CICD.md`]):
  push a `v*` tag → Android → Play internal, iOS binary → App Store Connect, then the
  `ios_prepare` job (ASC API, `tools/asc_prepare_version.py`) waits for build processing and
  **creates the App Store version + attaches the build + writes What's New** — leaving it one
  manual click from **Submit for Review** (it never auto-submits). To re-publish only iOS at
  the same versionCode after Android already shipped, run the workflow manually with
  `ios_only=true` + `publish=true` (a full re-run would fail Play's duplicate-versionCode check).
- **App Store submissions (Apple Guideline 2.1):** the **App Review Information → Notes**
  field is MANDATORY — paste `store/ios/APP_REVIEW_NOTES.md` verbatim and attach a
  screen recording made on a *physical* iPhone. An empty/thin Notes field is why our
  first submission was rejected ("Information Needed"). Keep that file in sync each
  release. Only request permissions the app actually uses (Dhikrer = notifications
  only, on reminder-enable); never add unused `NS*UsageDescription` keys to
  `ios/App/App/Info.plist` — an unused purpose string is a 5.1.1 rejection.
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
hero; no feature graphic (Play-only); iPhone frame; App Store 6.5" size (1284×2778 —
the 6.5" slot rejects 6.9" 1290×2796; accepted sizes are 1242×2688 / 1284×2778).

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

Voice-recognition dhikr tracking (auto-count via on-device speech recognition) ·
Bluetooth headset integration · dhikr audio narration (spoken playback) ·
statistics home-screen widget · dhikr sharing. Full list lives in `README.md`.

Note: Full Arabic (RTL) UI is done — Arabic strings live in `tools/langs.js` `ar`,
`gen_app.mjs` un-disables the `ar` option in the built `app.html`, and RTL renders.

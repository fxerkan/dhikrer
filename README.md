# Zikirci · Dhikrer

A modern, distraction‑free **dhikr (zikir) counter** for Android. Count with a big
tap button, the **volume keys** — even with the screen off — or a **home‑screen widget**.
Beautiful, fast, and completely private.

App ID `com.fxerkan.dhikrer` — named **Zikirci** in Turkish, **Dhikrer** in English.

## Why Zikirci is different

- 🚫 **No ads. Ever.** Not a single banner, interstitial, or "watch to unlock".
- 💛 **No cost.** Free, with no paywalls, subscriptions, or locked features.
- 🔒 **No personal information.** No account, no sign‑up, no email — just open and count.
- 📡 **No telemetry, no tracking.** Nothing is collected or sent anywhere. Every count,
  setting, and statistic lives **only on your device** (offline‑first, works with no network).
- 🧭 **No surprise permissions.** No location, contacts, camera, or storage snooping.

## Features

- **Counter** 0–999 with a "thousands" indicator (1 bin, 2 bin …), up **or** countdown, and it
  continues exactly where you left off.
- **Count anywhere:** big tap button, **volume keys (screen‑off)**, or a resizable **home widget**.
- **Three counter designs:** Classic ring, **Unified** giant button, and a **Tesbih** (prayer‑bead)
  ring that fills as you count, with 33 / 66 / 99 divider beads.
- **Milestones:** haptics + sound at 33, 66, 99, 100, 999, 1000 — each individually toggleable.
- **My Dhikrs:** save unlimited dhikrs, per‑dhikr sound & vibration, pin, reorder, swipe‑to‑delete.
- **Reminders:** daily notifications at the times you choose.
- **Statistics:** a git‑style intensity heatmap, streaks, daily/weekly/monthly trends, and a
  distribution donut — all from your **real** counting history, on‑device.
- **10 themes** (dark & light), **6 languages** (TR, EN, AR incl. RTL, ID, HI, ZH), a **Lock**
  mode (only the counter responds), full button customization (size/shape/color/position), and
  animation effects (ring / wave / fill / shape‑morph).
- **Accessible & responsive:** large, high‑contrast counter and button; adapts to small phones,
  large phones, and tablets; edge‑to‑edge on modern Android.

## Compatibility

Runs on **Android 8.0+ (API 26)** — Android **12, 13, 14, 15, 16** are all tested and supported.

## Project layout

```
webapp/            Web UI source of truth (self‑rendering React app)
tools/gen_app.mjs  webapp → android/app/src/main/assets bundling (offline, no CDN)
tools/langs.js     Extra UI translations (AR/ID/HI/ZH)
android/           Native Kotlin shell: WebView host + home widget + volume‑key service + reminders
releases/          Published APK / AAB artifacts
store/             Play Store listing: PLAY_RELEASE.md + screenshots (raw, framed, hero)
```

The app is a **native Kotlin shell** that hosts the polished web UI in a fullscreen WebView,
plus native modules for the home widget, screen‑off volume‑key counting, and reminders. All web
assets (fonts, icons, runtime) are **bundled** — the app makes **no network requests**.

## Build

Requires **JDK 21** and the Android SDK. After editing `webapp/Zikirci.dc.html` or
`tools/langs.js`, regenerate the bundled assets, then build:

```bash
node tools/gen_app.mjs .            # regenerate android/app/src/main/assets/app/app.html
cd android
./gradlew :app:assembleRelease      # signed APK  → app/build/outputs/apk/release/
./gradlew :app:bundleRelease        # Play AAB    → app/build/outputs/bundle/release/
```

Release signing reads secrets from a gitignored `android/keystore.properties` (the keystore is
**not** in the repo):

```bash
cp android/keystore.properties.template android/keystore.properties   # then fill in
```

Artifacts are named `Zikirci-Dhikrer-<versionName>.apk`. Versioning rules are in
[`CLAUDE.md`](CLAUDE.md); Play Store steps in [`store/PLAY_RELEASE.md`](store/PLAY_RELEASE.md).

## Author

Made by [@FXerkan](https://fxerkan.com).

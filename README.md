# Zikirci · Dhikrer

A modern, ad-free **dhikr (zikir) counter** for Android. Count your dhikr with a
big tap target, keep counting with the screen off (home-screen widget or volume
keys), track detailed statistics, and switch between many languages and themes.

App ID `com.fxerkan.dhikrer` — named **Zikirci** in Turkish, **Dhikrer** in English.

## Features

- **Counter** 0–999 with a "thousands" indicator above it; continues exactly where you left off.
- **Haptic / sound feedback** at milestones (33, 66, 99, 100, 999, 1000…), each toggleable.
- **Count with the screen off** — home-screen widget (2×2 / 4×2) and volume-key control.
- **Targets & progress** — up or down counting, donut/percentage progress to a goal.
- **Library** of dhikr types you can define, name, and resume independently.
- **Statistics** — commit-graph-style intensity heatmap plus hourly/daily/weekly/monthly charts.
- **Reminders** at scheduled times.
- **Customization** — button color/shape/size/position, counter animations, light & dark themes.
- **Multi-language** — Turkish, English, Arabic, Indonesian, Hindi, Chinese, and more.
- **No ads, ever.**

## Architecture

Native Kotlin shell hosting the Claude Design handoff web app
(`handoff/Zikirci.dc.html`) inside a fullscreen WebView.

```
handoff/           Claude Design handoff (source of truth for the web app)
tools/gen_app.mjs  handoff → android/app/src/main/assets pipeline
tools/langs.js     translation strings
android/           native Kotlin app (WebView shell, widget, notifications, volume-key service)
releases/          published APK / AAB artifacts
device-tests/      device screenshots
```

After editing the handoff or `tools/langs.js`, regenerate the bundled assets:

```bash
node tools/gen_app.mjs .
```

## Build

Requires **JDK 21** and the Android SDK.

```bash
cd android
./gradlew :app:assembleRelease
```

Release signing reads secrets from `android/keystore.properties` (gitignored).
Copy the template and fill in your own values — the release keystore is **not**
included in this repo:

```bash
cp android/keystore.properties.template android/keystore.properties
```

Release artifacts are named `Zikirci-Dhikrer-<versionName>.apk` and live in
[`releases/`](releases/). See [`PLAY_RELEASE.md`](PLAY_RELEASE.md) for the Play
Store process and [`TESTING.md`](TESTING.md) for the device test matrix.

## Versioning

Semver `MAJOR.MINOR.PATCH` in `android/app/build.gradle.kts`; `versionCode` is a
monotonic counter (+1 every release). See [`CLAUDE.md`](CLAUDE.md) for the full rules.

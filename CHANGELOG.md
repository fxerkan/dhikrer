# Changelog — Dhikrer (Zikirci)

All notable changes to this app are documented here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); versions use semver
**MAJOR.MINOR.PATCH** (see [`CLAUDE.md`](CLAUDE.md)). Türkçe: [`CHANGELOG.tr.md`](CHANGELOG.tr.md).

Each release also carries a **Store release note** — plain-text, ≤500 characters — ready to
paste into the Google Play "What's new" field and the App Store "What's New" section.

---

## [1.3.0] — 2026-08-12 · versionCode 13

- **Added: durable data safety net** — your zikir library, settings and statistics are now
  mirrored to permanent device storage and restored automatically if the app's local data is
  ever lost (WebView eviction, reinstall, device migration). App updates already kept your data;
  this adds a second layer so it survives more cases.
- **Added: edit the target in the customize screen** — the per-zikir customize dialog now lets
  you change the Target value directly (previously name + vibration only).
- **Improved: cleaner vibration options** — Vibration style and strength now appear only when
  Vibration is turned on.
- **Added: Help & rate buttons** — Settings now has a Help & Support button and a Rate on Play
  Store button. Help & Support opens your email app with a localized subject and the app version
  pre-filled, and shows the address (dhikrer@fxerkan.com) directly.
- **Added: "Every 100" notification point** — a recurring notification at every hundred (100,
  200 … 900); the point is now clearly labelled "Every 100".
- **Improved: localized footer brand** — the Settings footer now shows the app name in the
  current language (Dhikrer / Zikirci …) with the "-er" accent.
- **Fixed: Beads (tesbih) layout on tablets** — in landscape the shortcut controls no longer
  overlap the counter.
- **Updated:** now targets Android 16 (API 36) to meet Google Play's target API level
  requirement (compile + target SDK 35 → 36).

> **Store release note (EN):**
> Your zikirs, settings and stats are now safer — backed up on-device and auto-restored if ever
> lost. You can now edit a zikir's target in the customize screen, and vibration style/strength
> show only when vibration is on. Also updated to target Android 16.

## [1.2.3] — 2026-08-11 · versionCode 11

Store presentation only — no changes to app behavior.

- Added a new Google Play hero image set: volume-key + hand, ad-free, customize, easy-to-use,
  statistics, and languages (see `store/store-screenshots/hero-*-v1.png`).
- App-name accent styling in the listing and refreshed store copy.
- New framing/hero tooling for generating listing assets.

> **Store release note (EN):**
> Fresh Play Store visuals and listing copy. No changes to how the app works — same fast,
> ad-free, private dhikr counter you already use.

## [1.2.2] — 2026-08-09 · versionCode 10

- **Fixed:** volume-key counting is now more reliable, including with the screen off.
- **Fixed:** the tap/click sound plays correctly on each count.
- **Improved:** reduced the app's background footprint (less battery/memory while idle).

> **Store release note (EN):**
> Bug fixes: more reliable volume-key counting with the screen off, correct click sound, and a
> lighter background footprint for better battery life.

## [1.2.1] — 2026-08-08 · versionCode 9

- **Added: Lock mode** — only the counter responds to taps and volume keys, preventing
  accidental counts while the phone is in your pocket.
  (Screenshot: `store/store-screenshots/04-kilit-kehribar-v1.png`.)
- **Improved: clearer statistics charts** — easier-to-read daily/weekly trends and distribution.
  (Screenshot: `store/store-screenshots/07-istatistik-okyanus-v1.png`.)

> **Store release note (EN):**
> New Lock mode keeps counting accurate in your pocket — only the counter responds. Plus
> clearer, easier-to-read statistics charts.

## [1.1.0] — versionCode 7

Google Play readiness and platform-compliance release.

- **Added:** Android App Bundle (`.aab`) build for Play distribution.
- **Updated:** targetSdk / compileSdk **35** (Android 15) to meet Play's current target-API rules.
- **Added:** edge-to-edge layout — system-bar insets are passed through to the web UI; content
  stays in the safe area, bar icon color follows the theme.
- **Changed:** removed the exact-alarm permission; reminders are now Doze-friendly inexact alarms.
- **Changed:** foreground-service type `specialUse` (was `mediaPlayback`) for screen-off
  volume-key counting — same behavior, Play-policy compliant.
- **Changed:** signing secrets moved to a gitignored `android/keystore.properties`.
- 64-bit / all-ABI, non-debuggable release, no cleartext traffic.

> **Store release note (EN):**
> Google Play–ready build: edge-to-edge Android 15 support, battery-friendly reminders, and
> compliant background counting. Same features, better platform behavior.

## [1.0.0] – [1.0.5] — foundational release series (old 2-part `1.0`–`1.5`)

The first public releases established the full app:

- **Counter** 0–999 with a thousands indicator, count up **or** down, and resume where you left off.
- **Count anywhere:** big tap button, physical **volume keys (screen-off)**, and a resizable
  **home-screen widget**.
- **Three counter designs:** Classic ring, Unified giant button, and a Tesbih (prayer-bead) ring
  with 33 / 66 / 99 divider beads.
  (Screenshots: `store/store-screenshots/01-sayac-klasik-gece-v1.png`,
  `02-tespih-zumrut-v1.png`, `03-birlesik-gul-v1.png`.)
- **Milestones:** haptics + sound at 33, 66, 99, 100, 999, 1000 — each individually toggleable.
- **My Dhikrs:** save unlimited dhikrs, per-dhikr sound & vibration, pin, reorder, swipe-to-delete.
  (Screenshot: `store/store-screenshots/06-zikirler-gece-v1.png`.)
- **Reminders:** daily notifications at the times you choose.
- **Statistics:** git-style intensity heatmap, streaks, daily/weekly/monthly trends, and a
  distribution donut — all on-device from your real counting history.
- **10 themes** (dark & light), **6 languages** (TR, EN, AR incl. RTL, ID, HI, ZH), full button
  customization (size/shape/color/position), and animation effects (ring / wave / fill / shape-morph).
  (Screenshot: `store/store-screenshots/10-arapca-rtl-gece-v1.png`.)
- **Privacy-first:** no ads, no account, no telemetry, offline-only — everything stays on-device.

> **Store release note (EN):**
> Dhikrer — a fast, ad-free, private dhikr counter. Count by tap, volume keys, or a home widget;
> Classic / Unified / Tesbih designs, milestones, reminders, on-device statistics, 10 themes,
> 6 languages with RTL.

---

## Planned (roadmap)

Not yet released — tracked here so the changelog reflects direction:

- 🎧 Bluetooth headset integration — count/control via Bluetooth earbud buttons.
- 🔊 Dhikr audio narration — spoken playback of the active dhikr.
- 📊 Statistics widget — home-screen widget for daily count, streak, and progress.
- 📤 Dhikr sharing — share dhikrs and progress with others.

[1.2.3]: #123--2026-08-11--versioncode-11
[1.2.2]: #122--2026-08-09--versioncode-10
[1.2.1]: #121--2026-08-08--versioncode-9
[1.1.0]: #110--versioncode-7

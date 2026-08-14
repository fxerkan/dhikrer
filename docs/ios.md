# iOS (Capacitor) — MVP

The iOS app is the **same web UI** as Android, wrapped in a Capacitor `WKWebView`
shell. No Swift/native app code — the web app in `android/app/src/main/assets/app/`
is the single source of truth for both platforms. Android is untouched by this port.

- **appId:** `com.fxerkan.dhikrer` (matches Android `applicationId`)
- **Display name:** `Zikirci`
- The JS native bridge (`ZikirNative.*`) is already guard-checked in the web app, so
  it simply no-ops on iOS — no errors from the missing Android bridge.

## Build & run

Prereqs: full Xcode selected (`sudo xcode-select -s /Applications/Xcode.app/Contents/Developer`),
Node. Capacitor 8 uses Swift Package Manager — **no CocoaPods needed**.

```bash
npm install                 # first time only
npm run ios:web             # regenerate www/ from the Android web assets (+ iOS shim)
npx cap copy ios            # copy www/ into the Xcode project
npx cap open ios            # open in Xcode → pick a simulator/device → Run
```

`npm run ios:web` copies `android/app/src/main/assets/app/` into `www/`, drops the
store-shot scratch files, and appends `tools/ios-shim.html` to produce `index.html`
(Capacitor's entry point). **Re-run it after editing the web app** (`node tools/gen_app.mjs .`),
then `npx cap copy ios`. `www/` is generated and gitignored.

### CLI-only (no Xcode GUI)

```bash
xcodebuild -project ios/App/App.xcodeproj -scheme App -configuration Debug \
  -sdk iphonesimulator -destination 'platform=iOS Simulator,name=iPhone 17' \
  -derivedDataPath build/ios build
xcrun simctl install booted build/ios/Build/Products/Debug-iphonesimulator/App.app
xcrun simctl launch booted com.fxerkan.dhikrer
```

> Note: on this machine `xcrun simctl launch/terminate` may hang on return even though
> the app actually launches. Use the Xcode Run button, or ignore the hang and verify via
> screenshot (`xcrun simctl io booted screenshot x.png`).

## `tools/ios-shim.html` — the only iOS-specific code

Appended to `index.html` **only**, never to Android's `app.html`. Two fixes:

1. **Safe-area insets** — Android sets `--zk-sat/sab/sal/sar` natively via `WindowInsets`;
   on iOS we map them to `env(safe-area-inset-*)` so the header clears the status bar and
   the bottom nav clears the home indicator.
2. **Themed status-bar strip** — the themed `--color-bg` lives on `.zk-app`, not `<body>`,
   so the WKWebView safe-area strips would show through white. A 600ms poll mirrors the
   active theme's background onto `<html>`/`<body>` so they blend.

## Feature parity (verified on iOS 26 simulator, iPhone 17)

| Feature | Status | Notes |
|---|---|---|
| App launch + full UI render | ✅ works | Same web app, WKWebView |
| Counter (tap → increment, ring, %, remaining) | ✅ works | Verified: 33 taps → 33 / %33 |
| Themes (Gece/Okyanus/… 10 themes) | ✅ works | Render + switch confirmed |
| Turkish/English/Arabic UI strings | ✅ works | TR verified; EN/AR same code path |
| localStorage persistence | ✅ works | Survived reinstall + relaunch |
| Safe-area (notch / home indicator) | ✅ works | Via iOS shim (see above) |
| Bottom tab navigation | ✅ works | Sayaç/Zikirler/İstatistik/Ayarlar |
| Backup / restore to native file | ⚪ no-ops | Not needed — localStorage persists. Add `@capacitor/preferences` only if wanted |
| Haptics (vibrate on tap) | 🟡 device-only | No taptic engine in simulator. `navigator.vibrate` is a no-op in WKWebView → needs `@capacitor/haptics` bridge to buzz. Verify on the iPhone 11 |
| Local notifications / reminders | 🟡 not ported | Needs `@capacitor/local-notifications`. Deferred |
| Home-screen widget | ❌ out of scope | iOS needs a separate WidgetKit extension |
| Volume-key counting | ❌ impossible | iOS doesn't hand hardware volume keys to apps |

**MVP result:** the core dhikr experience (count, themes, languages, persistence, layout)
is at full parity on iOS. Haptics + notifications are the next increment; widget +
volume-keys are explicitly out of MVP scope.

## Before App Store submission (not done here)

- Real app icon (currently the default Capacitor icon) — generate from the brand asset.
- Signing team / provisioning profile for `com.fxerkan.dhikrer` in Xcode.
- Privacy nutrition labels (the app collects nothing — all data is on-device).

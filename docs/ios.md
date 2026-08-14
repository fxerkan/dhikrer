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

## Run on a physical device

Signing: `DEVELOPMENT_TEAM` + automatic signing are set in the project. For a free
personal team, let Xcode/`xcodebuild` create the cert & profile on the fly:

```bash
xcodebuild -project ios/App/App.xcodeproj -scheme App -configuration Debug \
  -destination 'platform=iOS,name=<DeviceName>' -derivedDataPath build/ios-device \
  -allowProvisioningUpdates build
xcrun devicectl list devices                       # get the device UDID
xcrun devicectl device install app --device <UDID> \
  build/ios-device/Build/Products/Debug-iphoneos/App.app
xcrun devicectl device process launch --device <UDID> com.fxerkan.dhikrer
```

First launch is blocked until you **trust the developer profile on the device**:
Settings → General → VPN & Device Management → *Apple Development: <your Apple ID>* → Trust.
(iOS 16+ also needs Developer Mode ON.) Free-team builds expire after 7 days.

## App icon & localized name

- **Icon:** `ios/App/App/Assets.xcassets/AppIcon.appiconset/AppIcon-512@2x.png` is the
  1024×1024, no-alpha icon (App Store requirement). `tools/store_assets.py` renders it
  as `store/shared/store-icon-1024.png`; copy it into the appiconset, or regenerate from
  the 512 master: `sips -z 1024 1024 store/shared/store-icon-512.png --out <that path>`.
- **Home-screen name follows the device language** via `App/<lang>.lproj/InfoPlist.strings`
  (`CFBundleDisplayName`): tr=Zikirci, en/id/hi/zh=Dhikrer, ar=الذّاكِر; other languages
  fall back to the Info.plist default. iOS can **not** switch the home-screen name from
  the in-app language picker — only the in-app brand follows that. Logo is identical
  across languages.

## Feature parity (✅ verified on physical iPhone 14, iOS 26)

| Feature | Status | Notes |
|---|---|---|
| App launch + full UI render | ✅ works | Same web app, WKWebView |
| Counter (tap → increment, ring, %, remaining) | ✅ works | 33 taps → 33 / %33 |
| Themes (Gece/Okyanus/… 10 themes) | ✅ works | Render + switch confirmed |
| Turkish/English/Arabic UI strings | ✅ works | Device-verified |
| localStorage persistence | ✅ works | Survived reinstall + relaunch |
| Safe-area (notch / home indicator) | ✅ works | Via iOS shim |
| Bottom tab navigation | ✅ works | Sayaç/Zikirler/İstatistik/Ayarlar |
| Haptics (buzz on tap + milestones) | ✅ works | `@capacitor/haptics`, routed via the shim |
| App icon = store icon | ✅ works | 1024×1024, no alpha |
| Localized home-screen name | ✅ works | Per device language (see above) |
| Reminders / local notifications | ✅ works | `@capacitor/local-notifications`, daily-repeating; text baked per in-app language |
| Backup / restore to native file | ⚪ no-ops | Not needed — localStorage persists |
| Home-screen widget | ❌ out of scope | iOS needs a separate WidgetKit extension |
| Volume-key counting | ❌ impossible | iOS doesn't hand hardware volume keys to apps |

Reminders: the iOS shim mirrors the web reminder list (`{time, on, label}` in
localStorage) into daily-repeating local notifications, reconciling whenever the set
changes and asking for notification permission only once a reminder is enabled.

**MVP result:** the core dhikr experience — count, haptics, themes, languages,
persistence, layout, icon, localized name, reminders — is at full parity on iOS,
verified on device. Widget + volume-keys are the only out-of-scope pieces.

## App Store submission

Full step-by-step process, store copy, and screenshot pipeline live in **`store/ios/`**:
`RELEASE.md` (the whole submission flow) + `LISTING.md` (per-language listing text &
assets). Localized copy is single-sourced in `store/shared/copy.json`. Screenshots
(1290×2796, per language) are generated by `PLATFORM=ios` runs of `tools/shots.mjs →
frame.py → hero_set.py`. Not done here (manual): paid Apple Developer membership, App
Store Connect record + distribution profile, and publishing the privacy policy at a URL.

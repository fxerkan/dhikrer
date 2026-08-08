# Zikirci / Dhikrer

Dhikr counter Android app: native Kotlin shell hosting the Claude Design handoff web app
(`handoff/Zikirci.dc.html`) in a fullscreen WebView. See
`tools/gen_app.mjs` for the handoff→assets pipeline; re-run `node tools/gen_app.mjs .`
after editing the handoff or `tools/langs.js`, then rebuild.

## Versioning

`versionName` is semver **MAJOR.MINOR.PATCH** (e.g. `1.0.4`). Bump per release in
`android/app/build.gradle.kts`:

- **MAJOR** — main features or large changes (new native module, redesign, breaking rework).
- **MINOR** — small feature additions or notable improvements, no big rework.
- **PATCH** — plain builds, bug fixes, tweaks.

Rules:
- Bumping a higher level resets the lower ones to 0 (`1.0.9` + feature → `1.1.0`; `1.4.2` + big change → `2.0.0`).
- `versionCode` is a separate monotonic counter — **+1 on every release**, never reset (Play Store requires it to only increase).
- Current: `1.0.4` / code `5`. History `1.0`–`1.4` (old 2-part scheme) maps to `1.0.0`–`1.0.4`.
- Name release APKs `Zikirci-Dhikrer-<versionName>.apk`.
- The settings footer version (`t.dev`) is **auto-stamped** by `tools/gen_app.mjs` from
  `versionName` on every regen — don't hand-edit `v…` in `langs.js`/handoff `t.dev`;
  bump `build.gradle.kts` and re-run `node tools/gen_app.mjs .`.

## Build

JDK 21, `./gradlew :app:assembleRelease`. Release signed with `android/zikirci-release.jks`.

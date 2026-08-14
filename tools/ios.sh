#!/usr/bin/env bash
# Zikirci / Dhikrer — iOS helper. One command per common task.
#
#   tools/ios.sh web            # regenerate www/ from the web app + copy into Xcode
#   tools/ios.sh sim [name]     # build + install + launch on a simulator (default: iPhone 17)
#   tools/ios.sh device         # build + install + launch on the connected iPhone
#   tools/ios.sh shot [file]    # screenshot the booted simulator (default: /tmp/sim.png)
#   tools/ios.sh open           # open the project in Xcode (then press ▶ Run)
#   tools/ios.sh help
#
# Notes
# - Run from the repo root. Needs full Xcode selected + Node.
# - First device launch: trust the profile on the phone once
#   (Settings ▸ General ▸ VPN & Device Management ▸ your Apple ID ▸ Trust).
# - `simctl launch` can hang on return on some machines; we launch it detached and
#   don't wait — the app still opens.
set -euo pipefail
cd "$(dirname "$0")/.."

APPID=com.fxerkan.dhikrer
PROJ=ios/App/App.xcodeproj

web() {
  npm run ios:web >/dev/null
  npx cap copy ios >/dev/null
  echo "✓ web synced into ios/App/App/public"
}

sim() {
  local name="${1:-iPhone 17}"
  web
  echo "→ building for simulator: $name"
  xcodebuild -project "$PROJ" -scheme App -configuration Debug -sdk iphonesimulator \
    -destination "platform=iOS Simulator,name=$name" -derivedDataPath build/ios \
    -skipPackagePluginValidation build >/dev/null
  local app=build/ios/Build/Products/Debug-iphonesimulator/App.app
  xcrun simctl bootstatus "$name" -b >/dev/null 2>&1 || xcrun simctl boot "$name" || true
  open -a Simulator
  xcrun simctl install booted "$app"
  nohup xcrun simctl launch booted "$APPID" >/dev/null 2>&1 &
  echo "✓ launched on $name"
}

device() {
  web
  local udid
  udid=$(xcrun devicectl list devices 2>/dev/null | grep -i connected \
    | grep -oE '[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}' | head -1)
  [ -z "$udid" ] && { echo "✗ no connected device (plug in the iPhone, unlock, trust)"; exit 1; }
  echo "→ building + signing for device $udid"
  xcodebuild -project "$PROJ" -scheme App -configuration Debug \
    -destination "id=$udid" -derivedDataPath build/ios-device \
    -allowProvisioningUpdates -skipPackagePluginValidation build >/dev/null
  local app=build/ios-device/Build/Products/Debug-iphoneos/App.app
  xcrun devicectl device install app --device "$udid" "$app" >/dev/null
  xcrun devicectl device process launch --device "$udid" --terminate-existing "$APPID" >/dev/null
  echo "✓ installed + launched on device"
}

shot() { xcrun simctl io booted screenshot "${1:-/tmp/sim.png}"; }
open_xcode() { npx cap open ios; }
usage() { grep '^#[^!]' "$0" | sed 's/^# \{0,1\}//'; }

case "${1:-help}" in
  web) web ;;
  sim) shift; sim "${1:-}" ;;
  device) device ;;
  shot) shift; shot "${1:-}" ;;
  open) open_xcode ;;
  *) usage ;;
esac

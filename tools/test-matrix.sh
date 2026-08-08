#!/usr/bin/env bash
# Zikirci/Dhikrer multi-device emulator tester.
#   ./tools/test-matrix.sh <api> <device> <label>   # one config
#   ./tools/test-matrix.sh all                       # full 5x3 matrix, sequential
# Downloads the system image, (re)creates an AVD, boots headless, installs the
# APK, screenshots to device-tests/<label>.png, then kills the emulator.
set -uo pipefail

export ANDROID_HOME="${ANDROID_HOME:-/opt/homebrew/share/android-commandlinetools}"
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home}"
export PATH="$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APK="$(ls -t "$ROOT"/Zikirci-Dhikrer-*.apk 2>/dev/null | head -1)"
SHOTS="$ROOT/device-tests"; mkdir -p "$SHOTS"
PKG=com.fxerkan.dhikrer
ACT=com.fxerkan.zikirci.MainActivity

one() {
  local API=$1 DEVICE=$2 LABEL=$3
  local IMG="system-images;android-${API};google_apis;arm64-v8a"
  local IMGDIR="$ANDROID_HOME/system-images/android-${API}/google_apis/arm64-v8a"
  local AVD="test_${API}_${DEVICE}"
  echo "=== [$LABEL] API $API on $DEVICE ==="
  if [ ! -d "$IMGDIR" ]; then
    echo "  downloading $IMG ..."
    yes 2>/dev/null | sdkmanager --licenses >/dev/null 2>&1 || true
    yes 2>/dev/null | sdkmanager "$IMG" >/dev/null 2>&1 || true
    [ -d "$IMGDIR" ] || { echo "  image download failed"; return 1; }
  fi
  echo no | avdmanager create avd -n "$AVD" -k "$IMG" -d "$DEVICE" --force >/dev/null 2>&1
  adb start-server 2>/dev/null
  emulator -avd "$AVD" -no-window -no-snapshot -no-audio -no-boot-anim \
    -gpu swiftshader_indirect -cores 4 -memory 3072 >/tmp/emu_$AVD.log 2>&1 &
  local EPID=$!
  # target ONLY the emulator (a real device may also be attached)
  export ANDROID_SERIAL=emulator-5554
  adb -s emulator-5554 wait-for-device
  local t=0
  until [ "$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')" = "1" ]; do
    sleep 3; t=$((t+3)); [ $t -gt 240 ] && { echo "boot timeout"; break; }
  done
  adb install -r "$APK" >/dev/null 2>&1
  adb shell pm grant $PKG android.permission.POST_NOTIFICATIONS >/dev/null 2>&1
  adb shell am start -n "$PKG/$ACT" >/dev/null 2>&1
  sleep 15
  adb exec-out screencap -p > "$SHOTS/${LABEL}.png" 2>/dev/null
  echo "  -> $SHOTS/${LABEL}.png ($(du -h "$SHOTS/${LABEL}.png" 2>/dev/null | cut -f1))"
  adb emu kill >/dev/null 2>&1; sleep 2; kill -9 $EPID 2>/dev/null
  pkill -9 -f "qemu-system.*$AVD" 2>/dev/null; sleep 2
}

if [ "${1:-}" = "all" ]; then
  for API in 31 33 34 35 36; do
    for DEV in small_phone medium_phone pixel_9_pro_xl; do
      one "$API" "$DEV" "android-api${API}-${DEV}"
    done
  done
else
  one "${1:?api}" "${2:?device}" "${3:?label}"
fi

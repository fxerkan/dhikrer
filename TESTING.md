# Zikirci / Dhikrer — Emülatörde Çoklu Cihaz Testi

Farklı Android sürümleri ve ekran boyutlarında hızlı test için basit rehber.
Her şey **terminalden**, Android Studio gerektirmez.

## 0) Ortam (her terminalde bir kez)

```bash
export ANDROID_HOME=/opt/homebrew/share/android-commandlinetools
export JAVA_HOME=/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home
export PATH="$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH"
```

## 1) Android sürümü → API karşılığı

| Android | API | Sistem imajı (indirilecek) |
|--------:|:---:|----------------------------|
| 12  | 31 | `system-images;android-31;google_apis;arm64-v8a` |
| 13  | 33 | `system-images;android-33;google_apis;arm64-v8a` |
| 14  | 34 | `system-images;android-34;google_apis;arm64-v8a` (kurulu) |
| 15  | 35 | `system-images;android-35;google_apis;arm64-v8a` |
| 16  | 36 | `system-images;android-36;google_apis;arm64-v8a` |

> `google_apis` kullanın (Play Store gerektirmez, giriş istemez). İmaj indirmesi sürüm başına ~1–1.5 GB.

## 2) Cihaz profilleri (boyut) — hazır id'ler

| Boyut | Profil id | Not |
|-------|-----------|-----|
| Küçük telefon | `small_phone` | ~5", düşük çözünürlük |
| Orta telefon  | `medium_phone` | ~6", 1080p |
| Büyük / amiral | `pixel_9_pro_xl` | ~6.8", QHD (S26+ muadili) |
| Pixel (referans) | `pixel_8` / `pixel_9` | |
| Katlanabilir | `pixel_9_pro_fold` | |
| Tablet | `pixel_tablet` | |

Tüm liste: `avdmanager list device`

## 3) Tek komutla test (script)

`tools/test-matrix.sh <api> <device> <etiket>` — imajı indirir, AVD'yi kurar,
başlatır, APK'yı yükler, ekran görüntüsü alır (`device-tests/<etiket>.png`), kapatır.

```bash
# örnek: Android 13, orta telefon
./tools/test-matrix.sh 33 medium_phone android13-medium

# örnek: Android 16, büyük telefon
./tools/test-matrix.sh 36 pixel_9_pro_xl android16-xl
```

Tüm matrisi sırayla çalıştır (5 sürüm × 3 boyut):

```bash
./tools/test-matrix.sh all
```

## 4) İnteraktif kullanmak (elle görmek) istersen

```bash
# imajı indir (bir kez)
sdkmanager "system-images;android-33;google_apis;arm64-v8a"
# AVD oluştur
avdmanager create avd -n test13 -k "system-images;android-33;google_apis;arm64-v8a" -d medium_phone
# PENCEREYLE başlat (gerçek renkler için -gpu auto)
emulator -avd test13 -gpu auto
# başka terminalde: APK yükle + aç
adb install -r Zikirci-Dhikrer-1.5.apk
adb shell am start -n com.fxerkan.dhikrer/com.fxerkan.zikirci.MainActivity
```

## 5) Faydalı komutlar

```bash
adb devices                       # bağlı emülatör/cihaz
adb exec-out screencap -p > s.png # ekran görüntüsü
adb shell pm clear com.fxerkan.dhikrer   # veriyi sıfırla (ilk açılış testi)
adb shell "cmd uimode night yes|no"      # sistem karanlık/aydınlık mod
adb emu kill                      # emülatörü kapat
avdmanager list avd ; avdmanager delete avd -n <ad>   # AVD yönetimi
```

## Notlar
- Headless (`-no-window`, script'in kullandığı) yazılım GPU'su kullanır; **düzen/boyut** testi için idealdir. **Pixel-perfect renk** için pencereyle `-gpu auto` çalıştır.
- Uygulamanın paketi: `com.fxerkan.dhikrer`, açılış aktivitesi `com.fxerkan.zikirci.MainActivity`.
- İngilizce locale'de uygulama adı **Dhikrer**, Türkçe'de **Zikirci** görünür.

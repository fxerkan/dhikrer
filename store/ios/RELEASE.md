# App Store — Yayınlama Süreci / Release Process

Zikirci / Dhikrer'i **Apple App Store**'da yayınlamak için baştan sona süreç. iOS
uygulaması Capacitor WKWebView kabuğudur (aynı web UI, `docs/ios.md`). Android'i
etkilemez. Bundle id her iki platformda da `com.fxerkan.dhikrer`.

## 0. Ön koşullar (tek seferlik)

- **Apple Developer Program üyeliği** — yıllık **$99**. Ücretsiz kişisel takım
  dağıtım yapamaz (`docs/ios.md`: "Before App Store submission"). https://developer.apple.com/programs/
- **Mac + Xcode** (App Store'a yükleme yalnızca macOS'tan; full Xcode seçili olmalı:
  `sudo xcode-select -s /Applications/Xcode.app/Contents/Developer`).
- **App Store Connect** erişimi (Developer hesabıyla gelir): https://appstoreconnect.apple.com

## 1. App Store Connect'te kayıt oluştur

App Store Connect → **Apps → +** → New App:
- **Platforms:** iOS
- **Name:** `Dhikrer` (birincil dil EN önerilir; App Store'da uygulama adı **global
  olarak benzersiz** olmalı — "Dhikrer" çakışırsa küçük bir ek gerekir).
- **Primary language:** English (U.S.)
- **Bundle ID:** `com.fxerkan.dhikrer` (Xcode'dan otomatik kaydolur; yoksa Certificates,
  Identifiers & Profiles → Identifiers → + ile App ID oluştur).
- **SKU:** serbest benzersiz dize, örn. `dhikrer-ios-001`.
- **User Access:** Full.

## 2. Sürüm imzalama (release signing)

Debug için otomatik imzalama zaten kurulu (`docs/ios.md`). Dağıtım için:
- Xcode → App target → **Signing & Capabilities** → Team = ücretli takımın.
- **Automatically manage signing** açık → Xcode dağıtım sertifikası + App Store
  provisioning profilini kendi üretir. (Manuel istersen: Distribution certificate +
  App Store profil.)

## 3. Sürüm numarası

- **Marketing version** (`CFBundleShortVersionString`) — Android `versionName` ile hizala
  (şu an `1.2.3`; bkz. `CLAUDE.md` sürümleme).
- **Build** (`CFBundleVersion`) — App Store'a her yüklemede **artan** tamsayı (Android
  `versionCode` muadili). Xcode target → General, veya:
  ```bash
  agvtool new-marketing-version 1.2.3
  agvtool new-version -all 1
  ```

## 4. Web varlıklarını tazele + arşivle

```bash
node tools/gen_app.mjs .        # webapp → android assets (tek kaynak)
npm run ios:web                 # android assets → www/ (+ iOS shim)
npx cap copy ios                # www/ → Xcode projesi
```
Sonra Xcode'da: **Product → Archive** (destination = "Any iOS Device (arm64)").
Veya CLI ile:
```bash
xcodebuild -project ios/App/App.xcodeproj -scheme App -configuration Release \
  -destination 'generic/platform=iOS' -archivePath build/App.xcarchive archive
xcodebuild -exportArchive -archivePath build/App.xcarchive \
  -exportOptionsPlist ios/ExportOptions.plist -exportPath build/ipa
```
(ExportOptions.plist: `method=app-store-connect`, takım id'si — henüz repoda yok, ilk
gönderimde Xcode Organizer GUI'si daha kolay.)

## 5. Build'i yükle

- Xcode **Organizer** → arşivi seç → **Distribute App → App Store Connect → Upload**.
- veya `xcrun altool` / **Transporter** uygulaması ile `.ipa` yükle.
- Yükleme sonrası build App Store Connect'te **TestFlight** sekmesinde işlenir (birkaç dk).

## 6. Mağaza içeriğini gir (dil başına: tr / en / ar)

App Store Connect → uygulaman → **App Store** sekmesi → sürüm. Her dil için metinler
`store/shared/copy.json → listing.ios.<lang>` (özet: `store/ios/LISTING.md`):
- Name, Subtitle, Promotional Text, Keywords, Description.
- **Screenshots (6.9" iPhone, 1290×2796):** `store/ios/<lang>/hero-*.png` — LISTING.md'deki
  önerilen 6'lı sıra. App Store'un **feature graphic'i yoktur**.
- **App icon:** build'in asset kataloğundan gelir (1024×1024, alpha'sız — `docs/ios.md`).

## 7. Zorunlu meta veriler

- **Privacy Policy URL** (zorunlu): `docs/privacy.html` / `PRIVACY.md`'yi bir URL'de yayınla
  (ör. GitHub Pages) ve gir.
- **Support URL** (zorunlu): repo/README veya iletişim sayfası.
- **App Privacy (nutrition labels):** uygulama **hiçbir veri toplamaz** — her şey cihazda
  (`docs/ios.md`). "Data Not Collected" seç.
- **Age Rating:** anketi doldur → büyük olasılıkla **4+** (dini içerik reklamsız, veri yok).
- **Category:** Primary = **Lifestyle** (veya Reference). Secondary opsiyonel.
- **Export Compliance:** standart HTTPS dışında şifreleme yok → "uses non-exempt
  encryption? **No**" (Info.plist'e `ITSAppUsesNonExemptEncryption=false` eklenirse App
  Store Connect bir daha sormaz).
- **Price:** Free.

## 8. Gönder ve incelet

- Sürüme yüklediğin **Build**'i seç.
- **App Review Information → Notes (ZORUNLU):** `store/ios/APP_REVIEW_NOTES.md`
  içindeki hazır metni **olduğu gibi** yapıştır. Boş/zayıf Notes = yeni uygulamada
  neredeyse kesin **Guideline 2.1 "Information Needed"** reddi (ilk reddimizin sebebi
  buydu — kod hatası değil). Metin Apple'ın 7 sorusunu sırayla yanıtlar: ne yaptığı +
  hedef kitle, kurulum/erişim (giriş yok), harici servis yok, bölgesel fark yok,
  regüle sektör değil.
- **Demo hesabı:** yok — uygulama giriş/hesap istemez; "sign-in required = No" işaretle.
- **Ekran kaydı (gönderiye ekle):** GERÇEK bir iPhone'da (simülatör değil, en güncel iOS)
  `APP_REVIEW_NOTES.md`'deki shot-list akışını kaydet ve Resolution Center yanıtına ekle.
- **Save → Add for Review → Submit**. Apple incelemesi tipik **~24–48 saat**.
- Onay sonrası: manuel yayın veya otomatik. Reddedilirse Resolution Center'daki gerekçeye
  göre düzelt, yeniden gönder.

### Reddi önleme kontrol listesi (Apple review videolarından)

- **Notes + ekran kaydı** her yeni uygulama/major güncellemede hazır olsun (bkz. yukarı).
- **Purpose string'ler (5.1.1):** yalnızca gerçekten kullanılan izin için string olsun,
  *neden + örnek* içersin. Dhikrer sadece **bildirim** izni ister (günlük hatırlatıcı
  açılınca) — konum/kamera/kişiler/foto/ATT izni İSTEME, `Info.plist`'e o
  `NS*UsageDescription` anahtarlarını EKLEME (kullanılmayan string = 5.1.1 reddi).
- **Veri minimizasyonu:** uygulama hiçbir veri toplamaz; App Privacy = "Data Not
  Collected". Yeni bir izin/SDK eklenmeden önce "bu veri gerçekten gerekli mi?" diye sor.
- **İzin reddi:** kullanıcı bildirime izin vermezse uygulama sorunsuz çalışmalı; "fikrini
  değiştir" baskısı YAPMA.
- **Ekran görüntüleri (2.3.3):** uygulamayı gerçek kullanımda göster (splash/logo değil) —
  mevcut hero'lar zaten sayaç/ayar ekranlarını gösteriyor.

## 9. Her sürümde

- `CLAUDE.md` sürümleme kuralınca marketing version'ı bump et, build'i +1 artır.
- `CHANGELOG.md` (EN) + `CHANGELOG.tr.md` (TR)'ye ≤500 karakter "What's new" notu ekle
  (App Store "Promotional Text" ayrı, sürümsüz güncellenebilir).
- Görsel/ metin değiştiyse: `store/shared/copy.json`'u düzenle → `PLATFORM=ios node
  tools/shots.mjs && PLATFORM=ios python3 tools/frame.py && PLATFORM=ios python3
  tools/hero_set.py` ile hero'ları yeniden üret.

## Henüz repoda olmayan / manuel adımlar

- Ücretli Apple Developer üyeliği (satın alım).
- App Store Connect kaydı + dağıtım profili (ilk arşivde Xcode üretir).
- `ios/ExportOptions.plist` (CLI export için; GUI ile gerekmez).
- Privacy Policy'nin herkese açık URL'de yayınlanması.

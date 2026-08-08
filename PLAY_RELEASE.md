# Google Play — Yayın Hazırlığı

## Kodda yapıldı (bu sürüm, v1.1.0 / code 7)

- ✅ **AAB üretimi** — Play `.aab` ister: `./gradlew :app:bundleRelease`
  → `android/app/build/outputs/bundle/release/app-release.aab`
- ✅ **targetSdk / compileSdk 35** (Android 15) — Play'in güncel hedef API şartı.
- ✅ **Edge-to-edge** (Android 15 zorunlu) — sistem çubuğu boşlukları (insets)
  web arayüzüne aktarılıyor; başlık/menü güvenli alanda, çubuk ikon rengi temaya göre.
- ✅ **Kesin alarm izni kaldırıldı** (`USE_EXACT_ALARM`) — hatırlatıcılar artık
  inexact + Doze uyumlu (`setAndAllowWhileIdle`); Play "Exact alarm" politikası sorunu yok.
- ✅ **Foreground service tipi `specialUse`** (mediaPlayback yerine) — ses tuşuyla
  sayım için MediaSession'ı ayakta tutuyoruz, medya oynatmıyoruz. Manifest'te
  `PROPERTY_SPECIAL_USE_FGS_SUBTYPE` açıklaması var.
- ✅ **İmza sırları** `android/keystore.properties`'e taşındı (gitignore'lu),
  build ondan okuyor.
- ✅ 64-bit uyumlu (native kod yok, tüm ABI'ler), release debuggable değil, cleartext yok.

## Play Console'da senin yapman gerekenler (manuel)

1. **İmzalama** — Play App Signing'i aç. `zikirci-release.jks` **upload key**'in olur.
   (Gerçek yayında parolaları değiştir; `keystore.properties` gizli kalsın.)
2. **specialUse FGS onayı** — Play, `specialUse` için gerekçe formu sorar. Gerekçe:
   *"Kullanıcı ekran kapalıyken ses tuşlarıyla zikir sayacını ilerletebilsin diye
   MediaSession'ı canlı tutan kısa ömürlü foreground service."*
3. **Gizlilik Politikası URL'si** — zorunlu (bildirim izni var). Basit bir sayfa yeter.
4. **Data safety formu** — uygulama veri toplamıyor/paylaşmıyor (her şey cihazda,
   localStorage). "No data collected/shared" işaretle.
5. **İzin gerekçeleri** — POST_NOTIFICATIONS (hatırlatıcılar), FOREGROUND_SERVICE_SPECIAL_USE.
6. **Store görselleri** — 512×512 ikon, feature graphic (1024×500), en az 2 telefon
   ekran görüntüsü (Sayaç, Zikirler, İstatistik, Ayarlar zaten hazır).
7. **İçerik derecelendirme** anketi, hedef kitle, ülkeler.
8. **Uygulama adı** — Play Console'da lokalize et: TR listesi "Zikirci",
   EN listesi "Dhikrer" (cihazdaki ad zaten locale'e göre değişiyor). İkonu da
   liste bazında farklı koyabilirsin (istersen "Dhikrer" ikon varyantı hazırlarım).

## Yükleme
- Internal testing track'e `app-release.aab`'yi yükle → kendi hesabınla test et → prod'a taşı.
- Her yeni sürümde `versionCode` +1 (CLAUDE.md "Versioning").

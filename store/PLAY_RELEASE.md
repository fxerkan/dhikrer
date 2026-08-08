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
- Hesap: fxerkan@gmail.com (onay sürecinde). `_credentials/google-play-console.txt` şu an boş;
  API ile otomatik yükleme istersen oraya bir **service-account JSON** koy (Play Console →
  Setup → API access), sonra `fastlane`/`bundletool` ile CI'dan yükleyebiliriz.

## specialUse vs mediaPlayback — neden değiştirdik?
- **İşlevsel fark YOK.** Ses tuşlarını ekran kapalıyken yakalamak için canlı tuttuğumuz
  MediaSession, foreground service **tipinden bağımsız** çalışır. İkisi de süreci ayakta tutar.
- **mediaPlayback**: Play'in FGS politikası, tipin gerçek kullanımı yansıtmasını ister. Biz
  medya **oynatmıyoruz** → "media playback FGS ama medya yok" ihlali → **red/kaldırılma riski**.
  Bazı OEM'lerde de arka plan kısıtları daha sıkı. Artısı: Play ekstra form sormaz.
- **specialUse**: Standart tiplere girmeyen kullanımların **doğru** karşılığı. Artısı: politika
  uyumlu. Eksisi: Play tek seferlik kısa bir **gerekçe formu** ister (yukarıda hazır metin var).
- **Karar:** Play için `specialUse` doğru ve risksiz seçim; özellikte hiçbir kayıp yok.
  (Sadece Play dışı sideload isteseydik `mediaPlayback` de sorunsuz çalışırdı.)

## Android sürüm desteği (12 → 17)
- **minSdk 26 (Android 8)** → uygulama Android **8'den itibaren** kurulur; yani 12–16 tamamen
  desteklenir, ileride 17 çıkınca da çalışır (ileri uyumlu). 12–16 emülatörde **test edildi**.
- **targetSdk 35, Android 15 GEREKTİRMEZ.** Sadece 15'in davranışlarına (edge-to-edge vb.)
  uyum sağlar; eski sürümlerde zarif şekilde ele alınır:
  - edge-to-edge inset'leri her sürümde uygulanıyor (eski sürümde status bar yüksekliği).
  - specialUse FGS tipi yalnız Android 14+ için ayarlanıyor (`if SDK>=34`), eskide düz FGS.
  - Hatırlatıcılar inexact — her sürümde çalışır. POST_NOTIFICATIONS runtime izni 13+; eskide otomatik.
- **Hiçbir özellik sürümden dolayı eksilmiyor.** İstersen minSdk'yı 24/21'e indirip daha da
  eski cihazları (Android 7/5) kapsayabiliriz — söylemen yeter.

## "Elde telefon + ses tuşu" hero görseli

Kod tarafı (kredisiz, deterministik): `tools/hero.py` (v1, alttan gelen tek parmak) ve
`tools/hero_v2.py` (arkadan kavrayan **vektörel beyaz ghost el**, sol kenardan kıvrılan 4 parmak +
ses tuşunda `+1` tıklama baloncuğu). Her yeni deneme versiyonlu isimle yazılır (`-v2`, `-v3`…),
öncekiler **ezilmez**. Çıktılar `store-screenshots/hero-volume-keys[-vN].png`.

### Gemini Nano Banana promptu (image-to-image — app screenshot'ı referans yükle)
Referans olarak temiz uygulama ekran görüntüsünü (ör. `store-screenshots/01-sayac-klasik-gece.png`
veya framed hâli) yükle, sonra:

> Use the provided Zikirci app screenshot as the exact phone screen. Keep the entire on-screen UI
> 100% identical and undistorted — same dark counter screen, the "47" counter, top bar, bottom
> navigation, all colors and text. Do NOT redraw, move, recolor or alter any UI element or text.
>
> Composite ONLY these overlays on top, in a clean FLAT VECTOR / illustration style (NOT
> photorealistic, no realistic skin, no fingernails, no shading detail):
> 1. A semi-transparent ghost-WHITE minimalist vector HAND silhouette holding the phone FROM
>    BEHIND: the back of the hand and wrist enter from the lower-left corner; four slim fingers
>    wrap around so their rounded fingertips curl over the phone's LEFT edge; a thumb rests on the
>    lower-left front. ~25–30% opacity white fill with a thin crisp white outline. Simple, elegant,
>    like a UI illustration. It must stay BEHIND/faint — never cover the "47" counter or the text.
> 2. At the LEFT volume-up button: a small "tap" click indicator — two concentric translucent
>    white ripple rings plus a purple accent ring — and a small purple "+1" speech bubble pointing
>    to that button.
>
> Background: keep the existing dark indigo→purple gradient. Vertical 9:16 phone format. Premium,
> minimal Google-Play feature-graphic look; the app UI sharp and in front, the white vector hand
> faint behind.
>
> Negative: photorealistic hand, realistic skin, hand covering the screen content, altered/blurred
> UI, changed text, extra fingers, warped phone.

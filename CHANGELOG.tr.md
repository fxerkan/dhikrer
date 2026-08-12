# Sürüm Notları — Zikirci (Dhikrer)

Uygulamadaki tüm önemli değişiklikler burada belgelenir. Biçim büyük ölçüde
[Keep a Changelog](https://keepachangelog.com/) yapısını izler; sürümler semver
**MAJOR.MINOR.PATCH** kuralına uyar (bkz. [`CLAUDE.md`](CLAUDE.md)). English: [`CHANGELOG.md`](CHANGELOG.md).

Her sürümde ayrıca bir **Mağaza sürüm notu** vardır — düz metin, ≤500 karakter — Google Play
"Yenilikler" alanına ve App Store "Yenilikler" bölümüne doğrudan yapıştırılabilir.

---

## [1.3.0] — 2026-08-12 · versionCode 13

- **Eklendi: kalıcı veri güvencesi** — zikir listen, ayarların ve istatistiklerin artık kalıcı
  cihaz depolamasına da yedekleniyor ve yerel veri herhangi bir nedenle kaybolursa (WebView
  temizliği, yeniden kurulum, cihaz değişimi) otomatik geri yükleniyor. Uygulama güncellemeleri
  verini zaten koruyordu; bu, daha fazla durumu kapsayan ikinci bir katman ekler.
- **Eklendi: özelleştirme ekranında hedef düzenleme** — zikir özelleştirme penceresinde artık
  Hedef değerini doğrudan değiştirebilirsin (önceden yalnızca ad + titreşim vardı).
- **İyileştirildi: daha temiz titreşim seçenekleri** — Titreşim Şekli ve Şiddeti yalnızca
  Titreşim açıkken görünüyor.
- **Eklendi: Yardım ve puanlama butonları** — Ayarlar'a Yardım & Destek ve Play Store'da Puan
  Ver butonları eklendi. Yardım & Destek, e-posta uygulamasını dile göre konu ve uygulama
  sürümü önceden dolu olarak açar; adresi (dhikrer@fxerkan.com) doğrudan gösterir.
- **Eklendi: "Her 100" bildirim noktası** — her yüzde bir tekrarlayan bildirim (100, 200 … 900);
  bu nokta artık açıkça "Her 100" olarak etiketleniyor.
- **İyileştirildi: yerelleştirilmiş footer markası** — Ayarlar footer'ı uygulama adını geçerli
  dilde (Dhikrer / Zikirci …), "-er" vurgusuyla gösteriyor.
- **Düzeltildi: tablette Tesbih (beads) yerleşimi** — yatay modda kısayol tuşları artık sayacın
  üstüne binmiyor.
- **Güncellendi:** Google Play'in hedef API düzeyi şartını karşılamak için artık Android 16
  (API 36) hedefleniyor (compile + target SDK 35 → 36).

> **Mağaza sürüm notu (TR):**
> Zikirlerin, ayarların ve istatistiklerin artık daha güvende — cihazda yedekleniyor ve kaybolursa
> otomatik geri yükleniyor. Özelleştirme ekranında zikir hedefini artık değiştirebilirsin; titreşim
> şekli/şiddeti yalnızca titreşim açıkken görünür. Ayrıca Android 16 hedeflenecek şekilde güncellendi.

## [1.2.3] — 2026-08-11 · versionCode 11

Yalnızca mağaza sunumu — uygulama davranışında değişiklik yok.

- Yeni Google Play hero görsel seti eklendi: ses tuşu + el, reklamsız, özelleştirme, kolay
  kullanım, istatistik ve diller (bkz. `store/store-screenshots/hero-*-v1.png`).
- Liste metninde uygulama adı vurgusu ve tazelenmiş mağaza kopyası.
- Liste görsellerini üretmek için yeni çerçeveleme/hero araçları.

> **Mağaza sürüm notu (TR):**
> Play Store için yeni görseller ve liste metni. Uygulamanın çalışma biçiminde değişiklik yok —
> aynı hızlı, reklamsız ve gizliliğe saygılı zikirmatik.

## [1.2.2] — 2026-08-09 · versionCode 10

- **Düzeltildi:** ses tuşuyla sayım artık ekran kapalıyken de daha güvenilir çalışıyor.
- **Düzeltildi:** her sayımda tık/dokunma sesi doğru şekilde çalıyor.
- **İyileştirildi:** arka plan ayak izi azaltıldı (boştayken daha az pil/bellek kullanımı).

> **Mağaza sürüm notu (TR):**
> Hata düzeltmeleri: ekran kapalıyken daha güvenilir ses tuşu sayımı, doğru tık sesi ve daha
> düşük arka plan tüketimiyle daha iyi pil ömrü.

## [1.2.1] — 2026-08-08 · versionCode 9

- **Eklendi: Kilit modu** — yalnızca sayaç dokunuşlara ve ses tuşlarına yanıt verir; telefon
  cebindeyken yanlışlıkla sayımı önler.
  (Ekran görüntüsü: `store/store-screenshots/04-kilit-kehribar-v1.png`.)
- **İyileştirildi: daha net istatistik grafikleri** — günlük/haftalık eğilimler ve dağılım
  daha okunaklı.
  (Ekran görüntüsü: `store/store-screenshots/07-istatistik-okyanus-v1.png`.)

> **Mağaza sürüm notu (TR):**
> Yeni Kilit modu cebinizdeyken sayımı doğru tutar — yalnızca sayaç yanıt verir. Ayrıca daha
> net ve okunaklı istatistik grafikleri.

## [1.1.0] — versionCode 7

Google Play'e hazırlık ve platform uyumluluğu sürümü.

- **Eklendi:** Play dağıtımı için Android App Bundle (`.aab`) üretimi.
- **Güncellendi:** targetSdk / compileSdk **35** (Android 15) — Play'in güncel hedef API şartı.
- **Eklendi:** edge-to-edge düzen — sistem çubuğu boşlukları (insets) web arayüzüne aktarılıyor;
  içerik güvenli alanda kalıyor, çubuk ikon rengi temaya göre değişiyor.
- **Değişti:** kesin alarm izni kaldırıldı; hatırlatıcılar artık Doze uyumlu inexact alarmlar.
- **Değişti:** ekran kapalı ses tuşu sayımı için foreground service tipi `specialUse`
  (önceden `mediaPlayback`) — aynı davranış, Play politikasına uygun.
- **Değişti:** imza sırları gitignore'lu `android/keystore.properties` dosyasına taşındı.
- 64-bit / tüm ABI'ler, release debuggable değil, cleartext trafik yok.

> **Mağaza sürüm notu (TR):**
> Google Play'e hazır sürüm: Android 15 edge-to-edge desteği, pil dostu hatırlatıcılar ve
> politikaya uygun arka plan sayımı. Özellikler aynı, platform davranışı daha iyi.

## [1.0.0] – [1.0.5] — temel sürüm serisi (eski 2 parçalı `1.0`–`1.5`)

İlk yayınlar uygulamanın tamamını oluşturdu:

- **Sayaç** 0–999, "bin" göstergesiyle; yukarı **veya** aşağı sayım; kaldığın yerden devam.
- **Her yerde say:** büyük dokunma butonu, fiziksel **ses tuşları (ekran kapalı)** ve yeniden
  boyutlanabilen **ana ekran widget'ı**.
- **Üç sayaç tasarımı:** Klasik halka, Birleşik dev buton ve 33 / 66 / 99 ayraç boncuklu
  Tesbih halkası.
  (Ekran görüntüleri: `store/store-screenshots/01-sayac-klasik-gece-v1.png`,
  `02-tespih-zumrut-v1.png`, `03-birlesik-gul-v1.png`.)
- **Kilometre taşları:** 33, 66, 99, 100, 999, 1000'de titreşim + ses — her biri ayrı ayrı açılıp
  kapatılabilir.
- **Zikirlerim:** sınırsız zikir kaydet, zikir başına ses & titreşim, sabitle, sırala, kaydırarak sil.
  (Ekran görüntüsü: `store/store-screenshots/06-zikirler-gece-v1.png`.)
- **Hatırlatıcılar:** seçtiğin saatlerde günlük bildirimler.
- **İstatistik:** git tarzı yoğunluk ısı haritası, seriler, günlük/haftalık/aylık eğilimler ve
  dağılım halkası — hepsi cihazda, gerçek sayım geçmişinden.
- **10 tema** (koyu & açık), **6 dil** (TR, EN, AR — RTL dahil, ID, HI, ZH), tam buton
  özelleştirmesi (boyut/şekil/renk/konum) ve animasyon efektleri (halka / dalga / dolum / şekil-morph).
  (Ekran görüntüsü: `store/store-screenshots/10-arapca-rtl-gece-v1.png`.)
- **Önce gizlilik:** reklam yok, hesap yok, telemetri yok, yalnızca çevrimdışı — her şey cihazda kalır.

> **Mağaza sürüm notu (TR):**
> Zikirci — hızlı, reklamsız ve gizli bir zikirmatik. Dokunarak, ses tuşuyla veya ana ekran
> widget'ıyla say; Klasik / Birleşik / Tesbih tasarımları, kilometre taşları, hatırlatıcılar,
> cihazda istatistik, 10 tema, RTL dahil 6 dil.

---

## Planlanan (yol haritası)

Henüz yayınlanmadı — changelog yönü yansıtsın diye burada tutuluyor:

- 🎧 Bluetooth kulaklık entegrasyonu — Bluetooth kulaklık tuşlarıyla say/kontrol et.
- 🔊 Zikir seslendirme — aktif zikrin sesli okunması.
- 📊 İstatistik widget'ı — günlük sayım, seri ve ilerleme için ana ekran widget'ı.
- 📤 Zikir paylaşma — zikirleri ve ilerlemeyi başkalarıyla paylaş.

[1.2.3]: #123--2026-08-11--versioncode-11
[1.2.2]: #122--2026-08-09--versioncode-10
[1.2.1]: #121--2026-08-08--versioncode-9
[1.1.0]: #110--versioncode-7

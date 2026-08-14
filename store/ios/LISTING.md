# App Store — Uygulama Bilgileri / App Information

Tüm metinler **tek kaynak** `store/shared/copy.json` → `listing.ios` içinden gelir; burada
sadece okunur özet + karakter limitleri var. Metni **orada** düzenle.

App Store limitleri: **Ad (name)** ≤30, **Alt başlık (subtitle)** ≤30, **Anahtar kelimeler
(keywords)** ≤100 (virgülle, boşluksuz), **Tanıtım metni (promotional text)** ≤170,
**Açıklama (description)** ≤4000.

Üç dil yerelleştirmesi (App Store Connect locale): **tr = Türkçe**, **en = İngilizce (ABD)**,
**ar = Arapça**. Cihazdaki uygulama adı zaten cihaz diline göre değişir (tr=Zikirci,
en=Dhikrer, ar=الذّاكِر — bkz. `docs/ios.md`).

> ⚠️ Android'den fark: **iOS'ta fiziksel ses tuşuyla sayma YOK** (iOS donanım ses tuşlarını
> uygulamalara vermez — `docs/ios.md`). Bu yüzden iOS açıklamaları ve hero'ları ses-tuşu
> özelliğini **içermez**; yerine dokunsal geri bildirim + kilit modu öne çıkar.

---

## 🇹🇷 Türkçe

- **Ad:** `Zikirci`
- **Alt başlık:** `Reklamsız, sade zikirmatik`
- **Anahtar kelimeler:** `zikir,tesbih,zikirmatik,tespih,dua,namaz,sayaç,dhikr,islam,müslüman`
- **Tanıtım metni / Açıklama:** `copy.json → listing.ios.tr`

## 🇬🇧 English

- **Name:** `Dhikrer`
- **Subtitle:** `Ad-free, simple dhikr counter`
- **Keywords:** `dhikr,tasbih,tasbeeh,counter,zikr,islam,muslim,prayer,rosary,misbaha`
- **Promotional text / Description:** `copy.json → listing.ios.en`

## 🇸🇦 العربية

- **الاسم:** `الذّاكِر`
- **العنوان الفرعي:** `عدّاد ذِكر بسيط بلا إعلانات`
- **الكلمات المفتاحية:** `ذكر,تسبيح,مسبحة,عداد,دعاء,صلاة,مسلم,اسلام,سبحة`
- **النص الترويجي / الوصف:** `copy.json → listing.ios.ar`

---

## Görseller / Assets

App Store'un feature-graphic'i **yoktur** (o Google Play'e özgü). Gerekenler:

- **Uygulama ikonu (1024×1024, alpha'sız):** `store/shared/store-icon-1024.png`.
  Not: App Store Connect ikonu genelde build'in asset kataloğundan (`AppIcon`) alır;
  bu dosya yedek/pazarlama kopyasıdır.
- **iPhone 6.9" ekran görüntüleri (1290×2796, portrait)** — dil başına 6 hero, önerilen sıra
  (özellik öncelikli). `<lang>` = tr/en/ar:

  1. `store/ios/<lang>/hero-easy.png` — Sade, kullanımı kolay
  2. `store/ios/<lang>/hero-ad-free.png` — Reklamsız, çevrimdışı
  3. `store/ios/<lang>/hero-customize.png` — Özelleştirilebilir
  4. `store/ios/<lang>/hero-stats.png` — İstatistik
  5. `store/ios/<lang>/hero-languages.png` — Çoklu dil + RTL
  6. `store/ios/<lang>/hero-lock.png` — Kilit modu

  Tek bir 6.9" seti tüm iPhone'ları kapsar (App Store artık daha küçük boyutları
  6.9"'dan ölçekler). iPad'i ayrıca yayınlamak istersen 13" (2064×2752) seti gerekir.

Üretim (repo kökünden, `node tools/gen_app.mjs .` sonrası):
```bash
PLATFORM=ios node tools/shots.mjs      # store/ios/<lang>/_raw/  (6 ekran × tr/en/ar)
PLATFORM=ios python3 tools/frame.py    # → framed/ (iPhone Dynamic Island çerçevesi)
PLATFORM=ios python3 tools/hero_set.py # → store/ios/<lang>/hero-*.png (1290×2796)
```
Süreç ve gönderim adımları: `store/ios/RELEASE.md`.

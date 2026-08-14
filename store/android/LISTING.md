# Google Play — Mağaza İçeriği / Store Listing

Play limitleri: **Başlık** ≤30, **Kısa açıklama** ≤80, **Tam açıklama** ≤4000 karakter.
İki liste yerelleştirmesi: **TR → Zikirci**, **EN → Dhikrer** (cihazdaki ad zaten locale'e göre değişir).

---

## 🇹🇷 Türkçe liste

**Uygulama adı:** `Zikirci`

**Kısa açıklama** (80):
`Reklamsız, tümüyle özelleştirilebilir, sade ve kolay kullanılabilir zikirmatik.`

**Tam açıklama:**

```
Zikirci — sade, hızlı ve dikkat dağıtmayan bir dijital tesbih (zikirmatik).

⭐ ÖNE ÇIKANLAR
• Reklamsız. Takip yok, hesap yok — her şey cihazında, çevrimdışı çalışır.
• Kullanımı kolay — tek dokunuşla say, sade arayüz, dağıtan hiçbir şey yok.
• Özelleştirilebilir tasarım — 10 tema, sayaç şekilleri, tesbih/birleşik/klasik düzenler.
• Kilit modu — cebindeyken yanlışlıkla sayımı önler.
• Hedef ve tesbih modları — 33 / 66 / 99 ayraçları, serbest sayım.
• Fiziksel ses tuşuyla say — ekran kapalıyken bile zikrine devam et.
• İstatistik — ısı haritası, günlük ve haftalık ilerleme.
• Çoklu dil ve tam sağdan-sola (RTL) desteği.

Kısacası: reklamsız, gizliliğe saygılı, hızlı bir zikir sayacı. İster ekrana dokun,
ister ses tuşuna bas — sen zikrine odaklan, saymayı Zikirci halletsin.
```

---

## 🇬🇧 English listing

**App name:** `Dhikrer`

**Short description** (80):
`Ad-free dhikr counter — volume-key count, offline, fully customizable.`

**Full description:**

```
Dhikrer — a simple, fast, distraction-free digital tasbih (dhikr counter).

⭐ HIGHLIGHTS
• Ad-free. No tracking, no account — everything stays on your device, works offline.
• Easy to use — one tap to count, clean UI, zero clutter.
• Customizable design — 10 themes, counter shapes, tasbih / unified / classic layouts.
• Goal & tasbih modes — 33 / 66 / 99 markers, or free counting.
• Lock mode — prevents accidental counts in your pocket.
• Count with the physical volume keys — keep going even with the screen off.
• Statistics — heatmap, daily and weekly progress.
• Multi-language with full right-to-left (RTL) support.

In short: an ad-free, privacy-respecting, fast dhikr counter. Tap the screen or press a
volume key — you focus on the dhikr, let Dhikrer handle the counting.
```

---

## Görseller / Assets

Tüm metin **tek kaynak** `store/shared/copy.json`. Üretim: `node tools/gen_app.mjs .`
sonrası `node tools/shots.mjs && python3 tools/frame.py && python3 tools/hero_set.py &&
python3 tools/store_assets.py` (varsayılan `PLATFORM=android`).

- **Feature graphic** (1024×500, yatay — Play'e özgü): `store/shared/store-icon-512.png`
  ile birlikte `store/android/<lang>/feature-graphic-1024x500.png` (dil başına).
- **Telefon ekran görüntüleri** (portrait) — dil başına 6 hero, önerilen sıra
  (özellik öncelikli). `<lang>` = tr/en/ar:

  1. `store/android/<lang>/hero-ad-free.png`
  2. `store/android/<lang>/hero-easy.png`
  3. `store/android/<lang>/hero-customize.png`
  4. `store/android/<lang>/hero-volume.png` — ses tuşuyla say (Android'e özgü)
  5. `store/android/<lang>/hero-stats.png`
  6. `store/android/<lang>/hero-languages.png`
- Hiçbir hero'da **el/parmak çizilmez** (bkz. memory: nano-banana-only). İsteğe bağlı
  ses-tuşu el görseli yalnızca **Gemini nano banana** ile: `NB_MODEL=gemini-3-pro-image
  NB_SIZE=2K python3 tools/nano_banana.py OUT.png "PROMPT" IN.png`.
- Eski TR-only / -v1 çıktılar: `store/android/_legacy-screenshots/`.

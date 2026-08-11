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
`Ad-free dhikr counter — count with volume keys, works offline, fully customizable.`

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

- **Feature graphic** (1024×500): ayrıca üret (yatay). Şimdilik hero'lardan biri kırpılabilir.
- **Telefon ekran görüntüleri** (portrait) — önerilen sıra (özellik öncelikli):

  1. @store/store-screenshots/hero-ad-free-v1.png
  2. @store/store-screenshots/hero-easy-v1.png
  3. @store/store-screenshots/hero-customize-v1.png
  4. @store/store-screenshots/hero-volume-button-counter-hand-v3.png
  5. @store/store-screenshots/hero-stats-v1.png
  6. @store/store-screenshots/hero-languages-v1.png
- **Ses tuşu hero'su (el görseli)**: yalnızca **Gemini nano banana** ile üretilir/düzeltilir —
  `NB_MODEL=gemini-3-pro-image NB_SIZE=2K python3 tools/nano_banana.py OUT.png "PROMPT" IN.png`.
  (`hero-volume-button-counter-hand-v3.png` = v1'in yazıları düzeltilmiş hâli: Sayaç/Kilitli/Sübhânallah.)
- Diğer (elsiz) hero'lar: `python3 tools/hero_set.py` — her özellik için farklı arka plan rengi +
  çerçeveli telefon + başlık. Çıktı `store-screenshots/hero-*-v1.png`. **El/parmak çizmez.**

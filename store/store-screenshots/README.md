# Store görselleri — Zikirci / Dhikrer

Hepsi gerçek uygulamadan (headless Chrome, WebView ile birebir render), 1350×2925 yüksek çözünürlük.

- **`*.png`** (bu dizin) — çerçevesiz ham ekran görüntüleri.
- **`framed/*.png`** — her birinin etrafında modern Android telefon çerçevesi (sol yan **ses tuşları** + sağ güç tuşu, punch-hole kamera). Play'e doğrudan yüklenebilir.
- **`hero-volume-keys*.png`** — "ses tuşlarıyla say" özelliğini vurgulayan tanıtım görseli (gerçek Zikirci ekranı + volume tuşuna +1 callout).

## Sürümleme

- **Eksiz isim** (`02-tespih-zumrut.png`) = **eski/orijinal** sürüm (git geçmişinden geri getirildi).
- **`-v1`** = **bu turda üretilen, güncel/en iyi** sürüm — Play'e bunları yükle. Sonraki turlarda `-v2`, `-v3`…
- Hiçbir eski sürüm ezilmez; her tur yeni sürüm ekler.
- Bu turda düzeltilen kritik hata: **tespih/birleşik tasarımda sayaç ile kontrol butonlarının üst üste binmesi** (artık düzeldi). Tespih hedefleri **66 / 33** (99 değil). Yeni: **koyu tema ayarlar** ekranı (`15-ayarlar-gece`).

## İçerik (sıralamayı sen seçeceksin — güncel set: `-v1`)

| Dosya | Ekran | Tema | Öne çıkan |
|---|---|---|---|
| 01-sayac-klasik-gece | Sayaç (klasik/halka) | Gece (koyu) | Ana sayaç, ilerleme halkası |
| 02-tespih-zumrut | Sayaç (Tesbih) | Zümrüt | 66'lık tesbih, 33/66 ayraçlar |
| 03-birlesik-gul | Sayaç (Birleşik) | Gül (açık) | Tek parça dev buton |
| 04-kilit-kehribar | Sayaç (Kilit) | Kehribar | Kilitli mod — büyük kilit rozeti |
| 05-sayac-kare-buz | Sayaç (kare şekil) | Buz (açık) | Sayaç şekli seçenekleri |
| 06-zikirler-gece | Zikirler | Gece | İlerleme kartları, pin |
| 07-istatistik-okyanus | İstatistik | Okyanus | Isı haritası, KPI, grafikler |
| 08-ayarlar-lavanta | Ayarlar | Lavanta | 10 tema, tüm ayarlar |
| 09-tespih-yakut-33 | Sayaç (Tesbih) | Yakut | 33'lük tesbih |
| 10-arapca-rtl-gece | Sayaç (Arapça RTL) | Gece | Çoklu dil / RTL |
| 11-modern-klasik | Sayaç | Modern (açık) | Açık tema varyasyonu |
| 12-istatistik-gece-gunluk | İstatistik (günlük) | Gece | Saatlik grafik + data label |
| 13-zikirler-zumrut | Zikirler | Zümrüt | Kütüphane (açık aksan) |
| 14-dalga-okyanus | Sayaç (Dalga efekti) | Okyanus | Animasyon efektleri |
| 15-ayarlar-gece | Ayarlar | Gece (koyu) | Koyu tema ayarlar ekranı |

**Play için önerilen ilk 8 sıra:** 01, 02, 03, 07, 06, 15, 04, 10.

## Yeniden üretmek
`node tools/shots.mjs`  (server :8790'da `shot.html` açıkken) → sonra `python3 tools/frame.py` ve `python3 tools/hero.py`.

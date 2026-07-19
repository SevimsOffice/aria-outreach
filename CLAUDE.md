# ARIA — Otomatik B2B Outreach Sistemi

Türk OSB (Organize Sanayi Bölgesi) üreticilerine yapay zeka verimlilik atölyesi
satan otomatik soğuk e-posta sistemi. Sahibi: Sevim Durmuş (aiandtech-info.com).

## Bu repoda çalışırken bilmen gereken 4 mimari gerçek

1. **Asıl e-posta içeriği bu repoda DEĞİL, Instantly'de.** Konu, gövde ve takip
   dizisi Instantly kampanya editöründe durur. ARIA sadece `{{personalization}}`
   değişkenini (kişiselleştirilmiş açılış cümlesi) üretip lead ile birlikte
   Instantly'ye gönderir. `templates/email_*.txt` dosyaları referanstır,
   gönderim yolunda kullanılmaz.
2. **Cron `main` branch'inden çalışır.** `.github/workflows/daily_pipeline.yml`
   her gün 04:00 UTC'de (07:00 TR) `main`'i koşturur. Feature branch'te kalan
   fix prod'a gitmez — bu yüzden 2 hafta boyunca 0 mail gitti. Fix'i bitirince
   kullanıcı onayıyla main'e merge et.
3. **Instantly v2 STATUS_MAP tuzağı:** `3 = completed` (durdurulmuş değil!),
   `4 = running_subsequences`. Lead'siz kampanya anında "completed" olur; lead
   ekledikten sonra `POST /api/v2/campaigns/{id}/activate` ile yeniden
   başlatılmalı. `PATCH {"status": 1}` ÇALIŞMAZ — `activate_campaign()` kullan
   (`src/outreach/instantly_client.py`).
4. **Veri kaynağı Google Sheet'tir** (Excel değil): `GOOGLE_SHEET_ID` secret'ı,
   sekme `ARIA_Prospects`. Satır, yalnızca Instantly ekleme BAŞARILIYSA yazılır
   (`scripts/run_daily_pipeline.py`) — "log'da var, Sheet'te yok" ise Instantly
   çağrısı 200 dönmemiştir.

## ASLA yapılmayacaklar (Sevim'in açık talimatları)

- **`allow_risky_contacts=true` YAPMA.** Bir kez yapıldı, geri alındı, Sevim
  açıkça yasakladı ("bunu yapma"). Domain itibarını bounce'larla yakar.
- **`source` alanı `guessed` ile başlayan hiçbir adresi Instantly'ye ekleme.**
  Filtre `run_daily_pipeline.py` ve `run_resend_from_sheet.py` içinde — kaldırma.
- **Yeni Instantly kampanyası oluşturma, mevcut kampanyayı silme.** Kampanya ID
  `INSTANTLY_CAMPAIGN_ID` secret'ındadır; ayarlarını düzelt, kendisini yeniden
  yaratma.
- **PR açma** — kullanıcı açıkça istemedikçe.
- Gönderici domain her müşteride ayrıdır; asıl web sitesi domain'inden asla
  gönderim kurma.

## Günlük komutlar

```bash
python scripts/run_daily_pipeline.py --dry-run --limit 10   # önce hep dry-run
python scripts/fix_campaign.py                              # kampanya/hesap onarımı
python scripts/run_resend_from_sheet.py --limit 30          # Sheet → Instantly
python scripts/diagnose.py                                  # durum teşhisi
```

GitHub Actions karşılıkları: `daily_pipeline.yml` (cron + manuel),
`fix_campaign.yml`, `resend_from_sheet.yml`, `diagnose.yml`,
`reply_handler.yml`, `weekly_report.yml` — hepsi workflow_dispatch ile elle
tetiklenebilir.

## Enrichment zinciri (sıra önemli)

OSB kaydı (`*_direct`) → firma sitesi (`website_scraper.py`) → Apollo →
Hunter → tahmin (`email_guesser.py`, gönderilmeden filtrelenir).
Apollo ücretsiz planda 422 döner (API ücretli planda). Hunter kotası 25/ay.

## Secrets (GitHub → Settings → Secrets)

`ANTHROPIC_API_KEY`, `INSTANTLY_API_KEY`, `INSTANTLY_CAMPAIGN_ID`,
`GOOGLE_SERVICE_ACCOUNT_JSON`, `GOOGLE_SHEET_ID`, `HUNTER_API_KEY`,
`APOLLO_API_KEY` (opsiyonel), `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`,
`DAILY_SEND_LIMIT` (hedef: 100).

## Yol haritası bağlamı

Çok-müşterili yapıya geçiliyor (`clients/<isim>/client.yaml` planı) — ikinci
müşteri: Konya Teşvik (ayrı klonda). Supabase + Lovable panel Aşama 2.
Detay: `ARIA.md` (dürüst durum değerlendirmesi) ve `aria_satis.md` (kök neden
analizi). Bu iki dosyayı güncel tut: sistemsel bir kök neden bulunduğunda
`aria_satis.md`'ye ekle.

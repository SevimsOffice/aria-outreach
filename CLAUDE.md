# ARIA — Otomatik B2B Outreach Sistemi

Türk OSB (Organize Sanayi Bölgesi) üreticilerine yapay zeka verimlilik atölyesi
satan otomatik soğuk e-posta sistemi. Sahibi: Sevim Durmuş (aiandtech-info.com).

## Bu repoda çalışırken bilmen gereken mimari gerçekler

0. **Instantly aboneliği Temmuz 2026'da iptal edildi (`402 Payment Required`).**
   Gönderim artık kendi Hostinger mailbox'ından SMTP ile yapılıyor
   (`src/outreach/smtp_sender.py`, `scripts/run_send_smtp.py`,
   `.github/workflows/smtp_send.yml`). `run_daily_pipeline.py` artık
   `SEND_MODE=smtp` (varsayılan) ile çalışır: scrape → enrich → Sheet'e yaz,
   gönderme kısmına dokunmaz. Instantly kodu (`instantly_client.py`,
   `fix_campaign.py`, `run_resend_from_sheet.py`) `SEND_MODE=instantly` ile
   hâlâ çalışır — abonelik yenilenirse tek satır env değişikliğiyle geri
   dönülebilir, ama şu an ÖLÜ.
1. **Asıl e-posta içeriği artık repoda:** `templates/email_initial_tr.txt` +
   `email_followup1_tr.txt` + `email_followup2_tr.txt` — SMTP modunda gerçekten
   gönderilen dosyalar bunlar. (Instantly modunda konu/gövde Instantly kampanya
   editöründeydi — o mod artık kullanılmıyor.)
2. **Cron `main` branch'inden çalışır.** `.github/workflows/daily_pipeline.yml`
   her gün 04:00 UTC'de (07:00 TR) `main`'i koşturur. Feature branch'te kalan
   fix prod'a gitmez. Fix'i bitirince kullanıcı onayıyla main'e merge et.
3. **Warmup yok, tempolama elle yapılır.** SMTP modunda Instantly'nin warmup/
   hız sınırlama altyapısı yok — `run_send_smtp.py` günlük limiti düşük tutar
   (varsayılan 20) ve gönderimler arası 45-90sn bekler. Limiti hızlı artırma;
   yanıt/şikayet oranına göre haftalık +10 kademeli artır.
4. **Veri kaynağı Google Sheet'tir** (Excel değil): `GOOGLE_SHEET_ID` secret'ı,
   sekme `ARIA_Prospects`. SMTP modunda satır, enrichment BAŞARILIYSA
   (doğrulanmış e-posta bulunduysa) `ARIA_Status` boş olarak yazılır —
   gönderim ayrı bir adım (`run_send_smtp.py`) tarafından yapılır ve durumu
   `Email1_Sent` / `Email2_Sent` / `Email3_Sent` olarak günceller.

## ASLA yapılmayacaklar (Sevim'in açık talimatları)

- **`allow_risky_contacts=true` YAPMA** (Instantly modu için geçerli kalır).
  Bir kez yapıldı, geri alındı, Sevim açıkça yasakladı ("bunu yapma"). Domain
  itibarını bounce'larla yakar.
- **`source` alanı `guessed` ile başlayan hiçbir adresi gönderime ekleme.**
  Filtre `run_daily_pipeline.py` ve `run_send_smtp.py` içinde — kaldırma.
- **Günlük SMTP limitini elle/aceleyle yükseltme.** Warmup yok — yüksek hacim
  spam klasörüne düşme riski taşır. Kademeli artır.
- **PR açma** — kullanıcı açıkça istemedikçe.
- Gönderici domain her müşteride ayrıdır; asıl web sitesi domain'inden asla
  gönderim kurma.
- **Instantly kodunu silme** — `SEND_MODE=instantly` ile hâlâ çalışır, abonelik
  yenilenirse geri dönüş yolu.

## Günlük komutlar

```bash
python scripts/run_daily_pipeline.py --dry-run --limit 10   # önce hep dry-run (scrape+enrich+Sheet)
python scripts/run_send_smtp.py --dry-run --limit 5         # gönderim önizleme
python scripts/run_send_smtp.py --limit 20                  # gerçek gönderim (Sheet → SMTP)
```

GitHub Actions karşılıkları: `daily_pipeline.yml` (cron + manuel, scrape+enrich),
`smtp_send.yml` (cron + manuel, gönderim), `reply_handler.yml`,
`weekly_report.yml` — hepsi workflow_dispatch ile elle tetiklenebilir.
Instantly-modu workflow'ları (`fix_campaign.yml`, `resend_from_sheet.yml`,
`diagnose.yml`) abonelik iptaliyle işlevsiz kaldı, silinmedi.

## Enrichment zinciri (sıra önemli)

OSB kaydı (`*_direct`) → firma sitesi (`website_scraper.py`) → Apollo →
Hunter → tahmin (`email_guesser.py`, gönderilmeden filtrelenir).
Apollo ücretsiz planda 422 döner (API ücretli planda). Hunter kotası 25/ay.

## Secrets (GitHub → Settings → Secrets)

`ANTHROPIC_API_KEY`, `GOOGLE_SERVICE_ACCOUNT_JSON`, `GOOGLE_SHEET_ID`,
`HUNTER_API_KEY`, `APOLLO_API_KEY` (opsiyonel), `TELEGRAM_BOT_TOKEN`,
`TELEGRAM_CHAT_ID`, `DAILY_SEND_LIMIT`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`,
`SMTP_PASS`, `SMTP_FROM_NAME`, `TEST_RECIPIENT` (ilk test için).
`INSTANTLY_API_KEY`/`INSTANTLY_CAMPAIGN_ID` artık opsiyonel — sadece
`SEND_MODE=instantly` ile kullanılır.

## Yol haritası bağlamı

Çok-müşterili yapıya geçiliyor (`clients/<isim>/client.yaml` planı) — ikinci
müşteri: Konya Teşvik (ayrı klonda). Supabase + Lovable panel Aşama 2.
Detay: `ARIA.md` (dürüst durum değerlendirmesi) ve `aria_satis.md` (kök neden
analizi). Bu iki dosyayı güncel tut: sistemsel bir kök neden bulunduğunda
`aria_satis.md`'ye ekle.

## AIandTech hizmet bilgi tabanı (bu repo, ARIA'nın dışında da kullanılıyor)

Bu repo aynı zamanda AIandTech'in genel hizmet dokümantasyonunu barındırıyor:
`satis_dokumani.md` (genel AI eğitim atölyesi satış dokümanı) ve
`docs/hizmetler/` (yeni hizmet hatları — ör. **ATOM Framework / AI Governance
danışmanlığı**, bkz. `docs/hizmetler/ai_governance_atom.md`). **Bu hizmet
hatlarının teknik altyapısı ARIA'nın koduyla KARIŞTIRILMAZ** — ATOM için ayrı
bir platform/repo gerekir (bkz. `docs/hizmetler/atom_teknik_yol_haritasi_notlari.md`),
`clients/` çok-müşterili planı yalnızca ARIA outreach motoru içindir.

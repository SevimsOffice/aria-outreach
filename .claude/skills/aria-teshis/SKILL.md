---
name: aria-teshis
description: ARIA mail göndermiyor / kampanya durdu / 0 gönderim şikayetinde çalıştırılacak teşhis runbook'u. "Mailler gitmiyor", "kampanya durdu", "neden gönderilmedi", "Instantly çalışmıyor" dendiğinde bu skill'i kullan.
---

# ARIA Teşhis Runbook'u

"Mail gitmiyor" şikayetinin bilinen 6 kök nedeni vardır. Tahmin yürütme —
aşağıdaki sırayla kontrol et, her adımın çıktısını kaydet, en sonunda tek bir
teşhis tablosu sun.

## Adımlar (sırayla, atlama)

1. **Fix branch'i main'de mi?** `git log origin/main --oneline -5` — kampanya
   fix'leri (`activate_campaign`, STATUS_MAP, account resume) main'de değilse
   diğer hiçbir kontrol anlamlı değil; cron main'den koşar. Önce bunu raporla.
2. **Kampanya durumu:** `python scripts/diagnose.py` çalıştır (yoksa
   `fix_campaign.py` dry mantığıyla oku). `status` alanına bak:
   - `completed` → lead bitti/hiç yoktu; lead ekle + `activate_campaign()`
   - `paused` → activate et
   - `accounts_unhealthy` / `bounce_protect` → Adım 3'e odaklan
3. **Gönderici hesap:** `list_accounts_v2()` çıktısında `sevim@aiandtech-info.com`
   status `2` (paused) veya `-1` (bağlantı hatası) mı? Paused → `resume_account()`.
   Bağlantı hatası kod ile çözülmez — kullanıcıya "Instantly UI'dan Gmail'i
   yeniden yetkilendir" de.
4. **Lead sayısı:** `get_leads_count()` 0 ise mail gidemez. Çözüm sırası:
   `run_resend_from_sheet.py --limit 30` → sonra `run_daily_pipeline.py`.
5. **Sheet vs Instantly tutarlılığı:** Sheet'te `Added_to_Instantly` olup
   Instantly'de olmayan kayıt = geçmiş API hatası. Log'daki
   `[INSTANTLY] POST /leads` satırlarında 200 olmayanları say.
6. **email_list boş mu?** Kampanyaya gönderici hesap atanmamışsa
   (`email_list: []`) hesap listesi PATCH'lenmeli — `fix_campaign.py` Adım B
   bunu yapar.

## Çıktı formatı (her teşhiste aynen bu yapı)

```
## Teşhis Sonucu — <tarih>

| # | Kontrol | Durum | Bulgu |
|---|---------|-------|-------|
| 1 | Fix'ler main'de | ✅/❌ | ... |
| 2 | Kampanya durumu | ✅/❌ | status=... |
| 3 | Gönderici hesap | ✅/❌ | ... |
| 4 | Lead sayısı | ✅/❌ | N lead |
| 5 | Sheet↔Instantly | ✅/⚠️ | ... |
| 6 | email_list | ✅/❌ | ... |

**Kök neden:** <tek cümle>
**Düzeltme sırası:** 1) ... 2) ... 3) ...
**Benim yapabildiklerim / Sevim'in yapması gerekenler** ayrımıyla bitir.
```

Kök nedeni bulunca `aria_satis.md`'deki kök neden bölümüne yeni madde ekle
(tekrarsa ekleme).

## Örnek iyi sonuç

> **Kök neden:** Kampanya "completed" durumunda ve 0 lead var; ayrıca gönderici
> hesap paused. **Düzeltme sırası:** 1) `fix_campaign.py` (hesap resume +
> activate), 2) `run_resend_from_sheet.py --limit 30`, 3) yarınki cron'u bekle
> veya `daily_pipeline` workflow'unu elle tetikle. Sevim'in yapması gereken:
> yok — hepsi koddan çözüldü.

## Asla yapma

- `allow_risky_contacts=true` YAPMA — hangi teşhis çıkarsa çıksın. Bu, çözüm
  değil domain intiharıdır (Sevim'in açık yasağı).
- Yeni kampanya oluşturarak "temiz başlangıç" yapma — mevcut kampanyayı onar.
- Teşhis bitmeden düzeltme uygulamaya başlama; önce tabloyu çıkar, sonra
  (kullanıcı sorun bildirmişse) düzeltmeleri uygula.
- `DAILY_SEND_LIMIT`'i teşhis sırasında değiştirme.

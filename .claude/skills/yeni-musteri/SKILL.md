---
name: yeni-musteri
description: ARIA'yı yeni bir müşteri (ör. Konya Teşvik) için kurarken izlenecek onboarding checklist'i. "Yeni müşteri ekle", "X firması için ARIA kur", "müşteri onboarding" dendiğinde bu skill'i kullan.
---

# Yeni Müşteri Kurulum Runbook'u

ARIA her müşteri için yeniden kurulur — hazır SaaS değil, ajans modelidir.
Kuruluma başlamadan önce aşağıdaki girdilerin HEPSİNİ topla; eksikse önce
kullanıcıdan iste, tahminle doldurma.

## Zorunlu girdiler

| Girdi | Örnek | Not |
|---|---|---|
| Müşteri adı | Konya Teşvik | |
| Hedef bölge/OSB listesi | Konya OSB | Her bölge için scraper gerekir |
| Teklif metni (tek cümle) | "teşvik danışmanlığı..." | `personalize.txt` prompt'una girer |
| **Ayrı gönderici domain** | konyatesvik-info.com | ANA DOMAİN ASLA KULLANILMAZ |
| Instantly kampanya ID | uuid | Müşteriye özel yeni kampanya |
| Google Sheet ID | ... | Müşteriye özel yeni sheet |
| Günlük limit hedefi | 100 | Warmup bitene kadar Instantly yönetir |

## Kurulum adımları (sırayla)

1. **Domain + mailbox:** Yeni domain al (~$10/yıl), mailbox kur, Instantly'ye
   bağla, **warmup'ı başlat**. Warmup 2-4 haftadır — bu süre beklenmeden
   gerçek gönderim AÇILMAZ. Kurulum tarihini not et.
2. **DNS:** SPF + DKIM + DMARC kayıtlarını kur, Instantly'nin domain testiyle
   doğrula. Üçü de yeşil olmadan devam etme.
3. **Instantly kampanyası:** Yeni kampanya aç; konu + gövde + 2 takip yaz
   (dizi Instantly'de yaşar, repoda değil). `{{personalization}}`, `{{firstName}}`,
   `{{companyName}}` değişkenlerini kullan. `allow_risky_contacts` KAPALI bırak.
4. **Sheet:** Yeni Google Sheet oluştur, service account'u editör olarak
   paylaş. `ARIA_Prospects` sekmesi kodda otomatik oluşur.
5. **Konfigürasyon:** Multi-tenant yapı (`clients/<isim>/client.yaml`) merge
   edilmişse yeni client dosyası oluştur; edilmemişse ayrı repo klonundaki
   secrets'ı güncelle (geçici model). Hangisinin geçerli olduğunu repoda
   `clients/` klasörü var mı diye kontrol ederek anla.
6. **Prompt uyarlama:** `templates/prompts/personalize.txt` içindeki teklif
   ve şehir bağlamını müşteriye göre düzenle.
7. **Dry-run doğrulama:** `python scripts/run_daily_pipeline.py --dry-run
   --limit 5` — scraper doğru bölgeyi buluyor mu, kişiselleştirme Türkçe ve
   teklifle uyumlu mu, logda kontrol et.
8. **İlk gerçek test:** Warmup bittikten sonra `--limit 1` ile kullanıcının
   kendi adresine tek mail; Instantly'de gönderildiğini ve spam'e düşmediğini
   birlikte doğrulayın.

## Çıktı formatı

Kurulum oturumunun sonunda şu checklist'i durumlarıyla ver:

```
## <Müşteri> Kurulum Durumu
- [x] Domain + mailbox + warmup başladı (bitiş: ~<tarih>)
- [x] SPF/DKIM/DMARC doğrulandı
- [ ] Instantly kampanyası + dizi
- [ ] Sheet + service account
- [ ] Config (client.yaml / secrets)
- [ ] Dry-run OK
- [ ] İlk test maili (warmup sonrası)
Sıradaki adım: <tek cümle>  ·  Engel: <varsa>
```

## Örnek iyi sonuç

> Konya Teşvik kurulumu: 7 adımdan 5'i tamam. Warmup 12. günde (~9 gün kaldı) —
> bu yüzden kampanya "paused"da bekliyor, bu NORMAL ve müdahale gerektirmez.
> Sıradaki adım: warmup bitince `--limit 1` test maili. Engel: yok.

## Asla yapma

- Warmup bitmeden gerçek gönderimi açma — "hazır görünüyor" yeterli değil,
  süre dolmalı.
- Müşteriler arası kaynak paylaştırma: kampanya, sheet, domain, mailbox hep
  müşteriye özel. Paylaşılan tek şey API anahtarları (Anthropic/Hunter).
- aiandtech'in kampanyasını/sheet'ini şablon diye kopyalayıp ID'lerini
  değiştirmeyi unutma riskine girme — her ID'yi tek tek doğrula.
- Müşteri lead listesi getirdiyse doğrulanmamış adresleri filtrelemeden
  Instantly'ye yükleme.

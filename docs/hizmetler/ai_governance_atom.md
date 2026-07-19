# AI Governance & Transformation Hizmeti — ATOM Framework

**Durum:** Yeni hizmet hattı — kalibrasyon aşaması · **Tarih:** 19 Temmuz 2026
**Sahibi:** Sevim Durmuş / AIandTech · **Metodoloji versiyonu:** ATOM v1.0

> Bu doküman AIandTech'in hizmet bilgi tabanına eklenen ikinci ürün hattıdır.
> Birincisi (`satis_dokumani.md`, `ARIA.md`) AI verimlilik eğitim atölyeleri ve
> ARIA otomatik outreach sistemidir. Bu belge onunla **karışmaz, üstüne biner**:
> aynı müşteri tabanına (Türk üretim firmaları) satılan, farklı bir ihtiyacı
> (tedarikçi güvenilirliği + AI risk yönetimi) hedefleyen ayrı bir tekliftir.

---

## 1. Bu hizmet ne satıyor?

**Eğitim satmıyoruz. Kurumsal bir AI yönetim sistemi satıyoruz.**

Kaynak sorun: üretim firmaları büyük kurumsal müşterilerine (Migros, Carrefour,
Beko, Arçelik, Bosch, Coca-Cola, Nestlé gibi) tedarikçi olarak çalışırken, bu
müşteriler artık satın alma sürecinde "AI'yi güvenli ve kontrollü kullanıyor
musunuz?" sorusunu soruyor — **AI Vendor Risk Assessment / AI Due Diligence
Questionnaire** olarak bilinen süreç. Otomotivde APQP/PPAP/IATF 16949,
havacılıkta AS9100, medikalde ISO 13485'in AI karşılığı hızla yaygınlaşıyor.

Bu sorulara hazırlıksız yakalanan firma ya işi kaybeder ya da hazırlığı
danışmanlık firmalarına yüksek proje ücretiyle sıfırdan yaptırır. AIandTech'in
teklifi: **tek bir Discovery görüşmesiyle** bu hazırlığı ölçülebilir bir skora
ve teslim edilebilir bir doküman setine dönüştürmek — ve bunu tekrarlanabilir,
ölçeklenebilir bir metodolojiyle (ATOM) yapmak.

**Üç alıcı sorusuna birden cevap veriyoruz:**
1. **Savunma:** "Müşterilerimize, denetçilere, düzenleyicilere AI'yi kontrollü
   kullandığımızı kanıtlayabiliyor muyuz?" (tedarikçi güvenilirliği, ISO/IEC
   42001 hazırlığı, KVKK, EU AI Act maruziyeti)
2. **Hücum:** "AI operasyonlarımızda nerede gerçekten para kazandırıyor, bunu
   yakalıyor muyuz?" (değer gerçekleştirme, kullanım senaryosu portföyü, ROI)
3. **Yörünge:** "Sektörümüze göre neredeyiz, önümüzdeki 12 ayda ne yapmalıyız?"
   (benchmark, yol haritası)

Rakiplerin çoğu (Big 4 danışmanlıkları, Credo AI/OneTrust/Holistic AI gibi GRC
platformları, MEXT gibi yerel oyuncular) bu üçünden yalnızca birini cevaplıyor.
Üçünü birden, **üretim süreçleri bilgisiyle** (ERP/MES/kalite/tedarik zinciri)
birleştiren bir oyuncu Türkiye pazarında henüz yok — bu, Sevim'in üretim
tecrübesinden gelen gerçek farklılaşma noktası.

---

## 2. ATOM Framework — özet

Tam teknik spesifikasyon: `docs/hizmetler/ATOM_Framework_v1.0_Specification.md`
(orijinal kaynak doküman, referans olarak saklanıyor). Aşağıda satış ve
konumlandırma için gereken özet.

### 8 boyut, 32 alt-boyut

| # | Boyut | Odak | ISO-kritik alt-boyut |
|---|---|---|---|
| D1 | Strateji ve Liderlik | AI vizyonu üst yönetimde sahiplenilmiş mi | 0 |
| D2 | Yönetişim ve Organizasyon | Kararları kim veriyor, hangi kurallarla | 4 |
| D3 | Risk, Uyum ve Güven | AI riskleri, KVKK/EU AI Act maruziyeti | 3 |
| D4 | Veri ve Kurumsal Bilgi | ERP/MES/CRM verisi + kurumsal know-how | 1 |
| D5 | Teknoloji ve Güvenlik | Shadow AI kontrolü, ISO 27001 köprüsü | 1 |
| D6 | YZ Yaşam Döngüsü ve Operasyon | Fikirden üretime disiplinli süreç | 4 |
| D7 | İnsan ve Yetkinlik | AI okuryazarlığı, eğitim programı | 2 |
| D8 | Değer ve Yaygınlaştırma | Ölçülen iş değeri, pilot→üretim | 0 |

**Puanlama:** Her alt-boyut 0-5 arası, kanıt zorunlu (bkz. Kanıt Modeli).
**ATOM Skoru:** 8 boyutun ağırlıklı ortalaması, 0-100'e ölçeklenir.

| Skor | Bant | Anlamı |
|---|---|---|
| 0-20 | Habersiz | AI firmanın başına geliyor, firma tarafından yönetilmiyor |
| 21-40 | Keşif | Yapısız deneme; risk maruziyeti genelde burada zirve yapar |
| 41-60 | Yapılandırılmış | Temeller belgelendi; ISO patikası gerçekçi hale gelir |
| 61-80 | Yönetilen | Ölçülüyor, denetleniyor, kurumsal müşteriye güven verir |
| 81-100 | Öncü | Sektör referansı |

### Kanıt Modeli (satışta en güçlü argüman)

**Stated Score** (firmanın iddia ettiği) ile **Evidenced Score** (kanıtla
desteklenen) ayrı tutulur. Kanıt yoksa puan otomatik **2'ye sabitlenir** —
firma ne söylerse söylesin. Aradaki fark **"Evidence Gap"** olarak raporlanır:
"uygulama var olabilir ama kanıtlanamıyor" — tam olarak bir ISO denetiminin
veya müşteri sorgusunun düşürdüğü nokta. Bu, bir günlük eğitimin
göstermediği somut riski müşteriye görünür kılar ve fiyatı savunur.

### Sertifikasyon Kapısı

Ortalama skor yüksek olsa bile **15 ISO-kritik alt-boyuttan** biri bile 3'ün
altındaysa: **"NOT MET"** raporlanır, hangi boşlukların kapıyı kapattığı
listelenir. Bu, "skor iyi ama denetimden geçemez" hatasını önler ve yol
haritasının birinci katmanını (Tier 1 = kapıyı kapat) otomatik olarak verir.

---

## 3. Hizmet paketleri (fiyatlandırma iskeleti)

Spesifikasyonda tanımlı iki değerlendirme derinliği, üç ticari pakete karşılık
gelir:

| Paket | Kapsam | Süre | Konumlandırma |
|---|---|---|---|
| **ATOM Rapid** | 21 Core alt-boyut | 2-4 hafta sprint | Giriş ürünü — "AI Readiness Assessment" |
| **ATOM Full** | 32 alt-boyutun tamamı | Tam dönüşüm programı | Ana teklif — Governance kurulumu + doküman seti |
| **Managed Governance** | Full'ün yıllık tekrarı | Abonelik | Tekrarlayan gelir — yıllık yeniden değerlendirme + politika güncelleme |

**Fiyatlandırma mantığı (henüz kalibre edilmedi — ilk 3 satışta netleşecek):**
- Rapid: sabit ücret, "bir günlük eğitim" fiyatının üstünde ama büyük
  danışmanlık projesi fiyatının çok altında — giriş kolaylaştırıcı.
- Full: Rapid'den kanıtlanan bulgulara dayalı teklif; teslimat somut (politika
  seti + risk matrisi + roadmap + dashboard + sertifikasyon hazırlığı).
- Managed: yıllık abonelik — "yeniden değerlendirme + güncel politikalar",
  tek seferlik eğitim ücretinden çok daha sürdürülebilir gelir modeli.

Bu, aria_satis.md'de belirtilen "ajans modeli" ile aynı ticari mantığı
izler: önce kanıt (Rapid ile küçük hacim), sonra ölçek (Full/Managed).

---

## 4. Teslim edilen çıktılar (doküman kataloğu — temsili liste)

Discovery'den tek seferde üretilebilecek doküman ailesi (tam liste 50-60'a
çıkabilir; aşağıdakiler en çok talep edilenler):

- AI Governance Policy, AI Security Policy, Responsible AI Policy
- AI Risk Register, AI Asset/Model Inventory
- AI Development Lifecycle, AI Change Management Procedure
- Human Oversight Procedure, AI Incident Response Plan
- AI Vendor/Supplier Questionnaire Response Pack
- Data Classification Policy, Data Privacy Policy
- AI Training Plan, AI Roles & Responsibilities
- Executive Dashboard (ATOM Skoru + boyut radar grafiği)
- Roadmap (Tier 1: Sertifikasyon Kapısı kapatma / Tier 2: değer hamleleri)

Rapor şablonu referansı: `ATOM_Rapid_Rapor_Sablonu_v1.0.docx` (yüklenen
belge — gerektiğinde tekrar isteyip repoya eklenebilir).

### Kapsanan standartlar
ISO/IEC 42001 (AI yönetim sistemi), NIST AI RMF, ISO/IEC 23894 (AI risk
yönetimi), ISO/IEC 27001, OWASP Top 10 for LLM Applications, KVKK, EU AI Act
(yalnızca Aralık 2027/Ağustos 2028 ertelenmiş yükümlülükler — Şubat 2025'ten
beri yürürlükte olan Madde 4 AI-okuryazarlığı yükümlülüğü hariç).

**Konumlandırma notu:** Türkiye'de henüz özel bir AI yasası yok — mesaj
"deadline paniği" değil, **"hazırlık penceresi ve tedarikçi güvenilirliği"**
olmalı.

---

## 5. Hedef müşteri profili ve satış tetikleyicisi

- Büyük kurumsal alıcılara (perakende zinciri, otomotiv OEM, gıda/içecek
  devleri) tedarikçi olan orta-büyük ölçekli Türk üretim firmaları.
- **En güçlü satış tetikleyicisi:** firma bir müşterisinden zaten bir tedarikçi
  değerlendirme formu / AI due diligence sorgusu almış veya alacağını biliyor.
  Bu, "bir gün eğitim" fiyat itirazını ortadan kaldırır — çünkü ödenen şey
  artık bir iş kaybı riskinin bertaraf edilmesidir.
- Mevcut ARIA/eğitim müşterileriyle **çapraz satış fırsatı**: eğitim verilen
  firmaya "bu arada müşterileriniz AI kullanımınızı sorgulamaya başladı mı?"
  sorusuyla girilebilir.

---

## 6. Bu hizmetin ARIA ile ilişkisi — net ayrım

| | ARIA (mevcut) | ATOM / AI Governance (yeni) |
|---|---|---|
| Sattığı şey | Soğuk e-posta ile lead bulma otomasyonu | AI risk/governance danışmanlığı + rapor seti |
| Müşteri teması | "Yeni müşteri bul" | "Mevcut müşterini kaybetme, tedarikçi güvenilirliğini kanıtla" |
| Teknik altyapı | Bu repo (aria-outreach) — GitHub Actions, Instantly, Sheets | **Ayrı proje** — henüz kodlanmadı, bu repoya karıştırılmayacak |
| Durum | Üretimde, aktif satış | Kalibrasyon aşaması — ilk 3 satışta anchor'lar netleşecek |

**Önemli:** ATOM'un teknik altyapısı (multi-agent discovery platformu,
LangGraph orkestrasyon, doküman üretim motoru) planlama aşamasında ayrıntılı
tartışıldı (bkz. `docs/hizmetler/atom_teknik_yol_haritasi_notlari.md`) ama
**henüz inşa edilmedi ve bu repoya ait değil.** Bu repo yalnızca ARIA outreach
sistemi içindir (bkz. CLAUDE.md). ATOM platformu ileride ayrı bir repo/proje
olarak kurulmalı — CLAUDE.md'deki "Çok-müşterili yapıya geçiş" planındaki
`clients/` mimarisiyle karıştırılmamalı, o farklı bir ölçekleme sorunudur.

---

## 7. Sonraki adımlar

1. İlk 3 ücretli katılımda kalibrasyon: her puanlama tartışmasını, belirsiz
   çıkan anchor'ı, kanıt bulunabilirliğini ve alt-boyut başına harcanan
   zamanı kaydet → v1.1'i 4. katılımdan önce dondur (spesifikasyon madde 11).
2. Marka adı netleşmeli: "ATOM" yer tutucu — Türk Patent + EUIPO marka
   taraması ve domain kontrolü yapılmadan dışarıda kullanılmamalı. Yedek aday:
   **MARI** (Manufacturing AI Readiness Index).
3. Workbook (`ATOM_Assessment_Workbook_v1.0.xlsx`) alt-boyut kayıtlarının
   Türkçe tam çevirisi tamamlanmalı — şu an yalnızca boyut/bant adları
   çevrildi (spesifikasyon madde 13, bilinen kısıt).
4. İlk satış konuşmasında kullanılacak somut açılış: "Müşterileriniz size AI
   kullanımınızla ilgili bir soru sordu mu / soracak mı?" — bu sorunun
   kendisi bir Discovery daveti işlevi görür.

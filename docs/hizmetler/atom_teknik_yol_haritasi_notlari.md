# ATOM — Teknik Platform Yol Haritası Notları (Ham Planlama)

**Durum:** Erken beyin fırtınası — henüz uygulanmadı, henüz kod yok.
**Amaç:** ATOM hizmeti (bkz. `ai_governance_atom.md`) ileride bir platform
haline getirilmek istenirse başlangıç noktası. **Bu repo (aria-outreach) bu
platformu inşa etmek için kullanılmayacak** — ayrı bir proje/repo gerekir.

---

## Neden ayrı bir proje, ARIA'nın `clients/` yapısı değil?

CLAUDE.md'deki çok-müşterili ARIA planı (`clients/<isim>/client.yaml`) tek bir
outreach motorunun farklı müşteriler için yeniden konfigüre edilmesiyle
ilgilidir. ATOM platformu ise tamamen farklı bir problem: her müşteri için
büyük miktarda özel veri (Discovery cevapları, yüklenen kanıt dosyaları, RAG
bilgi tabanı) tutan, çok-adımlı AI agent orkestrasyonu yapan bir sistem.
İkisini karıştırmak hem ARIA'yı hem ATOM'u karmaşıklaştırır.

## Önerilen mimari (10 katman özeti)

1. **Client Workspace** — multi-tenant; her müşteri kendi tenant'ında
   (görüşmeler, assessment'lar, dokümanlar, kanıtlar, agent çıktıları, yol
   haritaları, dashboard'lar izole tutulur). GitHub'da müşteri başına ayrı
   proje AÇILMAZ — tek platform, çok kiracı.
2. **Discovery Portal** — Stripe/HubSpot onboarding tarzı sihirbaz ekranı
   (sohbet arayüzü değil): Şirket Bilgisi → Departmanlar → ERP → ISO →
   Süreçler → Mevcut AI Kullanımı → Doküman Yükleme → Görüşme Notları →
   Assessment Üret.
3. **Evidence Management** — her soru yanında sürükle-bırak yükleme (PDF,
   Word, PNG, Excel, ses/video, toplantı transkripti). Kurumsal müşteriler
   iddiaya değil kanıta güvenir (bkz. Kanıt Modeli — spesifikasyon madde 5).
4. **Knowledge Base (RAG)** — yüklenen tüm dosyalar parçalanır → embedding →
   vektör veritabanı → knowledge graph → LLM. Agent'lar şirketi gerçekten
   "tanıyarak" çalışır.
5. **Agent Layer** — LangGraph önerilir (CrewAI alternatif ama kurumsal
   akışlarda LangGraph daha fazla kontrol sağlar). Örnek zincir: Coordinator
   → Organization Agent → Security Agent → ISO Agent → Risk Agent → Quality
   Agent → Governance Agent → Roadmap Agent → Executive Report Agent.
   **Tasarım ilkesi:** agent'ların görevi düşünmek/analiz etmektir, doküman
   üretmek değil — çıktı JSON olarak ayrı bir Document Generator servisine
   gider. Bu ayrım agent mantığını dokümandan bağımsızlaştırır ve yeni
   standart/rapor eklemeyi kolaylaştırır.
6. **Workflow Engine** — Flowise değil, doğrudan Python + FastAPI (ölçekte
   — 100 müşteri olduğunda görsel akış aracı yönetilemez hale gelir). n8n
   yalnızca dış sistem entegrasyonları için (e-posta, SharePoint, Google
   Drive, Microsoft 365, Slack) — platformun merkezi n8n olmamalı.
7. **AI Memory** — agent'lar arası paylaşılan hafıza; bir agent'ın öğrendiği
   bilgiyi (ör. "şirket Microsoft 365 kullanıyor") başka bir agent tekrar
   sormamalı.
8. **Dashboard** — CEO'nun gördüğü ekran: ATOM Skoru + 8 boyut radar grafiği
   + Top 10 Risk + Top 20 Fırsat + Sonraki 90 Gün + Tahmini ROI, hepsi
   otomatik üretilir.
9. **Document Center** — Generate → Word (politikalar), Excel (risk
   matrisi), PowerPoint (yönetici sunumu), Mermaid/Draw.io/SVG (roadmap,
   süreç akışı, BPMN).
10. **Consultant Workspace** — danışmanın (Sevim'in) kendi ekranı: To Do,
    Missing Evidence, Open Questions, Pending Approval, Agent Suggestions,
    Revision Requests. **Kilit ilke: AI sana iş yaptırmalı, sen AI'ya iş
    yaptırmamalısın.**

## Veri modeli önceliği

Teknik değil, kavramsal olarak ilk soru: **"Asıl veri modelim ne olacak?"**
Nesneler ve ilişkileri baştan doğru tasarlanırsa yeni bir ISO standardı veya
yeni bir rapor talebi geldiğinde agent'lar yeniden yazılmaz — sadece aynı
veriyi farklı yorumlayan yeni bir çıktı eklenir. Aday nesneler: Company,
Department, Process, Role, Policy, Evidence, Assessment, Risk, Control, AI
Tool, System, Standard, Use Case, Document.

## Önerilen geliştirme sırası

1. Domain model ve veri şeması
2. Discovery soru bankası (workbook'taki seed'den tam tiered instrument'a)
3. Kanıt yükleme sistemi
4. RAG ve bilgi tabanı
5. Assessment motoru (ATOM puanlama motoru)
6. Agent orkestrasyonu
7. Doküman üretim servisi
8. Dashboard ve KPI katmanı
9. Müşteri portalı
10. Yönetici ve danışman çalışma alanı

**Öneri:** Doğrudan kodlamaya başlamadan önce 8-12 haftalık bir "Product
Discovery" (ekran, veri modeli, agent mimarisi, çıktı kataloğu, iş akışları
netleştirme) yapılmalı — platformun değeri kodundan değil kurumsal bilgi
modelinden gelecek.

## Araç sırası önerisi (ileride bu proje başlatılırsa)

- **Claude Projects** — ürün hafızası ve mimari (vizyon, persona, veri
  modeli, agent tanımları, standart notları, doküman şablonları, prompt
  standartları, mimari karar kayıtları, backlog, ekran fikirleri).
- **Figma / Lovable** — ilk ekran prototipleri.
- **Claude Code** — kod üretimi ve refaktör (ayrı repo!).
- **GitHub** — versiyon kontrolü (ayrı repo!).
- **LangGraph** — agent orkestrasyonu.
- **FastAPI + PostgreSQL + pgvector** — backend, iş verisi, vektör arama.
- **n8n** — yalnızca dış sistem entegrasyonları.

Tek repo öneri yapısı (bu ATOM projesi başlatıldığında):
```
/frontend
/backend
/agents
/document-generator
/shared
/prompts
/infrastructure
/docs
```
İlk gün yazılması önerilen 4 dosya: `Domain_Model.md`, Entity Relationship
Diagram, `Agent_Responsibilities.md`, `Output_Catalog.md`.

## Pazar/rakip konumu (kısa not — satış konuşmalarında kullanılabilir)

Küresel: Big 4 danışmanlıklar (Accenture, Deloitte, EY, PwC, KPMG, McKinsey,
BCG) workshop+rapor modeliyle çalışıyor, otomatik doküman üretimi/multi-agent
mimarisi nadir. Özel platformlar (Credo AI, OneTrust AI Governance, Holistic
AI, Saidot, Regulativ AI, Sprinto, Drata, Vanta) GRC-ağırlıklı; üretim
entegrasyonu (MES/PLM) yok. Türkiye'de PwC/EY/KPMG Türkiye, MEXT (üretim
odaklı maturity, SIRI/COSIRI benzeri), ThinkStrait, Luminoris, Insight AI,
Internative gibi oyuncular var ama çoğu proje bazlı danışmanlık — ATOM'un
hedeflediği "tek Discovery → 50+ doküman + agent orkestrasyonu" ölçeğinde
entegre bir yerli oyuncu görünmüyor (Temmuz 2026 itibarıyla, teyit
edilmeli). **Fırsat:** ISO 42001 + KVKK + yerel regülasyon + operasyonel
(üretim) governance birleşimi Türkiye'de hâlâ niş.

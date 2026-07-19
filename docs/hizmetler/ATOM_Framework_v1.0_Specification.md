# ATOM — AI Transformation Operating Model
## Maturity & Readiness Framework — Specification v1.0

**Status:** Working draft for calibration · **Date:** 18 July 2026 · **Owner:** Sevim Durmuş / AIandTech
**Working name:** "ATOM" (AI Transformation Operating Model) is a placeholder brand. Verify trademark and domain availability before external use. Alternative candidate: MARI (Manufacturing AI Readiness Index).

---

## 1. Purpose and positioning

ATOM is a proprietary maturity and readiness framework for assessing how well a manufacturing company adopts, governs, and extracts value from artificial intelligence. It is the methodological core of the AIandTech assessment and transformation offering. Everything downstream derives from it: discovery questions, gap analysis, scoring, roadmap priorities, benchmark comparisons, and the client-facing ATOM Score.

ATOM is designed to answer three buyer questions simultaneously:

1. **Defense:** "Can we prove to our customers, auditors, and regulators that we use AI in a controlled way?" (supplier credibility, ISO/IEC 42001 readiness, KVKK, EU AI Act exposure)
2. **Offense:** "Where does AI actually pay off in our operations, and are we capturing it?" (value realization, use-case portfolio, ROI)
3. **Trajectory:** "Where are we versus our sector, and what should we do in the next 12 months?" (benchmark, roadmap)

Most competing frameworks answer only one of these. Pure GRC platforms answer question 1; consulting maturity models answer question 3 vaguely; nobody in the Turkish manufacturing market answers all three with evidence-anchored scoring. That combination is the framework's differentiation.

## 2. Design principles

**P1 — Evidence over claims.** A maturity score is a professional judgment that must survive challenge by an auditor, a customer's procurement team, or a skeptical CFO. Every score above Level 2 requires documentary evidence. Claims without evidence are capped (see Section 5).

**P2 — Framework as data.** Every dimension, sub-dimension, level anchor, question, and standards mapping carries a stable ID (e.g., `D3.2`). The framework is maintained as structured data (the companion workbook), not as prose. This is what later feeds the fact store, the assessment engine, and the benchmark database.

**P3 — Multi-framework crosswalk built in.** Each sub-dimension maps to ISO/IEC 42001 clauses and Annex A control groups, NIST AI RMF functions, and where relevant EU AI Act, KVKK, ISO/IEC 27001, and OWASP LLM Top 10. One assessment therefore yields several gap analyses without extra client effort.

**P4 — Manufacturing-native.** Anchors and questions assume the realities of a Turkish manufacturing supplier: ERP/MES environments, quality-management culture (ISO 9001, IATF-style customer audits), OT constraints, family-owned governance, and position in an enterprise customer's supply chain.

**P5 — Two-legged.** Governance/risk dimensions (D2, D3, D5) and value dimensions (D8, D6) carry equal structural weight. An organization cannot score as "Leading" on paperwork alone, nor on ungoverned experimentation.

**P6 — Benchmark-ready from client one.** Scoring rules, anchors, and version numbers are fixed and recorded per assessment so that results are comparable across companies and across years. Methodology version is stamped on every report.

## 3. Framework architecture

The framework has **8 dimensions** and **32 sub-dimensions**. Each sub-dimension is scored 0–5 against anchored descriptors. Two assessment depths use the same instrument:

- **ATOM Rapid** — the 21 *Core* sub-dimensions. Designed for the 2–4 week AI Readiness Assessment sprint (the entry product).
- **ATOM Full** — all 32 sub-dimensions. Designed for the transformation program and for annual reassessment under the managed-governance subscription.

Fifteen sub-dimensions are additionally flagged **ISO-critical**: they correspond to mandatory elements of an ISO/IEC 42001 management system. These drive the Certification Gate (Section 6.4).

| # | Dimension (EN) | Dimension (TR) | Sub-dims | Core | ISO-critical |
|---|---|---|---|---|---|
| D1 | Strategy & Leadership | Strateji ve Liderlik | 4 | 3 | 0 |
| D2 | Governance & Organization | Yönetişim ve Organizasyon | 4 | 4 | 4 |
| D3 | Risk, Compliance & Trust | Risk, Uyum ve Güven | 4 | 3 | 3 |
| D4 | Data & Knowledge | Veri ve Kurumsal Bilgi | 4 | 2 | 1 |
| D5 | Technology & Security | Teknoloji ve Güvenlik | 4 | 2 | 1 |
| D6 | AI Lifecycle & Operations | YZ Yaşam Döngüsü ve Operasyon | 4 | 2 | 4 |
| D7 | People & Competence | İnsan ve Yetkinlik | 4 | 2 | 2 |
| D8 | Value & Adoption | Değer ve Yaygınlaştırma | 4 | 3 | 0 |
| **Total** | | | **32** | **21** | **15** |

The full sub-dimension register — including what each assesses, key discovery questions, the Level-3 anchor, expected evidence, and standards mappings — lives in the companion workbook (`ATOM_Assessment_Workbook_v1.0.xlsx`, sheet *Sub-Dimensions*), which is the data source of record.

## 4. The maturity scale (generic level model)

All 32 sub-dimensions use the same six-level scale. Levels are **staged**: a level is awarded only when its criteria *and all lower levels'* criteria are satisfied.

| Level | Name (EN / TR) | Generic definition |
|---|---|---|
| 0 | Absent / Yok | No awareness or activity. The topic is not on anyone's agenda. |
| 1 | Ad hoc / Bireysel | Activity exists but depends entirely on individuals. Uncoordinated, invisible to management, undocumented. |
| 2 | Emerging / Yaygınlaşan | Repeated practices in pockets of the organization. Informal rules; management is aware but nothing is standardized or documented. |
| 3 | Defined / Tanımlı | Documented, approved, communicated organization-wide. Roles assigned, consistently applied. This is the ISO "documented information" threshold. |
| 4 | Managed / Yönetilen | Measured and monitored with KPIs and records over time. Audited or reviewed at defined intervals; deviations trigger corrective action. |
| 5 | Optimizing / Öncü | Systematic continual improvement. Benchmarked externally; anticipates regulatory and technology change; recognized practice. |

**The pivotal level is 3.** Level 3 across the ISO-critical sub-dimensions is the pragmatic definition of "ready to begin an ISO/IEC 42001 certification track" and "able to answer an enterprise customer's AI questionnaire credibly."

## 5. Evidence model

### 5.1 Evidence ladder

| Claimed level | Minimum evidence required |
|---|---|
| 1–2 | Interview statements; ad hoc examples shown on screen. |
| 3 | Approved documents (policy, procedure, RACI, plan), published and dated; system configurations; communication records. |
| 4 | Records and metrics spanning at least 3–6 months: logs, minutes, audit reports, dashboards, training records, monitoring data. |
| 5 | Improvement records (before/after), benchmark participation, external validation or recognition. |

### 5.2 The Evidence Cap rule (non-negotiable)

If the required evidence for the claimed level is not sighted, the **Evidenced Score is capped at 2**, regardless of what was stated in interviews. Both scores are recorded:

- **Stated Score** — what the organization believes/claims.
- **Evidenced Score** — what the evidence supports. *This is the score that is reported, aggregated, and benchmarked.*

The gap between Stated and Evidenced is itself a standard finding type: **Evidence Gap** — "practice may exist but cannot be demonstrated," which is precisely what fails a Stage 2 certification audit and what makes customer questionnaires risky to answer. Presenting this gap explicitly is one of the framework's most persuasive outputs.

### 5.3 Confidence rating

Each score carries a confidence flag: **H** (multiple independent sources, direct evidence), **M** (single source with evidence, or triangulated statements), **L** (single statement, evidence pending). Low-confidence scores are highlighted in the report and generate follow-up requests, never silent assumptions. A finding the assessor cannot support is recorded as *"insufficient evidence"* — never filled with plausible text.

### 5.4 Worked example of a defensible score

> **D2.2 AI policy & acceptable use — Evidenced Score: 2 (Stated: 3), Confidence: H.**
> Basis: IT manager stated a policy "exists" (interview, 14.07.2026). Document sighted is an unapproved draft dated 03/2025, never published to staff; no communication record; HR confirmed staff are unaware. Level 3 requires an approved, communicated policy → cap applied. Finding EG-04 raised; action: approve and publish policy, deliver awareness briefing (maps to ISO/IEC 42001 5.2, A.2).

Every reported score must be reconstructible in this form. If it cannot be, it is not reported.

## 6. Scoring and aggregation

### 6.1 Sub-dimension scoring
Whole numbers 0–5 against the anchors, applying the staged rule and the Evidence Cap. No half-points at sub-dimension level (half-points invite negotiation; anchors decide).

### 6.2 Dimension scores
Arithmetic mean of that dimension's scored sub-dimensions, one decimal. In Rapid mode only Core items are scored; every dimension contains at least two Core items, so all eight dimension scores are always produced.

### 6.3 ATOM Score and bands
The **ATOM Score** is the weighted mean of the eight dimension scores, scaled to 0–100. Default weights are equal (12.5% each); profile presets may reweight (Section 6.5) but the default is used for benchmarking.

| ATOM Score | Band (EN / TR) | Meaning |
|---|---|---|
| 0–20 | Unaware / Habersiz | AI is happening *to* the company, not *by* it. |
| 21–40 | Exploring / Keşif | Experimentation without structure; risk exposure typically peaks here. |
| 41–60 | Structured / Yapılandırılmış | Foundations documented; ISO-track becomes realistic. |
| 61–80 | Managed / Yönetilen | Measured, audited, scaling; credible to enterprise customers. |
| 81–100 | Leading / Öncü | Sector reference; AI embedded in the value chain and the management system. |

### 6.4 The Certification Gate (reported alongside the score)
Averages hide fatal gaps: a company can score 62 overall while having no risk register. Therefore the report always states, separately from the ATOM Score:

> **ISO/IEC 42001 Readiness Gate:** MET only if *all 15 ISO-critical sub-dimensions* have an Evidenced Score ≥ 3. Otherwise: NOT MET, with the list of gating gaps.

This single rule prevents the "nice score, unpassable audit" failure mode and gives the roadmap its non-negotiable first tier.

### 6.5 Profile presets (optional lenses, never for benchmarking)
- **Supplier Credibility profile** — overweights D2, D3, D5 (for companies facing customer questionnaires or audits).
- **Value-First profile** — overweights D8, D6, D4 (for companies with no external compliance pressure yet).
- **Certification Track profile** — reporting emphasis on ISO-critical items and the Gate.
Presets change emphasis and roadmap sequencing, not the underlying scores. Benchmark submissions always use default weights.

### 6.6 Anti-gaming and consistency rules
- Staged scoring: no level without the lower levels.
- One assessor scores, a second reviews all scores of 4–5 and all Evidence Gaps (four-eyes rule; in a solo practice, review after a 24-hour cooling period against the written evidence log).
- Scores are frozen at the validation workshop; later changes require a documented reason.
- Methodology version (v1.0) is printed on every report and stored with every benchmark record.

---

## 7. Dimensions, sub-dimensions, and level anchors

Each dimension below gives: scope, its sub-dimension register (Core = in Rapid assessment; ISO-c = ISO-critical), and the 0–5 level anchors used for scoring. Sub-dimension detail (assessment focus, key questions, Level-3 anchor, evidence, mappings) is in the workbook.

### D1 — Strategy & Leadership (Strateji ve Liderlik)
Whether AI direction is owned at the top, linked to business objectives, funded deliberately, and supported by realistic change management. In family-owned manufacturers this dimension usually decides everything else: without an owner-level sponsor, Level 3 elsewhere rarely survives.

| ID | Sub-dimension | Core | ISO-c |
|---|---|---|---|
| D1.1 | AI vision & strategic alignment | ✔ | |
| D1.2 | Executive ownership & sponsorship | ✔ | |
| D1.3 | Investment & portfolio discipline | ✔ | |
| D1.4 | Change readiness & culture | | |

**Anchors**
- **L0:** AI is not on the leadership agenda. No vision, no discussion, no budget.
- **L1:** Individual executives show interest; experiments approved case-by-case with no link to business strategy.
- **L2:** Leadership discusses AI recurrently and allocates some budget, but there is no documented strategy or measurable objectives.
- **L3:** A written AI strategy/roadmap approved by top management, linked to business objectives, with a named executive owner, allocated budget, and communicated objectives.
- **L4:** Strategy execution is tracked with KPIs and portfolio reviews; management reviews AI objectives at defined intervals and reallocates investment based on results.
- **L5:** AI strategy shapes business-model decisions; leadership anticipates regulatory and technology shifts and updates strategy proactively; the company is cited as a sector example.

### D2 — Governance & Organization (Yönetişim ve Organizasyon)
Whether anyone can say who decides, under what rules, with what accountability — internally and toward suppliers. This dimension carries the heart of ISO/IEC 42001 clauses 5.2–5.3 and Annex A.2/A.3/A.10, and is what enterprise procurement teams probe first.

| ID | Sub-dimension | Core | ISO-c |
|---|---|---|---|
| D2.1 | Governance structure & decision rights | ✔ | ✔ |
| D2.2 | AI policy & acceptable use | ✔ | ✔ |
| D2.3 | Roles, responsibilities & resourcing | ✔ | ✔ |
| D2.4 | Supplier & third-party AI governance | ✔ | ✔ |

**Anchors**
- **L0:** No rules and no ownership; AI decisions happen nowhere — or everywhere.
- **L1:** Individual managers set informal expectations; no policy; accountability unclear.
- **L2:** Draft rules or emailed guidance exist in pockets; some responsibilities are assumed but not formalized.
- **L3:** Approved AI policy and acceptable-use rules are published; a governance body or named owner holds defined decision rights; a RACI covers AI activities; supplier AI expectations are defined in procurement.
- **L4:** Governance runs on records: minutes, logged decisions, monitored policy compliance, managed exceptions; supplier AI assessments are performed and tracked.
- **L5:** The governance model is benchmarked and continually improved; policies are updated ahead of regulatory change; governance extends across the value chain as a commercial differentiator.

### D3 — Risk, Compliance & Trust (Risk, Uyum ve Güven)
Whether AI risks are identified, treated, and owned; whether legal exposure (KVKK, EU AI Act, sector rules) is known; and whether the company could handle an AI incident. Anchored to ISO/IEC 42001 6.1.2–6.1.4 and 8.2–8.4, ISO/IEC 23894, and ISO/IEC 42005 for impact assessment.

| ID | Sub-dimension | Core | ISO-c |
|---|---|---|---|
| D3.1 | AI risk management | ✔ | ✔ |
| D3.2 | AI system impact assessment | ✔ | ✔ |
| D3.3 | Regulatory readiness (EU AI Act, KVKK) | ✔ | |
| D3.4 | Incident response & continuity | | ✔ |

**Anchors**
- **L0:** AI risks have never been assessed; no awareness of AI-related legal obligations.
- **L1:** Risks are discussed anecdotally after problems occur; reactions are ad hoc.
- **L2:** Some risks are identified informally; KVKK is considered for AI occasionally; there is no method and no register.
- **L3:** A documented AI risk method and a maintained risk register exist; impact assessments are performed for significant AI systems; regulatory applicability (KVKK, EU AI Act exposure) is determined and recorded; incident response covers AI.
- **L4:** The register is maintained with owners, treatments, and scheduled reviews; incidents are recorded and analyzed; compliance is monitored with evidence; internal audits include AI.
- **L5:** Risk appetite is quantified; scenarios are tested; regulatory tracking proactively feeds change plans; the trust posture is used commercially (customer assurance pack).

### D4 — Data & Knowledge (Veri ve Kurumsal Bilgi)
Whether the data and corporate knowledge that AI must run on is governed, classified, lawful to use, and technically reachable. In manufacturing this includes the ERP/MES/CRM/PLM landscape and — critically — undocumented tribal knowledge held by veteran staff.

| ID | Sub-dimension | Core | ISO-c |
|---|---|---|---|
| D4.1 | Data governance & quality for AI | ✔ | ✔ |
| D4.2 | Data privacy & classification in AI flows | ✔ | |
| D4.3 | Knowledge management & AI-readiness of corporate knowledge | | |
| D4.4 | Data architecture & integration (ERP/MES/CRM) | | |

**Anchors**
- **L0:** The data landscape is unknown; knowledge is trapped in individuals; nothing is prepared for AI.
- **L1:** Individuals extract data manually for experiments; quality is unknown; documents are scattered.
- **L2:** Key data sources are identified; some cleanup efforts and partial repositories exist; no classification governs AI use.
- **L3:** Data governance for AI is defined: a classification scheme is applied, quality criteria and provenance are documented for AI-used data, the KVKK basis of AI data flows is mapped, and corporate knowledge is organized and access-controlled.
- **L4:** Data quality is measured with metrics; lineage is tracked; access is audited; the knowledge base has ownership and freshness rules; AI-ready datasets and pipelines are operational.
- **L5:** Data is treated as a product with continuous quality improvement; tribal know-how is systematically captured and reused across AI use cases.

### D5 — Technology & Security (Teknoloji ve Güvenlik)
Whether AI usage is technically controlled and secure — the shadow-AI question — and whether infrastructure and the ISMS can support governed AI at scale. Bridges to ISO/IEC 27001 and OWASP Top 10 for LLM Applications.

| ID | Sub-dimension | Core | ISO-c |
|---|---|---|---|
| D5.1 | Secure AI usage & shadow-AI control | ✔ | ✔ |
| D5.2 | Infrastructure & integration readiness | | |
| D5.3 | Sanctioned AI stack & tool governance | ✔ | |
| D5.4 | ISMS alignment (ISO 27001 bridge) | | |

**Anchors**
- **L0:** No control over AI tool usage; security has not been considered; infrastructure is unexamined.
- **L1:** Employees use public AI tools on personal accounts; IT is unaware or tolerating; no technical controls exist.
- **L2:** Some tools are blocked or allowed informally; corporate accounts exist for a few tools; risk awareness is basic; there is no defined stack.
- **L3:** A sanctioned AI stack is defined with an approval path; access management, logging, and data-loss rules apply to AI usage; AI security requirements are documented (aligned to OWASP LLM Top 10 where relevant); the ISMS scope covers AI.
- **L4:** AI usage is monitored (logs, DLP events); controls are tested; shadow-AI detection is routine; vendor security posture is reviewed periodically; metrics are reported.
- **L5:** Security architecture anticipates new AI threat classes; red-teaming and exercises occur; the security posture is a customer-facing asset.

### D6 — AI Lifecycle & Operations (YZ Yaşam Döngüsü ve Operasyon)
Whether there is a disciplined path from AI idea to governed production use: intake, approval, build/buy, validation, human oversight, monitoring, and change control. The operational core of ISO/IEC 42001 clause 8 and Annex A.6/A.9; ISO/IEC 5338 informs lifecycle detail.

| ID | Sub-dimension | Core | ISO-c |
|---|---|---|---|
| D6.1 | Use-case intake & approval | ✔ | ✔ |
| D6.2 | Development & deployment lifecycle | | ✔ |
| D6.3 | Validation, testing & human oversight | ✔ | ✔ |
| D6.4 | Monitoring & change management | | ✔ |

**Anchors**
- **L0:** No process; anything anyone builds or adopts goes live silently.
- **L1:** Enthusiasts launch pilots; no intake and no testing discipline; success depends on individuals.
- **L2:** Informal review precedes some deployments; occasional testing; lessons are not captured.
- **L3:** A defined lifecycle exists: intake and approval criteria, documented development/procurement steps, validation and human-oversight requirements per use case, and deployment/change control.
- **L4:** The lifecycle is instrumented: test and approval records, monitoring of performance and drift with thresholds, periodic revalidation, and a change log per AI system.
- **L5:** The lifecycle is optimized: automated evaluation harnesses, staged releases, post-incident learning loops; time-to-production and reliability improve continuously.

### D7 — People & Competence (İnsan ve Yetkinlik)
Whether people have the skills, awareness, and support to use AI well — a required control under ISO/IEC 42001 7.2–7.3 and, for companies in scope, the EU AI Act's Article 4 AI-literacy obligation (in force since February 2025). This is where the training business plugs into the management system.

| ID | Sub-dimension | Core | ISO-c |
|---|---|---|---|
| D7.1 | AI literacy & role-based competence | ✔ | ✔ |
| D7.2 | Training & awareness program | ✔ | ✔ |
| D7.3 | Applied proficiency in daily work | | |
| D7.4 | Talent & champions network | | |

**Anchors**
- **L0:** No AI skills, no training; fear or indifference dominates.
- **L1:** A few self-taught users; their knowledge stays with them.
- **L2:** Ad hoc trainings have been held; attendance is uneven; there is no role mapping.
- **L3:** Role-based competence requirements are defined; a structured training plan is executed with records; an awareness program covering policy and risks is running; AI-literacy obligations are addressed.
- **L4:** Competence is measured (assessments, certifications); training effectiveness is evaluated; a champions network operates with a defined role; skills gaps drive hiring and development plans.
- **L5:** A learning culture: internal academies, communities of practice, external recognition; competence-building anticipates upcoming AI capabilities.

### D8 — Value & Adoption (Değer ve Yaygınlaştırma)
Whether AI is actually producing measured business value across the value chain — office productivity and core operations (quality, maintenance, planning, supply chain, sales) — and whether pilots reach production. This is the offense leg and the dimension pure GRC tools ignore.

| ID | Sub-dimension | Core | ISO-c |
|---|---|---|---|
| D8.1 | Use-case portfolio coverage | ✔ | |
| D8.2 | Measured impact & ROI | ✔ | |
| D8.3 | Pilot-to-production scaling | ✔ | |
| D8.4 | Continuous opportunity discovery | | |

**Anchors**
- **L0:** No AI use cases anywhere.
- **L1:** Isolated personal-productivity use; no business use cases identified.
- **L2:** A few pilots in one or two functions; benefits are anecdotal; no baselines.
- **L3:** A documented use-case portfolio spans several functions, including at least one core-operations area; business cases have baselines; benefits are tracked for live cases.
- **L4:** The portfolio is managed with stage gates; ROI is measured on multiple production use cases including core operations; a scaling playbook exists.
- **L5:** AI is embedded in the core value chain; compounding benefits are measured year over year; new revenue or business-model effects appear; opportunity scouting is systematic.

---

## 8. Standards mapping approach

Every sub-dimension carries mappings in the workbook to: **ISO/IEC 42001:2023** (management clauses 4–10 and Annex A control groups A.2–A.10), **NIST AI RMF 1.0** functions (Govern, Map, Measure, Manage), and, where relevant, **EU AI Act** articles, **KVKK** obligations, **ISO/IEC 27001**, and **OWASP Top 10 for LLM Applications**. Supporting method standards referenced: ISO/IEC 23894 (AI risk management), ISO/IEC 42005:2025 (AI system impact assessment), ISO/IEC 5338 (AI lifecycle), ISO/IEC 5259 series (data quality for ML), ISO/IEC 38507 (governance implications of AI for boards).

Mapping is deliberately **many-to-many at the sub-dimension level**, not the question level, in v1.0. This keeps the crosswalk maintainable by one person while still allowing a single assessment to output: an ATOM report, an ISO/IEC 42001 gap analysis, a NIST AI RMF profile summary, and answers to the common blocks of customer AI questionnaires. Question-level mapping is a v2 refinement, to be done only after the discovery instrument stabilizes.

**Regulatory timeline note (as of July 2026, verify before each engagement):** the EU Digital Omnibus on AI, adopted June 2026, deferred stand-alone Annex III high-risk obligations to 2 December 2027 and product-embedded (Annex I) high-risk obligations to 2 August 2028; the Article 4 AI-literacy obligation has applied since February 2025; Türkiye has no dedicated AI law yet, with multiple proposals before the TBMM and KVKK board decisions guiding AI-related data processing. Implication for positioning: sell preparation windows and supplier credibility, not deadline panic — and keep D3.3 anchors current through the framework change log.

## 9. How the framework runs inside an engagement (evidence-first flow)

1. **Document request list (before day one).** A standing DRL maps document types to sub-dimensions (e.g., org chart → D2.3; ISO 27001 SoA → D5.4; training records → D7.2; ERP landscape → D4.4). The client uploads what exists.
2. **Evidence parsing & pre-scoring.** Uploaded evidence is parsed (AI-assisted) into facts with provenance; provisional Stated Scores are hypothesized per sub-dimension. Output: a gap-based interview guide containing only what the evidence could not answer — typically 40–60 targeted questions drawn from the workbook's key-question bank, not a 250-question interrogation.
3. **Targeted interviews & walkthroughs.** Role-specific sessions (owner/GM, IT, quality, HR, one operations lead) of 45–60 minutes, plus a live walkthrough of actual AI usage (D5.1, D7.3, D8.1 are best observed, not asked).
4. **Scoring.** Apply anchors, staged rule, Evidence Cap, confidence flags. Draft the finding log; every score reconstructible per the Section 5.4 pattern.
5. **Validation workshop (mandatory gate).** Client confirms the fact base and findings before any report or document is generated. Scores freeze here. This step is both quality control and professional-liability protection; skipping it is not permitted by the methodology.
6. **Report & roadmap.** ATOM Score and band, dimension radar, Certification Gate status, Evidence Gaps, top risks and top opportunities, and a two-tier roadmap: Tier 1 = close the Gate (ISO-critical gaps), Tier 2 = value moves (D8/D6 priorities). Benchmark comparison added once the database has ≥5 comparable records.

## 10. Benchmarking and data governance

Benchmark value compounds only if collection is disciplined from client one: store the 32 Evidenced Scores plus a minimal anonymized profile (sector at NACE-division level, employee-size band, export exposure yes/no), stamped with methodology version and assessment date. Rules: explicit written consent for anonymized benchmark use in every engagement contract; no company names, free text, or uploaded evidence in the benchmark store; KVKK-clean by design because only aggregate organizational scores — no personal data — are retained; a company can be excluded on request without breaking the dataset. Publish nothing externally until n ≥ 10 in a segment; before that, benchmarks are used only in private client reports as directional ranges.

## 11. Framework governance

Semantic versioning: patch = wording fixes; minor (v1.x) = anchor or question changes; major (v2) = structural changes to dimensions or scoring. Every assessment records the version used; benchmark comparisons only cross versions where a documented mapping exists. **Calibration protocol for v1.0 → v1.1:** during the first three paid engagements, log every scoring dispute, every anchor that felt ambiguous, evidence availability per sub-dimension, and time spent per sub-dimension; adjust anchors and the Core set accordingly; freeze v1.1 before engagement four. Maintain a change log at the end of this document.

## 12. Naming and brand

"ATOM — AI Transformation Operating Model" is the working name: short, bilingual-friendly, and consistent with the "operating system" positioning (it also nods to the atomic-fact data model underneath). Before external use: trademark search (Türk Patent + EUIPO), domain and social-handle check, and a collision check against existing assessment brands. Fallback candidate: MARI (Manufacturing AI Readiness Index). The score should always be branded (e.g., "ATOM Score: 47 — Structured"), because the branded number is what spreads inside client organizations and in sales conversations.

## 13. Known limitations and v1.1 backlog

Anchors are expert-drafted and not yet field-calibrated — treat the first three engagements as calibration runs. Turkish translations exist for dimension and band names only; sub-dimension anchors need full TR versions before client-facing use in Turkish. The key-question bank (in the workbook) is a seed, not the full tiered discovery instrument with branching logic. Sector overlays (automotive/IATF context, food & retail supply) are planned as add-on modules, not core changes. Inter-rater reliability is untested; the four-eyes rule in 6.6 is the interim control. Weight presets in 6.5 are directional and should be tuned against real client priorities.

---

### Change log
| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-18 | Initial framework: 8 dimensions, 32 sub-dimensions, staged 0–5 scale, Evidence Cap, Certification Gate, standards crosswalk v1. |

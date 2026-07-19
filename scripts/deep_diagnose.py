"""
ARIA Deep Diagnose — kampanyanın NEDEN göndermediğini bulur.

diagnose.py bağlantıları test eder; bu script gönderim zincirinin durumunu döker:
  - Kampanya: status, daily_limit, email_list, schedule, allow_risky
  - Gönderici hesaplar (v2): status + warmup + hata alanları (pause sebebi)
  - Kampanyadaki lead sayısı
  - Kampanya analytics: bugüne kadar kaç mail GERÇEKTEN gönderilmiş

Kullanım: python scripts/deep_diagnose.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

import requests

API = os.environ["INSTANTLY_API_KEY"]
CID = os.environ["INSTANTLY_CAMPAIGN_ID"]
H2  = {"Authorization": f"Bearer {API}", "Content-Type": "application/json"}

CAMP_STATUS = {0: "draft", 1: "ACTIVE", 2: "paused", 3: "completed", 4: "running_subsequences",
               -1: "accounts_unhealthy", -2: "bounce_protect", -99: "suspended"}
ACC_STATUS  = {1: "ACTIVE", 2: "PAUSED", -1: "connection_error", -2: "soft_bounce", -3: "send_error"}

print("=" * 62)
print("ARIA DEEP DIAGNOSE")
print("=" * 62)

# ── 1. Kampanya ─────────────────────────────────────────────────
print("\n── 1. Kampanya ──")
r = requests.get(f"https://api.instantly.ai/api/v2/campaigns/{CID}", headers=H2, timeout=15)
c = r.json() if r.status_code == 200 else {}
print(f"HTTP {r.status_code}")
print(f"  name        : {c.get('name')}")
print(f"  status      : {c.get('status')} = {CAMP_STATUS.get(c.get('status'), '?')}")
print(f"  daily_limit : {c.get('daily_limit')}")
print(f"  email_list  : {c.get('email_list')}")
print(f"  allow_risky : {c.get('allow_risky_contacts')}")
print(f"  end_date    : {c.get('end_date')}")
sched = c.get("campaign_schedule") or {}
for s in (sched.get("schedules") or []):
    print(f"  schedule    : {s.get('name')} | days={s.get('days')} | {s.get('timing')} | tz={s.get('timezone')}")

# ── 2. Gönderici hesaplar ───────────────────────────────────────
print("\n── 2. Gönderici Hesaplar (v2 /accounts) ──")
r = requests.get("https://api.instantly.ai/api/v2/accounts", params={"limit": 100}, headers=H2, timeout=15)
items = (r.json().get("items") if r.status_code == 200 else None) or []
print(f"HTTP {r.status_code} — {len(items)} hesap")
INTERESTING = ["email", "status", "warmup_status", "stat_warmup_score", "daily_limit",
               "sending_gap", "provider_code", "setup_pending", "is_managed_account",
               "status_message", "timestamp_last_used", "timestamp_updated"]
for a in items:
    print(f"\n  {a.get('email')}:")
    for k in INTERESTING:
        if k in a and a.get(k) is not None:
            print(f"    {k:22}: {a.get(k)}")
    st = a.get("status")
    print(f"    → yorum: {ACC_STATUS.get(st, f'bilinmiyor({st})')}")
    # Bilinmeyen ipucu alanlarını da göster (error/pause içeren her alan)
    for k, v in a.items():
        if k not in INTERESTING and any(w in k.lower() for w in ("error", "pause", "disable", "block")):
            print(f"    {k:22}: {v}")

# ── 3. Lead sayısı ──────────────────────────────────────────────
print("\n── 3. Kampanyadaki Lead Sayısı ──")
r = requests.get("https://api.instantly.ai/api/v1/lead/list",
                 params={"api_key": API, "campaign_id": CID, "limit": 5}, timeout=15)
if r.status_code == 200:
    d = r.json()
    total = d.get("total", "?")
    print(f"  toplam lead: {total}")
    leads = d.get("leads", d.get("data", [])) or []
    for l in leads[:5]:
        em = l.get("email", l.get("lead", "?"))
        st = l.get("status", l.get("lead_status", "?"))
        print(f"    örnek: {em} | status={st}")
else:
    print(f"  v1 lead/list HTTP {r.status_code}: {r.text[:200]}")

# ── 4. Analytics — gerçekte kaç mail gitti ──────────────────────
print("\n── 4. Kampanya Analytics (gerçek gönderim sayıları) ──")
r = requests.get("https://api.instantly.ai/api/v1/analytics/campaign/summary",
                 params={"api_key": API, "campaign_id": CID}, timeout=15)
print(f"  v1 summary HTTP {r.status_code}: {r.text[:400]}")
r = requests.get("https://api.instantly.ai/api/v2/campaigns/analytics",
                 params={"id": CID}, headers=H2, timeout=15)
print(f"  v2 analytics HTTP {r.status_code}: {r.text[:400]}")

print("\n" + "=" * 62)
print("Deep diagnose bitti.")
print("=" * 62)

"""
ARIA Diagnose — her bağlantıyı tek tek test eder.
Hangisi patlıyor anında görürsün.

Kullanım:
  python scripts/diagnose.py
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass  # GitHub Actions'ta .env yok, env vars direkt gelir

PASS = "✅"
FAIL = "❌"
WARN = "⚠️ "

def check(label, fn):
    try:
        result = fn()
        print(f"{PASS} {label}: {result}")
        return True
    except Exception as e:
        print(f"{FAIL} {label}: {e}")
        return False


print("\n═══════════════════════════════════")
print("       ARIA Diagnostic Check")
print("═══════════════════════════════════\n")

# 1. Environment variables
print("── 1. Environment Variables ──")
required_vars = [
    "ANTHROPIC_API_KEY",
    "GOOGLE_SERVICE_ACCOUNT_JSON",
    "GOOGLE_SHEET_ID",
    "INSTANTLY_API_KEY",
    "INSTANTLY_CAMPAIGN_ID",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
]
all_vars_ok = True
for var in required_vars:
    val = os.environ.get(var, "")
    if val:
        # Show first 8 chars only for security
        preview = val[:8] + "..." if len(val) > 8 else val
        print(f"{PASS} {var}: {preview}")
    else:
        print(f"{FAIL} {var}: MISSING")
        all_vars_ok = False

if not all_vars_ok:
    print("\n❌ Eksik env vars var. GitHub Secrets'a ekle ve tekrar dene.\n")
    sys.exit(1)

# 2. Google Service Account JSON format
print("\n── 2. Google Service Account JSON ──")
def check_google_json():
    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    data = json.loads(raw)
    required_keys = ["type", "project_id", "private_key", "client_email"]
    missing = [k for k in required_keys if k not in data]
    if missing:
        raise ValueError(f"JSON'da eksik alanlar: {missing}")
    return f"type={data['type']}, client_email={data['client_email'][:30]}..."

check("JSON format", check_google_json)

# 3. Google Sheets connection
print("\n── 3. Google Sheets ──")
def check_sheets():
    import json
    import gspread
    from google.oauth2.service_account import Credentials
    raw = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    creds_dict = json.loads(raw)
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    gc = gspread.authorize(creds)
    sheet_id = os.environ["GOOGLE_SHEET_ID"]
    sp = gc.open_by_key(sheet_id)
    return f"'{sp.title}' açıldı, {len(sp.worksheets())} tab var"

check("Google Sheets bağlantısı", check_sheets)

# 4. Anthropic API
print("\n── 4. Claude API (Anthropic) ──")
def check_anthropic():
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=10,
        messages=[{"role": "user", "content": "Say OK"}],
    )
    return f"Response: {msg.content[0].text}"

check("Claude Haiku API", check_anthropic)

# 5. Instantly.ai API
print("\n── 5. Instantly.ai ──")
def check_instantly():
    import requests
    api_key = os.environ["INSTANTLY_API_KEY"]
    campaign_id = os.environ["INSTANTLY_CAMPAIGN_ID"]
    resp = requests.get(
        "https://api.instantly.ai/api/v1/campaign/list",
        params={"api_key": api_key, "limit": 5},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    campaigns = data if isinstance(data, list) else data.get("data", [])
    ids = [c.get("id", "") for c in campaigns]
    if campaign_id in ids:
        return f"Kampanya bulundu ✓ ({len(campaigns)} kampanya toplam)"
    else:
        return f"{WARN} API çalışıyor ama kampanya ID eşleşmedi. Mevcut ID'ler: {ids}"

check("Instantly API + kampanya", check_instantly)

# 6. Telegram
print("\n── 6. Telegram Bot ──")
def check_telegram():
    import requests
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    # First verify bot exists
    resp = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
    resp.raise_for_status()
    bot_name = resp.json()["result"]["username"]
    # Send test message
    resp2 = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": "✅ ARIA diagnostic test — bağlantı çalışıyor!"},
        timeout=10,
    )
    resp2.raise_for_status()
    return f"Bot: @{bot_name} — mesaj gönderildi"

check("Telegram bot + mesaj gönderimi", check_telegram)

# 7. NOSAB Scraper — listing pages
print("\n── 7. NOSAB Scraper (listing pages A-Z) ──")
def check_nosab_listing():
    from src.scraper.nosab_scraper import scrape_nosab
    results = scrape_nosab()
    if not results:
        raise ValueError("Hiç firma bulunamadı — site yapısı değişmiş olabilir")
    sample = results[0]
    return f"{len(results)} firma bulundu | ilk: {sample['Company_Name']}"

check("NOSAB listing scraper", check_nosab_listing)

# 7b. NOSAB detail page — test on first company
print("\n── 7b. NOSAB Detail Page (1 firma detayı) ──")
def check_nosab_detail():
    import requests
    from src.scraper.nosab_scraper import scrape_nosab, scrape_nosab_detail
    from src.scraper.base_scraper import get_session
    results = scrape_nosab()
    if not results:
        raise ValueError("Listing scraper failed — cannot test detail page")
    # Find first company that has a detail URL
    for r in results:
        if r.get("detail_url"):
            session = get_session()
            detail = scrape_nosab_detail(session, r["detail_url"])
            email = detail.get("email", "—")
            domain = detail.get("domain", "—")
            return f"{r['Company_Name']} → email: {email} | domain: {domain}"
    raise ValueError("No company with detail_url found")

check("NOSAB detail page", check_nosab_detail)

# 7c. DOSAB Excel download
print("\n── 7c. DOSAB Excel Scraper ──")
def check_dosab():
    from src.scraper.dosab_scraper import scrape_dosab
    results = scrape_dosab()
    if not results:
        raise ValueError("Excel indirildi ama firma bulunamadı — sütun yapısı değişmiş olabilir")
    sample = results[0]
    return f"{len(results)} firma | örnek: {sample['Company_Name']} | email: {sample.get('Email', '—')}"

check("DOSAB Excel scraper", check_dosab)

print("\n═══════════════════════════════════")
print("  Diagnostic tamamlandı.")
print("  ❌ olan adımları düzelt, tekrar çalıştır.")
print("═══════════════════════════════════\n")

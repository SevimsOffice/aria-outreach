"""
Salt-okunur doğrulama scripti — hiçbir mail göndermez, sadece Sheet'in
gerçek durumunu raporlar. "Gönderildi mi, Sheet güncellendi mi?" sorusuna
varsayımsız, kanıtlı cevap vermek için.
"""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from src.config import get_config
from src.database.sheets_client import SheetsClient

cfg = get_config()
sheets = SheetsClient(cfg.google_service_account_json, cfg.google_sheet_id)
sheets.connect()

print("Sheet header (canlı):", sheets._ws.row_values(1))
print("Grid boyutu:", sheets._ws.row_count, "satır x", sheets._ws.col_count, "kolon")

records = sheets.get_all_records()
today = date.today().isoformat()

sent_today = [r for r in records if today in (r.get("Email1_Date", ""), r.get("Email2_Date", ""), r.get("Email3_Date", ""))]
with_content = [r for r in records if (r.get("Email1_Content") or r.get("Email2_Content") or r.get("Email3_Content"))]

print(f"\nToplam kayıt: {len(records)}")
print(f"Bugün ({today}) tarihli gönderim: {len(sent_today)}")
print(f"Email içeriği (Content kolonu) dolu olan kayıt: {len(with_content)}")

print("\n--- Bugün gönderilenlerin ilk 25'i ---")
for r in sent_today[:25]:
    content = r.get("Email1_Content") or r.get("Email2_Content") or r.get("Email3_Content") or ""
    print(f"  {r.get('Company_Name','?')} | {r.get('ARIA_Status','?')} | içerik uzunluğu: {len(content)} karakter")
    if content:
        print(f"    örnek: {content[:120]!r}")

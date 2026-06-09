"""
One-shot script — immediately fixes Instantly campaign settings:
  1. Enables allow_risky_contacts (so guessed emails are accepted, not silently dropped)
  2. Sets daily_limit to 50
  3. Extends end_date by 180 days if campaign ends within 60 days
  4. Activates campaign if it is paused/stopped/draft
  5. Prints a full status report

Run via GitHub Actions:
  Actions → "Fix Instantly Campaign" → Run workflow

Or locally:
  python scripts/fix_campaign.py
"""

import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from src.config import get_config
from src.outreach.instantly_client import InstantlyClient


def fix_campaign():
    cfg = get_config()
    client = InstantlyClient(cfg.instantly_api_key, cfg.instantly_campaign_id)

    print("=" * 60)
    print("ARIA — Instantly Campaign Fix")
    print("=" * 60)

    print("\nKampanya durumu kontrol ediliyor...")
    info = client.get_campaign_status()

    if not info.get("found"):
        print(f"❌ Kampanya bulunamadı (status={info.get('status')})")
        print(f"   Campaign ID: {cfg.instantly_campaign_id}")
        sys.exit(1)

    name            = info.get("name", "?")
    status          = info.get("status", "?")
    allow_risky     = info.get("allow_risky_contacts", "?")
    end_date_str    = info.get("end_date", "")
    daily_limit     = info.get("daily_limit", "?")

    print(f"\nKampanya: '{name}'")
    print(f"  Durum          : {status}")
    print(f"  allow_risky    : {allow_risky}")
    print(f"  end_date       : {end_date_str or '(yok)'}")
    print(f"  daily_limit    : {daily_limit}")

    patches = {}

    # Fix 1: allow_risky_contacts
    if allow_risky is False:
        patches["allow_risky_contacts"] = True
        print("\n⚠️  allow_risky_contacts=false — tahmin edilen emailler reddediliyor!")
        print("   → Düzeltiliyor: allow_risky_contacts=true")
    else:
        print("\n✅ allow_risky_contacts zaten OK")

    # Fix 2: daily_limit
    if daily_limit != 50:
        patches["daily_limit"] = 50
        print(f"\n⚠️  daily_limit={daily_limit} → 50'ye çekiliyor")
    else:
        print("\n✅ daily_limit zaten 50")

    # Fix 3: end_date
    if end_date_str:
        try:
            end = date.fromisoformat(end_date_str)
            days_left = (end - date.today()).days
            if days_left < 60:
                new_end = (date.today() + timedelta(days=180)).isoformat()
                patches["end_date"] = new_end
                print(f"\n⚠️  Kampanya {days_left} gün sonra bitiyor ({end_date_str})")
                print(f"   → Uzatılıyor: end_date={new_end}")
            else:
                print(f"\n✅ end_date OK ({days_left} gün kaldı)")
        except ValueError:
            print(f"\n⚠️  end_date parse edilemedi: {end_date_str}")
    else:
        print("\nℹ️  end_date belirtilmemiş (süresiz)")

    # Fix 4: activate if paused/stopped/draft
    if status in ("paused", "stopped", "draft"):
        patches["status"] = 1
        print(f"\n⚠️  Kampanya durumu='{status}' → aktivasyon uygulanıyor (status=1)")
    else:
        print(f"\n✅ Kampanya durumu OK ({status})")

    # Apply patches
    if patches:
        print(f"\nUygulanan düzeltmeler: {patches}")
        ok = client.patch_campaign(patches)
        if ok:
            print("✅ Kampanya başarıyla güncellendi!")
        else:
            print("❌ Kampanya güncellenemedi — Instantly API hatası")
            sys.exit(1)
    else:
        print("\n✅ Herhangi bir düzeltme gerekmedi")

    print("\n" + "=" * 60)
    print("İşlem tamamlandı. Pipeline'ı şimdi çalıştırabilirsiniz.")
    print("=" * 60)


if __name__ == "__main__":
    fix_campaign()

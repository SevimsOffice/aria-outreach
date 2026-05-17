"""
ARIA Daily Pipeline — runs every morning at 7 AM Turkey time via GitHub Actions.

Flow:
  1. Scrape NOSAB + DOSAB + KAYAPA OSB websites for new companies
  2. Deduplicate against master sheet
  3. Enrich each new company with email (Apollo → Hunter → guesser)
  4. Research each company website (Claude Haiku)
  5. Generate personalized email opening (Claude Haiku)
  6. Add to Instantly.ai campaign
  7. Update Google Sheets with status
  8. Send Telegram daily summary

Usage:
  python scripts/run_daily_pipeline.py
  python scripts/run_daily_pipeline.py --dry-run      (no sends, just print)
  python scripts/run_daily_pipeline.py --limit 10     (process only 10 new companies)
"""

import argparse
import logging
import os
import sys
import time

# Allow imports from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from src.config import get_config
from src.database.sheets_client import SheetsClient
from src.scraper.nosab_scraper import scrape_nosab, scrape_nosab_detail
from src.scraper.dosab_scraper import scrape_dosab
from src.scraper.kayapa_scraper import scrape_kayapa
from src.scraper.base_scraper import get_session
from src.scraper.deduplicator import merge_sources, deduplicate, validate_and_clean
from src.enrichment.apollo_client import ApolloClient
from src.enrichment.hunter_client import HunterClient
from src.enrichment.email_guesser import best_guess
from src.research.company_researcher import CompanyResearcher
from src.outreach.email_composer import EmailComposer
from src.outreach.instantly_client import InstantlyClient
from src.notifications.telegram import TelegramNotifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("aria.daily")


def run(dry_run: bool = False, limit: int = 50):
    logger.info(f"=== ARIA Daily Pipeline {'(DRY RUN) ' if dry_run else ''}===")

    cfg = get_config()
    errors = []

    # --- Clients ---
    sheets = SheetsClient(cfg.google_service_account_json, cfg.google_sheet_id)
    sheets.connect()

    apollo = ApolloClient(cfg.apollo_api_key) if cfg.apollo_api_key else None
    hunter = HunterClient(cfg.hunter_api_key) if cfg.hunter_api_key else None
    researcher = CompanyResearcher(cfg.anthropic_api_key)
    composer = EmailComposer(cfg.anthropic_api_key)
    instantly = InstantlyClient(cfg.instantly_api_key, cfg.instantly_campaign_id)
    telegram = TelegramNotifier(cfg.telegram_bot_token, cfg.telegram_chat_id)

    # --- Step 1: Scrape ---
    logger.info("Step 1: Scraping OSB websites...")
    try:
        nosab = scrape_nosab()
        dosab = scrape_dosab()
        kayapa = scrape_kayapa()
        all_scraped = merge_sources([nosab, dosab, kayapa])
        logger.info(f"Scraped total: {len(all_scraped)} companies")
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        errors.append(f"Scraping error: {e}")
        all_scraped = []

    # --- Step 2: Deduplicate ---
    logger.info("Step 2: Deduplicating...")
    existing_domains = sheets.get_existing_domains()
    existing_names   = sheets.get_existing_company_names()
    fresh = deduplicate(all_scraped, existing_domains, existing_names)
    fresh = validate_and_clean(fresh)
    fresh = fresh[:limit]
    logger.info(f"New companies to process: {len(fresh)}")

    if dry_run:
        logger.info("[DRY RUN] First 5 new companies:")
        for c in fresh[:5]:
            logger.info(f"  {c['Company_Name']} | {c['Domain']} | {c['OSB']}")

    # --- Steps 3–6: Enrich → Research → Compose → Send ---
    emails_sent = 0
    new_prospects_added = 0

    # Shared session for NOSAB detail page fetching
    nosab_session = get_session()

    for i, company in enumerate(fresh):
        name    = company["Company_Name"]
        domain  = company.get("Domain", "")
        sector  = company.get("Sector", "")
        osb     = company.get("OSB", "")

        logger.info(f"Processing [{i+1}/{len(fresh)}]: {name}")

        # Step 2.5: For NOSAB companies, fetch detail page to get email + domain
        # This runs BEFORE Apollo/Hunter so we use real contact data from the OSB site
        if osb == "NOSAB" and company.get("detail_url") and not company.get("Email"):
            logger.info(f"  Fetching NOSAB detail page for {name}")
            detail = scrape_nosab_detail(nosab_session, company["detail_url"])
            if detail.get("email"):
                company["Email"] = detail["email"]
                logger.info(f"  Found email from NOSAB detail: {detail['email']}")
            if detail.get("domain") and not domain:
                company["Domain"] = detail["domain"]
                domain = detail["domain"]
            if detail.get("phone") and not company.get("Phone"):
                company["Phone"] = detail["phone"]
            if detail.get("sector") and not sector:
                company["Sector"] = detail["sector"]
                sector = detail["sector"]

        # Step 3: Enrich email
        contact = None

        # Use email scraped directly from OSB site (highest quality — verified address)
        if company.get("Email"):
            contact = {
                "email":      company["Email"],
                "first_name": "",
                "last_name":  "",
                "title":      "",
                "source":     f"{osb.lower()}_direct",
            }
        elif domain:
            # Fallback: Apollo → Hunter → pattern guesser
            if apollo:
                contact = apollo.find_contact_by_domain(domain, name)
            if not contact and hunter:
                contact = hunter.find_email_by_domain(domain)
            if not contact:
                contact = best_guess(domain)

        if not contact or not contact.get("email"):
            logger.info(f"  No email found for {name} — skipping")
            continue

        email      = contact["email"]
        first_name = contact.get("first_name", "")
        last_name  = contact.get("last_name", "")
        title      = contact.get("title", "")
        source     = contact.get("source", "unknown")

        company["Email"]        = email
        company["Contact_Name"] = f"{first_name} {last_name}".strip()
        company["Source"]       = source

        logger.info(f"  Email: {email} (source: {source})")

        # Step 4: Research company
        research = researcher.research(name, domain, sector, osb)

        # Step 5: Compose personalized email
        email_content = composer.compose_initial(
            company_name=name,
            sector=sector,
            osb=osb,
            main_activity=research["main_activity"],
            pain_points=research["likely_pain_points"],
            contact_name=f"{first_name} {last_name}".strip(),
        )

        logger.info(f"  Subject: {email_content['subject']}")
        logger.info(f"  Personalized line: {email_content['personalized_line'][:80]}...")

        if dry_run:
            logger.info(f"  [DRY RUN] Would add to Instantly campaign")
            new_prospects_added += 1
            continue

        # Step 6: Add to Instantly campaign
        result = instantly.add_contact(
            email=email,
            first_name=first_name,
            last_name=last_name,
            company_name=name,
            personalized_line=email_content["personalized_line"],
            sector=sector,
            osb=osb,
        )

        if result:
            emails_sent += 1
            new_prospects_added += 1
            # Update Google Sheet
            sheets.add_prospects([company])
            sheets.update_status(
                domain=domain,
                email=email,       # Fallback for NOSAB companies with no domain
                fields={
                    "ARIA_Status": "Added_to_Instantly",
                    "Email1_Date": __import__("datetime").date.today().isoformat(),
                },
            )
        else:
            errors.append(f"Instantly failed for {name}")

        time.sleep(0.5)  # Polite rate limiting

    # --- Step 7: Telegram summary ---
    logger.info(f"Pipeline complete: {emails_sent} added to campaign, {len(errors)} errors")

    if not dry_run:
        telegram.send_daily_summary(
            new_prospects_found=len(all_scraped),
            emails_sent=emails_sent,
            replies_today=0,  # Handled by reply_handler
            hot_leads_today=0,
            errors=errors if errors else None,
        )

    logger.info("=== Done ===")
    return {"sent": emails_sent, "new": new_prospects_added, "errors": len(errors)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARIA Daily Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Run without sending anything")
    parser.add_argument("--limit", type=int, default=50, help="Max companies to process")
    args = parser.parse_args()
    run(dry_run=args.dry_run, limit=args.limit)

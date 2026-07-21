"""
ARIA SMTP Gönderim — Instantly'siz, kendi mailbox'ından (Hostinger vb.) doğrudan gönderim.

Instantly'nin üstlendiği 3 işi burada yapıyoruz:
  1. Gönderim (SMTPSender → smtplib)
  2. Takip zamanlaması (Email1_Sent → 4 gün sonra takip1 → 4 gün sonra takip2)
  3. Tempolama (gönderimler arası 45-90sn, günlük limit)

Kimler gönderilir (Sheet'ten, sırayla):
  1. Takip 2: ARIA_Status=Email2_Sent, Email2_Date ≥4 gün önce, yanıt yok
  2. Takip 1: ARIA_Status=Email1_Sent, Email1_Date ≥4 gün önce, yanıt yok
  3. İlk mail: ARIA_Status boş, Email dolu, Source 'guessed' ile başlamıyor

Kimler atlanır: Replied_*, Unsubscribed, Source 'guessed'.

Warmup YOK — bu yüzden limit düşük tutulur (varsayılan 20/gün) ve günlük
sayaç, bugün zaten gönderilmiş satırları da hesaba katar (aynı gün birden
fazla çalıştırma toplam limiti aşamaz).

Kullanım:
  python scripts/run_send_smtp.py --dry-run --limit 5
  python scripts/run_send_smtp.py --limit 10
  python scripts/run_send_smtp.py --limit 1 --to-test-recipient   # kendine test
  python scripts/run_send_smtp.py --ai                            # Claude ile kişiselleştir (ilk mail)
"""

import argparse
import logging
import os
import random
import sys
import time
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from src.config import get_config
from src.database.sheets_client import SheetsClient
from src.outreach.smtp_sender import SMTPSender
from src.outreach.email_composer import EmailComposer, _fallback_personalized_line
from src.notifications.telegram import TelegramNotifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("aria.smtp_send")

SKIP_STATUSES = {"Replied_HOT", "Replied_WARM", "Replied_COLD", "Unsubscribed"}
FOLLOWUP_GAP_DAYS = 4
MAX_CONSECUTIVE_FAILURES = 3
SLEEP_MIN_SEC = 45
SLEEP_MAX_SEC = 90


def _days_since(date_str: str) -> int | None:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (date.today() - d).days
    except (ValueError, TypeError):
        return None


def select_work(records: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """Sheet kayıtlarını 3 kovaya ayırır: takip2, takip1, ilk mail (bu sırada işlenir)."""
    followup2, followup1, initial = [], [], []
    for r in records:
        status = r.get("ARIA_Status", "")
        email = (r.get("Email") or "").strip()
        source = (r.get("Source") or "").strip()

        if status in SKIP_STATUSES or not email:
            continue

        if status == "Email2_Sent":
            days = _days_since(r.get("Email2_Date", ""))
            if days is not None and days >= FOLLOWUP_GAP_DAYS:
                followup2.append(r)
        elif status == "Email1_Sent":
            days = _days_since(r.get("Email1_Date", ""))
            if days is not None and days >= FOLLOWUP_GAP_DAYS:
                followup1.append(r)
        elif not status:
            if source.startswith("guessed"):
                continue
            initial.append(r)

    return followup2, followup1, initial


def count_sent_today(records: list[dict]) -> int:
    today = date.today().isoformat()
    count = 0
    for r in records:
        if today in (r.get("Email1_Date", ""), r.get("Email2_Date", ""), r.get("Email3_Date", "")):
            count += 1
    return count


def run(dry_run: bool = False, limit: int = 20, use_ai: bool = False, to_test_recipient: bool = False):
    logger.info(f"=== ARIA SMTP Gönderim {'(DRY RUN) ' if dry_run else ''}— limit={limit} ===")

    cfg = get_config()

    if not (cfg.smtp_host and cfg.smtp_user and cfg.smtp_pass):
        logger.error(
            "SMTP yapılandırması eksik — SMTP_HOST / SMTP_USER / SMTP_PASS "
            "GitHub Secrets'a (veya .env'e) eklenmeli. Duruyorum."
        )
        sys.exit(1)

    if to_test_recipient and not cfg.test_recipient:
        logger.error("--to-test-recipient için TEST_RECIPIENT ayarlı olmalı. Duruyorum.")
        sys.exit(1)

    sheets = SheetsClient(cfg.google_service_account_json, cfg.google_sheet_id)
    sheets.connect()
    sender = SMTPSender(cfg.smtp_host, cfg.smtp_port, cfg.smtp_user, cfg.smtp_pass, cfg.smtp_from_name)
    composer = EmailComposer(cfg.anthropic_api_key) if use_ai else None
    telegram = TelegramNotifier(cfg.telegram_bot_token, cfg.telegram_chat_id)

    records = sheets.get_all_records()
    logger.info(f"Sheet'te toplam {len(records)} kayıt")

    sent_today = count_sent_today(records)
    remaining = max(0, limit - sent_today)
    if sent_today:
        logger.info(f"Bugün zaten {sent_today} gönderim yapılmış — kalan kota: {remaining}/{limit}")
    if remaining == 0:
        logger.info("Günlük limit dolu — çıkılıyor.")
        return {"sent": 0, "skipped": 0, "errors": 0}

    followup2, followup1, initial = select_work(records)
    logger.info(
        f"Aday sayıları — takip2: {len(followup2)} | takip1: {len(followup1)} | "
        f"ilk mail: {len(initial)}"
    )

    work_queue = (
        [("followup2", r) for r in followup2]
        + [("followup1", r) for r in followup1]
        + [("initial", r) for r in initial]
    )[:remaining]

    sent = 0
    skipped = 0
    errors: list[str] = []
    consecutive_failures = 0

    for i, (stage, row) in enumerate(work_queue):
        name = row.get("Company_Name", "")
        domain = row.get("Domain", "")
        sector = row.get("Sector", "")
        osb = row.get("OSB", "")
        email = row.get("Email", "").strip()
        contact_name = row.get("Contact_Name", "")

        if stage == "initial":
            if use_ai:
                content = composer.compose_initial(
                    company_name=name, sector=sector, osb=osb,
                    main_activity="", pain_points="", contact_name=contact_name,
                )
            else:
                line = _fallback_personalized_line(name, sector, osb)
                from src.outreach.email_composer import _load_template, _make_salutation
                body = _load_template("templates/email_initial_tr.txt").format(
                    salutation=_make_salutation(contact_name),
                    personalized_line=line,
                    company_name=name,
                    sector=sector,
                )
                content = {"subject": f"{name} için yapay zeka verimlilik atölyesi", "body": body}
            status_field, date_field = "Email1_Sent", "Email1_Date"
        elif stage == "followup1":
            tmp = EmailComposer(cfg.anthropic_api_key) if composer is None else composer
            content = tmp.compose_followup1(company_name=name, sector=sector, contact_name=contact_name)
            status_field, date_field = "Email2_Sent", "Email2_Date"
        else:  # followup2
            tmp = EmailComposer(cfg.anthropic_api_key) if composer is None else composer
            content = tmp.compose_followup2(company_name=name, sector=sector, contact_name=contact_name)
            status_field, date_field = "Email3_Sent", "Email3_Date"

        recipient = cfg.test_recipient if to_test_recipient else email
        logger.info(f"[{i+1}/{len(work_queue)}] ({stage}) {name} <{recipient}> — {content['subject']}")

        if dry_run:
            logger.info(f"  [DRY RUN] gönderilmedi. Gövde ilk 100 karakter: {content['body'][:100]!r}")
            sent += 1
            continue

        ok = sender.send(recipient, content["subject"], content["body"])

        if ok:
            sent += 1
            consecutive_failures = 0
            if not to_test_recipient:
                sheets.update_status(
                    domain=domain, email=email,
                    fields={"ARIA_Status": status_field, date_field: date.today().isoformat()},
                )
            logger.info("  Gönderildi ✓")
        else:
            skipped += 1
            consecutive_failures += 1
            errors.append(f"SMTP hatası: {name} <{recipient}>")
            logger.warning(f"  Gönderilemedi — {name}")
            if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                logger.error(
                    f"{MAX_CONSECUTIVE_FAILURES} ardışık SMTP hatası — mailbox/parola sorunu "
                    "olabilir, gönderim durduruluyor."
                )
                break

        if i < len(work_queue) - 1:
            time.sleep(random.uniform(SLEEP_MIN_SEC, SLEEP_MAX_SEC))

    logger.info(f"=== Bitti: {sent} gönderildi, {skipped} atlandı, {len(errors)} hata ===")

    if not dry_run and not to_test_recipient:
        telegram.send_daily_summary(
            new_prospects_found=0,
            emails_sent=sent,
            replies_today=0,
            hot_leads_today=0,
            errors=errors[:3] if errors else None,
            sent_label="SMTP ile gönderildi",
        )

    return {"sent": sent, "skipped": skipped, "errors": len(errors)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARIA SMTP Gönderim")
    parser.add_argument("--dry-run", action="store_true", help="Göster, gönderme")
    parser.add_argument("--limit", type=int, default=20, help="Günlük max gönderim (varsayılan: 20)")
    parser.add_argument("--ai", action="store_true", help="İlk mail açılışını Claude ile kişiselleştir (maliyetli)")
    parser.add_argument(
        "--to-test-recipient", action="store_true",
        help="Gerçek adaylara değil, TEST_RECIPIENT'a gönder; Sheet güncellenmez",
    )
    args = parser.parse_args()
    run(dry_run=args.dry_run, limit=args.limit, use_ai=args.ai, to_test_recipient=args.to_test_recipient)

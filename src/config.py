"""
ARIA Configuration — loads and validates all environment variables.
Fails loudly at startup if anything is missing so you never get
a silent failure halfway through a 50-email run.
"""

import os
from dataclasses import dataclass


@dataclass
class Config:
    # Claude API
    anthropic_api_key: str

    # Google Sheets
    google_service_account_json: str
    google_sheet_id: str

    # Email enrichment
    apollo_api_key: str
    hunter_api_key: str

    # Telegram
    telegram_bot_token: str
    telegram_chat_id: str

    # Sending limits
    daily_send_limit: int = 50

    # Instantly.ai — opsiyonel: abonelik iptal edildi (Temmuz 2026, 402
    # Payment Required). SMTP moduna geçildi; bu alanlar sadece eski
    # Instantly scriptleri (fix_campaign.py, run_resend_from_sheet.py vb.)
    # elle çalıştırılırsa kullanılır.
    instantly_api_key: str = ""
    instantly_campaign_id: str = ""

    # SMTP (Instantly ödemesiz gönderim modu) — hepsi opsiyonel.
    # Boşsa run_send_smtp.py başlarken açıkça hata verir; diğer scriptler
    # bunlara hiç dokunmadığı için Instantly-modu bozulmaz.
    smtp_host: str = ""
    smtp_port: int = 465
    smtp_user: str = ""
    smtp_pass: str = ""
    smtp_from_name: str = ""
    test_recipient: str = ""


def load_config() -> Config:
    """Load config from environment variables. Raises EnvironmentError if any required var is missing."""
    missing = []

    def require(key: str) -> str:
        val = os.environ.get(key, "").strip()
        if not val:
            missing.append(key)
        return val

    def optional(key: str, default: str = "") -> str:
        return os.environ.get(key, default).strip()

    cfg = Config(
        anthropic_api_key=require("ANTHROPIC_API_KEY"),
        google_service_account_json=require("GOOGLE_SERVICE_ACCOUNT_JSON"),
        google_sheet_id=require("GOOGLE_SHEET_ID"),
        apollo_api_key=optional("APOLLO_API_KEY"),       # Optional — falls back to Hunter + guesser
        hunter_api_key=optional("HUNTER_API_KEY"),       # Optional — falls back to guesser
        telegram_bot_token=require("TELEGRAM_BOT_TOKEN"),
        telegram_chat_id=require("TELEGRAM_CHAT_ID"),
        daily_send_limit=int(optional("DAILY_SEND_LIMIT", "50")),
        instantly_api_key=optional("INSTANTLY_API_KEY"),
        instantly_campaign_id=optional("INSTANTLY_CAMPAIGN_ID"),
        smtp_host=optional("SMTP_HOST"),
        smtp_port=int(optional("SMTP_PORT", "465")),
        smtp_user=optional("SMTP_USER"),
        smtp_pass=optional("SMTP_PASS"),
        smtp_from_name=optional("SMTP_FROM_NAME"),
        test_recipient=optional("TEST_RECIPIENT"),
    )

    if missing:
        raise EnvironmentError(
            f"ARIA: Missing required environment variables:\n"
            + "\n".join(f"  - {k}" for k in missing)
            + "\n\nCopy .env.example to .env and fill in the values."
        )

    return cfg


# Singleton — import this in other modules
_config: Config | None = None


def get_config() -> Config:
    global _config
    if _config is None:
        _config = load_config()
    return _config

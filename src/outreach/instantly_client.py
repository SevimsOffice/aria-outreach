"""
Instantly.ai API client — adds contacts to campaigns and fetches replies.
Instantly handles all sequence logic (timing, follow-ups, unsubscribes).
API docs: https://developer.instantly.ai
"""

import logging
from datetime import datetime, timezone

import requests

logger = logging.getLogger(__name__)

INSTANTLY_BASE = "https://api.instantly.ai/api/v1"


class InstantlyClient:
    def __init__(self, api_key: str, campaign_id: str):
        self._api_key = api_key
        self._campaign_id = campaign_id
        self._headers = {
            "Content-Type": "application/json",
        }

    def _params(self, extra: dict = None) -> dict:
        p = {"api_key": self._api_key}
        if extra:
            p.update(extra)
        return p

    # ------------------------------------------------------------------ #
    #  Contact management                                                  #
    # ------------------------------------------------------------------ #

    def add_contact(
        self,
        email: str,
        first_name: str = "",
        last_name: str = "",
        company_name: str = "",
        personalized_line: str = "",
        sector: str = "",
        osb: str = "",
    ) -> dict | None:
        """
        Add a contact to the active campaign.
        Returns Instantly response dict, or None on failure.
        Custom variables map to {{personalized_line}}, {{sector}}, {{osb}} in templates.
        """
        payload = {
            "api_key": self._api_key,
            "campaign_id": self._campaign_id,
            "skip_if_in_workspace": True,   # Don't duplicate contacts
            "leads": [
                {
                    "email": email,
                    "first_name": first_name or "",
                    "last_name": last_name or "",
                    "company_name": company_name or "",
                    "custom_variables": {
                        "personalized_line": personalized_line,
                        "sector": sector,
                        "osb": osb,
                    },
                }
            ],
        }
        try:
            resp = requests.post(
                f"{INSTANTLY_BASE}/lead/add",
                json=payload,
                headers=self._headers,
                timeout=20,
            )
            if resp.status_code == 429:
                logger.warning("Instantly rate limit hit")
                return None
            resp.raise_for_status()
            data = resp.json()
            logger.info(f"Added to Instantly: {email} → {data}")
            return data
        except requests.RequestException as e:
            logger.error(f"Instantly add_contact error for {email}: {e}")
            return None

    def get_campaign_stats(self) -> dict:
        """Fetch high-level campaign statistics."""
        try:
            resp = requests.get(
                f"{INSTANTLY_BASE}/analytics/campaign/summary",
                params=self._params({"campaign_id": self._campaign_id}),
                headers=self._headers,
                timeout=15,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            logger.warning(f"Instantly stats error: {e}")
            return {}

    # ------------------------------------------------------------------ #
    #  Reply fetching                                                      #
    # ------------------------------------------------------------------ #

    def get_replies(self, since_timestamp: str = "") -> list[dict]:
        """
        Fetch replies received since a given ISO timestamp.
        Returns list of reply objects:
          {from_email, subject, body, lead_email, reply_time, campaign_id}
        """
        try:
            params = self._params({
                "campaign_id": self._campaign_id,
                "limit": 100,
            })
            resp = requests.get(
                f"{INSTANTLY_BASE}/unibox/emails",
                params=params,
                headers=self._headers,
                timeout=20,
            )
            resp.raise_for_status()
            data = resp.json()
            emails = data.get("emails", data) if isinstance(data, dict) else data

            replies = []
            for email in emails:
                # Filter to only inbound (replies, not sent)
                if email.get("email_type") not in ("reply", "inbound", 1, "1"):
                    continue
                # Filter by timestamp if provided
                if since_timestamp:
                    reply_time = email.get("created_at", email.get("timestamp", ""))
                    if reply_time and reply_time <= since_timestamp:
                        continue
                replies.append({
                    "from_email": email.get("from_address", email.get("from_email", "")),
                    "subject": email.get("subject", ""),
                    "body": _clean_reply_body(email.get("body", email.get("text", ""))),
                    "lead_email": email.get("lead_email", email.get("to_address", "")),
                    "reply_time": email.get("created_at", email.get("timestamp", "")),
                    "email_id": email.get("id", ""),
                })
            return replies
        except requests.RequestException as e:
            logger.error(f"Instantly get_replies error: {e}")
            return []

    def get_leads_count(self) -> int:
        """How many leads are currently in the campaign."""
        try:
            resp = requests.get(
                f"{INSTANTLY_BASE}/lead/list",
                params=self._params({"campaign_id": self._campaign_id, "limit": 1}),
                headers=self._headers,
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("total", 0)
        except requests.RequestException:
            return 0


def _clean_reply_body(body: str) -> str:
    """Remove quoted/forwarded content from reply body to get just the new text."""
    if not body:
        return ""
    import re
    # Remove common reply separators
    patterns = [
        r"-----Original Message-----.*",
        r"On .+wrote:.*",
        r"From:.*\nSent:.*\nTo:.*",
        r"_{10,}.*",
        r"> .*",
    ]
    for pattern in patterns:
        body = re.sub(pattern, "", body, flags=re.DOTALL | re.IGNORECASE)
    return body.strip()[:2000]  # Cap at 2000 chars

"""
Email pattern guesser — last resort when Apollo and Hunter find nothing.
Generates likely email addresses from company domain using common Turkish
business email patterns. Marks them as "guessed" so we know to be gentle.
"""

import logging

logger = logging.getLogger(__name__)

# Most common Turkish SMB email patterns, ordered by probability
GENERIC_PATTERNS = [
    "info",
    "iletisim",
    "bilgi",
    "satis",
    "mail",
    "ofis",
    "admin",
    "muhasebe",
    "ihracat",
]


def guess_emails(domain: str, first_name: str = "", last_name: str = "") -> list[dict]:
    """
    Generate candidate email addresses for a domain.
    Returns list sorted by most likely first.
    Only the first one is used for outreach — others as fallback if bounce.
    """
    if not domain:
        return []

    candidates = []

    # 1. Generic patterns first (most reliable for Turkish SMBs)
    for prefix in GENERIC_PATTERNS:
        candidates.append({
            "email": f"{prefix}@{domain}",
            "first_name": "",
            "last_name": "",
            "title": "",
            "source": "guessed_generic",
            "confidence": 40,
        })

    # 2. Personal email patterns if we have a name
    if first_name and last_name:
        fn = _clean(first_name)
        ln = _clean(last_name)
        personal_patterns = [
            f"{fn}.{ln}@{domain}",
            f"{fn}{ln}@{domain}",
            f"{fn[0]}{ln}@{domain}",
            f"{fn}@{domain}",
        ]
        for email in personal_patterns:
            candidates.append({
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "title": "",
                "source": "guessed_personal",
                "confidence": 55,
            })
        # Re-sort: personal patterns are more likely if we have a real name
        candidates = sorted(candidates, key=lambda c: c["confidence"], reverse=True)

    return candidates


def best_guess(domain: str, first_name: str = "", last_name: str = "") -> dict | None:
    """Return the single best email guess for a domain."""
    candidates = guess_emails(domain, first_name, last_name)
    if candidates:
        return candidates[0]
    return None


def _clean(name: str) -> str:
    """Normalize name for email: lowercase, remove accents, spaces."""
    if not name:
        return ""
    name = name.lower().strip()
    replacements = {
        "ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u",
        "â": "a", "î": "i", "û": "u",
    }
    for tr, en in replacements.items():
        name = name.replace(tr, en)
    # Remove non-alphanumeric
    import re
    name = re.sub(r"[^a-z0-9]", "", name)
    return name

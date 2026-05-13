"""
Deduplicator — removes companies already in Google Sheets master.
Also cleans and validates prospect records before inserting.
"""

import logging
import re

logger = logging.getLogger(__name__)


def deduplicate(prospects: list[dict], existing_domains: set[str]) -> list[dict]:
    """
    Filter out:
    - Companies whose domain already exists in the master sheet
    - Records with no company name
    - Records that look like junk (empty, test entries, etc.)
    Returns only genuinely new prospects.
    """
    fresh = []
    skipped_dupe = 0
    skipped_invalid = 0

    for p in prospects:
        domain = p.get("Domain", "").lower().strip()
        name = p.get("Company_Name", "").strip()

        if not name or len(name) < 3:
            skipped_invalid += 1
            continue

        if not domain:
            # No domain — keep but mark as needing enrichment
            pass
        elif domain in existing_domains:
            skipped_dupe += 1
            continue

        fresh.append(p)
        if domain:
            existing_domains.add(domain)  # Prevent intra-batch dupes

    logger.info(
        f"Dedup: {len(fresh)} new | {skipped_dupe} already in sheet | {skipped_invalid} invalid"
    )
    return fresh


def merge_sources(sources: list[list[dict]]) -> list[dict]:
    """
    Merge multiple scraper outputs, deduplicating by domain within the batch.
    Call this before passing to the master sheet dedup.
    """
    seen_domains = set()
    merged = []
    for batch in sources:
        for p in batch:
            domain = p.get("Domain", "").lower().strip()
            if domain and domain in seen_domains:
                continue
            if domain:
                seen_domains.add(domain)
            merged.append(p)
    return merged


def validate_and_clean(prospects: list[dict]) -> list[dict]:
    """Final cleaning pass — normalizes fields, removes garbage."""
    clean = []
    for p in prospects:
        name = p.get("Company_Name", "").strip()
        if not name:
            continue
        # Remove obvious non-company strings
        if re.match(r"^\d+$", name):
            continue
        if name.lower() in {"firma adı", "şirket adı", "company name", "name"}:
            continue
        domain = p.get("Domain", "").strip()
        # Validate domain looks like a real domain
        if domain and not re.match(r"^[\w\-]+\.[\w\.\-]+$", domain):
            p["Domain"] = ""
        clean.append(p)
    return clean

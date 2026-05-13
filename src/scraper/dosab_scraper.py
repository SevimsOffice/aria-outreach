"""
DOSAB (Demirtaş OSB) scraper — dosab.org.tr
"""

import logging
import re
from .base_scraper import get_session, fetch_page, extract_domain, normalize_phone, clean_company_name

logger = logging.getLogger(__name__)

BASE_URL   = "https://www.dosab.org.tr"
MEMBER_URL = f"{BASE_URL}/uyeler"
OSB_NAME   = "DOSAB"


def scrape_dosab() -> list[dict]:
    session = get_session()
    companies = []

    logger.info(f"Starting DOSAB scrape: {MEMBER_URL}")
    soup = fetch_page(MEMBER_URL, session)
    if not soup:
        # Try alternate URL pattern
        soup = fetch_page(f"{BASE_URL}/firmalar", session)
    if not soup:
        logger.error("Failed to load DOSAB member page")
        return []

    companies.extend(_parse_dosab(soup))

    # Handle pagination
    pagination = soup.find("ul", class_=lambda c: c and "page" in (c or ""))
    if pagination:
        for a in pagination.find_all("a", href=True):
            href = a["href"]
            if not href.startswith("http"):
                href = BASE_URL + href
            page_soup = fetch_page(href, session)
            if page_soup:
                companies.extend(_parse_dosab(page_soup))

    seen = set()
    unique = []
    for c in companies:
        key = c["Company_Name"].lower()
        if key and key not in seen:
            seen.add(key)
            unique.append(c)

    logger.info(f"DOSAB: scraped {len(unique)} companies")
    return unique


def _parse_dosab(soup) -> list[dict]:
    companies = []

    # Strategy 1: look for table rows
    for row in soup.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) >= 2:
            name = clean_company_name(cols[0].get_text())
            if not name or len(name) < 3:
                continue
            website = ""
            phone = ""
            sector = ""
            for col in cols:
                link = col.find("a", href=True)
                if link and ("http" in link.get("href", "") or "www" in link.get("href", "")):
                    website = link["href"]
                text = col.get_text()
                if re.search(r"0\d{10}", re.sub(r"\s", "", text)):
                    phone = normalize_phone(text)
            domain = extract_domain(website)
            companies.append(_make_record(name, sector, domain, phone, ""))

    # Strategy 2: cards/divs
    if not companies:
        for div in soup.find_all(["div", "li"], class_=True):
            classes = " ".join(div.get("class", []))
            if not any(x in classes for x in ["firma", "uye", "member", "card", "company", "item"]):
                continue
            name_el = div.find(["h2", "h3", "h4", "strong", "b", "a"])
            if not name_el:
                continue
            name = clean_company_name(name_el.get_text())
            if not name or len(name) < 3:
                continue
            website = ""
            for a in div.find_all("a", href=True):
                if "http" in a["href"] or "www" in a["href"]:
                    website = a["href"]
                    break
            text = div.get_text()
            phone_m = re.search(r"0\s*\d{3}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}", text)
            phone = normalize_phone(phone_m.group() if phone_m else "")
            domain = extract_domain(website)
            companies.append(_make_record(name, "", domain, phone, ""))

    return companies


def _make_record(name, sector, domain, phone, address) -> dict:
    return {
        "Company_Name": name,
        "Sector": sector,
        "Domain": domain,
        "Phone": phone,
        "Address": address,
        "OSB": OSB_NAME,
    }

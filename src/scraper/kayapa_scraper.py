"""
KAYAPA OSB scraper — kayapaosb.org.tr
"""

import logging
import re
from .base_scraper import get_session, fetch_page, extract_domain, normalize_phone, clean_company_name

logger = logging.getLogger(__name__)

BASE_URL   = "https://www.kayapaosb.org.tr"
MEMBER_URL = f"{BASE_URL}/firmalar"
OSB_NAME   = "KAYAPA"

ALTERNATE_URLS = [
    f"{BASE_URL}/uyeler",
    f"{BASE_URL}/firmalarimiz",
    f"{BASE_URL}/uye-firmalar",
]


def scrape_kayapa() -> list[dict]:
    session = get_session()
    companies = []

    soup = fetch_page(MEMBER_URL, session)
    if not soup:
        for alt in ALTERNATE_URLS:
            soup = fetch_page(alt, session)
            if soup:
                break
    if not soup:
        logger.error("Failed to load KAYAPA member page")
        return []

    companies.extend(_parse_kayapa(soup))

    # Pagination
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        if text.isdigit() and int(text) > 1:
            full_url = href if href.startswith("http") else BASE_URL + href
            page_soup = fetch_page(full_url, session)
            if page_soup:
                companies.extend(_parse_kayapa(page_soup))

    seen = set()
    unique = []
    for c in companies:
        key = c["Company_Name"].lower()
        if key and key not in seen:
            seen.add(key)
            unique.append(c)

    logger.info(f"KAYAPA: scraped {len(unique)} companies")
    return unique


def _parse_kayapa(soup) -> list[dict]:
    companies = []

    # Strategy 1: tables
    for row in soup.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) < 2:
            continue
        name = clean_company_name(cols[0].get_text())
        if not name or len(name) < 3:
            continue
        website, phone, sector, address = "", "", "", ""
        for col in cols:
            link = col.find("a", href=True)
            if link and ("http" in link.get("href", "") or "www" in link.get("href", "")):
                website = link["href"]
            text = col.get_text()
            if re.search(r"0\d{10}", re.sub(r"\s", "", text)):
                phone = normalize_phone(text)
        domain = extract_domain(website)
        companies.append(_make_record(name, sector, domain, phone, address))

    # Strategy 2: divs/cards
    if not companies:
        containers = soup.find_all(["div", "article", "li"], class_=True)
        for div in containers:
            classes = " ".join(div.get("class", []))
            if not any(x in classes.lower() for x in ["firma", "uye", "company", "member", "card", "post", "item"]):
                continue
            name_el = div.find(["h2", "h3", "h4", "strong", "b"])
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

"""
NOSAB (Nilüfer OSB) scraper — nosab.org.tr
Extracts member company list: name, website, phone, address, sector.
"""

import logging
from .base_scraper import get_session, fetch_page, extract_domain, normalize_phone, clean_company_name

logger = logging.getLogger(__name__)

BASE_URL    = "https://www.nosab.org.tr"
MEMBER_URL  = f"{BASE_URL}/uyeler"          # Primary listing page
OSB_NAME    = "NOSAB"


def scrape_nosab() -> list[dict]:
    """
    Scrape NOSAB member companies.
    Returns list of dicts with keys:
      Company_Name, Sector, Domain, Phone, Address, OSB
    """
    session = get_session()
    companies = []

    logger.info(f"Starting NOSAB scrape: {MEMBER_URL}")
    soup = fetch_page(MEMBER_URL, session)
    if not soup:
        logger.error("Failed to load NOSAB member page")
        return []

    # Try multiple known HTML patterns for OSB sites
    companies.extend(_parse_table_layout(soup))

    # If first parse found nothing, try card/list layout
    if not companies:
        companies.extend(_parse_card_layout(soup))

    # Paginate if there are multiple pages
    pagination = soup.find("ul", class_=lambda c: c and "pagination" in c)
    if pagination:
        page_links = pagination.find_all("a", href=True)
        visited = {MEMBER_URL}
        for link in page_links:
            href = link["href"]
            if not href.startswith("http"):
                href = BASE_URL + href
            if href not in visited:
                visited.add(href)
                page_soup = fetch_page(href, session)
                if page_soup:
                    companies.extend(_parse_table_layout(page_soup))
                    companies.extend(_parse_card_layout(page_soup))

    # Deduplicate by company name
    seen = set()
    unique = []
    for c in companies:
        key = c["Company_Name"].lower()
        if key and key not in seen:
            seen.add(key)
            unique.append(c)

    logger.info(f"NOSAB: scraped {len(unique)} companies")
    return unique


def _parse_table_layout(soup) -> list[dict]:
    """Parse table-based company listings."""
    companies = []
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        for row in rows[1:]:  # Skip header row
            cols = row.find_all(["td", "th"])
            if len(cols) >= 2:
                name = clean_company_name(cols[0].get_text())
                if not name or len(name) < 3:
                    continue
                website = ""
                phone = ""
                sector = ""
                address = ""
                for col in cols:
                    text = col.get_text().strip()
                    link = col.find("a", href=True)
                    if link and ("http" in link["href"] or "www" in link["href"]):
                        website = link["href"]
                    elif any(x in text for x in ["0224", "0212", "0216", "(0"]):
                        phone = normalize_phone(text)
                domain = extract_domain(website)
                companies.append(_make_record(name, sector, domain, phone, address))
    return companies


def _parse_card_layout(soup) -> list[dict]:
    """Parse card/div-based company listings."""
    companies = []
    # Common patterns for OSB sites
    containers = (
        soup.find_all("div", class_=lambda c: c and any(
            x in c for x in ["firma", "company", "uye", "member", "card", "item"]
        ))
        or soup.find_all("li", class_=lambda c: c and any(
            x in c for x in ["firma", "company", "uye", "member"]
        ))
    )
    for container in containers:
        name_tag = (
            container.find(["h2", "h3", "h4", "strong", "b"])
            or container.find("a")
        )
        if not name_tag:
            continue
        name = clean_company_name(name_tag.get_text())
        if not name or len(name) < 3:
            continue
        # Website
        website = ""
        for a in container.find_all("a", href=True):
            href = a["href"]
            if href.startswith("http") or "www." in href:
                website = href
                break
        # Phone
        text = container.get_text()
        import re
        phone_match = re.search(r"0\s*\d{3}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}", text)
        phone = normalize_phone(phone_match.group() if phone_match else "")
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

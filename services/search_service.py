import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

SOCIAL_DOMAINS = {
    "instagram.com", "facebook.com", "linkedin.com", "youtube.com",
    "tiktok.com", "x.com", "twitter.com", "pinterest.com", "reddit.com",
}

DIRECTORY_DOMAINS = {
    "go4worldbusiness.com", "alibaba.com", "made-in-china.com",
    "indiamart.com", "tradeindia.com", "europages.com", "thomasnet.com",
    "yellowpages.com", "revenuebase.ai", "zoominfo.com", "dnb.com",
    "globalsources.com", "exportersindia.com", "tradekey.com", "ec21.com",
    "kompass.com", "manta.com", "crunchbase.com", "wikipedia.org",
    "amazon.com", "ebay.com",
}

TYPE_TERMS = {
    "All relevant companies": "importers wholesalers distributors",
    "Importer": "importers",
    "Exporter": "exporters",
    "Wholesaler": "wholesalers",
    "Distributor": "distributors",
    "Retailer": "retailers",
    "Manufacturer": "manufacturers",
}


class SearchError(Exception):
    """Raised with a user-friendly message when a search fails."""


def get_domain(url: str) -> str:
    domain = urlparse(url).netloc.lower()
    return domain[4:] if domain.startswith("www.") else domain


def _matches(domain: str, known: set) -> bool:
    return any(domain == d or domain.endswith("." + d) for d in known)


def classify_source(domain: str) -> str:
    if _matches(domain, SOCIAL_DOMAINS):
        return "Social media"
    if _matches(domain, DIRECTORY_DOMAINS):
        return "Directory / marketplace"
    return "Company website (unverified)"


def build_query(product: str, country: str, company_type: str, keywords: str) -> str:
    type_term = TYPE_TERMS.get(company_type, "importers wholesalers")
    country_part = "" if country.startswith("Other") else country
    parts = [product, type_term, country_part, keywords]
    return " ".join(p for p in parts if p).strip()


def search_companies(
    product: str,
    country: str,
    company_type: str,
    keywords: str,
    num_results: int,
) -> dict:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise SearchError("TAVILY_API_KEY is missing from your .env file.")

    query = build_query(product, country, company_type, keywords)

    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(
            query=query,
            search_depth="basic",
            max_results=num_results,
        )
    except Exception as exc:
        name = exc.__class__.__name__
        if "InvalidAPIKey" in name:
            raise SearchError("The Tavily API key was rejected. Check .env.") from exc
        if "UsageLimit" in name:
            raise SearchError("The Tavily free credits are used up for now.") from exc
        raise SearchError(f"Search failed ({name}). Try again later.") from exc

    rows = []
    seen = set()
    for item in response.get("results", []):
        url = item.get("url") or ""
        if not url:
            continue
        domain = get_domain(url)
        source_type = classify_source(domain)

        key = url if source_type != "Company website (unverified)" else domain
        if key in seen:
            continue
        seen.add(key)

        rows.append(
            {
                "Page title": item.get("title") or "Not found",
                "Domain": domain,
                "Source type": source_type,
                "Company type searched": company_type,
                "Import/export evidence": "Not verified",
                "Source URL": url,
                "Snippet": (item.get("content") or "")[:200],
            }
        )

    return {"query": query, "rows": rows}
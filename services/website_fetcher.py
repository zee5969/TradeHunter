import ipaddress
import socket
import time
from urllib.parse import urljoin, urlparse

import requests

USER_AGENT = "TradeHunterBot/0.1 (business research; respects robots.txt)"
TIMEOUT_SECONDS = 10
MAX_BYTES = 1_500_000
MAX_REDIRECTS = 3
MIN_DELAY_SECONDS = 1.0

_last_request_time = {}


class FetchError(Exception):
    """Raised with a user-friendly message when a page cannot be fetched."""


def normalize_url(raw: str) -> str:
    raw = (raw or "").strip()
    if not raw:
        raise FetchError("Please enter a website URL.")
    if "://" not in raw:
        raw = "https://" + raw
    parsed = urlparse(raw)
    if parsed.scheme not in ("http", "https"):
        raise FetchError("Only http and https website addresses are supported.")
    if not parsed.hostname:
        raise FetchError("That does not look like a valid website address.")
    return raw


def _ensure_public_host(hostname: str) -> None:
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        raise FetchError("Could not find that website. Check the address.")
    for info in infos:
        address = info[4][0]
        if not ipaddress.ip_address(address).is_global:
            raise FetchError("That address is not a public website.")


def _wait_for_turn(hostname: str) -> None:
    last = _last_request_time.get(hostname)
    if last is not None:
        wait = MIN_DELAY_SECONDS - (time.monotonic() - last)
        if wait > 0:
            time.sleep(wait)
    _last_request_time[hostname] = time.monotonic()


def _robots_allows(url: str) -> bool:
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    try:
        resp = requests.get(
            robots_url,
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT_SECONDS,
            allow_redirects=False,
        )
    except requests.RequestException:
        raise FetchError(
            "Could not read the site's robots.txt, so the page was not fetched."
        )

    if resp.status_code in (401, 403) or resp.status_code >= 500:
        return False
    if resp.status_code >= 400:
        return True  # no robots.txt published

    from urllib.robotparser import RobotFileParser

    parser = RobotFileParser()
    parser.parse(resp.text.splitlines())
    return parser.can_fetch(USER_AGENT, url)


def fetch_page(raw_url: str) -> dict:
    url = normalize_url(raw_url)

    for _ in range(MAX_REDIRECTS + 1):
        hostname = urlparse(url).hostname
        _ensure_public_host(hostname)

        if not _robots_allows(url):
            raise FetchError(
                "This site's robots.txt does not allow automated access, "
                "so the page was not fetched."
            )

        _wait_for_turn(hostname)

        try:
            resp = requests.get(
                url,
                headers={"User-Agent": USER_AGENT, "Accept": "text/html"},
                timeout=TIMEOUT_SECONDS,
                allow_redirects=False,
                stream=True,
            )
        except requests.Timeout:
            raise FetchError("The website took too long to respond.")
        except requests.RequestException:
            raise FetchError("Could not connect to that website.")

        if resp.status_code in (301, 302, 303, 307, 308):
            location = resp.headers.get("Location")
            if not location:
                raise FetchError("The website sent an invalid redirect.")
            url = normalize_url(urljoin(url, location))
            continue

        if resp.status_code in (401, 403, 429):
            raise FetchError(
                f"The website blocked automated access (HTTP {resp.status_code}). "
                "Blocks and logins are never bypassed."
            )
        if resp.status_code >= 400:
            raise FetchError(f"The website returned an error (HTTP {resp.status_code}).")

        content_type = resp.headers.get("Content-Type", "").lower()
        if "html" not in content_type:
            raise FetchError("That address is not a regular web page.")

        chunks = []
        size = 0
        for chunk in resp.iter_content(chunk_size=65536):
            size += len(chunk)
            if size > MAX_BYTES:
                break
            chunks.append(chunk)
        raw_bytes = b"".join(chunks)
        html = raw_bytes.decode(resp.encoding or "utf-8", errors="replace")

        return {"url": url, "status": resp.status_code, "html": html}

    raise FetchError("The website redirected too many times.")
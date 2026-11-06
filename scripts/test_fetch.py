import sys

from services.website_fetcher import FetchError, fetch_page

tests = sys.argv[1:] or [
    "https://example.com",
    "localhost",
    "http://127.0.0.1",
    "ftp://example.com",
    "thisisnotarealsite12345.com",
    "",
]

for target in tests:
    try:
        page = fetch_page(target)
        print(f"[OK]    {target!r} -> HTTP {page['status']}, {len(page['html'])} characters")
    except FetchError as err:
        print(f"[BLOCKED] {target!r} -> {err}")
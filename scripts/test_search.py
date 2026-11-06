import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")
if not api_key:
    raise SystemExit("TAVILY_API_KEY was not found in your .env file.")

client = TavilyClient(api_key=api_key)

query = "sportswear importers wholesalers United States"
response = client.search(query=query, search_depth="basic", max_results=5)

results = response.get("results", [])
print(f"Query: {query}")
print(f"Results returned: {len(results)}\n")

for number, item in enumerate(results, start=1):
    snippet = (item.get("content") or "")[:150]
    print(f"{number}. {item.get('title')}")
    print(f"   URL: {item.get('url')}")
    print(f"   Snippet: {snippet}...\n")
# %% Imports
from ddgs import DDGS
import requests
from markdownify import markdownify as md

# %% AI Slop Fest (it actually did a pretty good job ngl)
def get_search_query_links(search_queries: list[str]) -> dict:
    results = {}
    for query in search_queries:
        print("Retrieving url for query: ", query)
        results[query] = [r["href"] for r in DDGS().text(query, max_results=4)]
    return results

test_queries = ["limits of nuclear energy", "risks associated with nuclear energy", "environmental impact of nuclear energy", "safety concerns in nuclear power plants", "disadvantages of nuclear energy production"]

url_dict = get_search_query_links(test_queries)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

results_md = {}
for query, urls in url_dict.items():
    results_md[query] = []
    for url in urls:
        print("Sending request for URL: ", url)
        r = requests.get(url, headers=HEADERS, timeout=60)
        print("Converting HTML to markdown for URL: ", url)
        results_md[query].append(md(r.text))

# %% Investigate

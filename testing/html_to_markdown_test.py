# %% Imports
from ddgs import DDGS
import requests
from markdownify import markdownify as md

# %% Restating Some Stuff for Testing
def get_search_query_links(search_queries: list[str]) -> dict:
    """Takes a list of search queries and returns a dict mapping each query to a list of up to 4 result URLs."""
    results = {}
    for query in search_queries:
        results[query] = [r["href"] for r in DDGS().text(query, max_results=4)]

    return results

test_queries = ["limits of nuclear energy", "risks associated with nuclear energy", "environmental impact of nuclear energy", "safety concerns in nuclear power plants", "disadvantages of nuclear energy production"]



# %% Display Results
url_dict = get_search_query_links(test_queries)
for key, value in url_dict.items():
    print(key, value, '\n\n')

# %% Retrieve html content and convert to markdown
for query, url in url_dict.items():
    r = requests.get(url)
    print(r)


# %% AI Slop (actually... not terrible code)
def get_search_query_links(search_queries: list[str]) -> dict:
    results = {}
    for query in search_queries:
        results[query] = [r["href"] for r in DDGS().text(query, max_results=4)]
    return results

test_queries = ["limits of nuclear energy", "risks associated with nuclear energy", "environmental impact of nuclear energy", "safety concerns in nuclear power plants", "disadvantages of nuclear energy production"]

url_dict = get_search_query_links(test_queries)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

results_md = {}
for query, urls in url_dict.items():
    results_md[query] = []
    for url in urls:
        r = requests.get(url, headers=HEADERS, timeout=10)
        results_md[query].append(md(r.text))

print(results_md)

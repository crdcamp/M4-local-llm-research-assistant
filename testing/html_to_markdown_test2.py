# %% Imports
from ddgs import DDGS
import requests
from markdownify import markdownify as md

# %% Function Declarations
def get_search_query_links(search_queries: list[str]) -> dict:
    results = {}
    for query in search_queries:
        print("Retrieving urls for query: ", query)
        results[query] = [r["href"] for r in DDGS().text(query, max_results=5)]
    return results

def convert_html_to_markdown(query_url_dict: dict) -> dict:
    results = {}
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

    for query, urls in query_url_dict.items():
        print("Beginning requests for query: ", query)
        results[query] = []
        for url in urls:
            try:
                print("Sending request for url: ", url)
                r = requests.get(url, headers=HEADERS, timeout=10)
                results[query].append(md(r.text, strip=['a', 'img', 'nav', 'header', 'footer']))
            except Exception as e:
                print(f"Error fetching {url}: {e}")
        print()

    return results

# %% Testing
test_queries = ["limits of nuclear energy", "risks associated with nuclear energy", "environmental impact of nuclear energy", "safety concerns in nuclear power plants", "disadvantages of nuclear energy production"]
url_dict = get_search_query_links(test_queries)
print()
md_dict = convert_html_to_markdown(url_dict)

# %% Inspect
for key, item in md_dict.items():
    print(f"Key: {key}\nItem:\n{item}\n\n")

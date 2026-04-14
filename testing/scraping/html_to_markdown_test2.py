# %% Imports
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
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

    STRIP_TAGS = ['script', 'style', 'nav', 'header', 'footer', 'aside',
                  'noscript', 'iframe', 'form', 'button', 'svg', 'figure',
                  'advertisement', 'cookie-banner']

    for query, urls in query_url_dict.items():
        print("Beginning requests for query: ", query)
        results[query] = {}
        for url in urls:
            try:
                print("Sending request for url: ", url)
                r = requests.get(url, headers=HEADERS, timeout=7)

                soup = BeautifulSoup(r.text, 'html.parser')
                for tag in soup(STRIP_TAGS):
                    tag.decompose()

                # Try to isolate main content if landmarks exist
                main = soup.find('main') or soup.find('article') or soup.find(id='content') or soup.find(class_='content') or soup.body
                clean_html = str(main) if main else str(soup)

                results[query][url] = md(clean_html, strip=['a', 'img'])

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
for query, url_dict in md_dict.items():
    for url, content in url_dict.items():
        print(f"Query: {query}\nURL: {url}\nContent:\n{content}\n\n")

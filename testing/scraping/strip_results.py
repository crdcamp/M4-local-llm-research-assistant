# %% Imports
from llama_cpp import Llama
import json
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# %% Load Model
print("Loading model...")
model = Llama(
    model_path="../../models/Qwen2.5-7B-Instruct-Q4_K_M.gguf",
    n_ctx = 32768,
    verbose=False,
    chat_format="chatml"
)

# %% Functions
def get_search_query_links(search_queries: list[str]) -> dict:
    """Takes a list of search queries and returns a dict mapping each query to a list of URLs resulting from the search query."""
    query_url_dict = {}
    for query in search_queries:
        query_url_dict[query] = [r["href"] for r in DDGS().text(query, max_results=4)]

    return query_url_dict

def convert_html_to_markdown(query_url_dict: dict) -> dict:
    """Retrieves HTML content from a given URL, strips the HTML content, and converts to markdown"""
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

    STRIP_TAGS = ['script', 'style', 'nav', 'header', 'footer', 'aside',
                    'noscript', 'iframe', 'form', 'button', 'svg', 'figure',
                    'advertisement', 'cookie-banner']

    md_results = {}

    for query, urls in query_url_dict.items():
        md_results[query] = {}

        for url in urls:
            try:
                r = requests.get(url, headers=HEADERS, timeout=7)
                soup = BeautifulSoup(r.text, 'html.parser')
                for tag in soup(STRIP_TAGS):
                    tag.decompose()

                main = soup.find('main') or soup.find('article') or soup.find(id='content') or soup.find(class_='content') or soup.body
                clean_html = str(main) if main else str(soup)

                md_results[query][url] = md(clean_html, strip=['a', 'img'])

            except Exception as e:
                print(f"Error fetching {url}: {e}")

    return md_results

# %% Testing variables
example_search_prompts_endo_vs_exo = ['definition of endogenous variables in statistics', 'exogenous variables in statistical models', 'difference between endogenous and exogenous variables', 'examples of endogenous and exogenous variables in statistics', 'endogenous vs exogenous variables explained']
search_links_endo_vs_exo = get_search_query_links(example_search_prompts_endo_vs_exo)
print(search_links_endo_vs_exo)

# %% Inspecting

for key, value in search_links_endo_vs_exo.items():
    print(f"{key}\n{value}\n\n")


"""
NEXT STEPS

Use llama.cpp's `tokenize()` method to calculate token usage
of a given web page
"""

# %% Imports
from pydoc import html
from llama_cpp import Llama
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import pprint

# For later: managing token usage
max_tokens = 32768

# %% Load Model
print("Loading model...")
model = Llama(
    model_path="../../models/Qwen2.5-7B-Instruct-Q4_K_M.gguf",
    n_ctx = 32768,
    verbose=False,
    chat_format="chatml"
)
print("Model done loading")

# %% Functions
def get_search_query_links(search_queries: list[str]) -> dict:
    """Takes a list of search queries and returns a dict mapping each query to a list of URLs resulting from the search query."""
    query_url_dict = {}
    for query in search_queries:
        query_url_dict[query] = [r["href"] for r in DDGS().text(query, max_results=4)]

    return query_url_dict

# %% Testing variables
example_search_prompts_endo_vs_exo = ['definition of endogenous variables in statistics', 'exogenous variables in statistical models', 'difference between endogenous and exogenous variables', 'examples of endogenous and exogenous variables in statistics', 'endogenous vs exogenous variables explained']
search_links_endo_vs_exo = get_search_query_links(example_search_prompts_endo_vs_exo)


# %% Inspecting
for key, value in search_links_endo_vs_exo.items():
    print(f"{key}\n{value}\n\n")


"""
NEXT STEPS

Use llama.cpp's `tokenize()` method to calculate token usage
of a given web page

Here's the outline for the functions so far:

def generate_search_queries():
def get_search_query_links():
def retrieve_html():
def calculate_token_usage():
def convert_html():
"""

# %% Testing new HTML retrieval function
# For extracting relevant text from HTML

"""
We'll start by just getting the HTML first, then we'll create another
function that extracts the relevant tags.

After both of these functions are solid, we'll combine them into one
function
"""

def get_html_text(query_url_dict):
    html_results = {}

    for query, urls in query_url_dict.items():
        html_results[query] = {}

        for url in urls:
            try:
                r = requests.get(url, timeout=7)
                html_results[query][url] = r.text

            except Exception as e:
                print(f"Error fetching {url}: {e}")

    return html_results

html_results = get_html_text(search_links_endo_vs_exo)

# %% Extracting semantic text from HTML
# We'll start by only extracting the `<p>` elements
def extract_text_from_html(html_dict):
    for query, urls in html_dict.items():
        print(f"Query: {query}")
        for url, html_text in urls.items():
            print(f"URL: {url}")
            print(f"HTML length: {len(html_text)}\n\n")

test = extract_text_from_html(html_results)

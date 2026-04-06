# %% Imports
from doctest import testfile
from mcp.server import FastMCP
from llama_cpp import Llama
from pydantic import BaseModel
import json
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# NOTE
# llama_context: n_ctx_seq (512) < n_ctx_train (32768) -- the full capacity of the model will not be utilized

# %% Load Model
mcp = FastMCP("Research Assistant")

# LOOK INTO PROPERLY LOADING THE MODEL:
# https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#core-concepts
print("Loading model...")
model = Llama(
    model_path="models/Qwen2.5-7B-Instruct-Q4_K_M.gguf",
    max_tokens=2048,
    verbose=False,
    chat_format="chatml"
)


# %% Functions
# Structured list output for `generate_search_queries`
class SearchQueries(BaseModel):
    queries: list[str]

def generate_search_queries(user_prompt: str) -> list[str]:
    """Generate five targeted search engine queries to research a given topic or question."""

    response = model.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a search query generator. When given a question or topic, generate exactly five concise search engine queries a person could enter into a browser to research it."
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        response_format={
            "type": "json_object",
            "schema": SearchQueries.model_json_schema()
        }
    )

    content = response["choices"][0]["message"]["content"]
    parsed = json.loads(content)

    return parsed["queries"]

def get_search_query_links(search_queries: list[str]) -> dict:
    """Takes a list of search queries and returns a dict mapping each query to a list of URLs resulting from the search query."""
    query_url_dict = {}
    for query in search_queries:
        query_url_dict[query] = [r["href"] for r in DDGS().text(query, max_results=4)]

    return query_url_dict

# %% Testing conversion function
# Rewrite conversion function here
def convert_html_to_markdown(query_url_dict: dict) -> dict:
    """
    `query_dict` structure:
        key: Internet search query
        value: List of URLS provided by search query
    """

    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

    STRIP_TAGS = ['script', 'style', 'nav', 'header', 'footer', 'aside',
                    'noscript', 'iframe', 'form', 'button', 'svg', 'figure',
                    'advertisement', 'cookie-banner']

    md_results = {}

    for query, urls in query_url_dict.items():
        md_results[query] = {}
        for url in urls:
            md_results[query][url] = "A bunch of markdown text"

    return md_results

test_search_queries = generate_search_queries("Tell me about the difference between endogenous and exogenous variables")
test_urls_dict = get_search_query_links(test_search_queries)

# %% Conversion Test
import pprint
conversion_test = convert_html_to_markdown(test_urls_dict)
pprint.pprint(conversion_test)

# %% Testing/Refacotring
#@mcp.tool()
def research_tool(prompt: str):
    search_queries_list = generate_search_queries(prompt)
    search_queries_dict = get_search_query_links(search_queries_list)

    return search_queries_dict

test = research_tool("Tell me the various ways to create an LLM from scratch")
for query, urls in test.items():
    print(f"QUERY: {query}\nURLs:\n{urls}\n\n")

# %% Cutoff
# THIS ALMOST CERTAINLY NEEDS SOME CLEANUP (AI slop)
def convert_html_to_markdown(query_url_dict: dict) -> dict:
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

    STRIP_TAGS = ['script', 'style', 'nav', 'header', 'footer', 'aside',
                  'noscript', 'iframe', 'form', 'button', 'svg', 'figure',
                  'advertisement', 'cookie-banner']

    results = {}

    for query, urls in query_url_dict.items():
        results[query] = {}
        for url in urls:
            try:
                r = requests.get(url, headers=HEADERS, timeout=7)  # ← requests, not request

                soup = BeautifulSoup(r.text, 'html.parser')
                for tag in soup(STRIP_TAGS):
                    tag.decompose()

                main = soup.find('main') or soup.find('article') or soup.find(id='content') or soup.find(class_='content') or soup.body
                clean_html = str(main) if main else str(soup)

                results[query][url] = md(clean_html, strip=['a', 'img'])

            except Exception as e:
                print(f"Error fetching {url}: {e}")

    return results

"""
Then, add another tool here that uses the LLM to strip out the unneeded text for each result...
Or something like that...
"""

if __name__ == "__main__":
    mcp.run(transport="stdio")

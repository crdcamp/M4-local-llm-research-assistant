from mcp.server import FastMCP
from llama_cpp import Llama
from pydantic import BaseModel
import json
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

mcp = FastMCP("Research Assistant")

print("Loading model...")
model = Llama(
    model_path="models/Qwen2.5-7B-Instruct-Q4_K_M.gguf",
    n_ctx = 2048,
    verbose=False,
    chat_format="chatml"
)

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

def interpret_md_results(markdown_results: dict) -> str:
    # We'll just start by accessing one entry.
    # Keep it simple for testing for now

    for query, url_dict in markdown_results.items():
        first_url = next(iter(url_dict))
        content = url_dict[first_url]

        response = model.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "You are a research assistant. Summarize the following web page content clearly and concisely, focusing on the most relevant facts and key points. Ignore navigation text, ads, or other boilerplate."
                },
                {
                    "role": "user",
                    "content": content
                }
            ]
        )

        return response["choices"][0]["message"]["content"]


@mcp.tool()
def research_tool(prompt: str) -> dict:
    """Search the web and return page content as markdown for a given research prompt."""
    search_queries_list = generate_search_queries(prompt)
    search_queries_dict = get_search_query_links(search_queries_list)
    url_md_results = convert_html_to_markdown(search_queries_dict)
    chat_response = interpret_md_results(url_md_results)

    return chat_response

if __name__ == "__main__":
    mcp.run(transport="stdio")

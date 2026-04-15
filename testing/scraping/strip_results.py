# %% Imports
from llama_cpp import Llama
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
import json
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
print("Getting search links...")
search_links_endo_vs_exo = get_search_query_links(example_search_prompts_endo_vs_exo)


"""
NEXT STEPS

Use llama.cpp's `tokenize()` method to calculate token usage
of a given web page
"""

#html_results[query][url] = r.text

def get_html_text(query_url_dict):
    html_results = {}

    for query, urls in query_url_dict.items():
        html_results[query] = {}

        for url in urls:
            try:
                r = requests.get(url, timeout=7)
                soup = BeautifulSoup(r.text, 'html.parser')

                paragraphs = soup.find_all('p')
                html_results[query][url] = [p.get_text() for p in paragraphs]

                if not html_results[query]:
                    del html_results[query]

            except Exception as e:
                print(f"Error fetching {url}: {e}")

    return html_results

print("Retrieving html text...")
html_results = get_html_text(search_links_endo_vs_exo)

# %% Save
with open("html_results.json", "w") as f:
    json.dump(html_results, f, indent=4)


"""
Don't forget to rename this function when tying everything together
"""
# %% Interpretation test
def interpret_md_results(html_results: dict) -> dict:
    summaries = {}

    for query, url_dict in html_results.items():
        first_url = next(iter(url_dict))
        content = "\n\n".join(url_dict[first_url])  # join list of paragraphs into one string

        response = model.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "You are a research assistant. Summarize the following web page content clearly and concisely, focusing on the most relevant facts and key points. Ignore navigation text, ads, or other boilerplate. If the page content appears to be a bot/security challenge, access denial, or CAPTCHA page rather than real content, respond with exactly: BLOCKED"
                },
                {
                    "role": "user",
                    "content": content
                }
            ]
        )

        summary = response["choices"][0]["message"]["content"]
        if summary.strip() != "BLOCKED":
            summaries[query] = summary

    return summaries

print("Interpreting results...")
results = interpret_md_results(html_results)
for query, summary in results.items():
    print(f"Query: {query}\nSummary: {summary}\n\n")

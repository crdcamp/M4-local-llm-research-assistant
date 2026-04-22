# %% Imports
import os
from fastapi import FastAPI, WebSocket
from llama_cpp import Llama
from pydantic import BaseModel
import json
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

"""
DOUBLE CHECK THE PROMPT INPUT SECTION... I think there's something wrong with it
Add ASYNC to parts if needed.
"""


input_prompt = "Tell me about the difference between endogenous and exogenous variables in statistics"

# We

# %%
dirs = ["results/html_results"]
for path in dirs:
    if not os.path.exists(path):
        os.makedirs(path)

html_dir = dirs[0]
train_data_path = "results/train_data.csv"

times = []

# FastAPI integration (for later)
# app = FastAPI()

# html = None

# @app.get("/")
# async def get():
#     return HTMLResponse(html)

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         result = research_tool(data)
#         await websocket.send_text(result)

# %% Load Model
print("Loading model...")
model_load_start_time = time.perf_counter()
model = Llama(
    model_path="models/Qwen2.5-7B-Instruct-Q4_K_M.gguf",
    n_ctx = 32768,
    max_tokens=2048,
    verbose=False,
    chat_format="chatml"
)
model_load_end_time = time.perf_counter()

model_load_total_time = model_load_end_time - model_load_start_time
print(f"Model loaded in {model_load_total_time} seconds\n")
times.append(model_load_total_time)

# Structured list output for `generate_search_queries`
class SearchQueries(BaseModel):
    queries: list[str]

# %% Generate search queries
def generate_search_queries(user_prompt: str) -> list[str]:
    print("Generating search queries...")

    start_time = time.perf_counter()
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
    # Ensure the queries are in list format
    query_list = json.loads(content)["queries"]
    end_time = time.perf_counter()

    total_time = end_time - start_time
    print(f"Search queries generated in {total_time} seconds")
    times.append(total_time)

    print(f"Queries: \n{query_list}\n")

    return query_list

# %% Get links
def get_search_query_links(search_queries: list[str]) -> dict:
    print("Retrieving search query links...")

    start_time = time.perf_counter()
    query_url_dict = {}
    for query in search_queries:
        query_url_dict[query] = [r["href"] for r in DDGS().text(query, max_results=4)]
    end_time = time.perf_counter()

    total_time = end_time - start_time
    print(f"Search query links retrieved in {total_time} seconds\n")
    times.append(total_time)

    return query_url_dict

# %% Get HTML
def get_html_text(query_url_dict):
    print("Retrieving HTML text...")
    html_results = {}

    start_time = time.perf_counter()
    for query, urls in query_url_dict.items():
        html_results[query] = {}

        for url in urls:
            try:
                r = requests.get(url, timeout=7)
                soup = BeautifulSoup(r.text, 'html.parser')
                paragraphs = soup.find_all('p')
                html_results[query][url] = [p.get_text() for p in paragraphs]

            except Exception as e:
                print(f"Error fetching {url}: {e}")
    end_time = time.perf_counter()

    total_time = end_time - start_time
    print(f"HTML text retrieved in {total_time} seconds\n")
    times.append(total_time)

    # Delete empty dictionary entries
    html_results = {
        query: {url: paragraphs for url, paragraphs in url_dict.items() if paragraphs}
        for query, url_dict in html_results.items()
        if any(paragraphs for paragraphs in url_dict.values())
    }

    # Save with date/time stamps
    timestr = time.strftime("%Y%m%d-%H%M%S") # Coulds just user `end_time` here
    with open(f"{html_dir}/html_{timestr}", 'w', encoding='utf-8') as f:
        json.dump(html_results, f, indent=4)

    return html_results

# %% Interpret
# Only interprets the first result for now
def interpret_results(html_results: dict) -> dict:
    print("Interpreting HTML results...")
    summaries = {}

    start_time = time.perf_counter()
    for query, url_dict in html_results.items():
        first_url = next(iter(url_dict))
        content = "\n\n".join(url_dict[first_url])  # join list of paragraphs into one string

        response = model.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "You are a research assistant. Summarize the following content clearly and concisely, focusing on the most relevant facts and key points. Write as if presenting the information directly — do not frame your summary with references to any source, document, or medium (never say 'the article', 'the page', 'the web page', 'the text', 'the source', 'the content', or anything similar). Just state the facts. Ignore navigation text, ads, or other boilerplate. If the content appears to be a bot/security challenge, access denial, or CAPTCHA page rather than real content, respond with exactly: BLOCKED"
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
    end_time = time.perf_counter()

    total_time = end_time - start_time
    print(f"Results interpreted in {total_time} seconds\n")
    times.append(total_time)

    # Append results to training data
    new_data = pd.DataFrame({
        "prompt": [input_prompt],
        "response": [summary],
    })
    new_data.to_csv(train_data_path, mode='a', header=False)

    return summaries

# %% Research tool
def research_tool(prompt: str) -> dict:
    """Search the web and return page content as markdown for a given research prompt."""
    search_queries_list = generate_search_queries(prompt)
    url_links = get_search_query_links(search_queries_list)
    html_text = get_html_text(url_links)
    chat_response = interpret_results(html_text)

    return chat_response

results = research_tool(input_prompt)
total_run_time = sum(times)
print(f"Results:\n {results}\n\n")

print(f"Total run time: {total_run_time} seconds")

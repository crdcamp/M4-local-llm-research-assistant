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
import pprint
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

"""
NOW WE JUST NEED TO CLEAN UP THE WEB SCRAPING ENTIRELY.
WE WANT PURELY SEMANTIC TEXT ORGANIZED BY WEBSITE THAT'S SAVED TO A
SINGLE MARKDOWN FILE TO FEED THE LLM

THIS IS A HARD REQUIREMENT. THE LLM WILL NOT KNOW WHAT TO DO OTHERWISE

* "BLOCKED" parameter isn't working every time. Might be fixed after cleaning up web scrape

"""

input_prompt = "Tell me about the difference between endogenous and exogenous variables in statistics"

clean_html_prompt = """You are a text cleaning engine. Your sole purpose is to convert messy scraped web text into clean, semantic Markdown for a database.

RULES:
1. Extract only the primary article content, headers, and lists.
2. Strip out all navigation menus, footers, ad blocks, social media links, and cookie consent warnings.
3. Use Markdown formatting (# for headers, - for lists, ** for bold).
4. If the text contains a CAPTCHA, "Access Denied," or a bot-protection message (like Cloudflare), respond with exactly one word: BLOCKED.
5. NEVER include introductory or concluding remarks. Do not say "Here is the cleaned text." Start immediately with the content.
6. Preserve the original meaning but remove repetitive "click here" or "read more" buttons."""

# Generating 5 search queries
# Each of these search queries are then used to retrieve the top 4 search results
# Therefore, we have 20 URL links in total

# %% File Paths
html_results_path = "results/html_results.json"
summary_results_path = "results/summaries.json"

html_text_dir = "data/html_text"
html_summary_dir = "data/summary"
os.makedirs(html_text_dir, exist_ok=True)

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
    print(f"{len(query_list)} search queries generated in {total_time} seconds")
    times.append(total_time)

    print(f"Search Queries:\n{query_list}\n")

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

    print(f"`query_url_dict`:\n{pprint.pformat(query_url_dict)}\n")

    return query_url_dict

def parse_page(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        result = soup.find_all('p')

        if result:
            name = "".join(c for c in url if c.isalnum())

            with open(f"{html_text_dir}/{name}.txt", 'w', encoding='utf-8') as f:
                for paragraph in result:
                    f.write(paragraph.get_text() + "\n\n")

        else:
            print(f"No paragraphs found for {url}. Skipping file creation")

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# %% Get HTML
def get_html_text(query_url_dict) -> dict:
    print("Retrieving HTML text...")

    start_time = time.perf_counter()
    html_results = {}

    MAX_THREADS = 4
    for query, urls in query_url_dict.items():
        # Process all 4 urls for each query simultaneously
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            results = list(executor.map(parse_page, urls))

        html_results[query] = dict(zip(urls, results))
        # Delete empty entries
        html_results[query] = {url: res for url, res in html_results[query].items() if res}


    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f"HTML text retrieved in {total_time} seconds\n")
    times.append(total_time)

    with open(html_results_path, "w") as f:
        json.dump(html_results, f, indent=2)

    return html_results

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
import pprint
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

"""
NOW WE JUST NEED TO CLEAN UP THE WEB SCRAPING ENTIRELY.
WE WANT PURELY SEMANTIC TEXT ORGANIZED BY WEBSITE THAT'S SAVED TO A
SINGLE MARKDOWN FILE TO FEED THE LLM

THIS IS A HARD REQUIREMENT. THE LLM WILL NOT KNOW WHAT TO DO OTHERWISE

* "BLOCKED" parameter isn't working every time. Might be fixed after cleaning up web scrape

"""

input_prompt = "Tell me about the difference between endogenous and exogenous variables in statistics"

clean_html_prompt = """You are a text cleaning engine. Your sole purpose is to convert messy scraped web text into clean, semantic Markdown for a database.

RULES:
1. Extract only the primary article content, headers, and lists.
2. Strip out all navigation menus, footers, ad blocks, social media links, and cookie consent warnings.
3. Use Markdown formatting (# for headers, - for lists, ** for bold).
4. If the text contains a CAPTCHA, "Access Denied," or a bot-protection message (like Cloudflare), respond with exactly one word: BLOCKED.
5. NEVER include introductory or concluding remarks. Do not say "Here is the cleaned text." Start immediately with the content.
6. Preserve the original meaning but remove repetitive "click here" or "read more" buttons."""

# Generating 5 search queries
# Each of these search queries are then used to retrieve the top 4 search results
# Therefore, we have 20 URL links in total

# %% File Paths
html_results_path = "results/html_results.json"
summary_results_path = "results/summaries.json"

html_text_dir = "data/html_text"
html_summary_dir = "data/summary"
os.makedirs(html_text_dir, exist_ok=True)

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
    print(f"{len(query_list)} search queries generated in {total_time} seconds")
    times.append(total_time)

    print(f"Search Queries:\n{query_list}\n")

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

    print(f"`query_url_dict`:\n{pprint.pformat(query_url_dict)}\n")

    return query_url_dict

def parse_page(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        result = soup.find_all('p')

        if result:
            name = "".join(c for c in url if c.isalnum())

            with open(f"{html_text_dir}/{name}.txt", 'w', encoding='utf-8') as f:
                for paragraph in result:
                    f.write(paragraph.get_text() + "\n\n")

        else:
            print(f"No paragraphs found for {url}. Skipping file creation")

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# %% Get HTML
def get_html_text(query_url_dict) -> dict:
    print("Retrieving HTML text...")

    start_time = time.perf_counter()
    html_results = {}

    MAX_THREADS = 4
    for query, urls in query_url_dict.items():
        # Process all 4 urls for each query simultaneously
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            results = list(executor.map(parse_page, urls))

        html_results[query] = dict(zip(urls, results))
        # Delete empty entries
        html_results[query] = {url: res for url, res in html_results[query].items() if res}


    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f"HTML text retrieved in {total_time} seconds\n")
    times.append(total_time)

    with open(html_results_path, "w") as f:
        json.dump(html_results, f, indent=2)

def clean_html(file):
    with open(file, 'r', encoding='utf-8') as input:
        html_text = input.read()

    response = model.create_chat_completion(
        messages=[
                    {"role": "system", "content": clean_html_prompt},
                    {"role": "user", "content": html_text}
                ]
            )

    result = response["choices"][0]["message"]["content"]

    if result != "BLOCKED":
        with open(html_summary_dir, 'a', encoding='utf-8') as output:
            output.write(result)

def research_tool(prompt: str):
    search_queries_list = generate_search_queries(prompt)
    url_links = get_search_query_links(search_queries_list)
    html_text = get_html_text(url_links)

    for file in html_text_dir:
        clean_html(file)

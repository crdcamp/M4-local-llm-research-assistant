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

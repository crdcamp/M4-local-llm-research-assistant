from mcp.server import FastMCP
from llama_cpp import Llama
from pydantic import BaseModel
import json
from ddgs import DDGS

# Start MCP server
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

# Structured list output for `generate_search_queries`
class SearchQueries(BaseModel):
    queries: list[str]

@mcp.tool()
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

@mcp.tool()
def get_search_query_links(search_queries: list[str]) -> dict:
    """Takes a list of search queries and returns a dict mapping each query to a list of up to 4 result URLs."""
    results = {}
    for query in search_queries:
        results[query] = [r["href"] for r in DDGS().text(query, max_results=4)]

    return results

#@mcp.tool()
# def get_query_link_results():
"""
Using a python library to convert HTML to markdown, gather text from all the web pages
so that the model can analyze the results from the links.

This might require messing around with the context length a bit (might have to limit the
search results to 3 links instead of 4)...
"""

"""
USE SAMPLING TO DEFINE THE PATH OF TOOL USAGE:
https://huggingface.co/learn/mcp-course/unit1/capabilities#sampling
"""

if __name__ == "__main__":
    mcp.run(transport="stdio")
